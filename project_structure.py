from pathlib import Path



#Folder Structure
folders=[
    "data/raw",
    "data/supporting",
    
    "src/etl/",
    "src/analytics/",
    "src/nlp/",
    "src/dashboard/"
    "src/reports/",
    "src/api/",

    "tests/",
    
    "config/",

    "reports/tearsheets/",
    "reports/sector/" ,
    "reports/portfolio/", 
    "reports/radar_charts/",

    "output/",

    "notebooks/",

    "docs/",

    "meakefile"
]

# Create folders
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Create common files   
files = [

    "requirements.txt",
    ".gitignore",
    ".env"
   ]

for file in files:
    Path(file).touch(exist_ok=True)

print(f" Project structure  created successfully!")