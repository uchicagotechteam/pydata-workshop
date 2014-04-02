# start shell with '$ ipython --pylab'

# set path to our data of interest
path = 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'
# try reading in first line of file
open(path).readline()

# import json module to store file as json object
import json

# use list comprehension to create json object
records = [json.loads(line) for line in open(path)]

# let's look at the first couple of records
records[0]
records[0]['tz']
print records[0]['tz']

'''COUNTING TIME ZONES'''

# this next line should throw an error
time_zones = [rec['tz'] for rec in records]

# fixed version: checks if record has tz field
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

# check first 10 time zones
time_zones[:10]

# naive way of counting time zones
def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

# a bit more knowledge of the Python Standard Library 
# allows us to do this
from collections import defaultdict

def get_counts2(sequence):
    counts = defaultdict(int) # values will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts

# using get_counts function and exploring results
counts = get_counts(time_zones)
counts['America/New_York']
len(time_zones)

# function to find top 10 time zones and their counts
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

# running our function
top_counts(counts)

# a much easier way to do this using the Python standard library
from collections import Counter
counts = Counter(time_zones)
counts.most_common(10)

'''counting time zones using pandas'''
# a DataFrame represents a table or spreadsheet of data
from pandas import DataFrame, Series
import pandas as pd; import numpy as np

# creating a new frame from our records
frame = DataFrame(records)
# display frame
frame

# checking out time zones
frame['tz'][:10]

# frame['tz'] returns series object, has method value_counts 
# that does what we need
tz_counts = frame['tz'].value_counts()
tz_counts[:10]

# we're now going to fill in unknown and missing values in our data
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
tz_counts[:10]

# let's make a horizontal bar plot
tz_counts[:10].plot(kind='barh', rot=0)

# another one of the fields contains information about browser, device,
# or application that was used to perform the shortening
frame['a'][1]
frame['a'][50]
frame['a'][51]

# want to parse data in these 'agent' strings
# we'll split off first token in string, corresponding to 
# browser capability
results = Series([x.split()[0] for x in frame.a.dropna()])
results[:5]
# let's see the top results
results.value_counts()[:8]

# let's say we want to decompose top time zones into Windows 
# and not windows
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
operating_system[:5]
