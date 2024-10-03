# import csv
from locust import LoadTestShape
import pandas as pd
# import redis
# from datetime import datetime, timezone
# from zoneinfo import ZoneInfo


class TraceShape(LoadTestShape):
    lastStage = None
    mod = None
    shift = None
    duration = None
    traceFile = None
    data = None

    def __init__(self, mod=45, shift=10, duration=4200, traceFile="./workloads/sin800.csv"): # 4200s = 70m, 2400s = 40m mod=130, shift=10 # mod=50, shift=20 (nel paper)
        super().__init__()
        self.mod = mod
        self.shift = shift
        self.duration = duration
        self.traceFile = traceFile
        self.data = pd.read_csv(self.traceFile).to_numpy().T[0]
        self.maxIndex = len(self.data)
        # self.rCon = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # Rescale the trace
        mx = max(self.data)
        mn = min(self.data)
        self.data = [(v - mn) / (mx - mn) * self.mod + self.shift for v in self.data]

    def tick(self):
        run_time = self.get_run_time()
        if run_time <= self.duration:
            if int(run_time) % 1 == 0:  # Update number of users every 1 sec
                users_value = self.f(run_time)
                self.users = (users_value, 100)
                # self.rCon.set("test1_wrk", str(users_value))
                # self.save_users(users_value) # Save users in a csv
            return self.users
        return None

    def f(self, x):
        return int(self.data[int(x) % self.maxIndex])

    # def save_users(self, users):
    #     with open("./workload_sin900.csv", mode='a', newline='') as file:
    #         writer = csv.writer(file)
    #         now = self.get_current_time_iso()
    #         writer.writerow([now, users])
    #         print(f"{now} Saved users: {users}")
    #
    # def get_current_time_iso(self):
    #     current_time = datetime.now(ZoneInfo('Etc/GMT-2'))
    #     formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S%z')
    #     return formatted_time
