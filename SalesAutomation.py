'''
Sales Automation script 

The whole Idea is getting information from a database [if available] from input list of company names
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import re

def create_output(company_names):
    i=0
    for num,name in enumerate(company_names):
        if(i == len(company_names)):
            break
        found = all_df.loc[all_df['App Name'].str.contains(name,na=False)][:10]
        #If Several : take the one with highest downloading rate - I could have added several rows 
        #But found it more convenient this way
        found['Installs'] = found['Installs'].map(lambda Installs: float(''.join(Installs.split('+')[0].split(','))))
        
        if(found['App Name'].count() >= 1):
            yield found.loc[found['Installs'].idxmax()],num
        else :
            yield found,num
        i += 1


if __name__ == '__main__':

	assert len(sys.argv) == 2 ,'Problem in specifying input file'

	inp = sys.argv[1]
	input_series  = pd.read_excel(inp)
	company_names = input_series['Company Name'].values

	#Load DB
	store_df = pd.read_csv('db/apps.csv',error_bad_lines=False)
	store_df = store_df[['name','numDownloadsMin','aggregateRating','url']]
	
	apps_df  = pd.read_csv('db/Google-Playstore-Full.csv')
	apps_df  = apps_df[['App Name','Rating','Installs']]

	#Joining the two data bases
	all_df = apps_df.merge(store_df,how='left',left_on='App Name',right_on='name')
	all_df = all_df[['App Name','Rating','Installs','url']]

	all_df['Developers Website'] = np.nan

	out_series = pd.DataFrame({'Company':company_names,'App Name': np.nan,'Rating':np.nan,'Installs':np.nan,'url':np.nan,'Developers Website':np.nan})
	
	for i,num in create_output(company_names):
		if(i.empty):
			continue
		out_series.iloc[num,1:] = i.values

	out_series.reset_index(drop=True)
	out_series.to_csv('out-WithCompanies.csv',index=False)