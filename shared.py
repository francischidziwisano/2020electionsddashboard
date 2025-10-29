from pathlib import Path
import pyproj
import pandas as pd

app_dir = Path(__file__).parent
tips = pd.read_csv(app_dir / "tips.csv")

# # EXCEL IMPORTS
# xlsx_df = "data/2020-Fresh-Presidential-Election-Results-Per-station.xlsx";

# # FUNCTION
# def wrangle_luanar(path):
#     df = pd.read_excel(path)
#     df['District Name'] = df['District Name'].fillna(method='ffill')
#     df['Constituency Name'] = df['Constituency Name'].fillna(method='ffill')
#     df['Ward Name'] = df['Ward Name'].fillna(method='ffill')
#     df['Centre Code'] = df['Centre Code'].fillna(method='ffill')
#     df['Centre Name'] = df['Centre Name'].fillna(method='ffill')
#     df['District Name'] = df['District Name'].replace('(Thekerani)', 'Thyolo')
#     df['District Name'] = df['District Name'].replace('Chikhwawa', 'Chikwawa')
#     df['Region'] = "";

#     # Mapping Regions to districts
#     districts_regions = {'Mwanza': 'Southern', 'Ntcheu': 'Central', 'Neno': 'Southern', 'Nkhatabay': 'Northern', 'Chikwawa': 'Southern', 
#                          'Nsanje': 'Southern', 'Nkhotakota': 'Central', 'Salima': 'Central', 'Mangochi': 'Southern', 'Machinga': 'Southern', 
#                          'Dedza': 'Central', 'Karonga': 'Northern', 'Chitipa': 'Northern', 'Balaka': 'Southern', 'Zomba': 'Southern', 
#                          'Mchinji': 'Central', 'Blantyre': 'Southern', 'Mzimba': 'Northern', 'Likoma': 'Northern', 'Rumphi': 'Northern', 
#                          'Kasungu': 'Central', 'Mulanje': 'Southern', 'Thyolo': 'Southern', 'Chiradzulu': 'Southern', 'Lilongwe': 'Central', 
#                          'Ntchisi': 'Central', 'Phalombe': 'Southern', 'Dowa': 'Central'}
#     df['Region'] = df['District Name'].map(districts_regions)

#     df = df.drop(columns='Unnamed: 2')
#     df = df[df['Centre Code'] != 'Total']
#     df['Number Of Registred Voters'] = df['Number Of Registred Voters'].mask(df.duplicated(subset='Centre Code', keep='first'), 0)

#     return df

# _1_2020_df_final = wrangle_luanar(app_dir / xlsx_df)
# # District Summary
# district_summary = pd.pivot_table(_1_2020_df_final, index=['District Name', 'Region'], values=['Number Of Registred Voters', 'Total Number Voted'], aggfunc='sum')
# district_summary['Voter_Empathy'] = ((district_summary['Number Of Registred Voters'] - district_summary['Total Number Voted']) / district_summary['Number Of Registred Voters']) * 100
# district_summary['Voter_Cast'] = ((district_summary['Total Number Voted'])) * 100
# district_summary['Voter_Turnout'] = (((district_summary['Total Number Voted']) / district_summary['Number Of Registred Voters']) * 100)
# district_summary = district_summary.reset_index()
# district_summary = district_summary.rename(columns={'District Name': 'District_Name', 'Number Of Registred Voters' : 'Number_Of_Registred_Voters', 'Total Number Voted': 'Total_Number_Voted'})
# district_summary["District_Name"] = district_summary["District_Name"].astype(str)
# district_summary["Voter_Empathy"] = pd.to_numeric(district_summary["Voter_Empathy"], errors="coerce").round()
# district_summary["Voter_Turnout"] = pd.to_numeric(district_summary["Voter_Turnout"], errors="coerce").round()
# district_summary["Voter_Cast"] = pd.to_numeric(district_summary["Voter_Cast"], errors="coerce").round()
# district_summary = district_summary.sort_values(by='Voter_Empathy', ascending=False)
# district_summary['Longtude'] = "";
# district_summary['Latitude'] = "";

