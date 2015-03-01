import http.cookiejar
import urllib
import html.parser
import datetime

class AuthParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.url = None
        self.method = "GET"
        self.params = {}
        self.form_opened = False
        self.form_parsed = False
        self.error = "OK"

    def handle_starttag(self, tag, attrs):
        if self.error != "OK":
            return
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                self.error = "Two Forms"
            elif self.form_opened:
                self.error = "Form started twice without closing"
            else:
                self.form_opened = True
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == "form":
            if "action" in attrs and "method" in attrs:
                self.url = attrs["action"]
                self.method = attrs["method"].upper()
            else:
                self.error = "Something wrong with <form> params"
        elif tag == "input":
            if "type" in attrs and "name" in attrs and attrs["type"] in ["hidden","text","password"]:
                self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        if self.error != "OK":
            return
        tag = tag.lower()
        if tag == "form":
            if not self.form_opened:
                self.error = "Unexpected end of tag <form>"
            self.form_opened = False
            self.form_parsed = True

    def print_params(self):
        for name in self.params:
            print(name)
            print(self.params[name])

def auth(email, password, client_id, scope):
    def auth_usr(email, password, client_id, scope, opener):
        print("TRY TO AUTH")
        #TODO словить эксепшн
        login_page = "http://oauth.vk.com/oauth/authorize?" + \
                "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
                "client_id=%s&scope=%s&display=wap" % (client_id, ",".join(scope))
        #print(login_page)
        auth_page = opener.open("http://oauth.vk.com/oauth/authorize?" + \
                "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
                "client_id=%s&scope=%s&display=wap" % (client_id, ",".join(scope)))
        auth_page = auth_page.read()
        parser = AuthParser()
        parser.feed(str(auth_page))
        parser.close()
        if not parser.form_parsed or parser.url is None or "pass" not in parser.params or \
              "email" not in parser.params or parser.method != "POST":
            parser.error = "Some problems"
        if parser.error != "OK":
            return -1, -1, parser.error
        parser.params["email"] = email
        parser.params["pass"] = password
        parser.params["v"] = "5.2"
        #TODO словить эксепшн
        response = opener.open(parser.url, urllib.parse.urlencode(parser.params).encode("UTF-8"))
        page = response.read()
        url = response.geturl()
        return page, url, parser.error

    def access(page, opener):
        parser = AuthParser()
        parser.feed(str(page))
        parser.close()
        if not parser.form_parsed or parser.url is None or parser.method != "POST":
            parser.error = "Problems with giving access"
            return -1, -1, parser.error
        #TODO словить эксепшн
        response = opener.open(parser.url, urllib.parse.urlencode(parser.params).encode("UTF-8"))
        return response.geturl()

    if not isinstance(scope, list):
        scope = [scope]
    error = "OK"
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPRedirectHandler())
    page, url, error = auth_usr(email, password, client_id, scope, opener)
    #print(page)
    #print(url)
    if error != "OK":
        return "", error
    second_page = url
    #print("SECOND")
    #print(second_page)
    if urllib.parse.urlparse(url).path != "/blank.html":
        url = access(page, opener)
    #print(urllib.parse.urlparse(url).path)
    if urllib.parse.urlparse(url).path != "/blank.html":
        #отрисовать капчу
      error = "Too much calls, u must log in at " + second_page
    return str(url), error

def try_auth(cfg):
    status = False
    while not status:
        if cfg.expires_in > datetime.datetime.now():
            break
        if cfg.email == "":
            cfg.email = input("email: ")
            cfg.save_config()
        if cfg.password == "":
            cfg.password = input("password: ")
            cfg.save_config()
        url, error = auth(cfg.email, cfg.password, cfg.client_id, cfg.scope)
        if error != "OK":
            print(error)
            cfg.email = ""
            cfg.password = ""
            cfg.save_config()
            continue
        url = urllib.parse.urlparse(url)
        attrs = dict(attr.split("=") for attr in url.fragment.split("&"))
        cfg.access_token = attrs["access_token"] if "access_token" in attrs else ""
        cfg.user_id = attrs["user_id"] if "user_id" in attrs else ""
        lifetime = int(attrs["expires_in"]) if "expires_in" in attrs and attrs["expires_in"] != "" else 0
        lifetime -= 3600
        lifetime = max(0, lifetime)
        delta = datetime.timedelta(seconds = lifetime)
        cfg.expires_in = datetime.datetime.now() + delta
        if cfg.access_token != "" and cfg.email != "" and cfg.password != "":
            cfg.save_config()
            status = True
