from sqlalchemy import *
from sqlalchemy.orm import *

from xml.sax import ContentHandler
from xml.sax import make_parser
from datetime import datetime

import sys

dbUser = "postgres"
dbPass = "._postgres_."
dbServer = "localhost"

pg_db = create_engine('postgresql://'+ dbUser + ':'+ dbPass + '@' + dbServer + '/mars_met')

metadata=MetaData(pg_db)

magnitude_table=Table('weather_magnitude',metadata,autoload=True)

class magnitude(object):
		pass

mapper (magnitude, magnitude_table)

class wr_handler(ContentHandler):
	def __init__(self):
		self.buffer=""
		self.sol = -1;
		self.inField=False
		
		self.session=create_session(bind=pg_db)

	def startElement(self,name,atributtes):
		if name=="sol":
			self.inField = True
		elif name=="min_temp":
			self.inField = True
		elif name=="max_temp":
			self.inField = True
		elif name=="pressure":
			self.inField = True
		elif name=="pressure_string":
			self.inField = True
		elif name=="abs_humidity":
			self.inField = True
		elif name=="wind_speed":
			self.inField = True
		elif name=="wind_direction":
			self.inField = True
		elif name=="atmo_opacity":
			self.inField = True
		elif name=="season":
			self.inField = True
		elif name=="ls":
			self.inField = True
		elif name=="sunrise":
			self.inField = True
		elif name=="sunset":
			self.inField = True

	def characters(self,data):
		if self.inField:
			self.buffer += data

	def endElement(self,name):

		if name=="record":
			try:
				self.session.begin()
				
				self.new_magnitude=magnitude()
				self.new_magnitude.sol = self.sol;
				self.new_magnitude.min_temp = self.min_temp;
				self.new_magnitude.max_temp = self.max_temp;
				self.new_magnitude.pressure = self.pressure;
				self.new_magnitude.pressure_string = self.pressure_string;
				self.new_magnitude.abs_humidity = self.abs_humidity;
				self.new_magnitude.wind_speed = self.wind_speed;
				self.new_magnitude.wind_direction = self.wind_direction;
				self.new_magnitude.atmo_opacity = self.atmo_opacity;
				self.new_magnitude.season = self.season;
				self.new_magnitude.ls = self.ls;
				self.new_magnitude.sunrise = self.sunrise;
				self.new_magnitude.sunset = self.sunset;
				
				self.session.merge(self.new_magnitude)
				self.session.commit()

			except:
				print "Detalles:\n", sys.exc_info()
				self.session.close()
				pass

		elif name=="sol":
			try:
				print self.buffer
				self.sol = int(self.buffer)
			except:
				pass
		elif name=="min_temp":
			try:
				self.min_temp = float(self.buffer)
			except:
				self.min_temp = None;
		elif name=="max_temp":
			try:
				self.max_temp = float(self.buffer)
			except:
				self.max_temp = None;
		elif name=="pressure":
			try:
				self.pressure = float(self.buffer)
			except:
				self.pressure = None;
		elif name=="pressure_string":
			try:
				self.pressure_string = self.buffer
			except:
				pass
		elif name=="abs_humidity":
			try:
				self.abs_humidity = float(self.buffer)
			except:
				self.abs_humidity = None;
		elif name=="wind_speed":
			try:
				self.wind_speed = float(self.buffer)
			except:
				self.wind_speed = None;
		elif name=="wind_direction":
			try:
				self.wind_direction = self.buffer
			except:
				pass
		elif name=="atmo_opacity":
			try:
				self.atmo_opacity = self.buffer
			except:
				pass
		elif name=="season":
			try:
				self.season = self.buffer
			except:
				pass
		elif name=="ls":
			try:
				self.ls = float(self.buffer)
			except:
				self.ls = None;
		elif name=="sunrise":
			try:
				self.sunrise = datetime.strptime(self.buffer, '%I %p').time()
			except:
				pass
		elif name=="sunset":
			try:
				self.sunset = datetime.strptime(self.buffer, '%I %p').time()
			except:
				pass
		self.buffer=""