# # Mapping latitude to districts
# districts_longtudes = {'Blantyre': '35.0058', 'Lilongwe': '33.7833', 'Mzuzu': '34.0151', 'Zomba': '35.3192', 'Karonga': '33.9333', 
#                            'Kasungu': '33.4833', 'Mangochi': '35.2667', 'Salima': '34.4333', 'Likoma': '34.7333', 'Dedza': '34.3333', 
#                            'Nkhotakota': '34.3', 'Mchinji': '32.9', 'Nsanje': '35.2667', 'Mzimba': '33.6', 'Rumphi': '33.8667', 
#                            'Ntcheu': '34.6667', 'Mulanje': '35.5081', 'Mwanza': '34.5178', 'Chitipa': '33.27', 'Nkhatabay': '34.3', 
#                            'Ntchisi': '34', 'Dowa': '33.9167', 'Thyolo': '35.1333', 'Phalombe': '35.6533', 'Chiradzulu': '35.1833', 
#                            'Machinga': '35.5167', 'Balaka': '34.9591', 'Neno': '34.6534', 'Chikwawa': '34.801'}
# district_summary['Longtude'] = district_summary['District_Name'].map(districts_longtudes)

# # Mapping longtude to districts
# districts_latitudes = {
#         'Blantyre': '-15.7861', 'Lilongwe': '-13.9833', 'Mzuzu': '-11.4581', 'Zomba': '-15.3869', 'Karonga': '-9.9333', 'Kasungu': '-13.0333', 
#         'Mangochi': '-14.4667', 'Salima': '-13.7833', 'Likoma': '-12.0667', 'Dedza': '-14.3667', 'Nkhotakota': '-12.9167', 
#         'Mchinji': '-13.8167', 'Nsanje': '-16.9167', 'Mzimba': '-11.9', 'Rumphi': '-11.0167', 'Ntcheu': '-14.8333', 'Mulanje': '-16.0258', 
#         'Mwanza': '-15.5986', 'Chitipa': '-9.7019', 'Nkhatabay': '-11.6', 'Ntchisi': '-13.3667', 'Dowa': '-13.6667', 'Thyolo': '-16.0667', 
#         'Phalombe': '-15.8033', 'Chiradzulu': '-15.7', 'Machinga': '-14.9667', 'Balaka': '-14.9889', 'Neno': '-15.3981', 'Chikwawa': '-16.035'}
# district_summary['Latitude'] = district_summary['District_Name'].map(districts_latitudes)

# # Region Summary
# region_summary = pd.pivot_table(_1_2020_df_final, index=['Region'], values=['Number Of Registred Voters', 'Total Number Voted'], aggfunc='sum')
# region_summary['Voter_Empathy'] = ((region_summary['Number Of Registred Voters'] - region_summary['Total Number Voted']) / region_summary['Number Of Registred Voters']) * 100
# region_summary = region_summary.reset_index()
# region_summary = region_summary.rename(columns={'Number Of Registred Voters' : 'Number_Of_Registred_Voters', 'Total Number Voted': 'Total_Number_Voted'})
# region_summary = region_summary.sort_values(by='Voter_Empathy', ascending=False)

