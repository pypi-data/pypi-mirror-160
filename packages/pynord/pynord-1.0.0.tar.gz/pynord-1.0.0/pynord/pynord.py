from pynord.util import util, parser
from pprint import pprint
import pandas as pd
import subprocess
import random
import os

class PyNord():
	def __init__(self, verbose=False):
		self.verbose = verbose
		util.check_install(self)

	def status(self):
		raw_out = util.system(self, command='nordvpn status')
		util.print(self, raw_out)
		status = parser.status(self, string=raw_out)
		return status
		
	def connect(self, server="The_Americas", rand=False, timeout=10):
		if rand:
			city_list = self.cities()
			city = random.choice(city_list)
			log = util.system(self, command=f'nordvpn connect {city}', timeout=timeout)
		else:
			log = util.system(self, command=f'nordvpn connect {server}', timeout=timeout)
		if self.status() is False:
			raise Exception('ERROR: VPN Connection Failed.')
		util.print(self, log)

	def disconnect(self):
		log = util.system(self, command='nordvpn disconnect')
		util.print(self, log)

	def killswitch(self, toggle: bool):
		if toggle:
			log = util.system(self, command='nordvpn set killswitch on')
		else:
			log = util.system(self, command='nordvpn set killswitch on')
		util.print(self, log)

	def cities(self, country="united_states"):
		raw_out = util.system(self, command=f'nordvpn cities {country}')
		cities = parser.available_cities(self, string=raw_out)
		return cities

	# TODO: parse status and retrieve "us8526" from Current server: us8526.nordvpn.com
	def info(self):
		raw_out = util.system(self, command='nordvpn status')
		server = parser.server(self, string=raw_out)
		ip = parser.ip(self, string=raw_out)
		city = parser.city(self, string=raw_out)
		time_zone = util.timezone(self, city=city)

		info = {
			"server": server,
			"ip": ip,
			"city": city,
			"timezone": time_zone
		}
		return info

	# TODO: add login and install functionality
	def login(self):
		return
