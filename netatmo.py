import requests
import json
import datetime
import secrets

url_token = "https://api.netatmo.com/oauth2/token"
url_getstationsdata = "https://api.netatmo.com/api/getstationsdata"
url_getmeasure = "https://api.netatmo.com/api/getmeasure"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "charset": "UTF-8"
}

def dateTimeToEpoch(dt):
    return int ((dt - datetime.datetime(1970,1,1)).total_seconds())

def nowInEpoch():
    return int ((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())

def getTokens() :

    post_token = {
        "client_id": secrets.client_id,
        "client_secret": secrets.client_secret,
        "grant_type": "password",
        "username": secrets.email,
        "password": secrets.password,
        "scope": "read_station"
    }

    access_token = ""
    refresh_token = ""
    r = requests.post(url_token, data=post_token, headers=headers)
    if r.status_code == 200 :
        #print(r.content)
        j = json.loads(r.content)
        access_token = j["access_token"]
        refresh_token = j["refresh_token"]
        print("")
        print("Access Token:  " + access_token)
        print("Refresh Token: " + refresh_token)

    return (access_token, refresh_token)

def refreshToken(refresh_token) :

    post_refresh = {
        "refresh_token": refresh_token,
        "client_id": secrets.client_id,
        "client_secret": secrets.client_secret,
        "grant_type": "refresh_token"
    }

    access_token = ""
    r = requests.post(url_token, data=post_refresh, headers=headers)
    if r.status_code == 200 :
        #print(r.content)
        j = json.loads(r.content)
        access_token = j["access_token"]
        print("New Access Token:  " + access_token)

    return access_token


def getDevices(access_token):

    post_getstationsdata = {
        "access_token": access_token,
        "device_id": None,
        "get_favorites": False
    }

    r = requests.post(url_getstationsdata, data=post_getstationsdata, headers=headers)
    if r.status_code == 200 :
        #print(r.content)
        j = json.loads(r.content)
        print("")

        devices = []
        print("Devices:")
        for device in j["body"]["devices"]:
            print("  ID: " + device["_id"]+ ", Name: " + device["module_name"])
            utc = device["dashboard_data"]["time_utc"]
            dt = datetime.datetime.fromtimestamp(utc)
            print("  Time: " + str(dt))

            types = []
            print("  Data Types:")
            for data_type in device["data_type"]:
                print("  - " + data_type)
                types.append(data_type)

            modules = []
            print("  Modules:")
            for module in device["modules"]:
                print("    ID: " + module["_id"]+ ", Name: " + module["module_name"])

                mtypes = []
                print("    Data Types:")
                for data_type in module["data_type"]:
                    print("    - " + data_type)
                    mtypes.append(data_type)

                m = {
                    "id": module["_id"],
                    "name": module["module_name"],
                    "types": mtypes
                }
                modules.append(m)

            d = {
                "id": device["_id"],
                "name": device["module_name"],
                "types": types,
                "modules": modules
            }

        devices.append(d)

        return devices


def getMeasure(access_token, device_id, module_id, type) :

    post_measure = {
        "access_token": access_token,
        "device_id": device_id,
        "module_id": module_id,
        "scale": "1day",
        "type": type,
        "date_begin": dateTimeToEpoch(datetime.datetime.now() - datetime.timedelta(days=30)),
        "date_end": nowInEpoch(),
        "limit": 1024,
        "optimize": False,
        "real_time": False
    }

    r = requests.post(url_getmeasure, data=post_measure, headers=headers)
    if r.status_code == 200 :
        print("")
        print(r.content)

if __name__ == '__main__':
    (access_token, refresh_token) = getTokens()
    access_token = refreshToken(refresh_token)
    devices = getDevices(access_token)

    getMeasure(access_token, devices[0]["id"], devices[0]["modules"][0]["id"], "sum_rain")

