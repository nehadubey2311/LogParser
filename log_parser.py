# log_parser.py
#
# Neha Dubey
# 
# Usage: python log_parser.py
# 
# This program accepts following user input:
# 	1. Path to zipped debugInfo (log file)
# 	2. Fault to be looked up in logs from pre-defined faults
# 	3. If not from pre-defined then any error string to look for
# It will then unzip debugInfo log to a predefined destination
# after clearing it up and parse logs for fault entered.
# The results are then plotted as bar graph and results are provided
# in tabular form.
# Also a detailed description is provided to help debug the issue
#

import glob
import io
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import sys
import zipfile

from collections import defaultdict
from faults_data import fault_data
from matplotlib.pyplot import figure

working_dir = os.getcwd()
log_extract_path =  "%s/%s" % (working_dir , "unzippedDebugInfo")
log_path = "%s/%s" % (working_dir , "unzippedDebugInfo/var/robot/logs")

def prep_extraction_dir():
	"""Cleans up and prepares directory where debugInfo
	would be extracted.
	"""
	if not os.path.exists(log_extract_path):
		os.mkdir(log_extract_path)
	try:
		if os.path.exists(log_extract_path) and os.path.isdir(log_extract_path):
			if os.listdir(log_extract_path):
				for entry in os.listdir(log_extract_path):
					if os.path.isdir(os.path.join(log_extract_path, entry)):
						shutil.rmtree(os.path.join(log_extract_path, entry))
					else:
						os.remove(os.path.join(log_extract_path, entry))
			print("Extraction directory cleaned up !")
	except:
		print(f"Extraction directory {log_extract_path} could not be cleaned up, exiting!")
		sys.exit()

def extract_debug_info(debugInfo_path):
	"""Extracts zipped log file to destination directory
	
	Arguments:
		debugInfo_path {[string]} -- [Path to zipped log file]
	
	Raises:
		ex -- [When zipped log could not be extracted]
	"""
	try:
		with zipfile.ZipFile(debugInfo_path, 'r') as zip_ref:
			zip_ref.extractall("./unzippedDebugInfo")
			print("DebugInfo extracted")
	except FileNotFoundError as ex:
		print("Zipped file not found")
		raise ex
	except zipfile.BadZipFile as ex:
		print("Bad zip file")
		raise ex
	except Exception as ex:
		raise ex

def parse_logs(log_path, fault):
	"""Loops over all logs for the input fault and
	calls generate_plots() function to create a plot
	
	Arguments:
		log_path {[string]} -- [path within zipped log file to search]
		fault {[string]} -- [Robot fault]
	
	Raises:
		ex -- [Exception when log files could not be found]
	"""
	# To hold mapping between Timestamp of fault : Frequency   
	data_dict = defaultdict(int)
	# List of lists to store logfile name and timestamp for fault occurance
	data_lst = []

	log_files = [f for f in glob.glob(log_path + "/log*.txt")]

	for log_file in log_files:
		try:
			with io.open(log_file, 'r', encoding='Windows-1252') as file_reader:
				text = file_reader.read()
				text = text.split('\n')
				for line in text:
					if fault in line:
						data_dict[line[:13]] += 1
						data_lst.append([os.path.basename(log_file), line[:26]])
		except FileNotFoundError as ex:
			raise ex
	if not bool(data_dict):
		print("Error was not found in the DebugInfo provided. Indeed a good thing !!")
		sys.exit()
	else:
		data_lst.sort(key=lambda x: x[1])
		generate_plots(data_dict, data_lst, fault)

def generate_plots(data_dict, data_lst, fault):
	""" Generates Matplotlib bar graph and table alongwith
	helpful description for next steps.
	
	Arguments:
		data_dict {[Dict]} -- [Dictionary to store Fault and frequency of fault]
		data_lst {[List]} -- [List of lists to store logfile name 
		                        and fault timestamp]
		fault {[String]} -- [Robot fault]
	"""
	x_axis = [i for i in data_dict.keys()]
	y_axis = [i for i in data_dict.values()]

	try:
		# Plotting two subplots
		fig, (ax1, ax2) = plt.subplots(1,2)
		fig.suptitle(f"{fault} Map", fontsize=18, fontweight='bold')
		# fig.set_figheight(15)
		# fig.set_figwidth(15)

		ax1.bar(x_axis, y_axis)
		ax1.set_xlabel('Timestamp', fontsize=12, fontweight='bold')
		ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')

		table_array = np.array(data_lst)
		columns=('Logfile Name', 'Timestamp')
		colors = ['#45adcc', '#45adcc']
		table = ax2.table(cellText=table_array, 
			loc='center', colLabels=columns,
			colColours=colors )
		table.auto_set_font_size(False)
		table.set_fontsize(14)
		
		ax2.axis('off')
		table.scale(1.2, 2.2) 
		figManager = plt.get_current_fig_manager()
		figManager.window.showMaximized()

		fault_desc = fault_data[fault]
		print("Generating graph now...")
		plt.gcf().text(0.5, 0.02, f"{fault_desc[0]}: {fault_desc[1]}",
			fontweight='bold', color='red', 
			verticalalignment='center',
			horizontalalignment='center', wrap=True)

		plt.show()
	except Exception as ex:
		print(f"Plots could not be created, {ex}")


def main():
	# Get user input for debugInfo file and error string
	debugInfo_path = input("\nPlease provide path to debugInfo file:\n")
	print()
	print(list(fault_data.keys()))

	fault = input("\n\nSelect a fault from listed above or enter an error keyword to search:\n")
	# Clear directory to unzip logs
	prep_extraction_dir()
	# Extract provided zipfile
	extract_debug_info(debugInfo_path)
	# Parse logs and plot results
	parse_logs(log_path, fault)

if __name__ == '__main__':
	main()

