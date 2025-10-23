from ipyleaflet import (
    Marker,
    DivIcon,
    Map,
    basemaps,
    leaflet,
    Popup,
    Choropleth,
    LayersControl,
    GeoJSON,
    GeoData,
    Popup,
    DivIcon,
    Marker,
    ScaleControl,
)
from collections import Counter
from shiny import App, reactive, ui, render
from shinywidgets import output_widget, render_widget
from ipywidgets import widgets
from shapely.geometry import shape
import pandas as pd
import shiny.experimental as x
import plotly.express as px
import plotly.graph_objects as go
from plotly_streaming import render_plotly_streaming
from pathlib import Path
from branca.colormap import linear
import json
import copy
import faicons
from shared import app_dir, tips, projects, projects_codes

with open("data/mw.json", "r") as f:
    districts_geojson = json.load(f)

category_colors = {
    "Serverless": 0,
    "Containers": 1,
    "Cloud Operations": 2,
    "Security & Identity": 3,
    "Dev Tools": 4,
    "Machine Learning & GenAI": 5,
    "Data": 6,
    "Networking & Content Delivery": 7,
    "Front-End Web & Mobile": 8,
    "Storage": 9,
    "Game Tech": 10,
}


def get_color_theme(theme, list_categories=None):

    if theme == "Custom":
        list_colors = [
            "#F6AA54",
            "#2A5D78",
            "#9FDEF1",
            "#B9E52F",
            "#E436BB",
            "#6197E2",
            "#863CFF",
            "#30CB71",
            "#ED90C7",
            "#DE3B00",
            "#25F1AA",
            "#C2C4E3",
            "#33AEB1",
            "#8B5011",
            "#A8577B",
        ]
    elif theme == "RdBu":
        list_colors = px.colors.sequential.RdBu.copy()
        del list_colors[5]  # Remove color position 5
    elif theme == "GnBu":
        list_colors = px.colors.sequential.GnBu
    elif theme == "RdPu":
        list_colors = px.colors.sequential.RdPu
    elif theme == "Oranges":
        list_colors = px.colors.sequential.Oranges
    elif theme == "Blues":
        list_colors = px.colors.sequential.Blues
    elif theme == "Reds":
        list_colors = px.colors.sequential.Reds
    elif theme == "Hot":
        list_colors = px.colors.sequential.Hot
    elif theme == "Jet":
        list_colors = px.colors.sequential.Jet
    elif theme == "Rainbow":
        list_colors = px.colors.sequential.Rainbow

    if list_categories is not None:
        final_list_colors = [
            list_colors[category_colors[category] % len(list_colors)]
            for category in list_categories
        ]
    else:
        final_list_colors = list_colors

    return final_list_colors


def get_color_template(mode):
    if mode == "light":
        return "plotly_white"
    else:
        return "plotly_dark"


def get_background_color_plotly(mode):
    if mode == "light":
        return "white"
    else:
        return "rgb(29, 32, 33)"


def get_map_theme(mode):
    print(mode)
    if mode == "light":
        return basemaps.CartoDB.Positron
    else:
        return basemaps.CartoDB.DarkMatter


def create_custom_icon(project_summary, ta_name, pillar_name):

    # size_circle = 60 + (count/2)
        # Define a color map for pillars
    pillar_colors = {
        "Agriculture": "#4CAF50",
        "Industrialization": "#E91E63",
        "Urbanisation": "#2196F3",
        "Private Sector": "#FF9800",
        "Human Capital Development": "#9C27B0",
        "Mindset Change": "#795548",
        "Enhanced Public Sector Performance": "#9FDEF1",
        "Economic Infrastructure": "#2A5D78",
        "Effective Governance Systems & Institutions": "#A8577B",
        "Environmental sustainability": "#C2C4E3",
    }

    color = pillar_colors.get(pillar_name, "#777")  # fallback color

    # Define the HTML code for the icon
    html_code = f""" <div 
        style="background: 
        transparent !important; 
        display: flex; 
        align-items: center; 
        justify-content: flex-start; 
        gap: 6px; 
        width: 25px; 
        height: 60px; "> 
            <!-- Small dot --> 
            <svg width="14" height="14" viewBox="0 0 10 10"> 
                <circle cx="5" cy="5" r="10" fill="{color}" stroke="#fff" stroke-width="1"/> 
            </svg> <!-- Country label --> 
            <span style="font-size: 10px; color: #000; font-weight: 300; width:50px;"> 
                {ta_name} : {project_summary}
            </span> 
    </div> """

    # Create a custom DivIcon {ta_name} : {project_summary}
    return DivIcon(
        icon_size=(50, 50), icon_anchor=(5, 30), html=html_code, class_name="dummy"
    )


