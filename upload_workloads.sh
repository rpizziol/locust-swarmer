#!/bin/bash

folderpath="/home/robb/PycharmProjects/locust-flask-test/locust/workloads/"

gcloud compute scp --recurse $folderpath roberto_pizziol@instance-1:/home/roberto_pizziol/