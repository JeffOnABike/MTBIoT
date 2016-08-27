'''
This module reads a gpx file specified by the user in the /raw_data folder then processes and saves it as a pickled pandas dataframe in the data/ folder. 
'''

import os
import argparse
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def parse_trkpt(trkpt, hr_offset = 7):
	'''
	parses each trackpoint in the gpx file's trkseg
	
	INPUT:
		trkpt:	bs4.element.Tag
		hr_offset: int (CA = 7)
			this needs some work - probably as a cli arg to make it robust!

	OUTPUT:
		[date_time, lat, lon, ele] : list
			date_time: date_time.datetime
			lat: float
			lon: float
			ele: float
	'''
	lon = float(trkpt['lon'])
	lat = float(trkpt['lat'])
	time_str = trkpt.time.text
	time_l = time_str.split('T')
	date = time_l[0]
	# not robust for +TZ see ISO 8601 conventions
	# CA is generaly -05:00 offset, but for some reason 7 here
	time, tz_offset = time_l[1][:-1], time_l[1][-1]
	date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S') - timedelta(hours = hr_offset)
	ele = float(trkpt.ele.text)
	return [date_time, lat, lon, ele]

def write_gpx_pickle(gpx_df, gpx_fname):
	'''
	checks for existence of data/ dir, then writes gpx_df to it as a pickle
	
	INPUT:
		gpx_df: pandas Dataframe
		gpx_fname: str
	'''
	cwd = os.getcwd()
	if 'data' not in os.listdir(cwd):
		os.mkdir('data')
	print 'writing gpx_data to %s.pkl' % gpx_fname	
	gpx_df.to_pickle('data/%s.pkl' % gpx_fname)
	return 

def process_gpx(gpx, gpx_fname, write_pickle = False):
	'''
	processes a full gpx file read in as text, optionally writes it to a pickle file

	INPUT:
		gpx: str
		gpx_fname: str
		write_pickle: bool
	OUTPUT:
		gpx_df: pandas DataFrame
	'''
	soup = BeautifulSoup(gpx)
	seg = soup.find('trkseg')
	trackpoints = seg.findAll('trkpt')
	data = [parse_trkpt(trkpt) for trkpt in trackpoints]
	cols = ['date_time', 'lat', 'lon', 'ele']
	gpx_df = pd.DataFrame(data = data, columns = cols)
	gpx_df.set_index('date_time', inplace = True)
	if write_pickle:
		gpx_fname = gpx_fname.split('.')[0]
		write_gpx_pickle(gpx_df, gpx_fname)
	return gpx_df


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('gpx_fname', help = 'name of the gpx file in the raw_data folder')
	args = parser.parse_args()
	with open('raw_data/%s' % args.gpx_fname, 'r') as f:
	    gpx = f.read()
	process_gpx(gpx, args.gpx_fname, write_pickle = True)