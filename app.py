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
)
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
from shared import app_dir, tips, district_summary, region_summary, projects

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
bill_rng = (
    min(district_summary.Voter_Empathy.round()),
    max(district_summary.Voter_Empathy.round()),
)


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


def create_custom_icon(count, country):

    # size_circle = 60 + (count/2)

    # Define the HTML code for the icon
    html_code = f"""
    <div style="background: transparent !important;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                gap: 6px;            
                width: 100px;
                height: 100px;">

    <!-- Small dot -->
    <svg width="12" height="12" viewBox="0 0 10 10">
                <circle cx="5" cy="5" r="4"
                        fill="rgb(241,158,56)" stroke="#fff" stroke-width="1"/>
    </svg>

    <!-- Country label -->
    <span style="font-size: 10px; color: #000; font-weight: 300;">
        {country}
        </br>
        {count}
    </span>
    </div>
    """

    # Create a custom DivIcon
    return DivIcon(
        icon_size=(50, 50), icon_anchor=(25, 25), html=html_code, class_name="dummy"
    )

app_ui = ui.page_fillable(
    ui.page_navbar(
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
                    # col_widths=(8, 4),
                ),
            ),
        ),
        title=ui.img(src="images/logo.png", style="max-width:100px;width:100%"),
        id="page",
        
        sidebar=ui.sidebar(
            ui.input_checkbox_group(
                "Pillar",
                "Pillar",
                sorted(projects["Pillar"].unique().tolist()),
                selected=(projects["Pillar"].unique().tolist()),
                inline=False,
            ),
            ui.input_checkbox_group(
                "Project_name",
                "Project Name",
                sorted(projects["Project_name"].unique().tolist()),
                selected=(projects["Project_name"].unique().tolist()),
                
                inline=False,
            ),
            # ui.input_checkbox_group(
            #     "Region",
            #     "Region",
            #     ["Southern", "Central", "Northern"],
            #     selected=["Southern", "Central", "Northern"],
            #     inline=False,
            # ),
            ui.input_checkbox_group(
                "DISTRICT_x",
                "District",
                sorted(projects["DISTRICT_x"].unique().tolist()),
                selected=(projects["DISTRICT_x"].unique().tolist()),
                inline=False,
            ),
            ui.input_checkbox_group(
                "TA",
                "TA",
                sorted(projects["TA"].unique().tolist()),
                selected=(projects["TA"].unique().tolist()),
                inline=False,
            ),
            ui.input_action_button("reset", "Reset filter"),
            ui.input_dark_mode(id="dark_mode", mode="light"),
            open="closed",
            # style="width: 100%; --bs-accent: #FD9902; color: #FD9902; height: 8px;",
        ),
        footer=ui.h6(
            ui.row(
                "www.francis.chidziwisano.github.io © 2024",
                style="color: white !important; text-align: center;",
            )
        ),
        window_title="Malawi 2020 General General Elections Turn Out",
    ),
    ui.tags.style(
        """
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
        """
    ),
    icon="images/favicon.ico",
)

def server(input, output, session):
    
    # @output
    @reactive.calc
    # @render.ui
    def tips_data():
            # bill = input.Voter_Empathy()
            idx1 = projects.Project_name.isin(input.Project_name())
            idx2 = projects.Pillar.isin(input.Pillar())
            # idx2 = district_summary.Region.isin(input.Region())
            idx3= projects.DISTRICT_x.isin(input.DISTRICT_x())
            idx4 = projects.TA.isin(input.TA())
            return projects[idx1 & idx2 & idx3 & idx4]
    
# MAPPED PROJECTS BOXES
# total mapped projects
    @output
    @render.ui
    def total_mapped():
        d = tips_data()
        return ui.value_box(
            title="Projects Mapped",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.TA.count()):,}",
        )
    
# total mapped projects
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
        
# total districts
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
# total ta's
    @output
    @render.ui
    def total_tas():
        d = tips_data()
        return ui.value_box(
            title="TA's",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.TA.nunique()):,}",
        )

    @reactive.Calc
    @output
    @render_widget
    # @reactive.event(input.dark_mode)
    def map_full():
        d = tips_data()
        map = Map(
            basemap=get_map_theme(input.dark_mode()),
            center=(-13.254308, 34.301525),
            zoom=7,
            scroll_wheel_zoom=True,
        )

        with ui.Progress(min=0, max=len(d)) as progress:
            progress.set(
                message="Calculation in progress", detail="This may take a while..."
            )

            for index, row in d.iterrows():
                lat = float(row["Y_COORD"])
                lon = float(row["X_COORD"])
                country = row["TA"]
                count = row["Project_name"]

                # Add a marker with the custom icon to the map
                custom_icon = create_custom_icon(count, country)

                marker = Marker(
                    location=(lat, lon),
                    icon=custom_icon,
                    draggable=False
                )

                map.add_layer(marker)

                progress.set(index, message=f"Calculating country {country}")

            map.add_control(leaflet.ScaleControl(position="bottomleft"))

            progress.set(index, message="Rendering the map...")

        return map

static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)

# @reactive.effect
# @reactive.event(input.reset)
# def _():
#     ui.update_slider("Voter_Empathy", value=bill_rng)
#     ui.update_checkbox_group("Region", selected=["Southern", "Central", "Northern"])
#     ui.update_checkbox_group("District_Name", selected=(district_summary["District_Name"].unique().tolist()))
