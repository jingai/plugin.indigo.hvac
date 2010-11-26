#!python
import sqlite3
import datetime
import ConfigParser
import re
import calendar
import time

####################
# Copyright (c) 2009, Benjamin Schollnick. All rights reserved.
# http://www.schollnick.net/wordpress
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
####################

####################
## IMPORTS
import cherrypy
from cherrypy import _cperror

from indigopy import indigoconn as ic
from indigopy import indigodb as idb
from indigopy.basereqhandler import BaseRequestHandler, kTrueStr, kFalseStr, kEmptyStr, kTextPageStr, kHtmlPageStr, kXmlPageStr
#import cgitb; cgitb.enable()
#from custom_colors import *
import socket
import os
import os.path
import sys
import csv
import glob
import cgi

####################
## CONSTANTS
kSqlConfigFile = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/IndigoSqlClient.conf"

####################
# Optional hooks to provide a plugin name and description (shown in Event Log and plugin index)
def PluginName():
	return u"Thermostat Temperature Historical Readings"

def PluginDescription():
	return u"Displays recent information historically from your Thermostat."

def ShowOnControlPageList():
	return True		# if True, then above name/description is shown on the Control Page list index

# Optional hook called when the IndigoWebServer first connects to IndigoServer
def IndigoConnected():
	pass

# Optional hook called when the IndigoWebServer disconnect from IndigoServer
def IndigoDisconnected():
	pass

#dbName = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/" + "sqlite_db"
#dbFileName = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/" + "crockett_sqlite_db"


class 	hvac_interface:
	def	__init__ (self, sql_db_file ):
		self.hvac_id 			= 0 
		self.hvac_ts 			= 1
		self.hvac_dev_name 		= 2
		self.hvac_temperature 	= 3
		self.hvac_humidity 		= 4
		self.hvac_setpoint_cool = 5
		self.hvac_setpoint_heat = 6
		self.hvac_current_mode 	= 7
		self.hvac_fan_mode		= 8
		self.hvac_raw_data		= None
		self.dbFileName = sql_db_file
		
	def		retrieve_query_from_sqlite ( self, query):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()
		cur.execute(query)
		return cur.fetchall()
		
		
	def		retrieve_hvac_data_from_sqlite ( self, inDate, thermo_name ):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()
		
		cur.execute(u"""select id, datetime(ts,'localtime'), dev_name, temperature, humidity, setpoint_cool, setpoint_heat, current_mode, fan_mode from device_history_hvac where dev_name = '%s' and date(ts, 'localtime') = date(?) order by ts""" % thermo_name, (unicode(inDate),))
		self.hvac_raw_data = cur.fetchall()
		#cur.execute(u"select distinct(dev_name) from device_history_basic where date(ts, 'localtime') = date(?) order by dev_name", (unicode(inDate),))
		
	def		retrieve_thermo_names ( self, inDate ):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()
		
		cur.execute(u"""select distinct dev_name from device_history_hvac where date(ts, 'localtime') = date(?) order by dev_name""", (unicode(inDate),))
		return cur.fetchall()
	
	def		return_thermostat_readings ( self ):
		thermo = []
		for x in self.hvac_raw_data:
			thermo.append ( x[self.hvac_temperature] )
		return thermo
	
	def		return_setpoint_heating_readings ( self ):
		thermo = []
		for x in self.hvac_raw_data:
			thermo.append ( x[self.hvac_setpoint_heat] )
		return thermo

	def		return_setpoint_cooling_readings ( self ):
		thermo = []
		for x in self.hvac_raw_data:
			thermo.append ( x[self.hvac_setpoint_cool] )
		return thermo
	
	def 	return_timestrings ( self ):
		dates = []
		for x in self.hvac_raw_data:
			stored_datetime = x[self.hvac_ts]
			raw_date = stored_datetime.split(" ")[1][0:-3].replace(":",".")
			dates.append (float(raw_date))
		return dates
		
	def 	return_datestrings ( self ):
		dates = []
		rawdates = self.retrieve_query_from_sqlite ( """select distinct date(ts, 'localtime') from device_history_hvac order by ts""")
		for x in rawdates:
			dates.append (x[0])
		return dates

	
