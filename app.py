import faicons as fa
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import json
import pandas as pd
from pathlib import Path
import geopandas as gpd
import contextily as cx

# Load data and compute static values
from shared import app_dir, tips, district_summary, region_summary
from shinywidgets import render_plotly, render_widget

from shiny import App, reactive, render
from shiny.express import input, ui, render
import json

from pathlib import Path

dir = Path(__file__).resolve().parent
# Step 1: Load Malawi GeoJSON as GeoDataFrame
with open("mw.json", "r") as f:
    districts_geojson = json.load(f)
# district_summary = district_summary.reset_index()

bill_rng = (
    min(district_summary.Voter_Empathy.round()),
    max(district_summary.Voter_Empathy.round()),
)
ui.tags.style("""
        .card_value {
            font-size: 30px;
            font-weight: bold;
        }
        .card_title {
            font-weight: bold      
        }
        .header{
              text-align:left; 
              font-weight: bold; 
              font-size: 40px;
              padding-left: 20px;
              }
        #map {
            height: 100vh;
            width: 100%;
        }
    """),

# Add page title and sidebar

ui.page_opts(
        title=ui.div(
            "Malawi 2020 Elections Dashboard",
            style="text-align: center; margin-right: 10px; font-size: 40px; font-weight: bold;"
        ),
        fillable=True
)

with ui.sidebar(open="desktop"):
    with ui.card():
        ui.input_slider(
            "Voter_Empathy",
            "Voter Turnout Rate",
            min=bill_rng[0],
            max=bill_rng[1],
            value=bill_rng,
            pre="",
        )
    with ui.card():
        ui.input_checkbox_group(
            "Region",
            "Region",
            ["Southern", "Central", "Northern"],
            selected=["Southern", "Central", "Northern"],
            inline=False,
        )
    with ui.card(style="height: 550px"):
        ui.input_checkbox_group(
            "District_Name",
            "District", sorted(district_summary["District_Name"].unique().tolist()),
            selected=(district_summary["District_Name"].unique().tolist()),
            inline=False,
        )
    with ui.card(): 
        ui.input_action_button("reset", "Reset filter")

