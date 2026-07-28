import pandas  as pd 
df= pd.read_excel("output/valuation_summary.xlsx")  
df.to_csv("output/valuation_summary.csv",index=False,header=True)