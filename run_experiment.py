import os
import datetime
import subprocess
import time
import argparse
import redis
from kubernetes import client, config
from kubernetes.client import ApiException
import shutil

results_path = "/home/roberto_pizziol/results"

def delete_folder(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Folder '{path}' and its contents deleted successfully.")
        except OSError as error:
            print(f"Error deleting folder: {error}")
    else:
        print(f"Folder '{path}' does not exist.")


def save_time(filename, mode):
    with open(filename, mode) as f:
        f.write(datetime.datetime.utcnow().isoformat(sep="T", timespec="milliseconds") + "Z\n")


def get_cli():
    """
    Get input arguments from CLI.
    :return:    ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="Run Experiment - Command Line Interface")
    parser.add_argument("-m", "--method", type=str,
                        help='The autoscaler.',
                        choices=["muOpt", "muOpt-H", "VPA", "HPA"], required=False)
    parser.add_argument("-wa", "--webapp", type=str,
                        help='The benchmark application.',
                        choices=["acmeair", "3tier"], required=True)
    parser.add_argument("-n", "--name", type=str,
                        help='The experiment name (e.g., sin200-1h-vpa)', required=True)
    parser.add_argument("-ht", "--host", type=str,
                        help='The ip target of the Locust swarm', required=True)
    parser.add_argument("-ut", "--utarget", type=float, default=0.2,
                        help='The target utilization (only available for µOpt)', required=False)
    parser.add_argument("-t", "--wctrl", type=int, default=15,
                        help='The control period (only available for µOpt)', required=False)
    parser.add_argument("-wl", "--wlshape", type=str, default="traceShape",
                        help='The kind of workload.',
                        choices=["traceShape", "fixed"], required=False)
    parser.add_argument("-u", "--users", type=int, default=1,
                        help='The number of users used in case of fixed workload.', required=False)
    parser.add_argument("-d", "--duration", type=int, default=60,
                        help='The total duration of the experiment.', required=False)
    return parser.parse_args()


def reset_redis():
    redis_client = redis.Redis(host="localhost", port=6379)
    redis_client.set("test1_wrk", 0)


def reset_deployment_replicas(deployment_name):
    try:
        # Configure client
        config.load_kube_config()
        v1_api = client.AppsV1Api()

        # Get deployment object
        try:
            deployment = v1_api.read_namespaced_deployment(deployment_name, 'default')
        except client.ApiException as e:
            print(f"Error getting deployment: {e}")
            return

        # Update deployment spec
        deployment.spec.replicas = 1

        # Prepare and patch deployment update
        deployment_update = client.AppsV1beta1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=deployment.metadata,
            spec=deployment.spec,
        )
        v1_api.patch_namespaced_deployment(deployment_name, 'default', deployment_update)

        print(f"Deployment '{deployment_name}' replicas updated to 1.")
    except client.ApiException as e:
        print(f"Error updating deployment: {e}")


def get_pod_names_by_deployment(deployment_name):
    v1_api = client.CoreV1Api()
    pods = []
    try:
        all_pods = v1_api.list_namespaced_pod(namespace='default')
        for pod in all_pods.items:
            pod_name = pod.metadata.name
            if deployment_name in pod_name:
                pods.append(pod_name)
        return pods
    except client.ApiException as e:
        print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}\n")


def scale_pod(pod_name, container_name, cpu_request, cpu_limit):
    """
    Vertically scale a pod.

    :param pod_name:        The name of the pod.
    :param container_name:  The name of the container.
    :param cpu_request:     The CPU requests to be set for the pod.
    :param cpu_limit:       The CPU limit to be set for the pod.
    :return:
    """
    v1_api = client.CoreV1Api()
    patch_body = {
        "spec": {
            "containers": [
                {
                    "name": container_name,
                    "resources": {
                        "requests": {
                            "cpu": cpu_request
                        },
                        "limits": {
                            "cpu": cpu_limit
                        }
                    }
                }
            ]
        }
    }
    try:
        # logger.info(f"Updating pod {pod_name} to CPU request {cpu_request} and CPU limit {cpu_limit}")
        v1_api.patch_namespaced_pod(name=pod_name, namespace="default", body=patch_body)
    except ApiException as e:
        if e.status == 403:
            print(f"Insufficient permissions to access pod '{pod_name}'.")
        elif e.status == 404:
            print(f"Pod '{pod_name}' not found in namespace 'default'.")
        else:
            print(f"Failed to scale pod: {e}")


def reset_conditions(wait_time):
    # Reset Redis value
    reset_redis()

    time.sleep(wait_time)  # Wait a minute to settle

    # # Reset replicas and requests
    # for i in range(1, 4):
    #     deployment_name = f"spring-test-app-tier{i}"
    #     reset_deployment_replicas(deployment_name)
    #     # Reset requests for each pod
    #     for pod in get_pod_names_by_deployment(deployment_name):
    #         scale_pod(pod, f"{deployment_name}-container", 1, 16)


def create_or_clean_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

    # Remove all files inside the experiment folder (if it exists)
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def run_experiment(exp_name, hostname, webapp, wlshape, method, duration, users):
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    exp_folder = f"{results_path}/{webapp}/{current_date}/{exp_name}"
    create_or_clean_folder(exp_folder)  # Create the experiment folder (if it doesn't exist)
    time_file = f"{exp_folder}/{exp_name}-time.txt"

    reset_conditions(wait_time=5)
    print(f"[Launching experiment {exp_name} with Locust. Results will be stored in the {exp_folder} folder.]")

    save_time(time_file, "w") # Starting time

    host_url = f"http://{hostname}:8080"
    if wlshape == "fixed":
        locust_command = f"locust -f locustfile_{webapp}.py -r {users} -u {users} --headless --csv=\"{exp_folder}/{exp_name}\" --host=\"{host_url}\" --run-time {duration}m"
    else:
        locust_command = f"locust -f locustfile_{webapp}.py,traceShape.py --headless --csv=\"{exp_folder}/{exp_name}-learning\" --host=\"{host_url}\""
    os.system(locust_command)

    # Ending time
    save_time(time_file, "a")

    print("[Experiment completed!]")
    reset_conditions(wait_time=0)

if __name__ == '__main__':
    args = get_cli()
    run_experiment(exp_name=args.name, hostname=args.host, webapp=args.webapp, wlshape=args.wlshape, method=args.method, duration=args.duration, users=args.users)


    # if method == "VPA":
    #     print("[Beginning of learning phase]")
    #     # Learning phase
    #     os.system(locust_command)

    #     print("[End of learning phase]")
    #     # End learning phase
    #     save_time(time_file, "a")

    #     # 5 minutes break
    #     time.sleep(5 * 60)
    #     save_time(time_file, "a")

    #     #Start enforcer (in parallel)
    #     print("[Starting enforcing VPA recommendations.]")

    # # if args.method != "HPA":
    # #     try:
    # #         test_name = "test1"
    # #         delete_folder(f"~/muOptK8s/ctrl/logs/{test_name}")
    # #         command = (f"gcloud container clusters get-credentials cluster-2 --region=northamerica-northeast1-a; "
    # #                    f"python3 ~/muOptK8s/ctrl/autoscaler.py -m {args.method} -wa {args.webapp} -n {test_name} -t {args.wctrl} -ut {args.utarget}")
    # #         enforcer_process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
    # #         print("Spawned autoscaler process")
    # #     except Exception as e:
    # #         enforcer_process.kill()
    # #         raise

    # # # Run the real experiment
    # # time.sleep(60)
