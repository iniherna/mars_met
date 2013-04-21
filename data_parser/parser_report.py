from sqlalchemy import *
from sqlalchemy.orm import *

from xml.sax import ContentHandler
from xml.sax import make_parser
from datetime import datetime,timedelta

import sys

dbUser = "postgres"
dbPass = "._postgres_."
dbServer = "localhost"

pg_db = create_engine('postgresql://'+ dbUser + ':'+ dbPass + '@' + dbServer + '/mars_met')

metadata=MetaData(pg_db)

report_table=Table('weather_report',metadata,autoload=True)

class report(object):
		pass

mapper (report, report_table)
class wr_handler(ContentHandler):
	def __init__(self):
		self.buffer=""
		self.sol = -1;
		self.inField=False
		self.day_zero=datetime(2012,8,05,13,49,00)

		
		self.session=create_session(bind=pg_db)

	def startElement(self,name,atributtes):
		if name=="sol":
			self.inField = True
		elif name=="terrestrial_date":
			self.inField = True

	def characters(self,data):
		if self.inField:
			self.buffer += data

	def endElement(self,name):

		if name=="record":
			try:
				self.session.begin()
				self.new_report=report()
				self.new_report.sol = self.sol
				self.new_report.terrestrial_date = self.terrestrial_date
				self.session.merge(self.new_report)
				self.session.commit()
			except:				
				self.session.close()
				pass

		elif name=="sol":
			try:
				#print self.buffer
				self.sol = int(self.buffer)
			except:
				print self.sol
		elif name=="terrestrial_date":
			aux=timedelta(hours=24,minutes=39,seconds=35,microseconds=244000)
			self.terrestrial_date = self.day_zero+self.sol*aux
		self.buffer=""