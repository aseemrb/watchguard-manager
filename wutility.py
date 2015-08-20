#!/usr/bin/env
# -*- coding: utf-8 -*-

import socket
import signal
import requests
import httplib
import os
from urllib import urlencode
from urllib2 import *
from os import system, devnull, path
from sys import argv, exit
from time import sleep
from json import load
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject as gobject
from time import sleep

# the base url where all requests will be made
BASEURL = 'https://10.0.1.254:4100/wgcgi.cgi'

# load the dictionary of credentials and the timeout for auto function
DIRPATH = path.dirname(path.realpath(__file__))
JSONDATA = load(open(DIRPATH + '/config.json'))
CREDENTIALS = JSONDATA[0]
AUTOTIMEOUT = JSONDATA[1]['timeout']*1000

# login parameters
PARAMSLOGIN = {
    'fw_username': '',
    'fw_password': '',
    'fw_domain': 'gpra.in',
    'submit': 'Login',
    'action': 'fw_logon',
    'fw_logon_type': 'logon',
    'redirect': '',
    'lang': 'en-US',
}

# logout parameters
PARAMSLOGOUT = {
    'Logout': 'Logout',
    'action': 'fw_logon',
    'fw_logon_type': 'logout'
}

# status check parameters
PARAMSSTATUS = {
    'action': 'fw_logon',
    'fw_logon_type': 'status'
}


# login utility function
def WatchguardLogin():
    # iterate over available credentials and break when any of them succeeds
    for username, password in CREDENTIALS.iteritems():
        PARAMSLOGIN['fw_username'] = username
        PARAMSLOGIN['fw_password'] = password
        response = requests.post(BASEURL, data=PARAMSLOGIN, verify=False)
        responseText = response.text

        # return true and the username which was logged in successfully
        if responseText.find('successfully authenticated') != -1:
            return True, username

    # return false if login was unsuccessful for all usernames
    return False, username

# logout utility function
def WatchguardLogout():
    try:
        responseText = requests.post(BASEURL, data=PARAMSLOGOUT, verify=False)
        return True
    except:
        return False

# check login status, return true if logged in
def CheckStatus():
    response = requests.post('https://10.0.1.254:4100/wgcgi.cgi', data=PARAMSSTATUS, verify=False)
    if response.text.find('successfully authenticated') != -1:
        return True
    return False

# send the pretty system notification using notify-send
def SendNotification(message, title='WatchGuard Tool'):
    notify.Notification.new('<b>' + title + '</b>', message, DIRPATH + '/icons/tick.png').show()

# login into watchguard
def Login():
    status, username = WatchguardLogin()
    if status:
        SendNotification('ID: ' + username, 'Logged In')
    else:
        SendNotification('Login failed. Recheck credentials', 'Failed')

# logout from watchguard
def Logout():
    if WatchguardLogout():
        SendNotification('Successfully logged out', 'Logged Out')
    else:
        SendNotification('Logout failed', 'Failed')

# function to check if the internet connection is up
def InternetOn():
    try:
        response = urlopen('http://google.com',timeout=2)
        print response
        return True
    except URLError, e:
        return False