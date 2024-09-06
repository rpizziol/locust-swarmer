import time
from locust import HttpUser, task
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import json
import redis


class MyUser(HttpUser):

    #host = "http://34.118.144.160:8080"

    def on_start(self):
        self.rCon = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.rCon.incr('test1_wrk')

    def on_stop(self):
        self.rCon.decr('test1_wrk')

    @task
    def user_task(self):
        # Think time
        think_time = np.random.exponential(1000)  # in ms
        time.sleep(think_time / 1000)  # in s

        # Auth (Login)
        data = {"login":"uid0@email.com", "password":"password"}
        r = self.client.post("/login", data)


        
        user_id = data["login"]

        # Customer (ByidGET)
        r = self.client.get(f"/byid/{user_id}")
        
        # Customer (ByidPOST)
        userData = json.loads(r.text);
        number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
        userData["phoneNumber"] = number
        userData["password"] = data["password"]
        r = self.client.post(f"/byid/{user_id}", headers={"Content-Type": "application/json; charset=utf-8"}, json=userData)

        # Customer (ByidGET)
        # r = self.client.get(f"/byid/{user_id}")

        # Flight (QueryFlight)
        queryData = {"fromAirport": "FCO",
                    "toAirport": "LHR",
                    "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                    "returnDate": "Sat Sep 03 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                    "oneWay": False}
        r = self.client.post("/queryflights", queryData)
        flightData = json.loads(r.text);

        # Booking (BookFlight)
        toFlight = flightData["tripFlights"][0]["flightsOptions"][0]
        #retFlight = flightData["tripFlights"][1]["flightsOptions"][0]
        bookingData = {
                  "userid": userData["_id"],
                  "toFlightId": toFlight["_id"],
                  "toFlightSegId": toFlight["flightSegmentId"],
                  "retFlightId": "", #retFlight["_id"],
                  "retFlightSegId": "", #retFlight["flightSegmentId"],
                  "oneWayFlight": True # False
            }
        r = self.client.post("/bookflights", data=bookingData)
        bookingRes = json.loads(r.text)
        #print(bookingRes)

        # Booking (CancelBooking)
        bookToCancel = {"userid": userData["_id"], "number": bookingRes["departBookingId"]}
        r = self.client.post("/cancelbooking", data=bookToCancel)
        #bookToCancel["number"] = bookingRes["returnBookingId"]
        #r = self.client.post("/cancelbooking", data=bookToCancel)