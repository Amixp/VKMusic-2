import datetime
import os
import auth

class config:
    def __init__(self):
        #appid must contain only your appid
        appid = ""
        with open('appid', 'r') as appidfile:
            appid = appidfile.read()
            if appid[len(appid) - 1] == '\n':
                appid = appid[:len(appid) - 1]
        if not os.path.exists('lib.cfg'):
            with open('lib.cfg', 'w') as cfgfile:
                cfgfile.write('email= \npassword= \nclient_id='+appid+'\nscope=audio\naccess_token= \nuser_id= \nexpires_in=2000-01-01 00:00:00.000000\npath=Songs/\ninterval=5\nreplacement=')
        cfgfile = open('lib.cfg', 'r')
        conf = cfgfile.read()
        if conf[len(conf) - 1] == '\n':
            conf = conf[:len(conf) - 1]
        tmp = conf.split("\n")
        attrs = dict( attr.split("=") for attr in conf.split("\n") )
        if "path" not in attrs or "email" not in attrs or \
            "password" not in attrs or "client_id" not in attrs or  \
            "scope" not in attrs or "access_token" not in attrs or  \
            "user_id" not in attrs or "expires_in" not in attrs or \
            "replacement" not in attrs or "interval" not in attrs:
            print("Config file was broken")
            with open('lib.cfg', 'w') as cfgfile:
                cfgfile.write('email= \npassword= \nclient_id='+appid+'\nscope=audio\naccess_token= \nuser_id= \nexpires_in=2000-01-01 00:00:00.000000\npath=Songs/\ninterval=5\nreplacement=')
            f = open('lib.cfg', 'r')
            conf = f.read()
            attrs = dict( attr.split("=") for attr in conf.split("\n") )

        self.path = attrs["path"]
        self.email = attrs["email"]
        self.password = attrs["password"]
        self.client_id = attrs["client_id"]
        self.scope = attrs["scope"]
        self.access_token = attrs["access_token"]
        self.user_id = attrs["user_id"]
        self.expires_in = attrs["expires_in"]
        self.replacement = attrs["replacement"]
        self.interval = int(attrs["interval"])
        if self.expires_in != '' :
            temp = self.expires_in.split(" ")
            ymd = temp[0].split("-")
            temp = temp[1].split(".")
            hms = temp[0].split(":")
            self.expires_in = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms[0]), int(hms[1]), int(hms[2]), int(temp[1]))
        else:
            self.expires_in = datetime.datetime.now()

    def save_config(self):
        cfgfile = open('lib.cfg', 'w')
        conf = ''
        conf += 'email=' + self.email
        conf += '\npassword=' + self.password
        conf += '\nclient_id=' + self.client_id
        conf += '\nscope=' + self.scope
        conf += '\naccess_token=' + self.access_token
        conf += '\nuser_id=' + self.user_id
        conf += '\nexpires_in=' + str(self.expires_in)
        conf += '\npath=' + self.path
        conf += '\nreplacement=' + self.replacement
        conf += '\ninterval=' + str(self.interval)
        cfgfile.write(conf)
        cfgfile.close()

    def update(self):
        auth.try_auth(self)
