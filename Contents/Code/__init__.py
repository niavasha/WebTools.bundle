#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################################################################
#					WebTools bundle for Plex
#
#					Allows you to manipulate subtitles on Plex Media Server
#
#					Author:			dagaluf, a Plex Community member
#					Author:			dane22, a Plex Community member
#
#					Support thread:	https://forums.plex.tv/discussion/126254
#
######################################################################################################################

#********* Constants used **********
SECRETKEY = ''

#********** Imports needed *********
import sys, locale
from webSrv import startWeb, stopWeb
from random import randint   #Used for Cookie generation
import uuid			#Used for secrectKey
import time
import socket
from consts import DEBUGMODE, VERSION, PREFIX, NAME, ICON

#********** Initialize *********
def Start():
	global SECRETKEY
	runningLocale = locale.getdefaultlocale()
	if DEBUGMODE:		
		print("********  Started %s on %s at %s with locale set to %s **********" %(NAME  + ' V' + VERSION, Platform.OS, time.strftime("%Y-%m-%d %H:%M"), runningLocale))
	Log.Debug("*******  Started %s on %s at %s with locale set to %s ***********" %(NAME + ' V' + VERSION, Platform.OS, time.strftime("%Y-%m-%d %H:%M"), runningLocale))
	# TODO: Nasty workaround for issue 189
	if (Platform.OS == 'Windows' and locale.getpreferredencoding() == 'cp1251'):
		sys.setdefaultencoding("cp1251")
		Log.Debug("Default set to cp1251")
	HTTP.CacheTime = 0
	DirectoryObject.thumb = R(ICON)
	ObjectContainer.title1 = NAME + ' V' + VERSION 
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.view_group = 'List'
	makeSettings()

	# Get the secret key used to access the PMS framework ********** FUTURE USE ***************
	SECRETKEY = genSecretKeyAsStr()
	startWeb(SECRETKEY)

####################################################################################################
# Generate secret key
####################################################################################################
''' This will generate the secret key, used to access the framework '''
@route(PREFIX + '/genSecretKeyAsStr')
def genSecretKeyAsStr():
	return str(uuid.uuid4())

####################################################################################################
# Make Settings file
####################################################################################################
''' This will generate the default settings in the Dict if missing '''
@route(PREFIX + '/makeSettings')
def makeSettings():
	# Used for Cookie generation
	Dict['SharedSecret'] = VERSION + '.' + str(randint(0,9999))		
	# Set default value for http part, if run for the first time
	if Dict['options_hide_integrated'] == None:
		Dict['options_hide_integrated'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['options_hide_withoutsubs'] == None:
		Dict['options_hide_withoutsubs'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['options_hide_local'] == None:
		Dict['options_hide_local'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['options_hide_empty_subtitles'] == None:
		Dict['options_hide_empty_subtitles'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['options_only_multiple'] == None:
		Dict['options_only_multiple'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['options_auto_select_duplicate'] == None:
		Dict['options_auto_select_duplicate'] = 'false'
	# Set default value for http part, if run for the first time
	if Dict['items_per_page'] == None:
		Dict['items_per_page'] = '15'
	# Create the password entry
	if Dict['password'] == None:
		Dict['password'] = ''
	# Create the debug entry
	if Dict['debug'] == None:
		Dict['debug'] = 'false'
	# Create the pwdset entry
	if Dict['pwdset'] == None:
		Dict['pwdset'] = False
	# Init the installed dict
	if Dict['installed'] == None:
		Dict['installed'] = {}
	# Init the allBundle Dict
	if Dict['PMS-AllBundleInfo'] == None:
		Dict['PMS-AllBundleInfo'] = {}
	return

####################################################################################################
# Main function
####################################################################################################
''' Main menu '''
@handler(PREFIX, NAME, ICON)
@route(PREFIX + '/MainMenu')
def MainMenu():
	Log.Debug("**********  Starting MainMenu  **********")	
	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(MainMenu), title="To access this channel, type the url's below to a new browser tab"))
	if Prefs['Force_SSL']:
		oc.add(DirectoryObject(key=Callback(MainMenu), title='https://' + Network.Address + ':' + Prefs['WEB_Port_https']))
	else:
		oc.add(DirectoryObject(key=Callback(MainMenu), title='http://' + Network.Address + ':' + Prefs['WEB_Port_http']))
		oc.add(DirectoryObject(key=Callback(MainMenu), title='https://' + Network.Address + ':' + Prefs['WEB_Port_https']))
	oc.add(PrefsObject(title='Preferences', thumb=R('icon-prefs.png')))
	Log.Debug("**********  Ending MainMenu  **********")
	return oc
	
####################################################################################################
# ValidatePrefs
####################################################################################################
@route(PREFIX + '/ValidatePrefs')
def ValidatePrefs():
#	HTTP.Request('http://127.0.0.1:32400/:/plugins/com.plexapp.plugins.WebTool/restart', immediate=True)
	Restart()

@route(PREFIX + '/Restart')
def Restart():
	time.sleep(3)
	startWeb(SECRETKEY)
	return

