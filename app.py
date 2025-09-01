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
from shared import app_dir, tips, district_summary, region_summary

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


def create_custom_icon(count):

    size_circle = 45 + (count / 10)

    # Define the HTML code for the icon
    html_code = f"""
    <div style=".leaflet-div-icon.background:transparent !important;
        position:relative; width: {size_circle}px; height: {size_circle}px;">
        <svg width="{size_circle}" height="{size_circle}" viewBox="0 0 42 42"
            class="donut" aria-labelledby="donut-title donut-desc" role="img">
            <circle class="donut-hole" cx="21" cy="21" r="15.91549430918954"
                fill="white" role="presentation"></circle>
            <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954"
                fill="transparent" stroke="color(display-p3 0.9451 0.6196 0.2196)"
                stroke-width="3" role="presentation"></circle>
            <text x="50%" y="60%" text-anchor="middle" font-size="13"
                font-weight="bold" fill="#000">{count}</text>
        </svg> Malawi
    </div>
    """

    # Create a custom DivIcon
    return DivIcon(
        icon_size=(50, 50), icon_anchor=(25, 25), html=html_code, class_name="dummy"
    )


def create_custom_popup(country, total, dark_mode, color_theme):

    # Group by 'region' and count occurrences of each region
    df = district_summary

    # Create a pie chart using plotly.graph_objects
    data = [
        go.Pie(
            labels="Region",
            values="Voter_Empathy",
            hole=0.3,
            textinfo="percent+label",
            marker=dict(colors=get_color_theme(color_theme, "Region")),
        )
    ]

    # Set title and template
    layout = go.Layout(
        title=f"{total} Community Builders in {country}",
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color_plotly(dark_mode),
        title_x=0.5,
        titlefont=dict(size=20),
        showlegend=False,
    )

    figure = go.Figure(data=data, layout=layout)
    figure.update_traces(
        textposition="outside", textinfo="percent+label", textfont=dict(size=15)
    )
    figure.layout.width = 600
    figure.layout.height = 400

    popup = Popup(child=go.FigureWidget(figure), max_width=600, max_height=400)

    return popup


