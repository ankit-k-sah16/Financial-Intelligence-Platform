"""
=========================================================
Charts Utility Module
N100 Financial Intelligence Platform

Reusable Plotly charts for the Streamlit Dashboard.
=========================================================
"""

from typing import List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# Global Theme
# =========================================================
PRIMARY = "#2563EB"
SECONDARY = "#10B981"
ACCENT = "#F59E0B"
DANGER = "#DC2626"

BACKGROUND = "white"

FONT = "Arial"

PLOT_TEMPLATE = "plotly_white"

HEIGHT = 450


# =========================================================
# Common Layout
# =========================================================
def apply_layout(fig, title):
    fig.update_layout(

        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(
                size=20,
                family=FONT
            )
        ),

        template=PLOT_TEMPLATE,

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        hovermode="x unified",

        height=HEIGHT,

        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        font=dict(
            family=FONT,
            size=13
        )

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False

    )

    fig.update_yaxes(

        gridcolor="rgba(220,220,220,0.5)",

        zeroline=False

    )

    return fig


# =========================================================
# KPI Card
# =========================================================

def create_kpi_card(

    title: str,

    value,

    delta=None,

    help_text=None

):
    """
    Displays a KPI card.
    """

    st.metric(

        label=title,

        value=value,

        delta=delta,

        help=help_text

    )


# =========================================================
# Line Chart
# =========================================================

