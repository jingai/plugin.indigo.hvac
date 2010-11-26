#!python

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
#
# Version History:
# 2.01 - Show average compressor usage over specified time
# 2.00 - Show compressor, furnace, and fan cycles/totals
# 1.00 - Public release as Indigo Plugin

import sqlite3
import datetime
import ConfigParser
import re
import calendar
import time
import cherrypy
from cherrypy import _cperror
from indigopy import indigoconn as ic
from indigopy import indigodb as idb
from indigopy.basereqhandler import BaseRequestHandler, kTrueStr, kFalseStr, kEmptyStr, kTextPageStr, kHtmlPageStr, kXmlPageStr
import socket
import os
import os.path
import sys
import copy
import math
import glob
import cgi

kSqlConfigFile = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/IndigoSqlClient.conf"

graph_width = 1100 # pixels


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


class hvac_interface:
	def __init__(self, sql_db_file):
		self.hvac_id 					= 0 
		self.hvac_ts 					= 1
		self.hvac_dev_name 				= 2

		self.hvac_temp					= 3
		self.hvac_temp_min				= 0
		self.hvac_temp_max				= 0
		self.hvac_temp_avg				= 0
		self.hvac_humidity 				= 4
		self.hvac_humidity_min			= 0
		self.hvac_humidity_max			= 0
		self.hvac_humidity_avg			= 0
		self.hvac_set_cool				= 5
		self.hvac_set_cool_min			= 0
		self.hvac_set_cool_max			= 0
		self.hvac_set_heat				= 6
		self.hvac_set_heat_min			= 0
		self.hvac_set_heat_max			= 0

		self.hvac_current_mode 			= 7
		self.hvac_fan_mode				= 8

		self.hvac_raw_data				= None
		self.hvac_mins_ac				= 1
		self.hvac_mins_ac_ts			= 2
		self.hvac_mins_ac_raw_data		= None
		self.hvac_mins_heat				= 1
		self.hvac_mins_heat_ts			= 2
		self.hvac_mins_heat_raw_data	= None
		self.hvac_mins_filter_total		= 0
		self.hvac_date_filter_changed	= "never"

		self.dbFileName = sql_db_file

	def retrieve_query_from_sqlite(self, query):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()
		cur.execute(query)
		return cur.fetchall()

	def retrieve_hvac_data_from_sqlite(self, inDate, thermo_name):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()

		cur.execute(u"""select id, datetime(ts,'localtime'), dev_name, temperature, humidity, setpoint_cool, setpoint_heat, current_mode, fan_mode from device_history_hvac where dev_name = '%s' and date(ts, 'localtime') = date(?) order by ts""" % thermo_name, (unicode(inDate),))
		self.hvac_raw_data = cur.fetchall()

		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'AC_%' and date(ts, 'localtime') = date(?) order by ts desc""", (unicode(inDate),))
		self.hvac_mins_ac_raw_data = cur.fetchall()

		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'Heating_%' and date(ts, 'localtime') = date(?) order by ts desc""", (unicode(inDate),))
		self.hvac_mins_heat_raw_data = cur.fetchall()

		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'Filter_%' and date(ts, 'localtime') <= date(?) order by ts desc""", (unicode(inDate),))
		row = cur.fetchone()
		if row:
			self.hvac_mins_filter_total = int(row[1])

		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'Filter_%' and var_value = '0' order by ts desc""")
		row = cur.fetchone()
		if row:
			self.hvac_date_filter_changed = row[2]

	def retrieve_thermo_names(self, inDate):
		con = sqlite3.connect(self.dbFileName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		con.isolation_level = None
		cur = con.cursor()

		cur.execute(u"""select distinct dev_name from device_history_hvac where date(ts, 'localtime') = date(?) order by dev_name""", (unicode(inDate),))
		return cur.fetchall()

	def return_temperature_readings(self):
		thermo = []
		for x in self.hvac_raw_data:
			if self.hvac_temp_min == 0 or x[self.hvac_temp] < self.hvac_temp_min:
				self.hvac_temp_min = x[self.hvac_temp]
			if x[self.hvac_temp] > self.hvac_temp_max:
				self.hvac_temp_max = x[self.hvac_temp]
			self.hvac_temp_avg += x[self.hvac_temp]

			thermo.append(x[self.hvac_temp])

		if len(self.hvac_raw_data) > 0:
			self.hvac_temp_avg = int(math.ceil(float(self.hvac_temp_avg) / len(self.hvac_raw_data)))

		return thermo

	def return_humidity_readings(self):
		thermo = []
		for x in self.hvac_raw_data:
			if self.hvac_humidity_min == 0 or x[self.hvac_humidity] < self.hvac_humidity_min:
				self.hvac_humidity_min = x[self.hvac_humidity]
			if x[self.hvac_humidity] > self.hvac_humidity_max:
				self.hvac_humidity_max = x[self.hvac_humidity]
			self.hvac_humidity_avg += x[self.hvac_humidity]

			thermo.append(x[self.hvac_humidity])

		if len(self.hvac_raw_data) > 0:
			self.hvac_humidity_avg = int(math.ceil(float(self.hvac_humidity_avg) / len(self.hvac_raw_data)))

		return thermo

	def return_setpoint_cooling_readings(self):
		thermo = []
		for x in self.hvac_raw_data:
			if self.hvac_set_cool_min == 0 or x[self.hvac_set_cool] < self.hvac_set_cool_min:
				self.hvac_set_cool_min = x[self.hvac_set_cool]
			if x[self.hvac_set_cool] > self.hvac_set_cool_max:
				self.hvac_set_cool_max = x[self.hvac_set_cool]

			thermo.append(x[self.hvac_set_cool])

		return thermo

	def return_setpoint_heating_readings(self):
		thermo = []
		for x in self.hvac_raw_data:
			if self.hvac_set_heat_min == 0 or x[self.hvac_set_heat] < self.hvac_set_heat_min:
				self.hvac_set_heat_min = x[self.hvac_set_heat]
			if x[self.hvac_set_heat] > self.hvac_set_heat_max:
				self.hvac_set_heat_max = x[self.hvac_set_heat]

			thermo.append(x[self.hvac_set_heat])

		return thermo

	def return_mins_ac_cycle_readings(self):
		thermo = []
		for x in self.hvac_mins_ac_raw_data:
			if x[0] == "AC_Started":
				thermo.append([x[self.hvac_mins_ac_ts], int(1)])
			elif x[0] == "AC_dailymins":
				thermo.append([x[self.hvac_mins_ac_ts], int(0)])

		return thermo

	def return_mins_heat_cycle_readings(self):
		thermo = []
		for x in self.hvac_mins_heat_raw_data:
			if x[0] == "Heating_Started":
				thermo.append([x[self.hvac_mins_heat_ts], int(1)])
			elif x[0] == "Heating_dailymins":
				thermo.append([x[self.hvac_mins_heat_ts], int(0)])

		return thermo

	def return_timestrings(self):
		dates = []
		for x in self.hvac_raw_data:
			stored_datetime = x[self.hvac_ts]
			raw_date = stored_datetime.split(" ")[1][0:-3].replace(":", ".")
			dates.append (float(raw_date))

		return dates

	def return_datestrings(self):
		dates = []
		rawdates = self.retrieve_query_from_sqlite("""select distinct date(ts, 'localtime') from device_history_hvac order by ts""")
		for x in rawdates:
			dates.append(x[0])

		return dates


def graph_defaults(html):
	html.append("myChart.setAxisWidth(1);")
	html.append('myChart.setIntervalStartX(00);')
	html.append('myChart.setIntervalEndX(24);')
	for x in range(0, 25):
		html.append("myChart.setLabelX([%s,%i]);" % (x, x))
	html.append("myChart.setShowXValues(false);")
	html.append("myChart.setTitleColor('#454545');")
	html.append("myChart.setAxisValuesNumberX(1);")
	html.append("myChart.setAxisValuesColor('#454545');")
#	html.append("myChart.setBackgroundImage('/hvac/images/chart_bg.jpg');")
	html.append('myChart.setSize(%d, 0);' % (graph_width))
	html.append('myChart.draw();')

def create_graphs(html, hvac_sql_interface, thermostat_name, inDate = datetime.date.today()):
#	inDate = "2010-03-29"
	graph_urls = []
	hvac_data = hvac_sql_interface
	hvac_data.retrieve_hvac_data_from_sqlite(inDate, thermostat_name)
	if hvac_data.hvac_raw_data == None:
		html.append("No HVAC Data was found")
		return html

	setpoint_cooling_data = hvac_data.return_setpoint_cooling_readings()
	setpoint_heating_data = hvac_data.return_setpoint_heating_readings()
	temperature_readings_data = hvac_data.return_temperature_readings()
	humidity_readings_data = hvac_data.return_humidity_readings()
	date_range = hvac_data.return_timestrings()

	html.append('<div id="graph-humidity-%s">Loading graph...</div>' % thermostat_name)
	html.append('<div id="graph-cool-%s">Loading graph...</div>' % thermostat_name)
	html.append('<div id="graph-heat-%s">Loading graph...</div>' % thermostat_name)

	# cooling totals/cycles
	mins_ac_total = 0
	for data in hvac_data.hvac_mins_ac_raw_data:
		if data[0] == "AC_dailymins" and data[1] != "0":
			mins_ac_total = data[hvac_data.hvac_mins_ac]
			break
	mins_ac_data = hvac_data.return_mins_ac_cycle_readings()
	mins_ac_cycles = 0
	y = 0
	for data in mins_ac_data:
		if y == 1 and data[1] != y:
			mins_ac_cycles += 1
		y = data[1]

	# heating totals/cycles
	mins_heat_total = 0
	for data in hvac_data.hvac_mins_heat_raw_data:
		if data[0] == "Heating_dailymins" and data[1] != "0":
			mins_heat_total = data[hvac_data.hvac_mins_heat]
			break
	mins_heat_data = hvac_data.return_mins_heat_cycle_readings()
	mins_heat_cycles = 0
	y = 0
	for data in mins_heat_data:
		if y == 1 and data[1] != y:
			mins_heat_cycles += 1
		y = data[1]

	html.append('<div align="center">')
	html.append('Cooling totals: %s mins, %s cycles' % (mins_ac_total, mins_ac_cycles))
	html.append(' &mdash; Heating totals: %s mins, %s cycles' % (mins_heat_total, mins_heat_cycles))
	html.append('</div>')
	html.append('<div align="center">')
	html.append('Filter runtime to date: %s hours (%s mins)' % (hvac_data.hvac_mins_filter_total / 60, hvac_data.hvac_mins_filter_total))
	html.append(' &mdash; Last changed: %s' % (hvac_data.hvac_date_filter_changed))
	html.append('</div>')
	html.append('<div align="center">Room temperature min/max/avg: %s/%s/%s</div>' % (hvac_data.hvac_temp_min, hvac_data.hvac_temp_max, hvac_data.hvac_temp_avg))
	html.append('<HR>')

	html.append('''<a href='#' onClick='toggle_it("table-%s")'">Show/Hide Thermostat Data</a><br>'''% thermostat_name.replace(" ", ""))
	html.append('<table id="table-%s" border=1 style="display:none;">' % thermostat_name.replace(" ", ""))
	html.append("<caption> %s Chart</caption>" % thermostat_name)
	html.append('<thead>')
	html.append('<tr>')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Humidity</th>')
	html.append('<th scope="col">Cooling</th>')
	html.append('<th scope="col">Heating</th>')
	html.append('<th scope="col">Temperature</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	humidity_matrix, cooling_matrix, heating_matrix, thermo_matrix = [], [], [], []
	for data in hvac_data.hvac_raw_data:
		html.append ('<TR>')
		html.append ('<TD scope="row">%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>' % (data[hvac_data.hvac_ts],
			data[hvac_data.hvac_humidity], data[hvac_data.hvac_set_cool], data[hvac_data.hvac_set_heat],
			data[hvac_data.hvac_temp]))
		html.append('</tr>')

		humidity_matrix.append([float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_humidity])])
		cooling_matrix.append([float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_set_cool])])
		heating_matrix.append([float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_set_heat])])
		thermo_matrix.append([float(data[hvac_data.hvac_ts].split(" ")[1][0:-3].replace(":",".")), int(data[hvac_data.hvac_temp])])
	html.append('</tbody> </table>')

	html.append('''<a href='#' onClick='toggle_it("table-mins-ac")'">Show/Hide Cooling Cycles</a><br>''')
	html.append('<table id="table-mins-ac" border=1 style="display:none;">')
	html.append("<caption> %s Cooling Cycle Chart</caption>" % thermostat_name)
	html.append('<thead>')
	html.append('<tr>')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Mode</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	mins_ac_matrix = []
	for data in mins_ac_data:
		stored_datetime = data[0]
		x = stored_datetime.split(" ")[1][0:-3].replace(":",".")
		y = data[1]
		if y == 1:
			onoff = "On"
		else:
			onoff = "Off"

		mins_ac_matrix.append([float(x), int(y)])

		html.append('<tr>')
		html.append('<TD scope="row">%s</TD><TD>%s</TD>' % (data[0], onoff))
		html.append('</tr>')
	html.append('</tbody> </table>')

	html.append('''<a href='#' onClick='toggle_it("table-mins-heat")'">Show/Hide Heating Cycles</a><br>''')
	html.append('<table id="table-mins-heat" border=1 style="display:none;">')
	html.append("<caption> %s Heating Cycle Chart</caption>" % thermostat_name)
	html.append('<thead>')
	html.append('<tr>')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Mode</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	mins_heat_matrix = []
	for data in mins_heat_data:
		stored_datetime = data[0]
		x = stored_datetime.split(" ")[1][0:-3].replace(":",".")
		y = data[1]
		if y == 1:
			onoff = "On"
		else:
			onoff = "Off"

		mins_heat_matrix.append([float(x), int(y)])

		html.append ('<tr>')
		html.append ('<TD scope="row">%s</TD><TD>%s</TD>' % (data[0], onoff))
		html.append ('</tr>')
	html.append('</tbody> </table>')

	html.append('<HR>')

	# Humidity graph -- BEGIN
	html.append('''<script type="text/javascript" src="js/jscharts.js"></script>''')
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-humidity-%s', 'line');" % thermostat_name)

	y_min = hvac_data.hvac_humidity_min - 6
	y_max = hvac_data.hvac_humidity_max + 6

	html.append('\nmyChart.setDataArray(%s, "humidity");\n' % humidity_matrix)
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		mins_ac_matrix_norm = copy.deepcopy(mins_ac_matrix)
		for x in mins_ac_matrix_norm:
			x[1] = y_max + x[1] * 2 - 2
		html.append('\nmyChart.setDataArray(%s, "ac_cycles");\n' % mins_ac_matrix_norm)
		del mins_ac_matrix_norm
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		mins_heat_matrix_norm = copy.deepcopy(mins_heat_matrix)
		for x in mins_heat_matrix_norm:
			x[1] = y_min + x[1] * 2 + 2
		html.append('\nmyChart.setDataArray(%s, "heat_cycles");\n' % mins_heat_matrix_norm)
		del mins_heat_matrix_norm

	for (x, y) in humidity_matrix:
		html.append('\nmyChart.setTooltip([%f, "(Humidity) Time: %s   Percent: %s", "humidity"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('#67ffca', 'humidity');")
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		for (x, y) in mins_ac_matrix:
			if y == 1:
				onoff = "On"
			else:
				onoff = "Off"
			html.append('\nmyChart.setTooltip([%f, "(AC %s) Time: %s", "ac_cycles"]);\n' % (x, onoff, x))
		html.append("myChart.setLineColor('#87cefa', 'ac_cycles');")
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		for (x, y) in mins_heat_matrix:
			if y == 1:
				onoff = "On"
			else:
				onoff = "Off"
			html.append('\nmyChart.setTooltip([%f, "(Heat %s) Time: %s", "heat_cycles"]);\n' % (x, onoff, x))
		html.append("myChart.setLineColor('#ff7a4b', 'heat_cycles');")

	html.append('myChart.setTitle("%s - Humidity");' % thermostat_name)
	html.append('myChart.setIntervalStartY(%s);' % (y_min))
	html.append('myChart.setIntervalEndY(%s);' % (y_max))

	graph_defaults(html)

	html.append('</script>')
	# Humidity graph -- END

	y_min = min(hvac_data.hvac_temp_min, min(hvac_data.hvac_set_cool_min, hvac_data.hvac_set_heat_min))
	y_max = max(hvac_data.hvac_temp_max, max(hvac_data.hvac_set_cool_max, hvac_data.hvac_set_heat_max)) + 6

	# Cooling graph -- BEGIN
	html.append('''<script type="text/javascript" src="js/jscharts.js"></script>''')
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-cool-%s', 'line');" % thermostat_name)

	html.append('\nmyChart.setDataArray(%s, "thermo");\n' % thermo_matrix)
	html.append('\nmyChart.setDataArray(%s, "ac");\n' % cooling_matrix)
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		mins_ac_matrix_norm = copy.deepcopy(mins_ac_matrix)
		for x in mins_ac_matrix_norm:
			x[1] = y_max + x[1] * 2 - 2
		html.append('\nmyChart.setDataArray(%s, "ac_cycles");\n' % mins_ac_matrix_norm)
		del mins_ac_matrix_norm

	for (x, y) in thermo_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Room Temp: %s", "thermo"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('#000000', 'thermo');")
	for (x, y) in cooling_matrix:
		html.append('\nmyChart.setTooltip([%f, "(AC) Time: %s   AC Temp: %s", "ac"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('#0000ff', 'ac');")
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		for (x, y) in mins_ac_matrix:
			if y == 1:
				onoff = "On"
			else:
				onoff = "Off"
			html.append('\nmyChart.setTooltip([%f, "(AC %s) Time: %s", "ac_cycles"]);\n' % (x, onoff, x))
		html.append("myChart.setLineColor('#87cefa', 'ac_cycles');")

	html.append('myChart.setTitle("%s - Cooling");' % thermostat_name)
	html.append('myChart.setIntervalStartY(%s);' % (y_min))
	html.append('myChart.setIntervalEndY(%s);' % (y_max))

	graph_defaults(html)

	html.append('</script>')
	# Cooling graph -- END

	# Heating graph -- BEGIN
	html.append('''<script type="text/javascript" src="js/jscharts.js"></script>''')
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-heat-%s', 'line');" % thermostat_name)

	html.append('\nmyChart.setDataArray(%s, "thermo");\n' % thermo_matrix)
	html.append('\nmyChart.setDataArray(%s, "heat");\n' % heating_matrix)
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		mins_heat_matrix_norm = copy.deepcopy(mins_heat_matrix)
		for x in mins_heat_matrix_norm:
			x[1] = y_max + x[1] * 2 - 2
		html.append('\nmyChart.setDataArray(%s, "heat_cycles");\n' % mins_heat_matrix_norm)
		del mins_heat_matrix_norm

	for (x, y) in thermo_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Room Temp: %s", "thermo"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('#000000', 'thermo');")
	for (x, y) in heating_matrix:
		html.append('\nmyChart.setTooltip([%f, "(Heat) Time: %s   Heat Temp: %s", "heat"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('#ff0000', 'heat');")
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		for (x, y) in mins_heat_matrix:
			if y == 1:
				onoff = "On"
			else:
				onoff = "Off"
			html.append('\nmyChart.setTooltip([%f, "(Heat %s) Time: %s", "heat_cycles"]);\n' % (x, onoff, x))
		html.append("myChart.setLineColor('#ff7a4b', 'heat_cycles');")

	html.append('myChart.setTitle("%s - Heating");' % thermostat_name)
	html.append('myChart.setIntervalStartY(%s);' % (y_min))
	html.append('myChart.setIntervalEndY(%s);' % (y_max))

	graph_defaults(html)

	html.append('</script>')
	# Heating graph -- END

	return html


# The functions in this class are automatically called based on the URL
# requested. This provides a mechanism for easily serving dynamic content.
#
# The URL path is based on the folder path of the plugin. For example,
# this plugin folder name is "sample" so any URL path containing "sample"
# as the first path identifier will call into these functions.
#
# The class name can be called whatever you want, but it must subclass
# from BaseRequestHandler to be loaded by the webserver plugin manager.
#
class HaloHomeRequestHandler(BaseRequestHandler):
	# The plugin page request handler must subclass from BaseRequestHandler
	# and must call the parent class __init__ method.
	#
	def __init__(self, logFunc, debugLogFunc):
		BaseRequestHandler.__init__(self, logFunc, debugLogFunc)

	# Contains the top of the report
	# Split from the index function to clarify / simplify the visual clutter
	#
	def form_top(self, html_elems, dates, selected_date):
		html_elems.append("<head>\n")
		html_elems.append("<title>Indigo HVAC Log Viewer</title></Head>\n")
		html_elems.append('<link rel="stylesheet" type="text/css" href="css/hvac.css">')
		html_elems.append('<meta name="apple-mobile-web-app-capable" content="yes">')
		html_elems.append('<meta name="viewport" content="width=320,initial-scale=0.8,maximum-scale=1.6,user-scalable=yes"/>')
		html_elems.append('''<script type="text/javascript" src="js/jscharts.js"></script>''')
		html_elems.append('''<script language="javascript">
			function toggle_it(itemID) { 
				// Toggle visibility between none and inline 
				if ((document.getElementById(itemID).style.display == 'none')) { 
					document.getElementById(itemID).style.display = 'inline'; 
				} else { 
					document.getElementById(itemID).style.display = 'none'; 
				} 
		}</script>''')

		html_elems.append("</head>")
		html_elems.append("<body>\n")

		html_elems.append('<table border=0 width="95%"><TR>')
		html_elems.append('<form method="post" action="">')
		html_elems.append("<td>")
		html_elems.append('View Day - <select name="date_selection" size="1">')
		html_elems.append('<option>Yesterday')
		dates.sort(reverse=True)
		for day in dates:
			if selected_date == day:
				html_elems.append('<option selected>%s'% day)
			else:
				html_elems.append('<option>%s'% day)
		html_elems.append('</select>')
		html_elems.append('<input type="submit">')
		html_elems.append("</td></tr> </table>\n")
		return html_elems

	def index(self, date_selection="None"):
		cherrypy.response.headers['Content-Type'] = 'text/html'
		if date_selection == "None":
			# default to yesterday
			date_selection = datetime.date.today() - datetime.timedelta(1)
		else:
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

		hvac = hvac_interface(dbFileName)
		html_elems = self.form_top(html_elems, hvac.return_datestrings(), date_selection)

		thermostats = hvac.retrieve_thermo_names(date_selection)
		for x in thermostats:
			html_elems = create_graphs(html_elems, hvac, x[0], date_selection)

		html_elems.append("</body>\n")

		return ''.join(html_elems)

	index.exposed = True
