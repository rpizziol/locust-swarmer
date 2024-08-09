import requests
import json
import numpy as np


proxy_url = "http://34.118.144.160:8080"
auth_url = "http://34.152.20.22:80"

s = requests.Session()

# Auth (and validateid)
print("-- Auth Test --")
data = {"login":"uid0@email.com", "password":"password"}
r = s.post(url=f"{proxy_url}/login", data=data)
print(r)
print(r.text)
print("\n")

s.close()


# # URLS
# auth_url = "http://34.47.9.198:80"

# booking_bookflights_url = "http://34.95.26.8:80"
# booking_cancelbooking = "http://34.95.33.134:80"

# customer_byidget_url = "http://34.118.136.45:80"
# customer_byidpost_url = "http://34.152.53.121:80"

# flight_queryflights_url = "http://34.118.165.242:80"


# mongo_url = "http://34.152.13.79:27017"

# s = requests.Session()

# # Auth (and validateid)
# print("-- Auth Test --")
# data = {"login":"uid0@email.com", "password":"password"}
# r = s.post(url=f"{auth_url}/login", data=data)
# print(r)
# print(r.text)
# print("\n")


# # customer-byid-GET
# print("-- ViewProfile Test --")
# r = s.get(url=f"{customer_byidget_url}/byid/%s" % (data["login"]), data={})
# print(r)
# print(r.text)
# print("\n")

# # customer-byid-POST
# print("-- UpdateProfile Test --")
# userData = json.loads(r.text);
# number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
# userData["phoneNumber"] = number
# userData["password"] = data["password"]
# r = s.post(url=f"{customer_byidpost_url}/byid/%s" % (data["login"]), headers={"Content-Type": "application/json; charset=utf-8"}, json=userData)
# print(r)
# print(r.text)
# print("\n")

# # query flight
# print("-- QueryFlights Test --")
# queryData = {"fromAirport": "FCO",
#             "toAirport": "LHR",
#             "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
#             "returnDate": "Sat Sep 03 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
#             "oneWay": False}
# r = s.post(url=f"{flight_queryflights_url}/queryflights", data=queryData)

# print(r)
# flightData = json.loads(r.text);
# print(flightData)
# print("\n")


# # book flight
# print("-- BookFlight Test --")
# toFlight = flightData["tripFlights"][0]["flightsOptions"][0]
# retFlight = flightData["tripFlights"][1]["flightsOptions"][0]
# bookingData = {
#           "userid": userData["_id"],
#           "toFlightId": toFlight["_id"],
#           "toFlightSegId": toFlight["flightSegmentId"],
#           "retFlightId": retFlight["_id"],
#           "retFlightSegId": retFlight["flightSegmentId"],
#           "oneWayFlight": False
#     }
# r = s.post(url=f"{booking_bookflights_url}/bookflights", data=bookingData)
# print(r)
# # print("booking")
# bookingRes = json.loads(r.text)
# print(bookingRes)
# print("\n")


# # cancel booking
# print("-- CancelBooking Test --")
# bookToCancel = {"userid": userData["_id"],
#                 "number": bookingRes["departBookingId"]}
# r = s.post(url=f"{booking_cancelbooking}/cancelbooking", data=bookToCancel)
# print(r)
# print(r.text)
# bookToCancel["number"] = bookingRes["returnBookingId"]
# r = s.post(url=f"{booking_cancelbooking}/cancelbooking", data=bookToCancel)
# print(r)
# print(r.text)
# print("\n")

# s.close()

# # # customer-validateid
# # data = {"login":"uid0@email.com", "password":"password"}
# # r = s.post(url=f"{proxy_url}/validateid", data=data)
# # print(r)
# # print(r.text)
