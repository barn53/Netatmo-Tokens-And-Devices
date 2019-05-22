import requests
import datetime
import netatmo_lib as na

def getMeasure(access_token, device_id, module_id, type) :

    post_measure = {
        "access_token": access_token,
        "device_id": device_id,
        "module_id": module_id,
        "scale": "1day",
        "type": type,
        "date_begin": na.dateTimeToEpoch(datetime.datetime.now() - datetime.timedelta(days=30)),
        "date_end": na.nowInEpoch(),
        "limit": 1024,
        "optimize": False,
        "real_time": False
    }

    r = requests.post(na.url_getmeasure, data=post_measure, headers=na.headers)
    if r.status_code == 200 :
        print("")
        print(r.content)

if __name__ == '__main__':
    (access_token, refresh_token) = na.getTokens()
    access_token = na.refreshToken(refresh_token)
    devices = na.getDevices(access_token)

    getMeasure(access_token, devices[0]["id"], devices[0]["modules"][0]["id"], "sum_rain")

