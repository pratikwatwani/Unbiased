<p align="center"><img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/logo.png" width="250" height="200" margin-right=500px></p>

# <h1 align="center">Spatio Temporal Event Based Influence on Wikipedia Edits</h1>

## Motivation
Every day there are thousands of notable transactions over the globe; protests, market dips, terrorist attacks, etc. 

The question is, <b>Do global events lead to influence in edits of Wikipedia articles?</b>

PRAXEOLOGY POLARIZATION is a tool to serve moderators and researchers to leverage open data to understand and further research patterns in Wikipedia edits contribution. 

## Data
| Type | Source                                               | Size    | Update Frequency | Location   |
|------|------------------------------------------------------|---------|------------------|------------|
|  <img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/structured%20data.png" width="80" margin-right="80">    | GDELT, Global Database of Events, Language, and Tone |   <b>6+ TB</b>  |    15 minutes    |  Public S3 |
|  <img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/unstructured%20data.png" width="80" height='90' margin-right="80">     | Wikipedia Metadata                                   | <b>~500 GB</b> |      Varies      | Private S3 |

</br><b>GDELT:</b></br><img src="https://maelfabien.github.io/assets/images/header.jpg" width="350"></br>
The GDELT Project monitors the world's broadcast, print, and web news from nearly every corner of every country in over 100 languages and identifies the people, locations, organizations, themes, sources, emotions, counts, quotes, images and events driving our global society every second of every day, creating a free open platform for computing on the entire world.</br>
</br><b>Wikipedia Metadata:</b></br><img src="https://www.bunkered.co.uk/uploads/site/_articleBodyImage/Wikipedia-logo-1024x576.jpg" width="300" margin-right="300"></br>
Historical and Current dump of English Wikipedia consisting metadata including edits, commits, messages, userids', timestamp of each edit on the wikipedia article.</br>
## Pipeline Architecture
<img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/pipeline.png" align='center'><br/>

## Architectural Components
| Entity  | Purpose          | Type                                             |Reason                                   |
|---------|------------------|--------------------------------------------------|-----------------------------------------|
| AWS S3  | Raw Data Storage | -                                                |
| AWS EC2 | Spark Cluster    | Master - 1 x m5a.large<br>Worker - 4 x m5a.large |
| AWS EC2 | TimescaleDB      | 1 x r5a.large                                    |
| AWS EC2 | Web App          | 1 x t3.large                                     |
| AWS EC2 | Airflow Scheduler| 1 x t3.large                                     |

## Challenges
### Data
1. Handling compressed files
2. Semi-Structured Data (XML)

### Engineering
1. Database memory optimization
2. Joining data
3. Distributed database design with Chunking

### Architectural 
1. Storage - Processing Cluster - Database Cluster connection

## Directory Structure
```bash

│  src
│   │ 
│   ├── scraper
│   │     ├── scraper.py
│   │     ├── lists
│   │           ├── current_urls.txt
│   │           ├── historic_urls.txt
│   │     ├── runScrapper.sh
│   ├── dataingestion
│   │     ├── ingester.py
│   │     ├── runIngester.sh
│   ├── processor
│   ├── 
│   │   ├── 
│   └── 
├── 
├── README.md
└── .gitignore
```

## Instructions

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

<br/><br/><h6>&copy; All product names, logos, and brands are property of their respective owners.</h6>
