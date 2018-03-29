#!/usr/bin/env python3

"""
script can be run as
./generate_trend_graph.py 1428998000 1429601000 testdata.txt output2.svg

Parameters
----------
arg1: start unix timestamp
arg2: end unix timestamp
arg3: full path of input data file
arg4: full path of output svg file

Returns
----------
error message in case of invalid inputs or exceptions

success message with output file path in case of successful completion

"""

import xml.etree.ElementTree as etree
from xml.dom import minidom
import sys, os

def read_data_file(start, end, data_file):

	"""
	Create a 2-dimensional list of the form 
	[['1429591293', 'True', 130], ['1429591423', 'False', 182],\
	 ['1429591605', 'True', 247], ['1429591852', 'False', 39],\
	  ['1429591891', 'True', 117], ['1429592008', 'False', 26]]

	where each sublist is as follows:
	first member: timestamp of state change or start/end in case of\
	 first and last elements
	second member: new state at the timestamp of first member
	third member: number of seconds the current state prevails 

	This 2-D list serves as a queue between input data file and the \
	output svg file.

	Parameters
	----------
	
	start : str
	    start timestamp received as command line argument
	end : str
	    end timestamp received as command line argument
	data_file : str
	    input file received as command line argument

	Returns
	----------
	list
	   A 2-D list with all the state change points and state durations\
	    captured
	"""
	change_queue = []
	try:
		with open(r'%s' %data_file) as f:
			line_list = f.readlines()
			try:
				first = line_list[0].split()[0]
				last = line_list[-1].split()[0]
				if start < int(first) or end > int(last):
					raise ValueError("Start and end should be in range of "\
					 + first + "-" + last)
				for line in line_list:
					data_arr = line.split()
					time = int(data_arr[0])
					state = data_arr[1]
					if time <= start:
						change_queue = [[start, state]]

					if start < time < end and state != change_queue[-1][1]:
						change_queue[-1].append(time -\
						 change_queue[-1][0])
						change_queue.append([time, state])

					if time >= end:
						change_queue[-1].append(end -\
						 change_queue[-1][0])
						break

			except ValueError as e:
				raise

	except IOError as e:
		raise

	return change_queue


def write_svg_file(svg_xml, output_file):
	try:
		with open(r'%s' %output_file, 'w') as f:
			f.write(svg_xml)
			return os.path.abspath(output_file)
	except IOError as e:
		raise



class XmlGenerator:

	"""
	An object of XmlGenerator class is initialized with the\
	change_queue created by reading input data file and\
	seconds_per_pixel calculated on the basis of difference in \
	start and end input arguments.

	Root element is created with tag svg and then a sub-element\
	rect is added corresponding to each state change as per\
	change_queue. width of each rect sub-element is calculated \
	using seconds_per_pixel and duration of the element state.
	"""

	def __init__(self, change_queue, seconds_per_pixel):
		self.change_queue = change_queue
		self.seconds_per_pixel = seconds_per_pixel 

	def generateXml(self):
		self.root = etree.Element(
				"svg", attrib={"viewBox": "0 0 500 50",\
				 "version": "1.1",\
				 "xmlns": "http://www.w3.org/2000/svg"}
			)
		self.x = 0

		for item in self.change_queue:
			fill = "white"
			if item[1] == "True":
				fill = "green"
			if item[1] == "False":
				fill = "red"
			width = item[2] / self.seconds_per_pixel
			attributes_dict = {
				"x": str(self.x), "y": "0", "height": "50",
				"width": str(width), "fill": fill
			}
			rectKwargs = { 
				"root": self.root, "tag": "rect",
				"attributes": attributes_dict
			}
			rect = self.addSubElement(**rectKwargs)
			self.x += width

	def addSubElement(self, root, tag, attributes={}):
		subElement = etree.SubElement(root, tag, attrib=attributes)
		return subElement

	def GetPrettyXml(self):
		reparsed = minidom.parseString(etree.tostring(self.root))
		XmlString = reparsed.toprettyxml()
		return XmlString


if __name__ == "__main__":
	try:
		start = int(sys.argv[1])
		end = int(sys.argv[2])
		data_file = sys.argv[3]
		output_file = sys.argv[4]
		time_range = end - start
		if time_range <= 0:
			raise ValueError("End should be greater than start")
	except ValueError as ve:
		sys.exit(ve)
	seconds_per_pixel = time_range/500
	try:
		change_queue = read_data_file(start, end, data_file)
	except ValueError as ve:
		sys.exit(ve)
	except IOError as ioe:
		sys.exit("Please provide a valid datafile. " + data_file +\
		 " could not be opened for reading data.")
	svg_object = XmlGenerator(change_queue, seconds_per_pixel)
	svg_object.generateXml()
	svg_xml = svg_object.GetPrettyXml()
	try:
		result = write_svg_file(svg_xml, output_file)
	except IOError as ioe:
		sys.exit("Please provide a valid file path for output. " +\
		 output_file + " seems to be an invalid or restricted path.")

	sys.exit("Output svg file saved successfully at " + result)

