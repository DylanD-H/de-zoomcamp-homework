import json
import csv
from kafka import KafkaProducer
from time import time

def json_serializer(data):
    return json.dumps(data).encode('utf-8')


server = 'localhost:9092'


producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

print("producer.bootstrap_connected: ", producer.bootstrap_connected())


green_trips = 'data/green_tripdata_2019-10.csv'
columns_to_keep = ['lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount']


t0 = time()
with open(green_trips, 'r', newline='',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        message = {}
        for col in columns_to_keep:
            if col in ['PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount']:
                if row[col] == '':
                    message[col] = 0 
                else:
                    message[col] = row[col]
            else:
                message[col] = row[col]

        producer.send('green-trips', value=message)
    producer.flush()
t1 = time()
took = t1-t0
print("Time to send and flush: ", took)