# Project Mapping
projects_path = "data/projects_mapping/projects.xlsx";
ta_coordinates = "data/projects_mapping/mwi_admin3_nso_points.xlsx";
utm36s = pyproj.CRS("EPSG:32736")  # UTM Zone 36S
wgs84 = pyproj.CRS("EPSG:4326")    # Lat/lon in decimal degrees
transformer = pyproj.Transformer.from_crs(utm36s, wgs84, always_xy=True)
projects_codes = {
                    'A101':  'Affordable Input Program (AIP)',
                    'A102':  'AGCOM 2/MFSRP',
                    'A103':  'AIYAP',
                    'A104':  'Completion of Kameme EPA Office Block & Furniture',
                    'A105':  'Construction of Kameme EPA Office Block',
                    'A106':  'Construction of schemes',
                    'A107':  'Construction of Thola-ilola irrigation scheme',
                    'A108':  'Empowering vulnerable population through climate smart and agroecological practices and gender equality ',
                    'A109':  'Fish Feed Meal',
                    'A110':  'Greenbelt Initiative (GBI)',
                    'A111':  'Implementation of River Diversion ',
                    'A112':  'Installation of solar ',
                    'A113':  'Kukolola Project',
                    'A114':  'Lura Intake Weir Water Rehabilitation Project',
                    'A115':  'Maintenance of existing irrigation schemes',
                    'A116':  'National Irrigation Strategy',
                    'A117':  'Nthola irrigation scheme',
                    'A118':  'Programme for Rural Irrigation Development (PRIDE)',
                    'A119':  'Scaling Up Climate-Adapted Agriculture in Malawi and Mozambique (MAMO II)',
                    'A120':  'Sustainable Capture Fisheries and Aquaculture Development Project (SFAD)',
                    'A121':  'The Agricultural Commercialization (AGCOM)',
                    'A122':  'TRADE',
                    'A123':  'Transform (Sustainable Food Systemes for Rural Agricultutre)',
                    'A124':  'Transforming Agriculture Through Diversification and Entrepreneurship',
                    'A125':  'Ulimi ndi Chilengedwe (UCHI)',
                    'A126':  'Youth Economic Empowerment',
                    'A116':  'Chemilamba Irrigation Scheme',
                    'A116':  'Khongono Irrigation Scheme ',
                    'A116':  'Maula Irrigation Scheme',
                    'A116':  'Mphuka Irrigation Scheme ',
                    'A116':  'Namadidi Irrigation Scheme',
                    'A116':  'Namalowa Irrigation Scheme',
                    'A116':  'Ndulu Irrigation Scheme',
                    'A116':  'Nkaya Irrigation Scheme',
                    'A127':  'AFIKEPO',
                    'A128':  'Akule ndi Thanzi',
                    'A129':  'CISP     ',
                    'A130':  'Kutukula Ulimi m\'Malawi',
                    'A131':  'Local Climate Adaptive Living (LoCAL)',
                    'A132':  'MEGAFARMS',
                    'A133':  'National Economic Empowerment Fund (NEEF)',
                    'A134':  'Sustainable Agriculture Productivity Programme (SAPP)',
                    'A135':  'AMIS',
                    'A136':  'Aswap SP2',
                    'A137':  'Center for Agriculture Transformation',
                    'A138':  'CLIMM',
                    'A139':  'DAESS',
                    'A140':  'DREAMS Project',
                    'A141':  'SATCP',
                    'A142':  'Space to Place (S2P)',
                    'A143':  'Post Cyclone Idai Recovery Emergency Project(PCIREP)',
                    'A144':  'Makhwira Community Livelihood Resilience and Strengthening Project(EAM)',
                    'A145':  'Shire Valley Transformation Project(SVTP)',
                    'A146':  'Mlimi Patsogolo – Catholic Relief Services (CRS)',
                    'A147':  'Food security (Nutrition )(WVI)',
                    'A148':  'Scalling micro drip irrigation in Chikwawa Norwegian Church Aid and Dan Church Aid Joint Country Program (NCA DCA)',
                    'A149':  'Promoting Sustainable Partinerships for Empowered  Resilience',
                    'A150':  'Agriculture Improvements  for climate resilience (BICC CODES)',
                    'A151':  'coordination and support to implement integrated watershed management(Evangelical Lutheren Development Services)',
                    'A152':  'Irrigation Agriculture for Rural Food and Economic Empowerment',
                    'A153':  'Integrated Resilience Building Project',
                    'A154':  'Improvement of Malawi’s Farm Input Subsidy Program (FISP)',
                    'A155':  'Farm Mechanisation ',
                    'A156':  'Governance to Enable Service Delivery (GESD)',
                    'A157':  'Integrated Resilience Program- Cyclone Freddy',
                    'A158':  'Input Loan Program – One Acre Fund',
                    'A159':  'Sustainable Aquatic Foods',
                    'A160':  'ORT',
                    'A161':  'M-CLIMES',
                    'A162':  'Aquaculture Value Chain Project. (AVCP)',
                    'A163':  'RAYS OF HOPE ',
                    'A164':  'Foundation for Farming',
                    'A165':  'Resilience and food security project',
                    'A166':  'Promotion of exposure visits',
                    'A167':  'Conduct market linkage',
                    'A168':  'Establishment of cooperatives',
                    'A169':  'Establishment of farmers field school ',
                    'A170':  'Establisment of fish ponds',
                    'A171':  'Evangelical Lutheran Development Service',
                    'A172':  'Facilitate distribution of drought tolerant crops and defined seed.',
                    'A173':  'Facilitate Agriculture fair day',
                    'A174':  'Procurement of cereal  and drought crops to the farmers',
                    'A175':  'Provision of capacity building  ',
                    'A176':  'Supporting farmers with processing machine',
                    'A177':  'EWAYA                                      ',
                    'A178':  'Malawi Watershed Improvement Services Project (MWASIP)',
                    'A179':  'Transforming Livelihoods and Landscapes Project ',
                    'A180':  'Tractor Hire Scheme',
                    'A181':  'YEFFA',
                    'A182':  'SAMALA',
                    'A183':  'Livehood and Reselience ',
                    'A184':  'Climate Reselience and  sustainable livelihoods',
                    'M601':  'Enhance Social Accountability in Local  Governance to Reduce Inequalities for  an Inclusive Malawi Project (Fighting Inequalities Project)',
                    'M602':  'Enhancing effective protection and promotion of rights of women and girls from Gender Based Violence through Improved Justice Delivery, Self-advocacy and Self-activism.',
                    'M603':  'Mindset Change Government of Malawi',
                    'M604':  'National Youth Service Program',
                    'M605':  'SPIRITUAL EVANGELIZATION',
                    'M606':  'Transform Conflict & Resettle Internally Displaced People (IDP)',
                    'M607':  'Womens Voice Against Poverty & Inequality in the Extractive Sector in Karonga District',
}

