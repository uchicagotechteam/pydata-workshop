''' now we will be exploring data from the 2012 election
    The dataset we will be exploring contains the Federal Election 
    Commissions data on contributions to political campaigns 
    this dataset is relatively large (150 mb), so we'll be exploring
    a limited portion
'''
# prepare your work environment
import pandas as pd
# read in the csv file containing the data
fec = pd.read_csv('ch09/P00000001-ALL.csv')

# let's look at the dataset overview and a sample record
fec
fec.ix[123456]

# there are no political party affiliations, so let's go ahead 
# and add some
# let's first get a list fo all the unique candidates
unique_cands = fec.cand_nm.unique()
unique_cands

# now we'll use a dict to add party affiliation
parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}
