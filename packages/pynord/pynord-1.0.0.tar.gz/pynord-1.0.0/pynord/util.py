import subprocess as sp
import pandas as pd
import subprocess
import random
import json
import sys
import os

# NOTE: Need to update "nord_cities" every-so-often. Last update: 07/15/2022

printer = print
class helper:
	def run(command: str, timeout):
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		try:
			process.wait(timeout=timeout)
			log = process.communicate()[0].decode('utf-8')
		except subprocess.TimeoutExpired:
			process.kill()
			log = 'WARNING: Timeout Error Occurred.'
		return log
	def print(message):
		printer(message)

class parser():
	def status(self, string):
		if 'Status' in string:
			string = string[string.find('Status:'):]
			string = string.split('\n')
			if 'Disconnected' in string[0]:
				status = False
			else:
				status = True
			return status

	def server(self, string):
		if "Current server" in string:
			string = string[string.find('Current server:'):]
			string = string.split('\n')[0]
			server = string.split(": ")[1].split(".")[0]
			return server
			
	def ip(self, string):
		if "Current server" in string:
			string = string[string.find('Server IP:'):]
			string = string.split('\n')[0]
			ip = string.split(": ")[1]
			return ip

	def city(self, string):
		if "Current server" in string:
			string = string[string.find('City:'):]
			string = string.split('\n')[0]
			city = string.split(": ")[1].replace(" ", "_")
			return city

	def available_cities(self, string):
		nord_cities = ['Atlanta', 'Charlotte', 'Dallas', 'Kansas_City', 'Manassas', 'New_York', 'Saint_Louis', 'San_Francisco', 'Buffalo', 'Chicago', 'Denver', 'Los_Angeles', 'Miami', 'Phoenix', 'Salt_Lake_City', 'Seattle']
		intersection = list(set(string.split()) & set(nord_cities))
		return intersection

class util():
	def check_install(self):
		# verify linux
		if sys.platform not in ['linux', 'linux2']:
			raise Exception('PyNord can only be run in a Linux enviroment.')
		# check nordvpn installation
		if 'command not found' in subprocess.getoutput('nordvpn --version'):
			selection = input("NordVPN Linux Client is not installed. Do you want to install it now? [Y/n] ").strip()
			if selection == 'Y':
				os.system('sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)')
			else:
				raise Exception('NordVPN is not installed. \nhttps://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm')

	def print(self, string):
		string = str(string)
		if self.verbose and string.strip():
			helper.print(string)

	def system(self, command, timeout=None):
		log = helper.run(command=command, timeout=timeout)
		return log

	def timezone(self, city):
	    zones = {
	    'Atlanta': "America/New_York", 
	    'Charlotte': "America/New_York", 
	    'Dallas': "America/Indiana/Indianapolis", 
	    'Kansas_City': "America/Indiana/Indianapolis", 
	    'Manassas': "America/New_York", 
	    'New_York': "America/New_York", 
	    'Saint_Louis': "America/Indiana/Indianapolis", 
	    'San_Francisco': "America/Los_Angeles", 
	    'Buffalo': "America/New_York", 
	    'Chicago': "America/Chicago", 
	    'Denver': "America/Denver", 
	    'Los_Angeles': "America/Los_Angeles", 
	    'Miami': "America/New_York", 
	    'Phoenix': "America/Phoenix", 
	    'Salt_Lake_City': "America/Phoenix", 
	    'Seattle': "America/Los_Angeles"
	    }

	    try:
	        zone = zones[city]
	    except:
	        zone = "America/Los_Angeles"

	    return zone