def create_line_chart(

    df: pd.DataFrame,

    x: str,

    y: str,

    title: str,

    color=PRIMARY,

):

    fig = px.line(

        df,

        x=x,

        y=y,

        markers=True

    )

    fig.update_traces(

        line=dict(

            width=3,

            color=color

        ),

        marker=dict(

            size=7

        )

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Multi Line Chart
# =========================================================

def create_multi_line_chart(

    df: pd.DataFrame,

    x: str,

    y_columns: List[str],

    title: str,

):

    fig = go.Figure()

    for column in y_columns:

        fig.add_trace(

            go.Scatter(

                x=df[x],

                y=df[column],

                mode="lines+markers",

                name=column,

                line=dict(width=3)

            )

        )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Bar Chart
# =========================================================

def create_bar_chart(

    df: pd.DataFrame,

    x: str,

    y: str,

    title: str,

    color=PRIMARY,

):

    fig = px.bar(

        df,

        x=x,

        y=y,

        text_auto=".2s"

    )

    fig.update_traces(

        marker_color=color

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Display Helper
# =========================================================

def show(fig, use_container_width=True):
    """
    Display Plotly figure in Streamlit.
    """

    st.plotly_chart(

        fig,

        use_container_width=use_container_width

    )

# =========================================================
# Horizontal Bar Chart
# =========================================================

def create_horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color=PRIMARY,
):

    """
    Creates a horizontal bar chart.

    Parameters
    ----------
    df : DataFrame

    x : Numeric column

    y : Category column

    title : Chart title
    """

    fig = px.bar(

        df,

        x=x,

        y=y,

        orientation="h",

        text_auto=".2s"

    )

    fig.update_traces(

        marker_color=color

    )

    fig.update_layout(

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Donut Chart
# =========================================================

def create_donut_chart(

    df: pd.DataFrame,

    names: str,

    values: str,

    title: str,

):

    """
    Creates a donut chart.

    Useful for:

    • Sector Allocation

    • Capital Allocation

    • Portfolio Distribution
    """

    fig = px.pie(

        df,

        names=names,

        values=values,

        hole=0.55

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Scatter Plot
# =========================================================

def create_scatter_chart(

    df: pd.DataFrame,

    x: str,

    y: str,

    title: str,

    color=None,

    size=None,

):

    """
    Creates a scatter chart.

    Useful for:

    ROE vs ROCE

    PE vs Growth

    Risk vs Return

    Market Cap vs Profit
    """

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=color,

        size=size,

        hover_data=df.columns,

    )

    fig.update_traces(

        marker=dict(

            size=10,

            opacity=0.8,

            line=dict(

                width=1,

                color="white"

            )

        )

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Top N Helper
# =========================================================

def top_n(

    df: pd.DataFrame,

    column: str,

    n: int = 10,

    ascending=False,

):

    """
    Returns Top N rows.

    Useful before plotting.

    Example

    -------

    top10 = top_n(

        df,

        "market_cap"

    )
    """

    return (

        df

        .sort_values(

            by=column,

            ascending=ascending

        )

        .head(n)

        .reset_index(drop=True)

    )


# =========================================================
# Bottom N Helper
# =========================================================

def bottom_n(

    df: pd.DataFrame,

    column: str,

    n: int = 10,

):

    """
    Returns Bottom N rows.
    """

    return (

        df

        .sort_values(

            by=column

        )

        .head(n)

        .reset_index(drop=True)

    )


# =========================================================
# Percentage Formatter
# =========================================================

def format_percentage(

    fig,

    axis="y"

):

    """
    Format chart axis as percentage.
    """

    if axis == "y":

        fig.update_yaxes(

            ticksuffix="%"

        )

    else:

        fig.update_xaxes(

            ticksuffix="%"

        )

    return fig


# =========================================================
# Currency Formatter
# =========================================================

def format_currency(

    fig,

    axis="y",

    symbol="₹"

):

    """
    Formats axis as Indian Rupees.
    """

    if axis == "y":

        fig.update_yaxes(

            tickprefix=symbol

        )

    else:

        fig.update_xaxes(

            tickprefix=symbol

        )

    return fig

# =========================================================
# Dashboard Color Palette
# =========================================================

COLORS = [
    "#2563EB",
    "#10B981",
    "#F59E0B",
    "#DC2626",
    "#7C3AED",
    "#06B6D4",
    "#84CC16",
    "#F97316",
    "#EC4899",
    "#64748B",
]


# =========================================================
# Radar Chart
# =========================================================

def create_radar_chart(
    company_values,
    peer_values,
    labels,
    title="Company vs Peer Comparison",
):

    """
    Radar Chart

    Parameters
    ----------
    company_values : list

    peer_values : list

    labels : list
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=company_values,

            theta=labels,

            fill="toself",

            name="Company",

            line=dict(

                color=PRIMARY,

                width=3

            )

        )

    )

    fig.add_trace(

        go.Scatterpolar(

            r=peer_values,

            theta=labels,

            fill=None,

            name="Peer Average",

            line=dict(

                color=DANGER,

                dash="dash",

                width=2

            )

        )

    )

    fig.update_layout(

        template=PLOT_TEMPLATE,

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 100]

            )

        ),

        showlegend=True,

        height=550,

        title=dict(

            text=title,

            x=0.5

        )

    )

    return fig


# =========================================================
# Treemap
# =========================================================

def create_treemap(

    df,

    path,

    values,

    color,

    title,

):

    """
    Treemap

    Example

    Sector

        ├── TCS

        ├── Infosys

        ├── Wipro
    """

    fig = px.treemap(

        df,

        path=path,

        values=values,

        color=color,

        color_continuous_scale="Blues"

    )

    return apply_layout(

        fig,

        title

    )


# =========================================================
# Company Comparison Table
# =========================================================

def create_comparison_table(

    df,

    height=500,

):

    """
    Streamlit DataFrame

    with better formatting.
    """

    st.dataframe(

        df,

        use_container_width=True,

        height=height

    )


# =========================================================
# Download CSV
# =========================================================

def download_dataframe(

    df,

    filename,

    label="Download CSV",

):

    csv = df.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        label=label,

        data=csv,

        file_name=filename,

        mime="text/csv"

    )


# =========================================================
# Save Plotly Figure
# =========================================================

def save_figure(

    fig,

    path,

    width=1400,

    height=700,

):

    """
    Save Plotly figure.

    Requires:

    pip install kaleido
    """

    fig.write_image(

        path,

        width=width,

        height=height

    )


# =========================================================
# Dashboard Separator
# =========================================================

def section_header(

    title,

):

    st.markdown("## " + title)

    st.divider()


# =========================================================
# Empty Chart
# =========================================================

def empty_chart(

    message="No Data Available",

):

    st.info(message)


# =========================================================
# Dashboard Footer
# =========================================================

def dashboard_footer():

    st.markdown("---")

    st.caption(

        "N100 Financial Intelligence Platform | Version 1.0"

    )