def	create_graphs ( html, hvac_sql_interface, thermostat_name, inDate = datetime.date.today() ):
#	inDate = "2010-03-29"
	graph_urls = []
	hvac_data = hvac_sql_interface
	hvac_data.retrieve_hvac_data_from_sqlite ( inDate, thermostat_name)#x[0] )

	setpoint_heating_data = hvac_data.return_setpoint_heating_readings()
	setpoint_cooling_data = hvac_data.return_setpoint_cooling_readings()
	thermostat_readings_data = hvac_data.return_thermostat_readings()
	date_range = hvac_data.return_timestrings ()
	
	if hvac_data.hvac_raw_data == None:
		html.append ("No HVAC Data was found")
		return html

	html.append ('<div id="graph-%s">Loading graph...</div>' % thermostat_name)
	html.append ('''<a href='#' onClick='toggle_it("table-%s")'">Show/Hide Thermostat Details</a><br>'''% thermostat_name.replace (" ", "") )
	html.append ('<table id="table-%s" border=1 style="display:none;">' % thermostat_name.replace(" ", ""))
	html.append ("<caption> %s Temperature Chart</caption>" % thermostat_name)
	html.append ('<thead>')
	html.append ('<tr>')
	html.append ('<th scope="col">Time</th>')
	html.append ('<th scope="col">Heating</th>')
	html.append ('<th scope="col">Cooling</th>')
	html.append ('<th scope="col">Temperature</th>')
	html.append ('</tr></thead>')
	html.append ('<tbody>')
	heating_matrix, cooling_matrix, thermo_matrix = [], [], []
	for data in hvac_data.hvac_raw_data:
		html.append ('<tr>')
#		html.append ('<th scope="row">%s</th>' )
		html.append ('<TD scope="row">%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>' % (data[hvac_data.hvac_ts],
		data[hvac_data.hvac_setpoint_heat], data[hvac_data.hvac_setpoint_cool], data[hvac_data.hvac_temperature]))
		thermo_matrix.append ( [float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_temperature])] )
		heating_matrix.append ( [float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_setpoint_heat])] )
		cooling_matrix.append ( [float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_setpoint_cool])] )

		html.append ('</tr>')

	html.append ('</tbody> </table>')
	html.append ('<HR>')
	html.append ('''<script type="text/javascript" src="js/jscharts.js"></script>''')
	html.append ('<script type="text/javascript">')
	html.append ("var myChart = new JSChart('graph-%s', 'line');" % thermostat_name)
	html.append ('\nmyChart.setDataArray(%s,"thermo" );\n' % thermo_matrix)
	html.append ('\nmyChart.setDataArray(%s,"ac" );\n' % cooling_matrix)
	html.append ('\nmyChart.setDataArray(%s,"heat" );\n' % heating_matrix)

	for (x, y) in thermo_matrix:
		html.append ('\nmyChart.setTooltip( [%f, "Time: %s   Room Temp: %s", "thermo"] );\n' % (x, x, y) )
		
	for (x, y) in heating_matrix:
		html.append ('\nmyChart.setTooltip( [%f, "(Heat) Time: %s   Heat Temp: %s", "heat"] );\n' % (x, x, y) )

	for (x, y) in cooling_matrix:
		html.append ('\nmyChart.setTooltip( [%f, "(AC) Time: %s   AC Temp: %s", "ac"] );\n' % (x, x, y) )

#	html.append ('myChart.setAxisValuesNumberY(11);')
	html.append ('myChart.setIntervalStartY(50);')
	html.append ('myChart.setIntervalEndY(95);')
	html.append ("myChart.setAxisWidth ( 1 );")
	html.append ('myChart.setIntervalStartX(00);')
	html.append ('myChart.setIntervalEndX(24);')
	for x in range(0, 25):
		html.append ("myChart.setLabelX([%s,%i]);" % (x, x) )
	html.append ("myChart.setShowXValues(false);")
	html.append ("myChart.setTitleColor('#454545');")
	html.append ("myChart.setAxisValuesNumberX ( 1);")
	html.append ("myChart.setAxisValuesColor('#454545');")
	html.append ("myChart.setLineColor('#87cefa', 'ac');")
	html.append ("myChart.setLineColor('#ff0000', 'heat');")
	html.append ("myChart.setLineColor('#000000', 'thermo');")
	html.append ('myChart.setTitle ("%s Thermostat Historical Readings");' % thermostat_name)

	html.append ("myChart.setBackgroundImage('images/chart_bg.jpg');")

	html.append ('myChart.setSize(900, 700);')
	html.append ('myChart.draw();')
	html.append ('</script>')

	return html
  
def		bundle_data_set  ( data1=[], thermo=[], x_axi=[], color1='000000', color2='FF0000', title='title', legend=[''] ):
	return ( {"data1":data1,
				"thermo":thermo,
				"x_axi":x_axi,
				"color1":color1,
				"color2":color2,
				"title":title,
				"legend":legend} )
	
	
####################
# The functions in this class are automatically called based on the URL
# requested. This provides a mechanism for easily serving dynamic content.
#
# The URL path is based on the folder path of the plugin. For example,
# this plugin folder name is "sample" so any URL path containing "sample"
# as the first path identifier will call into these functions.
#
# The class name can be called whatever you want, but it must subclass
# from BaseRequestHandler to be loaded by the webserver plugin manager.


