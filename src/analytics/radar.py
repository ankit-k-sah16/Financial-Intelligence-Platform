"""
Radar Chart Generator
---------------------

Creates peer comparison radar charts.
Output
------
reports/
    radar_charts/
        <ticker>_radar.png
"""

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from config.setting import DB_PATH


class RadarChartGenerator:

    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DB_PATH}")

        self.output_dir = Path( "reports/radar_charts" )
                 
        self.output_dir.mkdir(parents=True,exist_ok=True)

    # -------------------------------------------------------
    # Load Data
    # -------------------------------------------------------
    def load_data(self):

        self.df = pd.read_sql("SELECT * FROM stg_financial_ratios", self.engine )
            
           
       

        self.peers = pd.read_sql("SELECT * FROM stg_peer_groups",self.engine)

        self.df = self.df.merge( self.peers, on="company_id",how="left")
 
        print("Radar data loaded.")

    # -------------------------------------------------------
    # Normalize helper
    # -------------------------------------------------------
    @staticmethod
    def normalize(series, inverse=False):

        s = pd.to_numeric( series,errors="coerce" )

        if s.max() == s.min():

            return pd.Series(50,index=s.index)

        score = ( (s - s.min()) / (s.max() - s.min())  ) * 100

        if inverse:
            score = 100 - score

        return score

    # -------------------------------------------------------
    # Prepare Scores
    # -------------------------------------------------------
    def prepare_scores(self):

        df = self.df.copy()

        df["roe_score"] = self.normalize(df["return_on_equity_pct"]  )
                  
        df["roce_score"] = self.normalize(df["return_on_capital_employed_pct"] )
                 
        df["npm_score"] = self.normalize(df["net_profit_margin_pct"] )
                   
        df["de_score"] = self.normalize(df["debt_to_equity"],inverse=True)
                              
        df["fcf_score"] = self.normalize( df["free_cash_flow_cr"] )
                  
        df["pat_score"] = self.normalize(df["pat_cagr_5yr"] )
                   
        df["revenue_score"] = self.normalize( df["revenue_cagr_5yr"] )
                 
        self.df = df

    # -------------------------------------------------------
    # Draw Radar
    # -------------------------------------------------------
    def plot_company(self, row):

        labels = [ "ROE",
            "ROCE",       
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "Revenue CAGR",
            "Composite"
        ]

        values = [
            row["roe_score"],
            row["roce_score"],
            row["npm_score"],
            row["de_score"],
            row["fcf_score"],
            row["pat_score"],
            row["revenue_score"],
            row["composite_quality_score"]
        ]

        peer = self.df[self.df["peer_group_name"] ==  row["peer_group_name"]]
            
        peer_avg = [
            peer["roe_score"].mean(),

            peer["roce_score"].mean(),

            peer["npm_score"].mean(),

            peer["de_score"].mean(),

            peer["fcf_score"].mean(),

            peer["pat_score"].mean(),

            peer["revenue_score"].mean(),

            peer["composite_quality_score"].mean()
        ]

        angles = np.linspace( 0, 2*np.pi,len(labels), endpoint=False).tolist()
        
        values += values[:1]

        peer_avg += peer_avg[:1]

        angles += angles[:1]

        fig = plt.figure(figsize=(8,8))
        
        ax = plt.subplot(111,polar=True )
                              
        ax.plot( angles,values,linewidth=2)
                                   
        ax.fill(angles,values,alpha=0.30)

        ax.plot(angles, peer_avg, linestyle="--",linewidth=2
           
        )

        ax.set_xticks(
            angles[:-1]
        )

        ax.set_xticklabels(
            labels,
            fontsize=10
        )

        ax.set_ylim(0,100)

        plt.title(
            f"{row['ticker']} Peer Radar",
            fontsize=14,
            pad=20
        )

        plt.tight_layout()

        plt.savefig(

            self.output_dir /
            f"{row['ticker']}_radar.png",
            dpi=300
        )

        plt.close()

    # -------------------------------------------------------
    # Standalone Chart
    # -------------------------------------------------------
    def standalone_chart(self, row):

        fig = plt.figure(
            figsize=(5,5)
        )

        ax = plt.subplot(
            111,
            polar=True
        )

        labels = ["Composite" ]

        values = [ row["composite_quality_score"] ]

        nifty_avg = [

            self.df["composite_quality_score"].mean()]

        angles = [0,0]

        values = values*2

        nifty_avg = nifty_avg*2

        ax.plot(angles,
            values  )
        
        ax.fill( angles, values,
            alpha=0.3
        )
           
        ax.plot( angles, nifty_avg,
            linestyle="--"
        )

        ax.set_ylim(0,100)

        plt.title(row["ticker"])        
     
        plt.savefig(
            self.output_dir /
            f"{row['ticker']}_radar.png",
            dpi=300
        )

        plt.close()

    # -------------------------------------------------------
    # Generate
    # ------------------------------------------------------
    def generate(self):

        self.prepare_scores()

        latest = (
            self.df
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )

        for _, row in latest.iterrows():

            if pd.isna(row["peer_group_name"]):
                
                self.standalone_chart( row)

            else:
                self.plot_company( row)
                   
        print()
        print("="*60)
        print(f"Charts saved to {self.output_dir}")

        print("="*60)

    # -------------------------------------------------------
    # Run
    # -------------------------------------------------------
    def run(self):
        self.load_data()
        self.generate()