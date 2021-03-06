import glob
import json
import os
import re
import time

def readfile(filepath):
	"""
	reads a pipeline json file and returns the resulting dictionary
	"""
	with open(filepath, "r") as json_file:
		json_data = json.load(json_file)

	return json_data

def writefile(filepath, datadict):
	"""
	writes the given data dictionary to a pipeline json file at the given filepath
	"""
	with open(filepath, "w") as json_file:
		json.dump(datadict, json_file)

def mkdir(dirpath):
	"""
	create the given filepath. returns true if successful, false otherwise.
	"""
	try:
		os.mkdir(dirpath) # TODO: ensure correct permissions
	except OSError:
		return False # file already exists
	return True

def version_file(filepath, zero_pad=3):
	"""
	versions up the given file based on other files in the same directory. The given filepath 
	should not have a version at the end. e.g. given "/tmp/file.txt" this function will return 
	"/tmp/file000.txt" unless there is already a file000.txt in /tmp, in which case it will 
	return "/tmp/file001.txt". zero_pad specifies how many digits to include in the version 
	number--the default is 3.
	"""
	if zero_pad < 1:
		zero_pad = 1
	dirpath, filename = os.path.split(filepath)
	base, ext = os.path.splitext(filename)
	searchpath = os.path.join(dirpath, "*")
	files = glob.glob(searchpath)
	versions = []
	for f in files:
		tmpname = os.path.basename(f)
		if re.match(base+"[0-9]{%d}"%zero_pad+ext, tmpname):
			versions.append(tmpname)
	versions.sort()
	version_num = 0
	if len(versions) > 0:
		latest = versions[-1]
		latest_name = os.path.splitext(latest)[0]
		idx = len(latest_name) - zero_pad
		num_str = latest_name[idx:]
		version_num = int(num_str)+1
	return os.path.join(dirpath, base+str(version_num).zfill(zero_pad)+ext)

def version_dir(dirpath, zero_pad=3):
	"""
	versions up the given directory based on other directories in the same directory. The given dirpath 
	should not have a version at the end. e.g. given "/tmp/v" this function will return 
	"/tmp/v000" unless there is already a v000 dir in /tmp, in which case it will 
	return "/tmp/v001". zero_pad specifies how many digits to include in the version 
	number--the default is 3.
	"""
	raise NotImplementedError() # TODO

def timestamp():
	"""
	return a string containing the current time
	"""
	return time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())