app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_panel(
            "Dashboard",
            ui.row(
                ui.layout_columns(
                    ui.output_ui("total_registered_box"),
                    ui.output_ui("total_voted_box"),
                    # ui.output_ui(int("total_voted_box") / int("total_registered_box")),
                    ui.output_ui("turn_out_box"),
                    ui.output_ui("voter_empathy_box"),
                    col_widths=(3, 3, 3, 3),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    x.ui.card(
                        ui.row(
                            ui.layout_columns(
                                x.ui.card(output_widget("plot_0")),
                                x.ui.card(output_widget("plot_1")),
                                col_widths=(6, 6),
                            ),
                        ),
                        ui.row(
                            ui.layout_columns(
                                x.ui.card(output_widget("plot_3")),
                                col_widths=(12),
                            ),
                        ),
                    ),
                    x.ui.card(output_widget("plot_5")),
                    col_widths=(8, 4),
                ),
            ),
        ),
        ui.nav_panel(
            "Map",
            ui.row(
                ui.card(
                    output_widget("map_full"),
                    id="card_map",
                ),
            ),
        ),
        title=ui.img(src="images/logo.png", style="max-width:100px;width:100%"),
        id="page",
        sidebar=ui.sidebar(
            ui.input_slider(
                "Voter_Empathy",
                "Voter Turnout Rate",
                min=bill_rng[0],
                max=bill_rng[1],
                value=bill_rng,
                pre="",
            ),
            ui.input_checkbox_group(
                "Region",
                "Region",
                ["Southern", "Central", "Northern"],
                selected=["Southern", "Central", "Northern"],
                inline=False,
            ),
            ui.input_checkbox_group(
                "District_Name",
                "District",
                sorted(district_summary["District_Name"].unique().tolist()),
                selected=(district_summary["District_Name"].unique().tolist()),
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

    @reactive.calc
    def tips_data():
        bill = input.Voter_Empathy()
        idx1 = district_summary.Voter_Empathy.between(bill[0] - 1, bill[1] + 1)
        idx2 = district_summary.Region.isin(input.Region())
        idx3 = district_summary.District_Name.isin(input.District_Name())
        return district_summary[idx1 & idx2 & idx3]

    @output
    @render.ui
    def total_registered_box():
        d = tips_data()
        return ui.value_box(
            title="Total Registered Votes",
            showcase=faicons.icon_svg(
                "people-group", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.Number_Of_Registred_Voters.sum()):,}",
        )

    @output
    @render.ui
    def total_voted_box():
        d = tips_data()
        return ui.value_box(
            title="Total Voted",
            showcase=faicons.icon_svg(
                "user-check", width="50px", fill="#FD9902 !important"
            ),
            value=f"{int(d.Total_Number_Voted.sum()):,}",
        )

    @output
    @render.ui
    def turn_out_box():
        d = tips_data()
        total_registered = round(
            (d.Total_Number_Voted.sum() / d.Number_Of_Registred_Voters.sum()) * 100, 1
        )
        return ui.value_box(
            title="Turn Out Rate",
            showcase=faicons.icon_svg(
                "circle-check", width="50px", fill="#FD9902 !important"
            ),
            value=f"{total_registered} %",
        )

    @output
    @render.ui
    def voter_empathy_box():
        d = tips_data()
        voter_empathy = round(
            (
                (d.Number_Of_Registred_Voters.sum() - d.Total_Number_Voted.sum())
                / d.Number_Of_Registred_Voters.sum()
            )
            * 100,
            1,
        )
        return ui.value_box(
            title="Voter Empathy",
            showcase=faicons.icon_svg(
                "circle-xmark", width="50px", fill="#FD9902 !important"
            ),
            value=f"{voter_empathy} %",
        )

    @reactive.Calc
    @output
    @render_widget
    @reactive.event(input.dark_mode)
    def map_full():
        map = Map(
            basemap=get_map_theme(input.dark_mode()),
            center=(-13.254308, 34.301525),
            zoom=7,
            scroll_wheel_zoom=True,
        )

        with ui.Progress(min=0, max=len(district_summary)) as progress:
            progress.set(
                message="Calculation in progress", detail="This may take a while..."
            )

            for index, row in district_summary.iterrows():
                lat = float(row["Latitude"])
                lon = float(row["Longtude"])
                country = row["District_Name"]
                count = row["Voter_Empathy"]

                # Add a marker with the custom icon to the map
                custom_icon = create_custom_icon(count)

                # Create custom Pie chart with Community Builders from each country
                # custom_popup = create_custom_popup(
                #     country, count, input.dark_mode(), input.color_theme()
                # )

                marker = Marker(
                    location=(lat, lon),
                    icon=custom_icon,
                    draggable=False,
                    # popup=custom_popup,
                )

                map.add_layer(marker)

                progress.set(index, message=f"Calculating country {country}")

            map.add_control(leaflet.ScaleControl(position="bottomleft"))

            progress.set(index, message="Rendering the map...")

        return map

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_0():
        d = tips_data()
        fig1 = px.pie(
            d,
            names="Region",
            values="Voter_Cast",
            hole=0.5,
            # labels={"Region": "Region", "count": "Voter_Empathy"},
            title="Voter Turnout by Region",
            template=get_color_template(input.dark_mode()),
            color="Voter_Cast",
            color_discrete_sequence=px.colors.sequential.Oryel,
        )

        fig1.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig1.update_traces(
            textposition="outside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Voter Turnout: %{percent}<extra></extra>",
            textfont=dict(size=15),
        )
        fig1.update_layout(showlegend=False)

        return fig1

    @reactive.Calc
    @output
    @render_widget
    def plot_1():
        d = tips_data()
        # Create the bar plot
        fig3 = px.bar(
            region_summary,
            x="Region",
            y="Voter_Empathy",
            color="Voter_Empathy",
            # color_discrete_sequence = ["Oryel"],  # Or "Blues", "Plasma", etc.
            color_continuous_scale = "Oryel",
            # text="Voter_Turnout",
            # text_auto=True,
            # labels={
            #     "district": "Region",
            #     "count": "Voter_Turnout",
            #     "region": "Region",
            #     "location": "Latitude",
            # },
            title="Voter Turnout by Region",
            template=get_color_template(input.dark_mode()),
        )
        fig3.update_layout(
            xaxis=dict(
                tickfont=dict(size=14, color="black"),  # X-axis tick labels
                showgrid=False,  # Hide x-axis gridlines
            ),
            yaxis=dict(
                tickfont=dict(size=15, color="black"),  # Y-axis tick labels
                gridcolor="lightgray",  # Y-axis gridline color
                range=[5, 40],  # Set y-axis range
            ),
        )
        return fig3     

    @reactive.Calc
    @output
    @render_widget
    def plot_5():
        d = tips_data()  # Your reactive filtered dataframe

        fig5 = Map(center=(-13.254308, 34.301525), zoom=7)

        # Safe copy of geojson and filter districts
        geojson_fixed = copy.deepcopy(districts_geojson)
        district_names = d["District_Name"].str.strip().tolist()
        geojson_fixed["features"] = [
            f
            for f in geojson_fixed["features"]
            if f["properties"]["name"].strip() in district_names
        ]

        # Assign ID for Choropleth
        for f in geojson_fixed["features"]:
            f["id"] = f["properties"]["name"].strip()

        # Colormap
        values = list(d["Voter_Empathy"])
        colormap = linear.Oranges_04.scale(min(values), max(values))
        colormap.caption = "Voter Empathy (%)"

        # Choropleth layer
        choro = Choropleth(
            geo_data=geojson_fixed,
            choro_data={
                k.strip(): v for k, v in zip(d["District_Name"], d["Voter_Empathy"])
            },
            key_on="id",
            colormap=colormap,
            hover_style={"fillOpacity": 0.9, "color": "red"},
            border_color="black",
            style={"fillOpacity": 0.8, "dashArray": "5, 5"},
        )
        fig5.add_layer(choro)

        # Label marker holder
        label_marker = []

        # Hover callback
        def on_hover(event, feature, **kwargs):
            nonlocal label_marker
            if label_marker:
                fig5.remove_layer(label_marker[0])
                label_marker = []
            if event == "mouseover":
                geom = shape(feature["geometry"])
                centroid = geom.centroid
                name = feature["properties"]["name"].strip()
                voter_empathy = d.loc[
                    d["District_Name"].str.strip() == name, "Voter_Empathy"
                ].values[0]

                marker = Marker(
                    location=(centroid.y, centroid.x),
                    icon=DivIcon(
                        html=f"""
                            <div style="
                                display:inline-block;
                                text-align:center;
                                white-space:nowrap;
                                font-size:12pt;
                                color:black;
                                background:white;
                                padding:2px 6px;
                                border-radius:4px;
                                border:1px solid gray;
                            ">
                                <div>{name}</div>
                                <div style="font-size:12pt; color:darkgreen;">{round(voter_empathy)}%</div>
                            </div>
                            """
                    ),
                )
                fig5.add_layer(marker)
                label_marker = [marker]

        # Invisible GeoJSON layer for hover detection
        geo = GeoJSON(
            data=geojson_fixed,
            style={"color": "transparent", "fillOpacity": 0},
            hover_style={"fillOpacity": 0.1},
        )
        geo.on_hover(on_hover)
        fig5.add_layer(geo)

        # Controls
        fig5.add_control(LayersControl())
        fig5.add_control(colormap)

        return fig5

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_3():
        d = tips_data()
        # Create the bar plot
        fig3 = px.bar(
            d,
            x="District_Name",
            y="Voter_Empathy",
            color="Voter_Empathy",
            color_continuous_scale="Oryel",  # Or "Blues", "Plasma", etc.
            text="Voter_Empathy",
            text_auto=True,
            labels={
                "district": "District_Name",
                "count": "Voter_Empathy",
                "region": "Region",
                "location": "Latitude",
            },
            title="Voter Turnout by District",
            template=get_color_template(input.dark_mode()),
        )
        fig3.update_layout(
            xaxis=dict(
                tickfont=dict(size=14, color="black"),  # X-axis tick labels
                showgrid=False,  # Hide x-axis gridlines
            ),
            yaxis=dict(
                tickfont=dict(size=15, color="black"),  # Y-axis tick labels
                gridcolor="lightgray",  # Y-axis gridline color
                range=[10, 60],  # Set y-axis range
            ),
        )
        return fig3


static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)

# @reactive.effect
# @reactive.event(input.reset)
# def _():
#     ui.update_slider("Voter_Empathy", value=bill_rng)
#     ui.update_checkbox_group("Region", selected=["Southern", "Central", "Northern"])
#     ui.update_checkbox_group("District_Name", selected=(district_summary["District_Name"].unique().tolist()))
