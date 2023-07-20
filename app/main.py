import os
import re
import subprocess
from influxdb_client import InfluxDBClient
import threading
import time

print("Staring speedtest")

accepted_license = os.getenv('ACCEPT_LICENSE').lower() == 'true'
accepted_gdpr = os.getenv('ACCEPT_GDPR').lower() == 'true'
interval = os.getenv('INTERVAL')

influxdb_host = os.getenv('INFLUXDB_HOST')
influxdb_port = os.getenv('INFLUXDB_PORT')
influxdb_token = os.getenv('INFLUXDB_TOKEN')
influxdb_org = os.getenv('INFLUXDB_ORG')
influxdb_bucket = os.getenv('INFLUXDB_BUCKET')
influxdb_ssl = os.getenv('INFLUXDB_SSL')

if not (accepted_license and accepted_gdpr):
    print("You must accept the license and gdpr")
    exit(1)

if not interval:
    print("Interval not set")
    print("Defaulting to 60 minutes")
    interval = 60
else:
    interval = int(interval)
    if interval < 30:
        print("Interval not set or too low")
        print("Defaulting to 60 minutes")
        interval = 60

if not influxdb_host:
    print("Influxdb host not set")
    print("Defaulting to localhost")
    influxdb_host = 'localhost'

if not influxdb_port:
    print("Influxdb port not set")
    print("Defaulting to 8086")
    influxdb_port = 8086
else:
    influxdb_port = int(influxdb_port)

if not influxdb_bucket:
    print("Influxdb bucket not set")
    exit(1)

if not influxdb_token:
    print("Influxdb token not set")
    exit(1)

if not influxdb_org:
    print("Influxdb org not set")
    exit(1)

if not influxdb_ssl:
    influxdb_ssl = False
else:
    influxdb_ssl = influxdb_ssl.lower() == 'true'


def run_speedtest():
    print("Running speedtest " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    print("Speedtest complete now parsing results")

    ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
    jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)

    print("Ping: " + ping + "ms")
    print("Download: " + download + "Mbps")
    print("Upload: " + upload + "Mbps")
    print("Jitter: " + jitter + "ms")

    speed_data = [
        {
            "measurement" : "internet_speed",
            "tags" : {
                "host": "OoklaSpeedtest"
            },
            "fields" : {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping),
                "jitter": float(jitter)
            }
        }
    ]

    client = InfluxDBClient(url=(influxdb_host+':'+str(influxdb_port)), token=influxdb_token, org=influxdb_org, ssl=influxdb_ssl)
    write_api = client.write_api()
    write_api.write(influxdb_bucket, influxdb_org, speed_data)
    print("Speedtest complete")

run_speedtest()
loop = threading.Event()
print("Running speedtest every " + str(interval) + " minutes")
while not loop.wait(interval * 60):
    run_speedtest()
