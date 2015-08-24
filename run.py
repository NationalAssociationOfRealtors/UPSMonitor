from snimpy.manager import Manager as M
from snimpy.manager import load
from datetime import datetime
import schedule
import influxdb
import config
import time

INFLUX = influxdb.InfluxDBClient(
    config.INFLUX_HOST,
    config.INFLUX_PORT,
    config.INFLUX_USER,
    config.INFLUX_PASSWORD,
    config.INFLUX_DATABASE,
)

try:
    res = INFLUX.create_database(config.INFLUX_DATABASE)
except: pass

load("/app/UPSMonitor/RFC1155-SMI.txt")
load("/app/UPSMonitor/RFC-1215")
load("/app/UPSMonitor/RFC-1212-MIB.txt")
load("/app/UPSMonitor/RFC1213-MIB.txt")
load("/app/UPSMonitor/stdupsv1.mib")
m = M("172.16.14.36", "NARpublic", 1)

model = m.upsIdentModel
manuf = m.upsIdentManufacturer

def job():
    points = []
    points.append(dict(
        measurement="ups_battery_voltage",
        tags=dict(
            model=model,
            manufacturer=manuf
        ),
        time=datetime.utcnow(),
        fields=dict(
            value=m.upsBatteryVoltage
        )
    ))

    points.append(dict(
        measurement="ups_battery_current",
        tags=dict(
            model=model,
            manufacturer=manuf
        ),
        time=datetime.utcnow(),
        fields=dict(
            value=m.upsBatteryCurrent
        )
    ))



    for l in m.upsInputFrequency:
        points.append(dict(
            measurement="ups_input_frequency",
            tags=dict(
                model=model,
                manufacturer=manuf,
                line=l,
            ),
            time=datetime.utcnow(),
            fields=dict(
                value=m.upsInputFrequency[l]
            )
        ))

    for l in m.upsInputVoltage:
        points.append(dict(
            measurement="ups_input_voltage",
            tags=dict(
                model=model,
                manufacturer=manuf,
                line=l,
            ),
            time=datetime.utcnow(),
            fields=dict(
                value=m.upsInputVoltage[l]
            )
        ))

    for l in m.upsOutputCurrent:
        points.append(dict(
            measurement="ups_output_current",
            tags=dict(
                model=model,
                manufacturer=manuf,
                line=l,
            ),
            time=datetime.utcnow(),
            fields=dict(
                value=m.upsOutputCurrent[l]
            )
        ))

    for l in m.upsOutputPower:
        points.append(dict(
            measurement="ups_output_power",
            tags=dict(
                model=model,
                manufacturer=manuf,
                line=l,
            ),
            time=datetime.utcnow(),
            fields=dict(
                value=m.upsOutputPower[l]
            )
        ))

    INFLUX.write_points(points)

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
