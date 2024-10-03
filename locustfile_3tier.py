import time
from locust import HttpUser, task
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class MyUser(HttpUser):

    def on_start(self):
        # Create a session and configure retries
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.client.mount("http://", HTTPAdapter(max_retries=retries))
        self.client.mount("https://", HTTPAdapter(max_retries=retries))

    @task
    def index_page(self):
        think_time = np.random.exponential(1000)  # in ms
        time.sleep(think_time / 1000)  # in s
        try:
            self.client.get("/")
        except Exception as e:
            pass  # Don't die if there's an error
