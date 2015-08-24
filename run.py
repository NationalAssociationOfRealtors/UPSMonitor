from snimpy.manager import Manager as M
from snimpy.manager import load

load("/app/UPSMonitor/RFC1155-SMI.txt")
load("/app/UPSMonitor/RFC-1215")
load("/app/UPSMonitor/RFC-1212-MIB.txt")
load("/app/UPSMonitor/RFC1213-MIB.txt")
load("/app/UPSMonitor/stdupsv1.mib")
m = M("172.16.14.36", "NARpublic", 1)
print m.upsIdentManufacturer
print m.upsIdentModel
print m.upsBatteryStatus
print m.upsEstimatedMinutesRemaining
print m.upsBatteryVoltage
print m.upsBatteryCurrent
print m.upsInputLineBads
for l in m.upsInputFrequency:
    print "{}: {}".format(l, m.upsInputFrequency[l])

for l in m.upsInputVoltage:
    print "{}: {}".format(l, m.upsInputVoltage[l])

for l in m.upsOutputCurrent:
    print "{}: {}".format(l, m.upsOutputCurrent[l])

for l in m.upsOutputPower:
    print "{}: {}".format(l, m.upsOutputPower[l])
