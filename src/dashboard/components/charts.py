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