def project_mapping(path1, path2):
    
    # cleaning projects
    projects_df = pd.read_excel(path1)
    projects_df["TA"] = projects_df["TA"].str.title()
    projects_df["TA"] = projects_df["TA"].str.strip()
    projects_df["DISTRICT"] = projects_df["DISTRICT"].str.title()
    # projects_df["Project_Code"] = projects_df["Project_Code"].str.replace(r"^A\s+", "", regex=True)
    projects_df["DISTRICT"] = projects_df["DISTRICT"].str.strip()
    projects_df["KEY"] = projects_df["DISTRICT"] + "_" + projects_df["TA"]

    # cleaning coordinates
    coordinates_df = pd.read_excel(path2)
    coordinates_df["TA"] = coordinates_df["TA"].str.replace(r"^TA\s+", "", regex=True)
    coordinates_df["TA"] = coordinates_df["TA"].str.replace(r"^T/A\s+", "", regex=True)
    coordinates_df["TA"] = coordinates_df["TA"].str.replace(r"^STA\s+", "", regex=True)
    coordinates_df["TA"] = coordinates_df["TA"].str.replace(r"^ST/A\s+", "", regex=True)
    coordinates_df["TA"] = coordinates_df["TA"].str.title().str.strip()
    coordinates_df["DISTRICT"] = coordinates_df["DISTRICT"].str.title().str.strip()
    coordinates_df["KEY"] = coordinates_df["DISTRICT"] + "_" + coordinates_df["TA"]
    coordinates_df["latitude"] = round((coordinates_df["latitude"].astype(float)), 5)
    coordinates_df["longitude"] = round((coordinates_df["longitude"].astype(float)), 5)
    # coordinates_df["longitude"], coordinates_df["latitude"] = transformer.transform(coordinates_df["longitude"], coordinates_df["latitude"])

    registered_voted = pd.merge(projects_df, coordinates_df, on="KEY", how="left")
    registered_voted = registered_voted.dropna()
    registered_voted.to_excel("data/projects_mapping/merged.xlsx")
    return registered_voted

