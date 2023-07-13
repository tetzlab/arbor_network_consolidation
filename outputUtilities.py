#!/bin/python3

# Utility functions for displaying and storing data

# Copyright 2021-2023 Jannik Luboeinski
# License: Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Contact: mail[at]jlubo.net

import time
from datetime import datetime
import os
import re

###############################################################################
# redText
# Adds flags to print given text in red color in console.
# - text: the text to be colored
# - return: the text with red color/standard color flags
def redText(text):
	return "\x1b[31m" + str(text) + "\x1b[0m"

###############################################################################
# cyanText
# Adds flags to print given text in cyan color in console.
# - text: the text to be colored
# - return: the text with cyan color/standard color flags
def cyanText(text):
	return "\x1b[36m" + str(text) + "\x1b[0m"

###############################################################################
# getTimestamp
# Returns a previously determined timestamp, or the timestamp of the current point in time
# - refresh [optional]: if True, forcibly retrieves a new timestamp; else, only returns a new timestamp if no previous one is known
# - return: timestamp in the format YY-MM-DD_HH-MM-SS
def getTimestamp(refresh = False):
	global timestamp_var # make this variable static
		
	try:
		if timestamp_var and refresh == True:
			timestamp_var = datetime.now() # forcibly refresh timestamp
	except NameError:
		timestamp_var = datetime.now() # get timestamp for the first time
		
	return timestamp_var.strftime("%y-%m-%d_%H-%M-%S")
	
###############################################################################
# getFormattedTime
# Returns a string indicating the hours, minutes, and seconds of a time given in seconds
# - time_el: time in seconds
# - return: formatted time string
def getFormattedTime(time_el):
	if time_el < 1:
		time_el_str = "<1 s"
	elif time_el < 60:
		time_el_str = f"{time_el} s"
	elif time_el < 3600:
		time_el_str = f"{time_el // 60} m {time_el % 60} s"
	else:
		time_el_str = f"{time_el // 3600} h {(time_el % 3600) // 60} m {(time_el % 3600) % 60} s"
	
	return time_el_str	

###############################################################################
# getTimeDiff
# Returns current timepoint and the time that has passed since a given timepoint
# - t_ref [optional]: reference timepoint
# - return: current timepoint, time difference
def getTimeDiff(t_ref = 0):
	t_cur = time.time()

	return t_cur, t_cur - t_ref

###############################################################################
# setDataPathPrefix
# Sets prefix for the path names used by getDataPath()
# - prefix [optional]: prefix string
def setDataPathPrefix(prefix = ""):
	global data_path_prefix

	data_path_prefix = prefix
    
###############################################################################
# getDataPath
# Consumes a general description for the simulation and a file description, and returns 
# a path to a timestamped file in the output directory;  if no file description is provided, 
# returns the path to the output directory
# - sim_description: general description for the simulation
# - file_description [optional]: specific name and extension for the file
# - refresh [optional]: if True, enforces the retrieval of a new timestamp
# - return: path to a file in the output directory
def getDataPath(sim_description, file_description = "", refresh = False):
	global data_path_prefix

	timestamp = getTimestamp(refresh)
	out_path = data_path_prefix + timestamp 
	
	if sim_description != "":
			out_path = out_path + " " + sim_description

	if file_description == "":
		return out_path
		
	return os.path.join(out_path, timestamp + "_" + file_description)

###############################################################################
# initLog
# Initializes the global log file
# - desc: description in the data path
def initLog(desc):
	global logf

	logf = open(getDataPath(desc, "log.txt"), "w")

###############################################################################
# writeLog
# Writes string(s) to the global log file and prints to the console
# - ostrs: the string(s) to be written/printed
# - prnt [optional]: specifies whether to print to console or not
def writeLog(*ostrs, prnt = True):
	global logf

	for i in range(len(ostrs)):
		ostr = str(ostrs[i])
		ostr = re.sub(r'\x1b\[[0-9]*m', '', ostr) # remove console formatting
		if i == 0:
			logf.write(ostr)
		else:
			logf.write(" " + ostr)
	logf.write("\n")
	
	if prnt:
		print(*ostrs)

###############################################################################
# writeAddLog
# Writes string(s) to global log file (without printing to the console)
# - ostrs: the string(s) to be written
def writeAddLog(*ostrs):

	writeLog(*ostrs, prnt = False)

###############################################################################
# closeLog
# Close the global log file
def closeLog():
	global logf

	logf.close()

###############################################################################
# getSynapseId
# If provided, returns the synapse identifier for the corresponding neuron identifier in 'sample_gid_list', 
# otherwise, returns the generic identifier
# - sample_syn_list: the list of synapse indices (or value -1 to disbale reading)
# - index: pointing at the list element to be considered
# - return: the synapse identifier
def getSynapseId(sample_syn_list, index):

		# get synapse id provided for corresponding neuron in 'sample_gid_list'
		if len(sample_syn_list) > 1:
			sample_syn = sample_syn_list[index]

		# get generic synapse id that has been provided 
		else:
			sample_syn = sample_syn_list[0]

		return sample_syn
