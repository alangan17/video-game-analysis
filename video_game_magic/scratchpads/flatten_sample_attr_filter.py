import pandas as pd
import json

# Load the JSON data
with open('/home/src/sample_data/rawg_games_sample_attr_filters.json') as file:
    data = json.load(file)

# Prepare the data for the DataFrame
flatten_data = []

# Iterate through the years and their sub-years to flatten the structure
for entry in data['years']:
    for year in entry['years']:
        flatten_data.append({
            'Decade': entry['decade'],
            'From Year': entry['from'],
            'To Year': entry['to'],
            'Year': year['year'],
            'Count': year['count'],
            'Nofollow': year['nofollow']
        })

# Convert the data into a DataFrame
df = pd.DataFrame(flatten_data)
df.to_excel('output.xlsx', index=False)