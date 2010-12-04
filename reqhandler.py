#!python

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
import itertools

kSqlConfigFile = "/Library/Application Support/Perceptive Automation/Indigo 4/IndigoSqlClient/IndigoSqlClient.conf"

graph_width				= 1016			# pixels
graph_height			= 320			# pixels
graph_color_thermo		= '#4f4f4f'
graph_color_humidity	= '#67ffca'
graph_color_ac			= '#10109f'
graph_color_ac_cycles	= '#0000ff'
graph_color_heat		= '#9f1010'
graph_color_heat_cycles	= '#ff0000'
graph_lw_thermo			= 3				# line width in pixels
graph_lw_humidity		= 3				# line width in pixels
graph_lw_ac				= 2				# line width in pixels
graph_lw_ac_cycles		= 1				# line width in pixels
graph_lw_heat			= 2				# line width in pixels
graph_lw_heat_cycles	= 1				# line width in pixels


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


def normalize_timestring(ts):
	raw_time = ts.split(" ")[1].split(":")
	return round(float(raw_time[0]) + float(raw_time[1]) / 60.0, 2)

class hvac_interface:
	def __init__(self, sql_db_file, show_duplicate_data):
		self.hvac_id 							= 0 
		self.hvac_ts 							= 1
		self.hvac_dev_name 						= 2

		self.hvac_temp							= 3
		self.hvac_temp_yest						= 0
		self.hvac_temp_min						= 0
		self.hvac_temp_max						= 0
		self.hvac_temp_avg						= 0
		self.hvac_humidity 						= 4
		self.hvac_humidity_yest 				= 0
		self.hvac_humidity_min					= 0
		self.hvac_humidity_max					= 0
		self.hvac_humidity_avg					= 0
		self.hvac_set_cool						= 5
		self.hvac_set_cool_yest					= 0
		self.hvac_set_cool_min					= 0
		self.hvac_set_cool_max					= 0
		self.hvac_set_cool_avg					= 0
		self.hvac_set_heat						= 6
		self.hvac_set_heat_yest					= 0
		self.hvac_set_heat_min					= 0
		self.hvac_set_heat_max					= 0
		self.hvac_set_heat_avg					= 0

		self.hvac_current_mode 					= 7
		self.hvac_fan_mode						= 8

		self.hvac_raw_data						= None
		self.hvac_mins_ac						= 1
		self.hvac_mins_ac_ts					= 2
		self.hvac_mins_ac_raw_data				= None
		self.hvac_mins_heat						= 1
		self.hvac_mins_heat_ts					= 2
		self.hvac_mins_heat_raw_data			= None
		self.hvac_mins_filter_total				= 0
		self.hvac_date_filter_changed			= "never"

		self.bod_gap_fill						= False
		self.eod_gap_fill						= False

		if show_duplicate_data == "True":
			self.show_duplicate_data_points		= True
		else:
			self.show_duplicate_data_points		= False
		self.min_duplicate_data_points_interval	= 1 # hours

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

		# fetch all data for date selected
		cur.execute(u"""select id, datetime(ts, 'localtime'), dev_name, temperature, humidity, setpoint_cool, setpoint_heat, current_mode, fan_mode from device_history_hvac where dev_name = '%s' and date(ts, 'localtime') = date(?) order by ts""" % thermo_name, (unicode(inDate),))
		self.hvac_raw_data = cur.fetchall()
		self.hvac_temp_yest = self.hvac_raw_data[0][self.hvac_temp]
		self.hvac_humidity_yest = self.hvac_raw_data[0][self.hvac_humidity]
		self.hvac_set_cool_yest = self.hvac_raw_data[0][self.hvac_set_cool]
		self.hvac_set_heat_yest = self.hvac_raw_data[0][self.hvac_set_heat]

		# fetch last row from the day before date selected to fill in beginning of graph
		# if values hadn't changed since the day before
		cur.execute(u"""select id, datetime(ts, 'localtime'), dev_name, temperature, humidity, setpoint_cool, setpoint_heat from device_history_hvac where dev_name = '%s' and date(ts, 'localtime') = date(?, '-1 days') order by ts desc""" % thermo_name, (unicode(inDate),))
		row = cur.fetchone()
		if (row):
			self.hvac_temp_yest = row[self.hvac_temp]
			self.hvac_humidity_yest = row[self.hvac_humidity]
			self.hvac_set_cool_yest = row[self.hvac_set_cool]
			self.hvac_set_heat_yest = row[self.hvac_set_heat]
		bod = float(self.hvac_raw_data[0][self.hvac_ts].split(" ")[1][0:-3].replace(":","."))
		eod = float(self.hvac_raw_data[len(self.hvac_raw_data) - 1][self.hvac_ts].split(" ")[1][0:-3].replace(":","."))
		if (bod > 0.0):
			self.bod_gap_fill = True
		if (eod < 23.55 and inDate != datetime.date.today().isoformat()):
			self.eod_gap_fill = True

		# fetch cooling data
		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'AC_%' and date(ts, 'localtime') = date(?) order by ts desc""", (unicode(inDate),))
		self.hvac_mins_ac_raw_data = cur.fetchall()

		# fetch heating data
		cur.execute(u"""select var_name, var_value, datetime(ts, 'localtime') from variable_history where var_name like 'Heating_%' and date(ts, 'localtime') = date(?) order by ts desc""", (unicode(inDate),))
		self.hvac_mins_heat_raw_data = cur.fetchall()

		# fetch filter (fan) data
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
		if len(self.hvac_raw_data) == 0:
			return thermo

		if (self.bod_gap_fill == True):
			thermo.append(int(self.hvac_temp_yest))

		# calculate mean
		avg = 0
		for x in self.hvac_raw_data:
			avg += x[self.hvac_temp]
		avg = int(math.ceil(float(avg) / len(self.hvac_raw_data)))

		# add all points that are within 50% of mean value
		for x in self.hvac_raw_data:
			diff = avg * 0.5
			if (x[self.hvac_temp] < diff + avg and x[self.hvac_temp] > avg - diff):
				if self.hvac_temp_min == 0 or x[self.hvac_temp] < self.hvac_temp_min:
					self.hvac_temp_min = x[self.hvac_temp]
				if x[self.hvac_temp] > self.hvac_temp_max:
					self.hvac_temp_max = x[self.hvac_temp]
				self.hvac_temp_avg += x[self.hvac_temp]

				thermo.append(int(x[self.hvac_temp]))

		self.hvac_temp_avg = int(math.ceil(float(self.hvac_temp_avg) / len(self.hvac_raw_data)))

		if (self.eod_gap_fill == True):
			thermo.append(int(self.hvac_raw_data[len(self.hvac_raw_data) - 1][self.hvac_temp]))

		return thermo

	def return_humidity_readings(self):
		thermo = []
		if len(self.hvac_raw_data) == 0:
			return thermo

		if (self.bod_gap_fill == True):
			thermo.append(int(self.hvac_humidity_yest))

		# calculate mean
		avg = 0
		for x in self.hvac_raw_data:
			avg += x[self.hvac_humidity]
		avg = int(math.ceil(float(avg) / len(self.hvac_raw_data)))

		# add all points that are within 50% of mean value
		for x in self.hvac_raw_data:
			diff = avg * 0.5
			if (x[self.hvac_humidity] < diff + avg and x[self.hvac_humidity] > avg - diff):
				if self.hvac_humidity_min == 0 or x[self.hvac_humidity] < self.hvac_humidity_min:
					self.hvac_humidity_min = x[self.hvac_humidity]
				if x[self.hvac_humidity] > self.hvac_humidity_max:
					self.hvac_humidity_max = x[self.hvac_humidity]
				self.hvac_humidity_avg += x[self.hvac_humidity]

				thermo.append(int(x[self.hvac_humidity]))

		self.hvac_humidity_avg = int(math.ceil(float(self.hvac_humidity_avg) / len(self.hvac_raw_data)))

		if (self.eod_gap_fill == True):
			thermo.append(int(self.hvac_raw_data[len(self.hvac_raw_data) - 1][self.hvac_humidity]))

		return thermo

	def return_setpoint_cooling_readings(self):
		thermo = []
		if len(self.hvac_raw_data) == 0:
			return thermo

		if (self.bod_gap_fill == True):
			thermo.append(int(self.hvac_set_cool_yest))

		# calculate mean
		avg = 0
		for x in self.hvac_raw_data:
			avg += x[self.hvac_set_cool]
		avg = int(math.ceil(float(avg) / len(self.hvac_raw_data)))

		# add all points that are within 50% of mean value
		for x in self.hvac_raw_data:
			diff = avg * 0.5
			if (x[self.hvac_set_cool] < diff + avg and x[self.hvac_set_cool] > avg - diff):
				if self.hvac_set_cool_min == 0 or x[self.hvac_set_cool] < self.hvac_set_cool_min:
					self.hvac_set_cool_min = x[self.hvac_set_cool]
				if x[self.hvac_set_cool] > self.hvac_set_cool_max:
					self.hvac_set_cool_max = x[self.hvac_set_cool]
				self.hvac_set_cool_avg += x[self.hvac_set_cool]

				thermo.append(int(x[self.hvac_set_cool]))

		self.hvac_set_cool_avg = int(math.ceil(float(self.hvac_set_cool_avg) / len(self.hvac_raw_data)))

		if (self.eod_gap_fill == True):
			thermo.append(int(self.hvac_raw_data[len(self.hvac_raw_data) - 1][self.hvac_set_cool]))

		return thermo

	def return_setpoint_heating_readings(self):
		thermo = []
		if len(self.hvac_raw_data) == 0:
			return thermo

		if (self.bod_gap_fill == True):
			thermo.append(int(self.hvac_set_heat_yest))

		# calculate mean
		avg = 0
		for x in self.hvac_raw_data:
			avg += x[self.hvac_set_heat]
		avg = int(math.ceil(float(avg) / len(self.hvac_raw_data)))

		# add all points that are within 50% of mean value
		for x in self.hvac_raw_data:
			diff = avg * 0.5
			if (x[self.hvac_set_heat] < diff + avg and x[self.hvac_set_heat] > avg - diff):
				if self.hvac_set_heat_min == 0 or x[self.hvac_set_heat] < self.hvac_set_heat_min:
					self.hvac_set_heat_min = x[self.hvac_set_heat]
				if x[self.hvac_set_heat] > self.hvac_set_heat_max:
					self.hvac_set_heat_max = x[self.hvac_set_heat]
				self.hvac_set_heat_avg += x[self.hvac_set_heat]

				thermo.append(int(x[self.hvac_set_heat]))

		self.hvac_set_heat_avg = int(math.ceil(float(self.hvac_set_heat_avg) / len(self.hvac_raw_data)))

		if (self.eod_gap_fill == True):
			thermo.append(int(self.hvac_raw_data[len(self.hvac_raw_data) - 1][self.hvac_set_heat]))

		return thermo

	def return_mins_ac_cycle_readings(self):
		thermo = []
		if len(self.hvac_mins_ac_raw_data) == 0:
			return thermo

		for x in self.hvac_mins_ac_raw_data:
			if x[0] == "AC_Started":
				thermo.append([x[self.hvac_mins_ac_ts], 1])
			elif x[0] == "AC_dailymins":
				thermo.append([x[self.hvac_mins_ac_ts], 0])

		# default to OFF for first data point if prior day contains no cycle data
		if (self.bod_gap_fill == True):
			dt = self.hvac_mins_ac_raw_data[len(self.hvac_mins_ac_raw_data) - 1][self.hvac_mins_ac_ts].split(" ")
			st = float(dt[1][0:-3].replace(":","."))
			if (st > 0.0):
				dt[1] = "00:00:00"
				thermo.append([' '.join(dt), 0])

		return thermo

	def return_mins_heat_cycle_readings(self):
		thermo = []
		if len(self.hvac_mins_heat_raw_data) == 0:
			return thermo

		for x in self.hvac_mins_heat_raw_data:
			if x[0] == "Heating_Started":
				thermo.append([x[self.hvac_mins_heat_ts], 1])
			elif x[0] == "Heating_dailymins":
				thermo.append([x[self.hvac_mins_heat_ts], 0])

		# default to OFF for first data point if prior day contains no cycle data
		if (self.bod_gap_fill == True):
			dt = self.hvac_mins_heat_raw_data[len(self.hvac_mins_heat_raw_data) - 1][self.hvac_mins_heat_ts].split(" ")
			st = float(dt[1][0:-3].replace(":","."))
			if (st > 0.0):
				dt[1] = "00:00:00"
				thermo.append([' '.join(dt), 0])

		return thermo

	def return_timestrings(self):
		dates = []
		if len(self.hvac_raw_data) == 0:
			return dates

		if (self.bod_gap_fill == True):
			dates.append(0.0)

		for x in self.hvac_raw_data:
			dates.append(normalize_timestring(x[self.hvac_ts]))

		if (self.eod_gap_fill == True):
			dates.append(23.59)

		return dates

	def return_datestrings(self):
		dates = []
		rawdates = self.retrieve_query_from_sqlite("""select distinct date(ts, 'localtime') from device_history_hvac order by ts""")
		for x in rawdates:
			dates.append(x[0])

		return dates


def graph_defaults(html):
	html.append("myChart.setAxisNameColor('#333639');")
	html.append("myChart.setGridColor('#a4a4a4');")
	html.append("myChart.setFlagRadius(3);")
	html.append("myChart.setFlagWidth(2);")
	html.append("myChart.setAxisNameX('Time');")
	html.append('myChart.setIntervalStartX(00);')
	html.append('myChart.setIntervalEndX(24);')
	html.append("myChart.setAxisWidth(1);")
	html.append("myChart.setAxisValuesNumberX(25);")
	html.append("myChart.setAxisValuesColor('#454545');")
	html.append("myChart.setAxisPaddingBottom(38);")
	html.append("myChart.setTextPaddingBottom(8);")
	html.append("myChart.setBackgroundImage('images/chart_bg.jpg');")
	html.append('myChart.setSize(%d, %d);' % (graph_width, graph_height))
	html.append('myChart.draw();')

def create_graphs(html, hvac_sql_interface, thermostat_name, inDate = datetime.date.today()):
#	inDate = "2011-11-14"
	graph_urls = []
	hvac_data = hvac_sql_interface
	hvac_data.retrieve_hvac_data_from_sqlite(inDate, thermostat_name)
	if hvac_data.hvac_raw_data == None:
		html.append("No HVAC Data was found")
		return html

	temperature_readings_data = hvac_data.return_temperature_readings()
	humidity_readings_data = hvac_data.return_humidity_readings()
	setpoint_cooling_data = hvac_data.return_setpoint_cooling_readings()
	setpoint_heating_data = hvac_data.return_setpoint_heating_readings()
	time_data = hvac_data.return_timestrings()

	html.append('<div id="graph-humidity-%s" style="text-align: center;">Loading graph...</div>' % thermostat_name)
	html.append('<div id="graph-cool-%s" style="text-align: center;">Loading graph...</div>' % thermostat_name)
	html.append('<div id="graph-heat-%s" style="text-align: center;">Loading graph...</div>' % thermostat_name)

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

	humidity_matrix, cooling_matrix, heating_matrix, thermo_matrix = [], [], [], []
	hum_last = csp_last = hsp_last = temp_last = 999, 999, 999, 999
	t_hum_last = t_csp_last = t_hsp_last = t_temp_last = 999, 999, 999, 999
	t_end = time_data[len(time_data) - 1]
	for t, temp, hum, csp, hsp in zip(time_data, temperature_readings_data, humidity_readings_data, setpoint_cooling_data, setpoint_heating_data):
		if (hum != hum_last or t == t_end or int(t) - int(t_hum_last) >= hvac_data.min_duplicate_data_points_interval):
			if (hum >= hvac_data.hvac_humidity_min and hum <= hvac_data.hvac_humidity_max):
				humidity_matrix.append([t, hum])
				if (hvac_data.show_duplicate_data_points == False):
					hum_last = hum
					t_hum_last = t
		if (csp != csp_last or t == t_end or int(t) - int(t_csp_last) >= hvac_data.min_duplicate_data_points_interval):
			if (csp >= hvac_data.hvac_set_cool_min and csp <= hvac_data.hvac_set_cool_max):
				cooling_matrix.append([t, csp])
				if (hvac_data.show_duplicate_data_points == False):
					csp_last = csp
					t_csp_last = t
		if (hsp != hsp_last or t == t_end or int(t) - int(t_hsp_last) >= hvac_data.min_duplicate_data_points_interval):
			if (hsp >= hvac_data.hvac_set_heat_min and hsp <= hvac_data.hvac_set_heat_max):
				heating_matrix.append([t, hsp])
				if (hvac_data.show_duplicate_data_points == False):
					hsp_last = hsp
					t_hsp_last = t
		if (temp != temp_last or t == t_end or int(t) - int(t_temp_last) >= hvac_data.min_duplicate_data_points_interval):
			if (temp >= hvac_data.hvac_temp_min and temp <= hvac_data.hvac_temp_max):
				thermo_matrix.append([t, temp])
				if (hvac_data.show_duplicate_data_points == False):
					temp_last = temp
					t_temp_last = t

	# Summary -- BEGIN
	html.append('<hr>')
	html.append('<div id="summary" style="text-align: center;">')
	html.append('Cooling totals: %s mins, %s cycles' % (mins_ac_total, mins_ac_cycles))
	html.append(' &mdash; Heating totals: %s mins, %s cycles' % (mins_heat_total, mins_heat_cycles))
	html.append('<br>')
	html.append('Filter runtime to date: %s hours (%s mins)' % (hvac_data.hvac_mins_filter_total / 60, hvac_data.hvac_mins_filter_total))
	html.append(' &mdash; Last changed: %s' % (hvac_data.hvac_date_filter_changed))
	html.append('<br>')
	html.append('Room temp min/max/avg: %s/%s/%s' % (hvac_data.hvac_temp_min, hvac_data.hvac_temp_max, hvac_data.hvac_temp_avg))
	html.append(' &mdash; Humidity min/max/avg: %s/%s/%s' % (hvac_data.hvac_humidity_min, hvac_data.hvac_humidity_max, hvac_data.hvac_humidity_avg))
	html.append('</div>')
	html.append('<hr>')
	# Summary -- END

	# Raw data -- BEGIN
	html.append('<table id="rawdata-%s">' % (thermostat_name.replace(" ", "")))
	html.append('<tbody valign="top"><tr>')

	html.append('<td>')
	html.append('<table id="table-temp-%s" style="border-style: outset; border-width: 2px;">' % thermostat_name.replace(" ", ""))
	html.append('<caption style="color: %s;">Temperature Data</caption>' % graph_color_thermo)
	html.append('<thead><tr style="font-size: 12;">')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Set Cool</th>')
	html.append('<th scope="col">Set Heat</th>')
	html.append('<th scope="col">Temp</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	clvals = itertools.cycle(['even', 'odd'])
	for clval, data in itertools.izip(clvals, reversed(hvac_data.hvac_raw_data)):
		html.append('<tr class="row%s">' % clval)
		html.append('<td scope="row">%s</td><td>%s</td><td>%s</td><td>%s</td>' % (data[hvac_data.hvac_ts],
			data[hvac_data.hvac_set_cool], data[hvac_data.hvac_set_heat], data[hvac_data.hvac_temp]))
		html.append('</tr>')
	html.append('</tbody>')
	html.append('</table>')
	html.append('</td>')

	html.append('<td>')
	html.append('<table id="table-hum-%s" style="border-style: outset; border-width: 2px;">' % thermostat_name.replace(" ", ""))
	html.append('<caption style="color: %s;">Humidity Data</caption>' % graph_color_humidity)
	html.append('<thead><tr style="font-size: 12;">')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Humidity</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	clvals = itertools.cycle(['even', 'odd'])
	for clval, data in itertools.izip(clvals, reversed(hvac_data.hvac_raw_data)):
		html.append('<tr class="row%s">' % clval)
		html.append('<td scope="row">%s</td><td>%s</td>' % (data[hvac_data.hvac_ts], data[hvac_data.hvac_humidity]))
		html.append('</tr>')
	html.append('</tbody>')
	html.append('</table>')
	html.append('</td>')

	html.append('<td>')
	html.append('<table id="table-mins-ac"  style="border-style: outset; border-width: 2px;">')
	html.append('<caption style="color: %s;">Cooling Cycles</caption>' % graph_color_ac)
	html.append('<thead><tr style="font-size: 12;">')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Mode</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	mins_ac_matrix = []
	clvals = itertools.cycle(['even', 'odd'])
	for clval, data in itertools.izip(clvals, mins_ac_data):
		x = normalize_timestring(data[0])
		y = int(data[1])
		if y == 1:
			onoff = "On"
		else:
			onoff = "Off"

		mins_ac_matrix.append([x, y])

		html.append('<tr class="row%s">' % clval)
		html.append('<td scope="row">%s</td><td>%s</td>' % (data[0], onoff))
		html.append('</tr>')
	html.append('</tbody>')
	html.append('</table>')
	html.append('</td>')

	html.append('<td>')
	html.append('<table id="table-mins-heat" style="border-style: outset; border-width: 2px;">')
	html.append('<caption style="color: %s;">Heating Cycles</caption>' % graph_color_heat)
	html.append('<thead><tr style="font-size: 12;">')
	html.append('<th scope="col">Time</th>')
	html.append('<th scope="col">Mode</th>')
	html.append('</tr></thead>')
	html.append('<tbody>')
	mins_heat_matrix = []
	clvals = itertools.cycle(['even', 'odd'])
	for clval, data in itertools.izip(clvals, mins_heat_data):
		x = normalize_timestring(data[0])
		y = int(data[1])
		if y == 1:
			onoff = "On"
		else:
			onoff = "Off"

		mins_heat_matrix.append([x, y])

		html.append('<tr class="row%s">' % clval)
		html.append('<td scope="row">%s</td><td>%s</td>' % (data[0], onoff))
		html.append('</tr>')
	html.append('</tbody>')
	html.append('</table>')
	html.append('</td>')

	html.append('</tr></tbody>')
	html.append('</table>')
	# Raw data -- END

	html.append('''<script type="text/javascript" src="js/jscharts/jscharts.js"></script>''')

	# Humidity graph -- BEGIN
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-humidity-%s', 'line');" % thermostat_name)

	y_min = hvac_data.hvac_humidity_min - 4
	y_max = hvac_data.hvac_humidity_max + 3

	html.append('\nmyChart.setDataArray(%s, "humidity");\n' % humidity_matrix)
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		mins_ac_matrix_norm = copy.deepcopy(mins_ac_matrix)
		for x in mins_ac_matrix_norm:
			x[1] = y_max + x[1] * 1 - 1
		html.append('\nmyChart.setDataArray(%s, "ac_cycles");\n' % mins_ac_matrix_norm)
		del mins_ac_matrix_norm
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		mins_heat_matrix_norm = copy.deepcopy(mins_heat_matrix)
		for x in mins_heat_matrix_norm:
			x[1] = y_min + x[1] * 1 + 1
		html.append('\nmyChart.setDataArray(%s, "heat_cycles");\n' % mins_heat_matrix_norm)
		del mins_heat_matrix_norm

	for (x, y) in humidity_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Humidity: %s", "humidity"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('%s', 'humidity');" % (graph_color_humidity))
	html.append("myChart.setLineWidth(%d, 'humidity');" % (graph_lw_humidity))
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		for (x, y) in mins_ac_matrix:
			if y == 1:
				onoff = "ON"
			else:
				onoff = "OFF"
			html.append('\nmyChart.setTooltip([%f, "Time: %s   Cool %s", "ac_cycles"]);\n' % (x, x, onoff))
		html.append("myChart.setLineColor('%s', 'ac_cycles');" % (graph_color_ac_cycles))
		html.append("myChart.setLineWidth(%d, 'ac_cycles');" % (graph_lw_ac_cycles))
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		for (x, y) in mins_heat_matrix:
			if y == 1:
				onoff = "ON"
			else:
				onoff = "OFF"
			html.append('\nmyChart.setTooltip([%f, "Time: %s   Heat %s", "heat_cycles"]);\n' % (x, x, onoff))
		html.append("myChart.setLineColor('%s', 'heat_cycles');" % (graph_color_heat_cycles))
		html.append("myChart.setLineWidth(%d, 'heat_cycles');" % (graph_lw_heat_cycles))

	html.append('myChart.setTitle("%s - Humidity");' % thermostat_name)
	html.append("myChart.setTitleColor('#67ffca');")
	html.append("myChart.setAxisColor('#67ffca');")
	html.append("myChart.setAxisNameY('%');")
	html.append('myChart.setIntervalStartY(%s);' % (y_min))
	html.append('myChart.setIntervalEndY(%s);' % (y_max))

	graph_defaults(html)

	html.append('</script>')
	# Humidity graph -- END

	# min and max Y axis values for cooling and heating graphs
	y_min = min(hvac_data.hvac_temp_min, min(hvac_data.hvac_set_cool_min, hvac_data.hvac_set_heat_min))
	y_max = max(hvac_data.hvac_temp_max, max(hvac_data.hvac_set_cool_max, hvac_data.hvac_set_heat_max)) + 3

	# Cooling graph -- BEGIN
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-cool-%s', 'line');" % thermostat_name)

	html.append('\nmyChart.setDataArray(%s, "thermo");\n' % thermo_matrix)
	html.append('\nmyChart.setDataArray(%s, "ac");\n' % cooling_matrix)
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		mins_ac_matrix_norm = copy.deepcopy(mins_ac_matrix)
		for x in mins_ac_matrix_norm:
			x[1] = y_max + x[1] * 1 - 1
		html.append('\nmyChart.setDataArray(%s, "ac_cycles");\n' % mins_ac_matrix_norm)
		del mins_ac_matrix_norm

	for (x, y) in thermo_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Room Temp: %s", "thermo"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('%s', 'thermo');" % (graph_color_thermo))
	html.append("myChart.setLineWidth(%d, 'thermo');" % (graph_lw_thermo))
	for (x, y) in cooling_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Cool Temp: %s", "ac"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('%s', 'ac');" % (graph_color_ac))
	html.append("myChart.setLineWidth(%d, 'ac');" % (graph_lw_ac))
	html.append("myChart.setLineOpacity(1.0, 'ac_cycles');")
	if mins_ac_total > 0 and len(mins_ac_matrix) != 0:
		for (x, y) in mins_ac_matrix:
			if y == 1:
				onoff = "ON"
			else:
				onoff = "OFF"
			html.append('\nmyChart.setTooltip([%f, "Time: %s   Cool %s", "ac_cycles"]);\n' % (x, x, onoff))
		html.append("myChart.setLineColor('%s', 'ac_cycles');" % (graph_color_ac_cycles))
		html.append("myChart.setLineWidth(%d, 'ac_cycles');" % (graph_lw_ac_cycles))

	html.append('myChart.setTitle("%s - Cooling");' % thermostat_name)
	html.append("myChart.setTitleColor('#10109f');")
	html.append("myChart.setAxisColor('#10109f');")
	html.append("myChart.setAxisNameY('Degree');")
	html.append('myChart.setIntervalStartY(%s);' % (y_min))
	html.append('myChart.setIntervalEndY(%s);' % (y_max))

	graph_defaults(html)

	html.append('</script>')
	# Cooling graph -- END

	# Heating graph -- BEGIN
	html.append('<script type="text/javascript">')
	html.append("var myChart = new JSChart('graph-heat-%s', 'line');" % thermostat_name)

	html.append('\nmyChart.setDataArray(%s, "thermo");\n' % thermo_matrix)
	html.append('\nmyChart.setDataArray(%s, "heat");\n' % heating_matrix)
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		mins_heat_matrix_norm = copy.deepcopy(mins_heat_matrix)
		for x in mins_heat_matrix_norm:
			x[1] = y_max + x[1] * 1 - 1
		html.append('\nmyChart.setDataArray(%s, "heat_cycles");\n' % mins_heat_matrix_norm)
		del mins_heat_matrix_norm

	for (x, y) in thermo_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Room Temp: %s", "thermo"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('%s', 'thermo');" % (graph_color_thermo))
	html.append("myChart.setLineWidth(%d, 'thermo');" % (graph_lw_thermo))
	for (x, y) in heating_matrix:
		html.append('\nmyChart.setTooltip([%f, "Time: %s   Heat Temp: %s", "heat"]);\n' % (x, x, y))
	html.append("myChart.setLineColor('%s', 'heat');" % (graph_color_heat))
	html.append("myChart.setLineWidth(%d, 'heat');" % (graph_lw_heat))
	html.append("myChart.setLineOpacity(1.0, 'heat_cycles');")
	if mins_heat_total > 0 and len(mins_heat_matrix) != 0:
		for (x, y) in mins_heat_matrix:
			if y == 1:
				onoff = "ON"
			else:
				onoff = "OFF"
			html.append('\nmyChart.setTooltip([%f, "Time: %s   Heat %s", "heat_cycles"]);\n' % (x, x, onoff))
		html.append("myChart.setLineColor('%s', 'heat_cycles');" % (graph_color_heat_cycles))
		html.append("myChart.setLineWidth(%d, 'heat_cycles');" % (graph_lw_heat_cycles))

	html.append('myChart.setTitle("%s - Heating");' % thermostat_name)
	html.append("myChart.setTitleColor('#9f1010');")
	html.append("myChart.setAxisColor('#9f1010');")
	html.append("myChart.setAxisNameY('Degree');")
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
	def form_top(self, html_elems, dates, selected_date, show_duplicate_data):
		html_elems.append('<head>')
		html_elems.append('<title>Indigo HVAC Log Viewer</title></head>')
		html_elems.append('<link rel="stylesheet" type="text/css" href="css/hvac.css">')
		html_elems.append('<meta name="apple-mobile-web-app-capable" content="yes">')
		html_elems.append('<meta name="viewport" content="width=320, initial-scale=0.8, maximum-scale=1.6, user-scalable=yes"/>')
		html_elems.append('''<script type="text/javascript" src="js/jscharts/jscharts.js"></script>''')
		html_elems.append('''<script language="javascript">
			function toggle_it(itemID) { 
				// Toggle visibility between none and inline 
				if ((document.getElementById(itemID).style.display == 'none')) { 
					document.getElementById(itemID).style.display = 'inline'; 
				} else { 
					document.getElementById(itemID).style.display = 'none'; 
				} 
		}</script>''')
		html_elems.append('</head>')

		html_elems.append("<body>")
		html_elems.append('<table><tr><td>')

		html_elems.append('<table style="margin-left: 0px;">')
		html_elems.append('<tr><form method="post" action="">')
		html_elems.append('<td>')
		html_elems.append('View Day - <select name="date_selection" size="1">')
		html_elems.append('<option>Yesterday')
		dates.sort(reverse=True)
		for day in dates:
			if selected_date == day:
				html_elems.append('<option selected>%s' % day)
			else:
				html_elems.append('<option>%s' % day)
		html_elems.append('</select>')
		html_elems.append('</td>')
		html_elems.append('<td>')
		html_elems.append('<input type="checkbox" name="show_duplicate_data" value="True" ')
		if show_duplicate_data == "True":
			html_elems.append('checked="checked" ')
		html_elems.append('/>Show duplicate data points')
		html_elems.append('</td>')
		html_elems.append('<td>')
		html_elems.append('<input type="submit">')
		html_elems.append('</td>')
		html_elems.append('</tr>')
		html_elems.append('</table>')
		return html_elems

	def index(self, date_selection="None", show_duplicate_data="False"):
		cherrypy.response.headers['Content-Type'] = 'text/html'
		if (date_selection == "None" or date_selection == "Yesterday"):
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

		hvac = hvac_interface(dbFileName, show_duplicate_data)
		html_elems = self.form_top(html_elems, hvac.return_datestrings(), date_selection, show_duplicate_data)

		thermostats = hvac.retrieve_thermo_names(date_selection)
		for x in thermostats:
			html_elems = create_graphs(html_elems, hvac, x[0], date_selection)

		html_elems.append('</td></tr></table>')
		html_elems.append('</body>')

		return ''.join(html_elems)

	index.exposed = True

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