class HaloHomeRequestHandler(BaseRequestHandler):
	""" Handles HTTP page requests. """

	####################
	# The plugin page request handler must subclass from BaseRequestHandler
	# and must call the parent class __init__ method.
	def __init__(self, logFunc, debugLogFunc):
		BaseRequestHandler.__init__(self, logFunc, debugLogFunc)


	def form_top ( self, html_elems, dates, selected_date):
		#
		#		Contains the top of the report
		#		Split from the index function to clarify / simplify the visual clutter
		#
		html_elems.append ("<head>\n")
		html_elems.append("<title>Indigo log viewer</title></Head>\n")
		html_elems.append('<link rel="stylesheet" type="text/css" href="css/hvac.css">')
		html_elems.append ('<meta name="apple-mobile-web-app-capable" content="yes">')
		html_elems.append ('<meta name="viewport" content="width=320,initial-scale=0.8,maximum-scale=1.6,user-scalable=yes"/>')
		html_elems.append ('''<script type="text/javascript" src="js/jscharts.js"></script>''')
		html_elems.append ('''<script language="javascript"> 
  function toggle_it(itemID){ 
      // Toggle visibility between none and inline 
      if ((document.getElementById(itemID).style.display == 'none')) 
      { 
        document.getElementById(itemID).style.display = 'inline'; 
      } else { 
        document.getElementById(itemID).style.display = 'none'; 
      } 
  } 
</script> 
''')

		html_elems.append ("</head>")
		html_elems.append("<body>\n")

		
		html_elems.append ('<table border=0 width="95%"> <TR>')
		html_elems.append ('<form method="post" action="">')
		html_elems.append ("<td>")
		html_elems.append ('View a Particular Day - <select name="date_selection" size="1">')
		html_elems.append ('<option>Yesterday')
		dates.sort ( reverse=True)
		for day in dates:
			if selected_date == day:
				html_elems.append ('<option selected>%s'% day)
			else:
				html_elems.append ('<option>%s'% day)
		html_elems.append ('</select>')
		html_elems.append ('<input type="submit">')
		html_elems.append ("</td></tr> </table>\n")
		return html_elems

	####################
	def index(self, date_selection="None"):
				#
				#
		cherrypy.response.headers['Content-Type'] = 'text/html'
		if date_selection == "None":
			#
			#		List all files in the Indigo Log File Directory
			#
			date_selection = datetime.date.today() - datetime.timedelta(1)

		else:
			#
			#		Load only the log file that was requested.
			#
			pass
		
		html_elems = []
		try:
			config = ConfigParser.ConfigParser()
			config.read(kSqlConfigFile)
			dbType = config.get("client_options", "database_type").lower()
			if dbType == "sqlite":
				dbFileName = config.get("sqlite_client", "database")
				if (len(dbFileName) < 1):
					return "The database file is missing in the SQL logging client so nothing is being logged."
				else:
					dbFileName = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/" + dbFileName
				deviceChanges = config.get("client_options", "log_device_changes")
				if (deviceChanges == "0"):
					return "Device logging is disabled - you need to configure the SQL logging client to log all device changes."
			elif dbType == "postgres":
				return "This plugin can only use SQLite databases, not PostgreSQL databases."
		except Exception, e:
			return "The plugin can't read the config file for the SQL logging client."
			
		
		hvac = hvac_interface ( dbFileName )
		html_elems = self.form_top ( html_elems, hvac.return_datestrings (), date_selection )

		#thermostats = hvac_data.retrieve_query_from_sqlite ( dbFileName, """select distinct dev_name from device_history_hvac where date(ts, 'localtime') = date(?) order by dev_name""", (unicode(inDate),)
		thermostats = hvac.retrieve_thermo_names ( date_selection )
		for x in thermostats:
			html_elems = create_graphs ( html_elems, hvac, x[0], date_selection)
		
		if date_selection == "None": 
			date_selection = datetime.date.today()

		html_elems.append("</body>\n")
		
		return ''.join(html_elems)
	index.exposed = True

#
#		Version History - 
#		1.50	- Added External CSS Support
#		1.35	- Table Header revision
#				- Fixed bug with loading a specific day
#				- Added Ability to restrict to particular event tags (eg. iTunes, Application, Web Server)
#
#		1.30	- Table Header revision
#				- Added Custom color support
#				
#		1.21	- Fixed issues with Sort / Reverse with Python v2.4x
#		1.20	- Added Select Form features
#				- Added Color coding for Error messages
#				- Now displayed in newest to oldest order

#		1.00	- Public release as Indigo Plugin
#
