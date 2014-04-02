''' now we will be exploring data from the 2012 election
    The dataset we will be exploring contains the Federal Election 
    Commissions data on contributions to political campaigns 
    this dataset is relatively large (150 mb), so we'll be exploring
    a limited portion
'''
# prepare your work environment
import pandas as pd
import numpy as np
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

# with this mapping and map method on series objects, we can
# compute an array of political parties from candidate names
fec.cand_nm[123456:123461]
fec.cand_nm[123456:123461].map(parties)

# now let's add this as a column
fec['party'] = fec.cand_nm.map(parties)
fec['party'].value_counts()

# note that the data includes both contributions and refunds
(fec.contb_receipt_amt > 0).value_counts()

# let's restrict the dataset to positive contributions
fec = fec[fec.contb_receipt_amt > 0]
# let's now restrict the dataset to Obama and Romney
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

'''Donation statistics by Occupation and Employer'''
# let's first find total number of occupations
fec.contbr_occupation.value_counts()[:10]

# many of these occupations are pretty much the same, so let's clean
# that up
occ_mapping = {
    'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
    'INFORMATION REQUESTED' : 'NOT PROVIDED',
    'INFORMATION REQUESTED (BEST EFFORTS)' : 'NOT PROVIDED',
    'C.E.O.' : 'CEO'
}

# if no mapping provided, return x
f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)
fec_mrbo.contbr_occupation = fec_mrbo.contbr_occupation.map(f)

# let's do the same thing for employers
emp_mapping = {
    'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
    'INFORMATION REQUESTED' : 'NOT PROVIDED',
    'SELF' : 'SELF-EMPLOYED',
    'SELF EMPLOYED' : 'SELF-EMPLOYED'
}

# if no mapping provided, return x
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)
fec_mrbo.contbr_employer = fec_mrbo.contbr_employer.map(f)

# let's now use a pivot table to aggregated data by party and occupation
# and then filter down to subset that contributed at least 2 million
by_occupation = fec.pivot_table('contb_receipt_amt', rows='contbr_occupation', cols='party', aggfunc='sum')

# limiting to at least 2 million
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
over_2mm

# let's turn this data into a bar plot
over_2mm.plot(kind='barh')

# le's say we're interested in top donor occupations or top donor companies
# can group by candidate name and use a variant of top method from earlier
def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    # order totals by key in descending order
    return totals.order(ascending=False)[:n]

# now let's aggregate by occupation and employer
grouped = fec_mrbo.groupby('cand_nm')
grouped.apply(get_top_amounts, 'contbr_occupation', n=7)
grouped.apply(get_top_amounts, 'contbr_employer', n=10)


''' Bucketing Donation Amounts '''
# let's use the cut function to discretize contributor amounts into 
# buckets by contribution size
bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)

# group data by name and bin label to get histogram of donation size 
grouped = fec_mrbo.groupby(['cand_nm', labels])
grouped.size().unstack(0)

# can also sum contribution amounts and normalzie within buckets 
# to visualize percentage of total donatiosn of each size by candidate
bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
bucket_sums
# let's now normalize these sums
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
normed_sums
# now let's plot this data
normed_sums[:-2].plot(kind='barh', stacked=True)

''' Donation Statistics by State '''
# let's first aggregate data by candidate and state
grouped = fec_mrbo.groupby(['cand_nm', contbr_st])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
totals[:10]

# if divide each row by total contb amt, we get relative percentage
# of total donations by stat for each candidate
percent = totals.div(totals.sum(1), axis=0)
percent[:10]