pillars = [
    "1 - Agriculture",
    "2 - Industrialization",
    "3 - Urbanisation",
    "4 - Private sector",
    "5 - Human capital",
    "6 - Mindset Change",
    "7 - Public sector",
    "8 - Economic Infrastructure",
    "9 - Effective Governance systems and Institutions",
    "10 - Environmental sustainability",
]

agricodes = [
    "101 - Affordable Input Program (AIP)",
    "102 - AGCOM 2/MFSRP",
    "103 - AIYAP",
    "104 - Completion of Kameme EPA Office Block & Furniture",
    "105 - Construction of Kameme EPA Office Block",
    "106 - Construction of schemes",
    "107 - Construction of Thola-ilola irrigation scheme",
    "108 - Empowering vulnerable population through climate smart and agroecological practices and gender equality ",
    "109 - Fish Feed Meal",
    "110 - Greenbelt Initiative (GBI)",
    "111 - Implementation of River Diversion ",
    "112 - Installation of solar ",
    "113 - Kukolola Project",
    "114 - Lura Intake Weir Water Rehabilitation Project",
    "115 - Maintenance of existing irrigation schemes",
    "116 - National irrigation stratrgy",
    "117 - Nthola irrigation scheme",
    "118 - Programme for Rural Irrigation Development (PRIDE)",
    "119 - Scaling Up Climate-Adapted Agriculture in Malawi and Mozambique (MAMO II)",
    "120 - Sustainable Capture Fisheries and Aquaculture Development Project (SFAD)",
    "121 - The Agricultural Commercialization (AGCOM)",
    "122 - TRADE",
    "123 - Transform (Sustainable Food Systemes for Rural Agricultutre)",
    "124 - Transforming Agriculture Through Diversification and Entrepreneurship",
    "125 - Ulimi ndi Chilengedwe (UCHI)",
    "126 - Youth Economic Empowerment",
]

