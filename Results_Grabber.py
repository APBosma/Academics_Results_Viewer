import pandas as pd
import urllib.request
from pprint import pprint # Use pprint if you want to see the table in the least pretty way possible (ex. pp.pprint(p.tables[4]))
from html_table_parser.parser import HTMLTableParser

# Opens a website and read its
# binary contents (HTTP Response Body)
def urlGetContents(url):
    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()

# Constants
DISCTRICTS_COUNT = 32
REGIONS_COUNT = 4
SEASON_ID = 18
CONFERENCE = 3

# Note that 2 is for some reason not a valid grouping id, so we skip it :(
GROUPING_IDS = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

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

for district in range(1, DISCTRICTS_COUNT + 1):
    for grouping_id in GROUPING_IDS:
        # Getting stuff from url
        xhtml = urlGetContents(f'https://postings.speechwire.com/r-uil-academics.php?groupingid={grouping_id}&Submit=View+postings&region=&district={district}&state=&conference={CONFERENCE}&seasonid={SEASON_ID}').decode('utf-8')

        # HTMLTableParser object
        p = HTMLTableParser()
        p.feed(xhtml)

        # Cleaning up the data
        p.tables[4][0].pop(0)
        p.tables[4][0][0] = 'Place'

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

        # Handles scienc
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

# converting the parsed data to dataframe
print("\nTable\n")
# print(pd.DataFrame(data_with_columns))
# print(pd.DataFrame(data_with_columns).to_markdown())

with open("ResultsTesting.md", "w") as file:
    file.write(pd.DataFrame(data_with_columns).to_markdown())