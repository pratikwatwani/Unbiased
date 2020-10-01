# Spatio Temporal Event Based Influence on Wikipedia Edits
| <img src="https://www.bunkered.co.uk/uploads/site/_articleBodyImage/Wikipedia-logo-1024x576.jpg" width="300" margin-right="300"> | <img src="https://maelfabien.github.io/assets/images/header.jpg" width="350">|
| ------------- | ------------- |

## Motivation
## Data
| Type | Source                                               | Size    | Update Frequency | Location   |
|------|------------------------------------------------------|---------|------------------|------------|
|  <img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/structured%20data.png" width="80" margin-right="80">    | GDELT, Global Database of Events, Language, and Tone |   <b>6+ TB</b>  |    15 minutes    |  Public S3 |
|  <img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/unstructured%20data.png" width="80" height='90' margin-right="80">     | Wikipedia Metadata                                   | <b>~500 GB</b> |      Varies      | Private S3 |

## Pipeline Architecture
<img src="https://github.com/pratikwatwani/Event-Based-Influence-on-Wikipedia/blob/master/assets/pipeline.png" align='center'><br/>

## Architectural Components
| Entity  | Purpose          | Type                                             |
|---------|------------------|--------------------------------------------------|
| AWS S3  | Raw Data Storage | -                                                |
| AWS EC2 | Spark Cluster    | Master - 1 x m5a.large<br>Worker - 3 x m5a.large |
| AWS EC2 | TimescaleDB      | 1 x r5a.large                                    |

## Challenges
### Data
1. Handling compressed files
2. Semi-Structured Data (XML)

## Engineering
1. Database memory optimization
2. Joining data

<br/><br/><h6>&copy; All product names, logos, and brands are property of their respective owners.</h6>
