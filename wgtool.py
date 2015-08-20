#!/usr/bin/env
# -*- coding: utf-8 -*-

from wutility import *

APPINDICATOR_ID = 'wgtool'
AUTOMODE = True
item_auto = None
item_manual = None
item_login = None
item_logout = None

def BuildMenu():
    menu = gtk.Menu()
    global item_auto, item_login, item_logout, item_manual
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', Quit)
    item_auto = gtk.MenuItem('✓Auto')
    item_auto.connect('activate', WGAuto)
    item_manual = gtk.MenuItem('Manual')
    item_manual.connect('activate', WGManual)
    item_login = gtk.MenuItem('Login')
    item_login.connect('activate', WGLogin)
    item_logout = gtk.MenuItem('Logout')
    item_logout.connect('activate', WGLogout)
    menu.append(item_auto)
    menu.append(item_manual)
    menu.append(gtk.SeparatorMenuItem())
    menu.append(item_login)
    menu.append(item_logout)
    menu.append(item_quit)
    menu.show_all()
    return menu

def WGAuto(source):
    LoopCheck()
    gobject.timeout_add(AUTOTIMEOUT, LoopCheck)
    item_auto.set_label('✓Auto')
    item_manual.set_label('Manual')

def LoopCheck():
    global AUTOMODE
    if InternetOn():
        if not CheckStatus():
            Login()
    return AUTOMODE

def WGManual(source):
    global AUTOMODE
    AUTOMODE = False
    item_auto.set_label('Auto')
    item_manual.set_label('✓Manual')


def WGLogin(source):
    if InternetOn():
        isLoggedIn = CheckStatus()
        if isLoggedIn:
            SendNotification('You are already logged in', 'Logged In')
        else:
            Login()
    else:
        SendNotification('Internet down', 'Disconnected')

def WGLogout(source):
    if InternetOn():
        isLoggedIn = CheckStatus()
        if isLoggedIn:
            Logout()
        else:
            SendNotification('Already logged out', 'Logged Out')
            
    else:
        SendNotification('Internet down', 'Disconnected')

def Quit(source):
    notify.uninit()
    gtk.main_quit()

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icons/tray.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(BuildMenu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    notify.init(APPINDICATOR_ID)
    LoopCheck()
    gobject.timeout_add(AUTOTIMEOUT, LoopCheck)
    gtk.main()

if __name__ == "__main__":
    main()