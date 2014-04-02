# start shell with '$ ipython --pylab'
path = 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'
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
