from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os

def parse_trkpt(trkpt, hr_offset = 7):
	'''
	# parses each trackpoint in the gpx file's trkseg
	INPUT:
		trkpt:	bs4.element.Tag
		hr_offset: int (CA = 7)

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

def write_gpx_pickle(gpx_df):
	'''
	checks for existence of data dir, then writes gpx_df to it as a pickle
	INPUT:
		gpx_df: pandas Dataframe
	'''
	cwd = os.getcwd()
	if 'data' not in cwd:
		os.mkdir('data')
	gpx_df.to_pickle('data/gpx_df.pkl')
	return 

def process_gpx(gpx, write_pickle = False):
	'''
	processes a full gpx file read in as text

	INPUT:
		gpx: str
	OUTPUT:
		gpx_df
	'''
	soup = BeautifulSoup(gpx)
	seg = soup.find('trkseg')
	trackpoints = seg.findAll('trkpt')
	data = [parse_trkpt(trkpt) for trkpt in trackpoints]
	cols = ['date_time', 'lat', 'lon', 'ele']
	gpx_df = pd.DataFrame(data = data, columns = cols)
	gpx_df.set_index('date_time', inplace = True)
	if write_pickle:
		write_gpx_pickle(gpx_df)
	return gpx_df

if __name__ == '__main__':
	with open('data/JMP_Quickie.gpx', 'r') as f:
	    gpx = f.read()
	process_gpx(gpx, write_pickle = True)