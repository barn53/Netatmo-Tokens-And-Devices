import netatmo_lib as na

(access_token, refresh_token) = na.getTokens()
devices = na.getDevices(access_token)
