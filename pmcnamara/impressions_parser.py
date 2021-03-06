import os
import pandas as pd
import numpy as np
import datetime
import glob
import statsmodels as sm

# WEB IMPRESSIONS #
imp_17 = '/Users/mcnamarp/Downloads/Initiative_Files/MSG INI Weekly Reporting - 2017.12.17.xlsx'
newest = max(glob.iglob('/Users/mcnamarp/Downloads/Initiative_Files/*.xlsx'), key=os.path.getctime)
impressions = pd.read_excel(newest, sheetname = 'Paid Pivot', converters= {'Week Starting': pd.to_datetime})
impressions_17 = pd.read(imp_17, sheetname = 'Paid Pivot', converters= {'Week Starting': pd.to_datetime})
impressions = impressions.append(impressions_17)

# ARGUS ANALYSIS #
argus_imp = impressions[impressions['Campaign Name'] == 'Knicks Indy']
argus_imp = argus_imp[argus_imp['Week Number'].isin(range(43,53)]
argus_imp = argus_imp[argus_imp['Placement_14'].isin(['DATA DRIVEN PROSPECTING','INDY CRM TARGETING'])]

drops = ['Year','Month Number','Week Number','%Viewable Impressions','Placement_1','Placement_2','Placement_3',
		'Placement_4','Placement_5','Placement_6','Placement_7','Placement_8','Placement_9','Placement_10','Placement_11','Placement_12',
		'Placement_13','Placement_14','Placement_15','Placement_16','Placement_17','Placement_18','Concert Creative_1','ConcertCreative_2',
		'Creative Concept','Unit Size','Placement','Placement ID','Site ID','Campaign ID',
		'Area','Media Category','Campaign Name','Publisher','Actualized Imps','Week Starting','Week Ending','Actualized Clicks','Actualized Cost',
		'Viewable Impression Distribution','Viewable Impressions','Media','Campaign','Site (Social)','DCM Imps','DCM Clicks','DCM Spend','Revenue']
		
argus_imp.drop(drops, axis = 1, inplace = True)


impressions.drop(drops, axis = 1, inplace = True)
impressions.drop(['Devices','Tactic','Segment'], axis = 1, inplace = True)
impressions.rename(columns = {'Sales':'Orders','DATE':'Date'}, inplace = True)
impressions.groupby('Date').sum()

impressions.drop_duplicates().to_csv('/Users/mcnamarp/Downloads/Initiative_Files/web_impressions.csv', index = False)

# FB IMPRESSIONS #
# import and combine files #
fb_impressions_16_17 = pd.read_excel('/Users/mcnamarp/Downloads/FB_Files/Knicks Daily Data thru end of fiscal - 11 15 17.xlsx', sheetname = 'Raw Data')
drops = ['Reporting Ends','Website Purchases [7 Days After Viewing]','Website Purchases [7 Days After Clicking]','Website Purchases Conversion Value [7 Days After Viewing]','Website Purchases Conversion Value [7 Days After Clicking]']
fb_impressions_16_17.drop(drops, axis = 1, inplace = True)
newest_fb = max(glob.iglob('/Users/mcnamarp/Downloads/FB_Files/*.xlsx'), key=os.path.getctime)
fb_impressions_17_18 = pd.read_excel(newest, sheetname = 'Sheet1')
drops = ['Website Purchases Conversion Value','Website Purchases']
fb_impressions_17_18.drop(drops, axis = 1, inplace = True)
fb_impressions = fb_impressions_16_17.append(fb_impressions_17_18)

# clean and normalize #

fb_impressions['Date'] = fb_impressions['Date'].dt.date
fb_impressions = fb_impressions.set_index('Date')

date_range_1 = pd.date_range(datetime.date(2016,9,27), datetime.date(2017,4,12)).date
date_range_2 = pd.date_range(datetime.date(2017,9,12), fb_impressions_17['Date'].max().date()).date
date_range = pd.DataFrame(index = list(date_range_1)+list(date_range_2))
fb_impressions = date_range.join(fb_impressions).fillna(0)
fb_impressions.to_csv('/Users/mcnamarp/Downloads/Initiative_Files/fb_impressions.csv')


# RADIO DATA #
'/Users/mcnamarp/Downloads/NY KNICKS_ RADIO PRE + POST LOGS W.O_11.6.xlsb'