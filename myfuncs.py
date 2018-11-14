# -*- coding: utf-8 -*-
# mqttwarn example function extensions
import time
import copy

try:
    import json
except ImportError:
    import simplejson as json

def icinga2_sensor_battery(data, srv):
    batt_warn = 20
    batt_crit = 10

    batt_val = int(float(data['payload']))
    status = 0
    code = 'OK'

    if batt_val <= batt_warn:
        status = 1
        code   = 'WARNING'
    if batt_val <= batt_crit:
        status = 2
        code   = 'CRITICAL'

    # /sensor/location/type/battery
    parts    = data['topic'].split('/')
    location = parts[2]
    type     = parts[3]
    host     = "iot-mqtt-host-{0}-{1}".format(location, type)
    service  = "{0}!mqtt-battery".format(host)

    #print "Sending mqttwarn check result to host '{0}' and service '{1}'".format(host, service)
    icinga2_payload = {
        'exit_status'     : status,
        'plugin_output'   : "BATTERY {0}: {1}%".format(code, batt_val),
        'service'         : service,
        'performance_data': [ "battery={0}%;{1};{2}".format(batt_val, batt_warn, batt_crit) ],
        }
    return json.dumps(icinga2_payload)
