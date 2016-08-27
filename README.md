# MTBIoT

This project aims to provide a common place for cycling enthusiasts & pythonistas to acquire and build tools for working with personally-collected data.

## General use instructions
Once forked, use as current working directory:
/MTBIoT
refer to requirements.txt for environment packages and versions

## Writing your own data

### From Strava 

While logged into your Strava account:
- Select Segment
- Export the GPX(Actions (wrench icon) >> Export GPX filename format: SEGMENT_NAME.gpx)
- If not already downloaded to directory, move it to /raw_data (e.g. my last ride's gpx file is in MTBIoT/raw_data/JMP_Quickie.gpx)

### From command line:
```
$ python gpx_to_df.py SEGMENT_NAME.gpx
```

## Loading data from data/

In a python environment:
```
import pandas as pd
gpx_df = pd.read_pickle('data/SEGMENT_NAME.pkl')
```

You now have a date-time indexed pandas dataframe of the trackpoints recorded from your Strava segment.