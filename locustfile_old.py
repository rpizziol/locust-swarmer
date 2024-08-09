import time
from locust import HttpUser, task
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import json



class MyUser(HttpUser):

    auth_url = "http://34.47.9.198:80"

    booking_bookflights_url = "http://34.95.26.8:80"
    booking_cancelbooking = "http://34.95.33.134:80"

    customer_byidget_url = "http://34.118.136.45:80"
    customer_byidpost_url = "http://34.152.53.121:80"

    flight_queryflights_url = "http://34.118.165.242:80"

    mongo_url = "http://34.152.13.79:27017"

    def on_start(self):

        pass
        # Create a session and configure retries
        # retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        # self.client.mount("http://", HTTPAdapter(max_retries=retries))
        # self.client.mount("https://", HTTPAdapter(max_retries=retries))

    # @task
    # def index_page(self):
    #     data = {"login":"uid0@email.com", "password":"password"}
    #     think_time = np.random.exponential(1000)  # in ms
    #     time.sleep(think_time / 1000)  # in s
    #     try:
    #         self.client.post("/login", data=data)
    #     except Exception as e:
    #         pass  # Don't die if there's an error
    
    @task        
    def user_logic(self):
        think_time = np.random.exponential(1000)  # in ms
        time.sleep(think_time / 1000)  # in s

        s = requests.Session()

        # Auth (and validateid)
        # print("-- Auth Test --")
        data = {"login":"uid0@email.com", "password":"password"}
        r = s.post(url=f"{self.auth_url}/login", data=data)
        # print(r)
        # print(r.text)
        # print("\n")


        # customer-byid-GET
        # print("-- ViewProfile Test --")
        r = s.get(url=f"{self.customer_byidget_url}/byid/%s" % (data["login"]), data={})
        # print(r)
        # print(r.text)
        # print("\n")

        # customer-byid-POST
        # print("-- UpdateProfile Test --")
        userData = json.loads(r.text);
        number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
        userData["phoneNumber"] = number
        userData["password"] = data["password"]
        r = s.post(url=f"{self.customer_byidpost_url}/byid/%s" % (data["login"]), headers={"Content-Type": "application/json; charset=utf-8"}, json=userData)
        # print(r)
        # print(r.text)
        # print("\n")

        # query flight
        # print("-- QueryFlights Test --")
        queryData = {"fromAirport": "FCO",
                    "toAirport": "LHR",
                    "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                    "returnDate": "Sat Sep 03 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                    "oneWay": False}
        r = s.post(url=f"{self.flight_queryflights_url}/queryflights", data=queryData)

        # print(r)
        flightData = json.loads(r.text);
        # print(r.text)
        # print("\n")


        # book flight
        # print("-- BookFlight Test --")
        toFlight = flightData["tripFlights"][0]["flightsOptions"][0]
        retFlight = flightData["tripFlights"][1]["flightsOptions"][0]
        bookingData = {
                  "userid": userData["_id"],
                  "toFlightId": toFlight["_id"],
                  "toFlightSegId": toFlight["flightSegmentId"],
                  "retFlightId": retFlight["_id"],
                  "retFlightSegId": retFlight["flightSegmentId"],
                  "oneWayFlight": False
            }
        r = s.post(url=f"{self.booking_bookflights_url}/bookflights", data=bookingData)
        # print(r)
        # print("booking")
        bookingRes = json.loads(r.text)
        # print(r.text)
        # print("\n")


        # cancel booking
        # print("-- CancelBooking Test --")
        bookToCancel = {"userid": userData["_id"],
                        "number": bookingRes["departBookingId"]}
        r = s.post(url=f"{self.booking_cancelbooking}/cancelbooking", data=bookToCancel)
        # print(r)
        # print(r.text)
        # print("\n")
        bookToCancel["number"] = bookingRes["returnBookingId"]
        r = s.post(url=f"{self.booking_cancelbooking}/cancelbooking", data=bookToCancel)
        # print(r)
        # print(r.text)
        # print("\n")

        s.close()


        # istanzio il workload
        # nuser=1
        # users=[]
        # for i in range(nuser):
        #     users.append(clientThread())
        
        #s = requests.Session() 
        
        # come primo workload eseguo login/view_profile/update_profile
        # come workload finale eseguo un untete che con una certa probabilita 
            # login
            # modifica il suo profilo
            # cerca un volo esistente 
                # con prob p1
                    # fa il booking di quel volo (Devo cancellare il booking? forse si per coerenza)
                # con prob 1-p1
                # torna alla ricerca
        
        # login
        # data to be sent to api
        # # estraggo un profilo random da visualizzare e aggiornare in base a quelli disponibili
        # #s = self.client.Session() #requests.Session()
        # data = {"login":"uid0@email.com", "password":"password"}
        # r = self.client.post(url=f"http://{MyUser.auth_ip}/login", data=data)
        # #print('login resp', r.text)
        
        # # view profile
        # st = time.time()
        # r = self.client.get(url=f"http://{MyUser.customer_ip}/byid/%s" % (data["login"]), data={})
        # #print('view profile resp', r.text)
        # # print("view profile time %f"%(time.time()-st))
        # userData = json.loads(r.text);
        
        # # update profile
        # number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
        # userData["phoneNumber"] = number
        # userData["password"] = data["password"];
        # st = time.time()
        # r = self.client.post(url=f"http://{MyUser.customer_ip}/byid/%s" % (data["login"]), headers={"Content-Type": "application/json;"},
        #          json=userData)
        # #print("update profile resp", r.text)
        
        # # print("update profile time %f"%(time.time()-st))
        # userData = json.loads(r.text);
        
        # # view profile
        # st = time.time()
        # r = self.client.get(url=f"http://{MyUser.customer_ip}/byid/%s" % (data["login"]), data={})
        # # print("view profile time %f"%(time.time()-st))
        # userData = json.loads(r.text);
        # #print("view2 profile", userData)
        
        # if(not userData["phoneNumber"] == number):
        #     raise ValueError("number not saved successfully")

        # # query flight
        # queryData = {"fromAirport": "FCO",
        #             "toAirport": "LHR",
        #             "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora legale dell’Europa centrale)", #Tue Sep 13 2022 00:00:00 GMT+0200 (Ora legale dell’Europa centrale)",
        #             "returnDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora legale dell’Europa centrale)", #Tue Sep 13 2022 00:00:00 GMT+0200 (Ora legale dell’Europa centrale)",
        #             "oneWay": False}
        # r = self.client.post(url=f"http://{MyUser.flight_ip}/queryflights", data=queryData)

        # #print(r)
        # flightData = json.loads(r.text);
        # #print(flightData)
                              
        # # book flight
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
        # r = self.client.post(url=f"http://{MyUser.booking_ip}/bookflights", data=bookingData)
        # #print("booking")
        # bookingRes = json.loads(r.text)
        # #print(bookingRes)
        
        # # cancel booking
        # bookToCancel = {"userid": userData["_id"],
        #                 "number": bookingRes["departBookingId"]}
        # r = self.client.post(url=f"http://{MyUser.booking_ip}/cancelbooking", data=bookToCancel)
        # #print(r.text)
        # bookToCancel["number"] = bookingRes["returnBookingId"]
        # r = self.client.post(url=f"http://{MyUser.booking_ip}/cancelbooking", data=bookToCancel)
        # #print(r.text)