from datetime import datetime
from time import sleep


def schedulerProcessor(bridge_config, run_service):
    while run_service:
        for schedule in bridge_config["schedules"].keys():
            delay = 0
            if bridge_config["schedules"][schedule]["status"] == "enabled":
                if bridge_config["schedules"][schedule]["localtime"][-9:-8] == "A":
                    delay = random.randrange(0, int(bridge_config["schedules"][schedule]["localtime"][-8:-6]) * 3600 + int(bridge_config["schedules"][schedule]["localtime"][-5:-3]) * 60 + int(bridge_config["schedules"][schedule]["localtime"][-2:]))
                    schedule_time = bridge_config["schedules"][schedule]["localtime"][:-9]
                else:
                    schedule_time = bridge_config["schedules"][schedule]["localtime"]
                if schedule_time.startswith("W"):
                    pices = schedule_time.split('/T')
                    if int(pices[0][1:]) & (1 << 6 - datetime.today().weekday()):
                        if pices[1] == datetime.now().strftime("%H:%M:%S"):
                            print("execute schedule: " + schedule + " withe delay " + str(delay))
                            sendRequest(bridge_config["schedules"][schedule]["command"]["address"], bridge_config["schedules"][schedule]["command"]["method"], json.dumps(bridge_config["schedules"][schedule]["command"]["body"]), 1, delay)
                elif schedule_time.startswith("PT"):
                    timmer = schedule_time[2:]
                    (h, m, s) = timmer.split(':')
                    d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    if bridge_config["schedules"][schedule]["starttime"] == (datetime.utcnow() - d).strftime("%Y-%m-%dT%H:%M:%S"):
                        print("execute timmer: " + schedule + " withe delay " + str(delay))
                        sendRequest(bridge_config["schedules"][schedule]["command"]["address"], bridge_config["schedules"][schedule]["command"]["method"], json.dumps(bridge_config["schedules"][schedule]["command"]["body"]), 1, delay)
                        bridge_config["schedules"][schedule]["status"] = "disabled"
                else:
                    if schedule_time == datetime.now().strftime("%Y-%m-%dT%H:%M:%S"):
                        print("execute schedule: " + schedule + " withe delay " + str(delay))
                        sendRequest(bridge_config["schedules"][schedule]["command"]["address"], bridge_config["schedules"][schedule]["command"]["method"], json.dumps(bridge_config["schedules"][schedule]["command"]["body"]), 1, delay)
                        if bridge_config["schedules"][schedule]["autodelete"]:
                            del bridge_config["schedules"][schedule]
        if (datetime.now().strftime("%M:%S") == "00:10"): #auto save configuration every hour
            saveConfig()
            if (datetime.now().strftime("%H") == "23" and datetime.now().strftime("%A") == "Sunday"): #backup config every Sunday at 23:00:10
                saveConfig("config-backup-" + datetime.now().strftime("%Y-%m-%d") + ".json")
        sleep(1)

