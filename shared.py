from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
tips = pd.read_csv(app_dir / "tips.csv")

# EXCEL IMPORTS
xlsx_df = "2020-Fresh-Presidential-Election-Results-Per-station.xlsx";

# FUNCTION
def wrangle_luanar(path):
    df = pd.read_excel(path)
    df['District Name'] = df['District Name'].fillna(method='ffill')
    df['Constituency Name'] = df['Constituency Name'].fillna(method='ffill')
    df['Ward Name'] = df['Ward Name'].fillna(method='ffill')
    df['Centre Code'] = df['Centre Code'].fillna(method='ffill')
    df['Centre Name'] = df['Centre Name'].fillna(method='ffill')
    df['District Name'] = df['District Name'].replace('(Thekerani)', 'Thyolo')
    df['District Name'] = df['District Name'].replace('Chikhwawa', 'Chikwawa')
    df['Region'] = "";
    districts_regions = {'Mwanza': 'Southern', 'Ntcheu': 'Central', 'Neno': 'Southern', 'Nkhatabay': 'Northern', 'Chikwawa': 'Southern', 
                         'Nsanje': 'Southern', 'Nkhotakota': 'Central', 'Salima': 'Central', 'Mangochi': 'Southern', 'Machinga': 'Southern', 
                         'Dedza': 'Central', 'Karonga': 'Northern', 'Chitipa': 'Northern', 'Balaka': 'Southern', 'Zomba': 'Southern', 
                         'Mchinji': 'Central', 'Blantyre': 'Southern', 'Mzimba': 'Northern', 'Likoma': 'Northern', 'Rumphi': 'Northern', 
                         'Kasungu': 'Central', 'Mulanje': 'Southern', 'Thyolo': 'Southern', 'Chiradzulu': 'Southern', 'Lilongwe': 'Central', 
                         'Ntchisi': 'Central', 'Phalombe': 'Southern', 'Dowa': 'Central'}
    df['Region'] = df['District Name'].map(districts_regions)
    df = df.drop(columns='Unnamed: 2')
    df = df[df['Centre Code'] != 'Total']
    df['Number Of Registred Voters'] = df['Number Of Registred Voters'].mask(df.duplicated(subset='Centre Code', keep='first'), 0)

    return df

_1_2020_df_final = wrangle_luanar(app_dir / xlsx_df)
# District Summary
district_summary = pd.pivot_table(_1_2020_df_final, index=['District Name', 'Region'], values=['Number Of Registred Voters', 'Total Number Voted'], aggfunc='sum')
district_summary['Voter_Empathy'] = ((district_summary['Number Of Registred Voters'] - district_summary['Total Number Voted']) / district_summary['Number Of Registred Voters']) * 100
district_summary = district_summary.reset_index()
district_summary = district_summary.rename(columns={'District Name': 'District_Name', 'Number Of Registred Voters' : 'Number_Of_Registred_Voters', 'Total Number Voted': 'Total_Number_Voted'})
district_summary["District_Name"] = district_summary["District_Name"].astype(str)
district_summary["Voter_Empathy"] = pd.to_numeric(district_summary["Voter_Empathy"], errors="coerce")
district_summary = district_summary.sort_values(by='Voter_Empathy', ascending=False)

# Region Summary
region_summary = pd.pivot_table(_1_2020_df_final, index=['Region'], values=['Number Of Registred Voters', 'Total Number Voted'], aggfunc='sum')
region_summary['Voter_Empathy'] = ((region_summary['Number Of Registred Voters'] - region_summary['Total Number Voted']) / region_summary['Number Of Registred Voters']) * 100
region_summary = region_summary.reset_index()
region_summary = region_summary.rename(columns={'Number Of Registred Voters' : 'Number_Of_Registred_Voters', 'Total Number Voted': 'Total_Number_Voted'})
region_summary = region_summary.sort_values(by='Voter_Empathy', ascending=False)

# _1_2020_df_final.to_excel(export_path + "first_cleaned_all.xlsx", index=False)
# district_summary.to_excel(export_path + "summary.xlsx", index=True)