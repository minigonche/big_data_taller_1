#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import datetime


#init

# Date Format YYYY-MM-DD hh:mm:ss
format = '%Y-%m-%d H:%M:%S'
inTimeFrame = False
start = 10
end = 11
counter = 0
header = ''
headers = []

possible_headers = ['Dispatching_base_num,Pickup_date,locationID', 'Dispatching_base_num,Pickup_DateTime,DropOff_datetime,PUlocationID,DOlocationID',
    'VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount',
    'vendor_id,pickup_datetime,dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,rate_code,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,surcharge,mta_tax,tip_amount,tolls_amount,total_amount',
    'vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance, pickup_longitude, pickup_latitude, rate_code, store_and_fwd_flag, dropoff_longitude, dropoff_latitude, payment_type, fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount',
    'vendor_name,Trip_Pickup_DateTime,Trip_Dropoff_DateTime,Passenger_Count,Trip_Distance,Start_Lon,Start_Lat,Rate_Code,store_and_forward,End_Lon,End_Lat,Payment_Type,Fare_Amt,surcharge,mta_tax,Tip_Amt,Tolls_Amt,Total_Amt',
    'VendorID,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,RatecodeID,PULocationID,DOLocationID,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_surcharge,total_amount,payment_type,trip_type',
    'VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,RatecodeID,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount',
    'VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,RateCodeID,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount',
    'VendorID,lpep_pickup_datetime,Lpep_dropoff_datetime,Store_and_fwd_flag,RateCodeID,Pickup_longitude,Pickup_latitude,Dropoff_longitude,Dropoff_latitude,Passenger_count,Trip_distance,Fare_amount,Extra,MTA_tax,Tip_amount,Tolls_amount,Ehail_fee,Total_amount,Payment_type,Trip_type',
    'VendorID,lpep_pickup_datetime,Lpep_dropoff_datetime,Store_and_fwd_flag,RateCodeID,Pickup_longitude,Pickup_latitude,Dropoff_longitude,Dropoff_latitude,Passenger_count,Trip_distance,Fare_amount,Extra,MTA_tax,Tip_amount,Tolls_amount,Ehail_fee,improvement_surcharge,Total_amount,Payment_type,Trip_type']

def inHeaders(header):

    if header in possible_headers:
        return True
    else:
        return False

for line in sys.stdin:

    destination = None
    pickupTime = None


    line = line.strip()
    data = line.split(',')
    header = []

    if counter == 0:
        header = line
        #print(header)
        continue

    counter += 1

    if inHeaders(header):
        pickupTime = data[1]
        if 'DOlocationID' in headers:
            index = headers.index('DOlocationID')
            destination = data[index]
    else:
        continue

    if pickupTime:
        try:
            pickupTime = datetime.strptime(pickupTime, format)
            hour = pickupTime.hour
            if (start <= hour) and (hour <= end):
                inTimeFrame = True

        except ValueError:
            print(pickupTime + 'does not match format')


    else:
        hour = None

    if destination and hour and inTimeFrame:
        print('%s\t%s' % (destination, 1))

