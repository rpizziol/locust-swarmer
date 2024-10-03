import time
from locust import HttpUser, task
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import redis


class MyUser(HttpUser):

    def on_start(self):
        # Create a session and configure retries
        # retries = Retry(total=1, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        # self.client.mount("http://", HTTPAdapter(max_retries=retries))
        # self.client.mount("https://", HTTPAdapter(max_retries=retries))
        self.rCon = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.rCon.incr('test1_wrk')

    def on_stop(self):
        self.rCon.decr('test1_wrk')

    @task
    def index_page(self):
        think_time = 1000 #np.random.exponential(1000)  # in ms
        time.sleep(think_time / 1000)  # in s
        self.client.get("/")
