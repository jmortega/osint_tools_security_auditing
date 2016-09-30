#!/usr/bin/env python2.7
#coding=UTF-8

import pygeoip 
import os
import sys
import argparse

class Geoip(object):

	def __init__(self, target):
		self.target = target
		try:
			self.gip = pygeoip.GeoIP('GeoLiteCity.dat',pygeoip.MEMORY_CACHE)
			self.search()
		except pygeoip.GeoIPError:
			print("[!] You probably forgot to set the target or give an invalid target as argument.")
		except Exception as e: 
        		print("[!] Exception caught: {}".format(e))

	def search(self):
		addr = self.target
		rec = self.gip.record_by_addr(addr)
		for key,val in rec.items():
			print("[*] %s: %s" %(key, val))
			

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Geo localizate IP addresses')
	parser.add_argument('--target', action="store", dest="target",required=True)
	given_args = parser.parse_args()
	target = given_args.target
	geoip  = Geoip(target);
	geoip.search();		