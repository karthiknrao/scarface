import stem
import stem.connection

import time
import urllib2

from stem import Signal
from stem.control import Controller

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}

oldIP = "0.0.0.0"
newIP = "0.0.0.0"

nbrOfIpAddresses = 3
secondsBetweenChecks = 2

def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()

for i in range(0, nbrOfIpAddresses):
    if newIP == "0.0.0.0":
        renew_connection()
        newIP = request("http://icanhazip.com/")
    else:
        oldIP = newIP
        renew_connection()
        newIP = request("http://icanhazip.com/")

    seconds = 0

    while oldIP == newIP:
        time.sleep(secondsBetweenChecks)
        seconds += secondsBetweenChecks
        newIP = request("http://icanhazip.com/")
        print ("%d seconds elapsed awaiting a different IP address." % seconds)
    print ("")
    print ("newIP: %s" % newIP)