projects = project_mapping(app_dir / projects_path, app_dir / ta_coordinates)
# projects_summary = pd.pivot_table(projects, index=['DISTRICT_x'], values=['Project_name'], aggfunc='count')


# Pivot table: districts as rows, project names as columns
projects_summary = pd.pivot_table(
    projects,
    index='DISTRICT_x',
    columns='Pillar',
    aggfunc='size',   # counts occurrences
    fill_value=0      # replace NaN with 0
)

# Ensure all column names are strings
projects_summary.columns = projects_summary.columns.astype(str)
projects_summary['Total'] = projects_summary.sum(axis=1)
projects_summary['Overall'] = ((projects_summary['Total'] / projects_summary['Total'].sum())*100).round()
# Compute row totals
projects_summary['Agriculture_pct'] = ((projects_summary['Agriculture'] / projects_summary['Agriculture'].sum())*100).round()
projects_summary['Industrialization_pct'] = ((projects_summary['Industrialization'] / projects_summary['Industrialization'].sum())*100).round()
projects_summary['Urbanisation_pct'] = ((projects_summary['Urbanisation'] / projects_summary['Urbanisation'].sum())*100).round()
projects_summary['Mindset_Change_pct'] = ((projects_summary['Mindset Change'] / projects_summary['Mindset Change'].sum())*100).round()
projects_summary['Effective_Governance_Systems_Institutions_pct'] = ((projects_summary['Effective Governance Systems & Institutions'] / projects_summary['Effective Governance Systems & Institutions'].sum())*100).round()
projects_summary['Private_Sector_pct'] = ((projects_summary['Private Sector'] / projects_summary['Private Sector'].sum())*100).round()
projects_summary['Enhanced_Public_Sector_Performance_pct'] = ((projects_summary['Enhanced Public Sector Performance'] / projects_summary['Enhanced Public Sector Performance'].sum())*100).round()
projects_summary['Human_Capital_Development_pct'] = ((projects_summary['Human Capital Development'] / projects_summary['Human Capital Development'].sum())*100).round()
projects_summary['Economic_Infrastructure_pct'] = ((projects_summary['Economic Infrastructure'] / projects_summary['Economic Infrastructure'].sum())*100).round()
projects_summary['Environmental_Sustainability_pct'] = ((projects_summary['Environmental Sustainability'] / projects_summary['Environmental Sustainability'].sum())*100).round()

summary_mask = ["Agriculture_pct",  
                "Industrialization_pct", 
                "Urbanisation_pct",
                "Mindset_Change_pct",
                "Effective_Governance_Systems_Institutions_pct", 
                "Private_Sector_pct",
                "Enhanced_Public_Sector_Performance_pct", 
                "Human_Capital_Development_pct",
                "Economic_Infrastructure_pct",
                "Environmental_Sustainability_pct",
                "Total", 
                "Overall"]

projects_summary = projects_summary[summary_mask]
projects_summary = projects_summary.rename(columns={"DISTRICT_x": "District",
                                                    "Agriculture_pct": "01",  
                                                    "Industrialization_pct": "02", 
                                                    "Urbanisation_pct": "03",
                                                    "Mindset_Change_pct": "04",
                                                    "Effective_Governance_Systems_Institutions_pct": "05", 
                                                    "Private_Sector_pct": "06",
                                                    "Enhanced_Public_Sector_Performance_pct": "07", 
                                                    "Human_Capital_Development_pct": "08",
                                                    "Economic_Infrastructure_pct": "09",
                                                    "Environmental_Sustainability_pct": "10"})

# Remove column name grouping
projects_summary.columns.name = None
projects_summary = projects_summary.reset_index()
projects_summary.to_excel("data/projects_mapping/projects_summary.xlsx")

projects.head()
