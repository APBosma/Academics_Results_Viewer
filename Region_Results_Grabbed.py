# Author: Adele Bosma
# Purpose: Grabs all region data from the UIL website for the given year and saves it to a csv file.
# How to use: Verify you are correct year's information you are looking for by seeing the season id in the url. For example, for the 2025-2026 season,
# you want to make sure SEASON_ID is set to 18. Then, run the script and it will create a folder for each conference and save the region results in that folder.
# The naming conventions for the files are Results_{conference}A_{region}R.csv. For example, the results for conference 1A region 1 will be saved as 
# Results_1A_1R.csv in the Results_1A folder.
import pandas as pd
import urllib.request
from html_table_parser.parser import HTMLTableParser

# Opens a website and read its
def urlGetContents(url):
    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()

# Constants
CONFERENCE_COUNT = 6
REGION_COUNT = 4
SEASON_ID = 18

# Note that 2 is for some reason not a valid grouping id, so we skip it :(
GROUPING_IDS = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

for conference in range(1, CONFERENCE_COUNT + 1):
    for region in range(1, REGION_COUNT + 1):
        data_with_columns = {
            'Contest_ID': [],
            'Place': [],
            'School': [],
            'Entry': [],
            'Code': [],
            'Total': [],
            'Objective': [],     # Social Studies and Lit Crit
            'Essay': [],         # Social Studies and Lit Crit
            'Biology': [],       # Science Only
            'Chemistry': [],     # Science Only
            'Physics': []        # Science Only
        }
        for grouping_id in GROUPING_IDS:
            # Getting stuff from url
            xhtml = urlGetContents(f'https://postings.speechwire.com/r-uil-academics.php?groupingid={grouping_id}&Submit=View+postings&region={region}&district=&state=&conference={conference}&seasonid={SEASON_ID}').decode('utf-8')
            p = HTMLTableParser()
            p.feed(xhtml)

            # Cleaning up the data and adding needed columns
            p.tables[4][0].pop(0)
            p.tables[4][0][0] = 'Place'

            # Setting basic setup data (Contest, place, school, entry, code)
            for row in p.tables[4][1:len(p.tables[4])]:
                data_with_columns['Contest_ID'].append(grouping_id)
                data_with_columns['Place'].append(row[0])
                data_with_columns['School'].append(row[1])
                data_with_columns['Entry'].append(row[2])
                data_with_columns['Code'].append(row[3])

            # Handles accounting, calculator, computer science, mathematics, number sense, etc. (Items graded as is)
            if grouping_id in [1, 7, 8, 9, 10, 11]:
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Total'].append(row[4])
                    data_with_columns['Biology'].append(None)
                    data_with_columns['Chemistry'].append(None)
                    data_with_columns['Physics'].append(None)
                    data_with_columns['Objective'].append(None)
                    data_with_columns['Essay'].append(None)

            # Handles science
            elif grouping_id == 12:
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Biology'].append(row[4])
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Chemistry'].append(row[5])
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Physics'].append(row[6])
                    data_with_columns['Total'].append(None)
                    data_with_columns['Objective'].append(None)
                    data_with_columns['Essay'].append(None)
            
            # Handles social studies and lit crit
            elif grouping_id in [6, 4]:
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Objective'].append(row[4])
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Essay'].append(row[5])
                    data_with_columns['Total'].append(None)
                    data_with_columns['Biology'].append(None)
                    data_with_columns['Chemistry'].append(None)
                    data_with_columns['Physics'].append(None)

            # Everything with no scores listed, just points
            else:
                for row in p.tables[4][1:len(p.tables[4])]:
                    data_with_columns['Total'].append(None)
                    data_with_columns['Biology'].append(None)
                    data_with_columns['Chemistry'].append(None)
                    data_with_columns['Physics'].append(None)
                    data_with_columns['Objective'].append(None)
                    data_with_columns['Essay'].append(None)

        # Saving the data to a csv file
        pd.DataFrame(data_with_columns).to_csv(f'Results_{conference}A//Results_{conference}A_{region}R.csv', index=False)