# src Folder

This folder contains all scripts to execute the program end-to-end

## Main directories:

```bash

│ 
├── dataingestion
│
├── decompressor  
│
├── processor
│
├── frontend
│
└── airflow

```

#### `dataingestion`
Contains files to scrape contents of the Wikipedia dump and upload relevant data onto Private S3 bucket

#### `decompressor`
Fetches data from S3 bucket to decompressed and replace original files in the intended directory of S3 bucket

#### `processor`
Contains core components of pipeline to process Wikipedia and GDELT data from respective S3 buckets and written in the database

#### `frontend`
Dashboard script based on Dash Plotly with Flask backend 

#### `airflow`
Airflow DAG script that automates pipeline execution
