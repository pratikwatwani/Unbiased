# Spatio Temporal Event Based Influence on Wikipedia Edits
| <img src="https://www.bunkered.co.uk/uploads/site/_articleBodyImage/Wikipedia-logo-1024x576.jpg" width="300" margin-right="300"> | <img src="https://maelfabien.github.io/assets/images/header.jpg" width="350">|
| ------------- | ------------- |

## Motivation
## Data
1. GDELT, Global Database of Events, Language, and Tone<br/>
   Location: Public S3<br/>
   Size: <b>6+ TB</b><br/>
   Update interval: 15 minutes<br/>

2. Wikipedia Metadata<br/>
   Location: Private S3<br/>
   Size: <b>~500 GB</b> <br/>
   Update Interval: Varies<br/>

## Pipeline Architecture
<img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/pipeline.png" align='center'><br/>

## Architectural Components
| Entity  | Purpose          | Type                                             |
|---------|------------------|--------------------------------------------------|
| AWS S3  | Raw Data Storage | -                                                |
| AWS EC2 | Spark Cluster    | Master - 1 x m5a.large<br>Worker - 3 x m5a.large |
| AWS EC2 | TimescaleDB      | 1 x m5a.large                                    |



<br/><br/>&copy; All product names, logos, and brands are property of their respective owners including but not limited to Wikipedia Foundation, GDELT Project, AWS.
