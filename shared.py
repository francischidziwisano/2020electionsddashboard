from pathlib import Path
import pyproj
import pandas as pd

app_dir = Path(__file__).parent
file_id = "1x_mQDMQ_e0DFRqpelmVpAI65VkE6qUjD"
url = f"https://drive.google.com/uc?id={file_id}"
# Project Mapping
projects_path = url;

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

projects = project_mapping(projects_path, app_dir / ta_coordinates)
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