app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_spacer(),
        ui.nav_panel(
            "Map",
            ui.row(
                ui.layout_columns(
                    ui.output_ui("total_mapped"),
                    ui.output_ui("total_mapped_distinct"),
                    # ui.output_ui(int("total_voted_box") / int("total_registered_box")),
                    ui.output_ui("total_districts"),
                    ui.output_ui("total_tas"),
                    col_widths=(3, 3, 3, 3),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    x.ui.card(
                        output_widget("map_full"),
                        # id="card_map",
                    ),
                    x.ui.card(
                        ui.row(
                            x.ui.card(
                                ui.card_header("Pillars & Enablers - Key"),
                                ui.div(
                                    ui.output_ui("pillar_list"),
                                    class_="list-group",
                                    style="max-height: auto; overflow-y: auto; padding: 10px; style:none;",
                                ),
                            )
                        ),
                        ui.row(x.ui.card()),
                    ),
                    col_widths=(9, 3),
                ),
            ),
        ),
        ui.nav_panel(
            "Projects & Codes",
            ui.row(
                x.ui.card(
                    ui.card_header("Agriculture"),
                    ui.div(
                        ui.output_ui("agricode_list"),
                        style="max-height: auto; overflow-y: auto; padding: 10px; style:none;",
                    ),
                )
            ),
        ),
        title=ui.div(
            ui.img(
                src="images/logo.png", style="max-height: 40px; vertical-align: middle;"
            ),
            ui.span(
                "National Planning Commission - Projects Mapping",
                style="font-size: 22px; font-weight: 600; margin-left: 8px; vertical-align: middle;",
            ),
            style="display: flex; align-items: center;",
        ),
        id="page",
        sidebar=ui.sidebar(
            ui.div(ui.input_switch("switch", "Labels (On/Off)", False)),
            ui.div(
                ui.input_checkbox_group(
                    "Pillar",
                    "Pillar",
                    sorted(projects["Pillar"].unique().tolist()),
                    selected=projects["Pillar"].unique().tolist(),
                    inline=False,
                ),
                ui.input_action_button(
                    "select_all_pillars", "Select All", class_="btn-sm me-1"
                ),
                ui.input_action_button(
                    "clear_all_pillars", "Clear All", class_="btn-sm"
                ),
                style="max-height: 150px; overflow-y: auto; font-size: 12px;",
            ),
            ui.div(
                ui.input_checkbox_group(
                    "Project_name",
                    "Project Name",
                    sorted(projects["Project_name"].unique().tolist()),
                    selected=(projects["Project_name"].unique().tolist()),
                    inline=False,
                ),
                ui.input_action_button(
                    "select_all_projects", "Select All", class_="btn-sm me-1"
                ),
                ui.input_action_button(
                    "clear_all_projects", "Clear All", class_="btn-sm"
                ),
                style="max-height: 150px; overflow-y: auto; font-size: 12px;",
            ),
            ui.div(
                ui.input_checkbox_group(
                    "DISTRICT_x",
                    "District",
                    sorted(projects["DISTRICT_x"].unique().tolist()),
                    selected=(projects["DISTRICT_x"].unique().tolist()),
                    inline=False,
                ),
                ui.input_action_button(
                    "select_all_districts", "Select All", class_="btn-sm me-1"
                ),
                ui.input_action_button(
                    "clear_all_districts", "Clear All", class_="btn-sm"
                ),
                style="max-height: 150px; overflow-y: auto; font-size: 12px;",
            ),
            ui.div(
                ui.input_checkbox_group(
                    "TA_x",
                    "TA",
                    sorted(projects["TA_x"].unique().tolist()),
                    selected=(projects["TA_x"].unique().tolist()),
                    inline=False,
                ),
                ui.input_action_button(
                    "select_all_tas", "Select All", class_="btn-sm me-1"
                ),
                ui.input_action_button("clear_all_tas", "Clear All", class_="btn-sm"),
                style="max-height: 150px; overflow-y: auto; font-size: 12px;",
            ),
            ui.input_action_button("reset_filters", "Reset filters"),
            ui.input_dark_mode(id="dark_mode", mode="light"),
            open="closed",
            # style="width: 100%; --bs-accent: #FD9902; color: #FD9902; height: 8px;",
        ),
        footer=ui.h6(
            ui.row(
                "www.npc.mw © 2025",
                style="color: white !important; text-align: center;",
            )
        ),
        window_title="National Planning Commission - Projects Mapping",
        # --- Inject custom CSS ---
    ),
    ui.tags.style(
        """
        .navbar-nav {
            margin-left: auto !important;
        }
        .navbar {
            background-color: #FD9902 !important;
        }
        .navbar-nav .nav-link:hover {
            color: black !important;
        }
        .leaflet-popup-content {
            width: 600px !important;
        }
        .leaflet-div-icon {
            background: transparent !important;
            border: transparent !important;
        }
        .collapse-toggle {
            color: #FD9902 !important;
        }
        .main {
            /* Background image */
            background-image: url("images/background_dark.png");
            height: 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
        div#map_full.html-fill-container {
            height: -webkit-fill-available !important;
            min-height: 850px !important;
            max-height: 2000px !important;
        }
        div#main_panel.html-fill-container {
            height: -webkit-fill-available !important;
        }
        .input_checkbox_group:checked{
            color: #000;
            accent-color: FD9902;
        }
        .nav_panel {
                margin-right: 800px;
                background: #FD9902;
        }
        """
    ),
    icon="images/favicon.ico",
)


