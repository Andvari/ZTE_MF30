#!/usr/bin/env python
'''
Created on Oct 26, 2012

@author: nemo
'''

import os
import gtk
import appindicator
import urllib
import threading
import pynotify

class ZTE_MF30(object):

    def __init__(self):
        self.old_bstatus = 0
        self.bstatus = 0
        self.old_type = "EDGE"
        self.type = "3G"
        
        self.ind = appindicator.Indicator("hello world client", "", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        
        self.ind.set_icon_theme_path("home/nemo/workspace/ZTE_MF30/src/images")
        self.ind.set_icon("router_on")
        
        self.tmr = threading.Timer(0.5, self.on_timer)
        self.tmr.start()

        
    def on_timer(self):
        try:
            params = urllib.urlencode({'systemDate' : 0113131112, 'user' : 'admin', 'psw' : 'admin', 'languageSelect' : 'ru', 'save_login' : 1, 'save_login_enablebox' : 1})
            response = urllib.urlopen('http://192.168.0.1/goform/login', params)
            page = response.read()
            response = urllib.urlopen('http://192.168.0.1/index.asp', params)
            page = response.read()
        
            response = urllib.urlopen('http://192.168.0.1/logo.asp', params)
            page = response.read()

            self.bstatus = page[page.find('battery_status') + 18 : ]
            self.bstatus = self.bstatus[: self.bstatus.find("'")]
        
            self.network = page[page.find('network_provider') + 20 : ]
            self.network = self.network[: self.network.find("'")]
        
            self.type = page[page.find('network_type') + 16 : ]
            self.type = self.type[: self.type.find("'")]
        
            response = urllib.urlopen('http://192.168.0.1/content.asp', params)
            page = response.read()
        
            self.strenght = page[page.find('sig_strength') + 16 : ]
            self.strenght = self.strenght[: self.strenght.find("'")]
            self.ind.set_icon("router_on")
            
            self.tmr = threading.Timer(60, self.on_timer)
        except:
            self.bstatus = " -- "
            self.strenght = " -- "
            self.type = " -- "
            self.network = " -- "
            self.ind.set_icon("router_off")
            self.tmr = threading.Timer(5, self.on_timer)

        
        self.menu = gtk.Menu()
        
        item = gtk.MenuItem()
        item.add(gtk.Label("Battery: " + str(self.bstatus) + "%"))
        self.menu.append(item)
        item.show()

        item = gtk.MenuItem()
        item.add(gtk.Label("Strenght: " + str(self.strenght) + " dB"))
        self.menu.append(item)
        item.show()

        item = gtk.MenuItem()
        item.add(gtk.Label("Network: " + str(self.type)))
        self.menu.append(item)
        item.show()
        
        item = gtk.MenuItem()
        item.add(gtk.Label("Provider: " + str(self.network)))
        self.menu.append(item)
        item.show()
        
        item = gtk.SeparatorMenuItem()
        self.menu.append(item)
        item.show()
        
        item_quit = gtk.MenuItem()
        item_quit.add(gtk.Label("Quit"))
        self.menu.append(item_quit)
        item_quit.show()
        
        item_quit.connect("activate", gtk.main_quit)
        
        self.ind.set_menu(self.menu)
        
        self.tmr.start()
            
zte = ZTE_MF30()
gtk.gdk.threads_init()
gtk.main()
os._exit(0)