# Add main content
ICONS = {
    "registered": fa.icon_svg("people-group", "solid"),
    "voted": fa.icon_svg("user-check", "solid"),
    "wallet": fa.icon_svg("person-circle-check"),
    "currency-dollar": fa.icon_svg("person-circle-xmark"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=ICONS["registered"]):
        ui.tags.span("Total Registered Voters", class_= "card_title")

        @render.express
        def total_tippers():
            d = tips_data()
            # tips_data().shape[0]
            ui.tags.span(f"{int(d.Number_Of_Registred_Voters.sum()):,}", class_="card_value")

    with ui.value_box(showcase=ICONS["voted"]):
        ui.tags.span("Total Casted Votes", class_= "card_title")

        @render.express
        def total_voters():
            d = tips_data()
            ui.tags.span(f"{int(d.Total_Number_Voted.sum()):,}", class_="card_value")

    with ui.value_box(showcase=ICONS["wallet"]):
        ui.tags.span("Voter Turnout Rate", class_= "card_title")

        @render.express
        def average_tip():
            d = tips_data()
            perc = d.Total_Number_Voted.sum() / d.Number_Of_Registred_Voters.sum()
            ui.tags.span(f"{perc:.1%}", class_="card_value")

    with ui.value_box(showcase=ICONS["currency-dollar"]):
        ui.tags.span("Voter Empathy", class_= "card_title")

        @render.express
        def average_bill():
            d = tips_data()
            bill = (
                d.Number_Of_Registred_Voters.sum() - d.Total_Number_Voted.sum()
            ) / d.Number_Of_Registred_Voters.sum()
            ui.tags.span(f"{bill:.1%}", class_="card_value")  # ✔ just write the tag


with ui.layout_columns(col_widths=[9, 3]):
    with ui.card():
        with ui.div():
            with ui.layout_columns(col_widths=[6, 6]):
                with ui.card(style="height: 100%; min-height: 400px;"):  # Set minimum height
                    with ui.card_header(
                        class_="d-flex justify-content-between align-items-center",
                        style="font-weight: bold; font-size: 1.25rem; padding: 1rem;"
                    ):
                        "Voter Empathy by Region"
                    
                    @render_plotly
                    def regbar():
                        d = tips_data()
                        
                        fig = px.pie(
                            d,
                            names="Region",
                            values="Voter_Empathy",
                            color="Region",
                            color_discrete_sequence=px.colors.sequential.RdBu,
                            hole=0.3,
                        )
                        
                        # Mobile-responsive settings
                        fig.update_traces(
                            textinfo="percent+label",
                            textposition="inside",
                            textfont_size=14,
                            marker=dict(line=dict(color='white', width=1)),
                            insidetextorientation='horizontal',  # Better for small screens
                        )
                        
                        fig.update_layout(
                            autosize=True,
                            margin=dict(l=10, r=10, t=30, b=10),  # Tighter margins
                            uniformtext_minsize=10,  # Smaller minimum text size
                            uniformtext_mode='hide',  # Hide text if too small
                            legend=dict(
                                orientation="h",  # Horizontal legend for mobile
                                yanchor="bottom",
                                y=-0.2,  # Position below chart
                                xanchor="center",
                                x=0.5
                            ),
                            height=400,  # Fixed height helps with mobile rendering
                        )
                        
                        # Mobile-specific adjustments
                        @reactive.Effect
                        def _():
                            if input.device_is_mobile():
                                fig.update_layout(
                                    margin=dict(l=5, r=5, t=20, b=5),
                                    uniformtext_minsize=8,
                                    height=300,
                                )
                        
                        return fig
                    
                with ui.card():
                    with ui.card_header(
                        class_="d-flex justify-content-between align-items-center",
                        style = "font-weight: bold; font-size: 20px"
                    ):
                        "Voter Empathy Distribution | By Region"
                    # regs = region_summary

                    @render_widget
                    def regscatter():
                        # Optional: refresh data
                        dscatter = tips_data()  # Remove this line if unnecessary
                        dscatter["Turnout_Rate"] = (dscatter["Total_Number_Voted"] / dscatter["Number_Of_Registred_Voters"]) * 100

                        # Create scatter plot

                        fig = px.box(dscatter,
                                    x="Region",
                                    y="Voter_Empathy",
                                    color="Region",
                                    points="all",  # Show all points
                                    hover_data=["District_Name", "Turnout_Rate"],  # Extra hover info
                                    labels={"Voter_Empathy": "Empathy Score", "Region": ""}
                                )

                                # Add stripplot overlay for better point visibility
                        fig.update_traces(
                                    # jitter=0.3,  # Spread points horizontally
                                    # marker=dict(size=8, opacity=0.7, line=dict(width=1, color="DarkSlateGrey")),
                                    selector=dict(type="box")
                                )

                                # Customize layout
                        fig.update_layout(
                                    plot_bgcolor="white",
                                    showlegend=False,  # Hide legend if redundant
                                    xaxis=dict(
                                        title_font=dict(size=18, family="Arial", color="black"),
                                        tickfont=dict(size=20)
                                    ),
                                    yaxis=dict(
                                        title_font=dict(size=18, family="Arial", color="black"),
                                        tickfont=dict(size=20),
                                        range=[15, 60], gridcolor="lightgrey"
                                    ),
                                    autosize=True
                                )

                        # fig = px.box(
                        #     dscatter, 
                        #     x="Region", 
                        #     y="Voter_Empathy", 
                        #     color="Region",
                        #     points="all",
                        #     title="Empathy Score Distribution by Region"
                        # )

                        # fig = px.scatter(dscatter, x="Number_Of_Registred_Voters", y="Total_Number_Voted", 
                        # color="Region", hover_name="District_Name",
                        # title="Registered vs Total Voted")

                        # fig = px.treemap(dscatter, path=["Region", "District_Name"], values="Total_Number_Voted",
                        # color="Voter_Empathy", color_continuous_scale="Reds",
                        # title="Voter Turnout and Empathy by Region and District")

                        return fig    

            with ui.card():
                with ui.card_header(
                    class_="d-flex justify-content-between align-items-center",
                    style = "font-weight: bold; font-size: 20px"
                ):
                    "Voter Empathy | By District"

                @render_widget
                def bar(style="display: flex; flex-direction: row; flex-wrap: wrap; gap: 10px; width: 100%;"):
                    d = tips_data()

                    fig = px.bar(
                        d,
                        x="District_Name",
                        y="Voter_Empathy",
                        text="Voter_Empathy",
                        labels={"Voter_Empathy": "Voter Empathy (%)"},
                        color="Voter_Empathy",  # Use empathy as the color scale
                        color_continuous_scale="Reds",  # Or "Blues", "Plasma", etc.
                    )
                    fig.update_layout(
                        xaxis=dict(
                            tickfont=dict(size=14, color="black"),                       # X-axis tick labels
                            showgrid=False                                              # Hide x-axis gridlines
                    ),
                        yaxis=dict(
                            tickfont=dict(size=15, color="black"),                       # Y-axis tick labels
                            gridcolor="lightgray",                                      # Y-axis gridline color
                            range=[10, 60]                                              # Set y-axis range
                    ),
                    # plot_bgcolor="white"  # Background color
                    margin=dict(l=10, r=10, t=30, b=10),  # Reduce margins for full width
                    autosize=True
                )

                    return fig

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center", 
                            style = "font-weight: bold; font-size: 20px"):
            "Voter Empathy Hitmap | By District"

        @render.plot
        def map():
            gdf = gpd.GeoDataFrame.from_features(districts_geojson["features"])
            gdf = gdf.set_crs("EPSG:4326")  # WGS84
            dd = tips_data()

            gdf["District_Name"] = gdf["name"].str.strip().str.title()
            dd["District_Name"] = dd["District_Name"].str.strip().str.title()
            merged = gdf.merge(dd, on="District_Name", how="left")
            merged = merged.to_crs(epsg=3857)

            fig3, ax = plt.subplots()
            merged.plot(
                column="Voter_Empathy",
                cmap="Reds",
                linewidth=0.8,
                edgecolor="white",
                legend=True,
                ax=ax
            )

                        # Add labels for each district
            for x, y, label in zip(
                merged.geometry.centroid.x,  # X-coordinate of district center
                merged.geometry.centroid.y,  # Y-coordinate of district center
                merged["District_Name"]           # Text to display
            ):
                ax.annotate(
                    text=label,
                    xy=(x, y),
                    xytext=(-10, 0),  # Slight offset
                    textcoords="offset points",
                    # fontsize=9,
                    # color="black"
                )

            # Step 5: Add basemap and remove axes
            cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
            cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)

                    # Remove axes and fill space
            ax.set_axis_off()
            fig3.tight_layout(pad=0)

            return fig3   # ⇦ raw HTML string





            # fig3 = px.choropleth(
            #     d,
            #     geojson=districts,
            #     featureidkey="properties.name",
            #     locations="District_Name",  # column in dataframe which contains districts names
            #     color="Voter_Empathy",  # data from this column in dataframe is plotted
            #     color_continuous_scale="Reds",  # 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd'
            # )
            # fig3.update_layout(
            #     geo=dict(
            #         showframe=False,
            #         showcoastlines=False,
            #         showland=False,
            #         projection_type="natural earth",
            #         fitbounds="locations",
            #         bgcolor="rgba(0,0,0,0)",
            #     ),
            #     autosize=True,
            #     margin=dict(l=0, r=0, t=0, b=0),
            #     height=None,
            #     width=None,
            # )

            # return fig3

ui.include_css(app_dir / "styles.css")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------


@reactive.calc
def tips_data():
    bill = input.Voter_Empathy()
    idx1 = district_summary.Voter_Empathy.between(bill[0] - 1, bill[1] + 1)
    idx2 = district_summary.Region.isin(input.Region())
    idx3 = district_summary.District_Name.isin(input.District_Name())
    return district_summary[idx1 & idx2 & idx3]


@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("Voter_Empathy", value=bill_rng)
    ui.update_checkbox_group("Region", selected=["Southern", "Central", "Northern"])
    ui.update_checkbox_group("District_Name", selected=(district_summary["District_Name"].unique().tolist()))