def server(input, output, session):
    ##################### Start of selecting all checkboxes
    @reactive.effect
    @reactive.event(input.select_all_pillars)
    def _():
        ui.update_checkbox_group(
            "Pillar",
            choices=sorted(projects["Pillar"].unique().tolist()),
            selected=sorted(projects["Pillar"].unique().tolist()),
        )

    @reactive.effect
    @reactive.event(input.select_all_projects)
    def _():
        ui.update_checkbox_group(
            "Project_name",
            choices=sorted(projects["Project_name"].unique().tolist()),
            selected=sorted(projects["Project_name"].unique().tolist()),
        )

    @reactive.effect
    @reactive.event(input.select_all_districts)
    def _():
        ui.update_checkbox_group(
            "DISTRICT_x",
            choices=sorted(projects["DISTRICT_x"].unique().tolist()),
            selected=sorted(projects["DISTRICT_x"].unique().tolist()),
        )

    @reactive.effect
    @reactive.event(input.select_all_tas)
    def _():
        ui.update_checkbox_group(
            "TA_x",
            choices=sorted(projects["TA_x"].unique().tolist()),
            selected=sorted(projects["TA_x"].unique().tolist()),
        )

    ######################## End of selecting all filters
    ######################## start of Clearing Filters
    @reactive.effect
    @reactive.event(input.clear_all_pillars)
    def _():
        ui.update_checkbox_group("Pillar", selected=[])

    @reactive.effect
    @reactive.event(input.clear_all_projects)
    def _():
        ui.update_checkbox_group("Project_name", selected=[])

    @reactive.effect
    @reactive.event(input.clear_all_districts)
    def _():
        ui.update_checkbox_group("DISTRICT_x", selected=[])

    @reactive.effect
    @reactive.event(input.clear_all_tas)
    def _():
        ui.update_checkbox_group("TA_x", selected=[])

    ######################## End of clearing filters
    # Your existing filtered data calculation
    @reactive.calc
    def tips_data():
        idx2 = projects.Pillar.isin(input.Pillar())
        idx1 = projects.Project_name.isin(input.Project_name())
        idx3 = projects.DISTRICT_x.isin(input.DISTRICT_x())
        idx4 = projects.TA_x.isin(input.TA_x())
        return projects[idx1 & idx2 & idx3 & idx4]

    ####################### PROJECTS MAPPED FOR EACH PROJECT CODE ##############
    @output
    @render.ui
    def agricode_list():
        d = tips_data()

        # Handle no data
        if d.empty:
            return ui.div(
                "No data available for current filters", class_="alert alert-info"
            )

        # Detect correct column names dynamically
        code_col = next(
            (c for c in d.columns if c.strip().lower() == "project_code".lower()), None
        )
        name_col = next(
            (c for c in d.columns if c.strip().lower() == "project_name".lower()), None
        )
        dist_col = next(
            (c for c in d.columns if c.strip().lower() == "district_x".lower()), None
        )
        ta_col = next(
            (c for c in d.columns if c.strip().lower() == "ta_x".lower()), None
        )

        if not all([code_col, name_col, dist_col, ta_col]):
            return ui.div(
                "Required columns ('Project_Code', 'Project_Name', 'DISTRICT_x', 'TA_x') not found.",
                class_="alert alert-warning",
            )

        # Map project codes using provided dictionary
        mapped_names = d[code_col].map(projects_codes).fillna(d[name_col])

        # Prepare grouped summary
        df = d[[code_col, name_col, dist_col, ta_col]].copy()
        df["Mapped_Name"] = mapped_names

        grouped = (
            df.groupby([code_col, "Mapped_Name"])
            .agg(
                Districts=(dist_col, lambda x: len(set(x.dropna()))),
                TAs=(ta_col, lambda x: len(set(x.dropna()))),
            )
            .reset_index()
            .sort_values(by="Districts", ascending=False)
        )

        # Build styled list items
        items = []
        for _, row in grouped.iterrows():
            district_badge = ui.tags.span(
                f"{row['Districts']} District{'s' if row['Districts'] != 1 else ''}",
                class_="badge bg-primary ms-2",
            )
            ta_badge = ui.tags.span(
                f"{row['TAs']} TA{'s' if row['TAs'] != 1 else ''}",
                class_="badge bg-success ms-2",
            )
            items.append(
                ui.tags.li(
                    ui.tags.b(
                        f"{str(row[code_col]).lstrip(
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                        )} – {row['Mapped_Name']} "
                    ),
                    district_badge,
                    ta_badge,
                    class_="list-group-item d-flex justify-content-left align-items-center",
                )
            )

        return ui.tags.ul(*items, class_="list-group")

    @output
    @render.ui
    def pillar_list():
        pillar_colors = {
            "Agriculture": "#4CAF50",
            "Industrialization": "#E91E63",
            "Urbanisation": "#2196F3",
            "Private Sector": "#FF9800",
            "Human Capital Development": "#9C27B0",
            "Mindset Change": "#795548",
            "Enhanced Public Sector Performance": "#9FDEF1",
            "Economic Infrastructure": "#2A5D78",
            "Effective Governance Systems & Institutions": "#A8577B",
            "Environmental sustainability": "#C2C4E3",
        }
        d = tips_data()

        if d.empty:
            return ui.div(
                "No project codes available for current filters",
                class_="alert alert-info",
            )

        # Extract Pillar code from second character of Project_Code
        d = d.copy()  # avoid SettingWithCopyWarning
        d["Pillar_Code"] = d["Project_Code"].str[1]  # second character

        # Count occurrences of each Pillar along with its code
        counts = Counter(zip(d["Pillar"], d["Pillar_Code"]))

        # Sort by frequency descending
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        items = [
            ui.tags.li(
                # Show colored dot + code - name
                f"{pillar} ({code})",
                # Badge with count
                ui.tags.span(f"x{count}", class_="badge ms-2", 
                             style=f"background:{pillar_colors.get(pillar,'#777')};"),
                class_="list-group-item d-flex justify-content-between align-items-center",
            )
            for (pillar, code), count in sorted_counts
        ]

        return ui.tags.ul(*items, class_="list-group")

    # MAPPED PROJECTS BOXES
    @output
    @render.ui
    def total_mapped():
        d = tips_data()
        return ui.value_box(
            title="Projects Mapped",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.TA_x.count()):,}",
        )

    @output
    @render.ui
    def total_mapped_distinct():
        d = tips_data()
        return ui.value_box(
            title="Unique Projects",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.Project_name.nunique()):,}",
        )

    @output
    @render.ui
    def total_districts():
        d = tips_data()
        return ui.value_box(
            title="Districts",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.DISTRICT_x.nunique()):,}",
        )

    @output
    @render.ui
    def total_tas():
        d = tips_data()
        return ui.value_box(
            title="TA's",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.TA_x.nunique()):,}",
        )

    @output
    @render_widget
    def map_full():
        d = tips_data()  # your dataset

        # Create the map
        map = Map(
            basemap=basemaps.OpenStreetMap.Mapnik,
            center=(-13.254308, 34.301525),
            zoom=7.2,
            scroll_wheel_zoom=True,
        )

        #################################################
        with open("data/mw.json", "r") as f:
            districts_geojson = json.load(f)

        # Safe copy of geojson and filter districts
        geojson_fixed = copy.deepcopy(districts_geojson)
        district_names = d["DISTRICT_x"].str.strip().tolist()
        geojson_fixed["features"] = [
            f
            for f in geojson_fixed["features"]
            if f["properties"]["name"].strip() in district_names
        ]

        # Assign ID for Choropleth
        for f in geojson_fixed["features"]:
            f["id"] = f["properties"]["name"].strip()
        ##################################################

        # Only add markers if there's data
        if not d.empty:
            # Group by TA so each TA appears once
            ta_groups = d.groupby("TA_x")

            with ui.Progress(min=0, max=len(ta_groups)) as progress:
                progress.set(
                    message="Calculation in progress", detail="This may take a while..."
                )

                for index, (ta_name, group) in enumerate(ta_groups):
                    # Use first record's coordinates for the TA
                    base_lat = float(group["latitude"].iloc[0])
                    base_lon = float(group["longitude"].iloc[0])

                    # Combine project names
                    projects_list = group["Project_Code"].unique().tolist()
                    project_numbers = [
                        str(p).lstrip(
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                        )
                        for p in projects_list
                    ]
                    project_summary = ", ".join(project_numbers)

                    pillar_name = group["Pillar"].mode().iloc[0] if "Pillar" in group else "Unknown"

                    # Create a custom icon showing project count or TA name
                    if input.switch():
                        custom_icon = create_custom_icon(project_summary, ta_name, pillar_name)
                    else:
                        custom_icon = create_custom_icon("", "", pillar_name)

                    # Create the marker
                    marker = Marker(
                        location=(base_lat, base_lon),
                        icon=custom_icon,
                        draggable=False,
                    )
                    map.add_layer(marker)

                    progress.set(
                        index,
                        message=f"Added {ta_name} ({len(projects_list)} projects)",
                    )

                #####################################
                # Choropleth layer - only if there are districts
                if district_names:
                    choro = Choropleth(
                        geo_data=geojson_fixed,
                        choro_data={
                            str(k).strip(): 1 for k in d["DISTRICT_x"] if pd.notna(k)
                        },
                        key_on="id",
                        border_color="Red",
                        style={
                            "fillOpacity": 0,  # transparent fill
                            "color": "brown",  # border color
                            "weight": 4,
                            "opacity": 0.3,
                        },
                    )
                    map.add_layer(choro)

                #####################################
                # Add scale control
                map.add_control(ScaleControl(position="bottomleft"))
                progress.set(len(ta_groups), message="Rendering the map...")
        else:

            @render.ui
            def display_message():
                return ui.div(
                    "No data available for current filters",
                    class_="alert alert-warning",
                )

        return map


static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)
