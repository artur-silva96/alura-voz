# %%
import requests
import pandas as pd

# %%
# Function to get the content of the json in a 'url' and return a normalized DataFrame
def df_normalized(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f'Status code error ({response.status_code})')
    return pd.json_normalize(data)

# %%
# Visualizing the data
url = 'https://raw.githubusercontent.com/sthemonica/alura-voz/main/Dados/Telco-Customer-Churn.json'
df = df_normalized(url)
df

# %%
# Renaming the columns, droping the prefixes ('customer.', 'phone.', 'internet.' and 'account.',)
df.columns = df.columns.str.replace(r'^[^.]*\.', '', regex=True)
df

# %%
# Checking DataFrame information
df.info()

# %%
# Checking unique values
for column in df.columns:
    print(df[column].value_counts())
    print('-----')

# %%
# Checking what values does 'Churn' column have
df['Churn'].value_counts()

# %%
# Droping rows with missing values in column 'Churn'
df = df[df['Churn'] != '']
df.reset_index(drop=True, inplace=True)
df['Churn'].value_counts()

# %%
# When 'tenure' is 0, 'Charges.Total' becomes a whitespaced string (' '). It's because didn't make a full month yet
df[df['tenure'] == 0]

# %%
# Then we need to take into account that, in these cases, the total expenses is equal to the montly expenses
mask = df['Charges.Total'] == ' '
df.loc[mask, 'Charges.Total'] = df.loc[mask, 'Charges.Monthly']
df.loc[:,'Charges.Total'] = pd.to_numeric(df['Charges.Total'])
df[df['tenure'] == 0]

# %%
# [Extra] Inserting column 'Charges.Daily' in DataFrame
# Since we don't have the specific months to work with, the average month will be 30.42 days (365/12)
daily_charges = round(df['Charges.Monthly'] / 30.42, 2)
df.insert(19, 'Charges.Daily', daily_charges)

# %%
df.head()

# %%
# Exporting the cleaned data to a new json file
df.to_json('data/Telco-Customer-Churn_cleaned.json')