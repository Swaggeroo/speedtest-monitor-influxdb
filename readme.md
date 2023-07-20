# Internet Monitor (for InfluxDB2)
This is a simple docker image to monitor your internet connection and send the results to InfluxDB2.

It uses the CLI of [speedtest.net](https://www.speedtest.net/) service to measure the speed of your internet connection.

### IMPORTANT: 
**This is not an official speedtest.net client, it is a third-party implementation. \
You have to agree to the speedtest.net [EULA](https://www.speedtest.net/about/eula), [Terms](https://www.speedtest.net/about/terms) and [Privacy](https://www.speedtest.net/about/privacy) before using it. (You can accept them via [ENV-VAR](#environment-variables)) \
Only non-commercial is allowed.**

## Usage
A sample docker-compose file is provided in the repository.

### Environment Variables
| Variable | Description | Default   | Required |
| --- | --- |-----------|----------|
| ACCEPT_GDPR | Accept the speedtest.net GDPR | FALSE     | **YES**  |
| ACCEPT_LICENSE | Accept the speedtest.net License | FALSE     | **YES**  |
| INFLUXDB_HOST | The InfluxDB host | localhost | no       |
| INFLUXDB_PORT | The InfluxDB port | 8086      | no       |
| INFLUXDB_ORG | The InfluxDB organization | -         | **YES**  |
| INFLUXDB_TOKEN | The InfluxDB token | -         | **YES**  |
| INFLUXDB_BUCKET | The InfluxDB bucket to write to | -         | **YES**  |
| INFLUXDB_SSL | Use SSL to connect to InfluxDB | false     | no       |
| INTERVAL | The interval in seconds to run the speedtest | 60        | no        |
