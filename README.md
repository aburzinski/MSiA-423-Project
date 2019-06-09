# MSiA 423 Project Repository
- [Project Charter](#project-charter)
- [Planning](#planning)
- [Data Sources](#data-sources)
- [Project Initialization](#project-initialization)
- [Testing](#testing)

## Project Charter
### Vision
Provide Major League Baseball MLB with an application that improves fan experience by engaging and sustaining fan interest in MLB teams and players.
### Mission
Build an application incorporating an intuitive user interface, data updated daily, and accurate logistic regression models that predict MLB team and player season outcomes and awards.  This application will assist MLB in driving and sustaining season-long fan engagement. 
### Success Criteria
- The success of the logistic regression models used will be based on achieving an AUC measure and F-score of above .9.
- The success of the application with respect to the business outcome will be improved fan engagement.  A successful application will drive users to attend a higher number of MLB games and purchase a larger amount MLB merchandise and memorabilia.  This will be assessed by analyzing fan user behavior before and after using the application.


## Planning
### Theme 1: MLB Award Prediction App
- Epic 1: Create and Test Models
  - Collect Historial Data
  - Clean Historical Data
  - Engineer and Transform Features
  - Create Models with Python
    - Pitching Data Models
    - Batting Data Models
    - Fielding Data Models
  - Assess Model Performance
  - Tune Models to Optimize Performance
  - Create Documentation for Models
- Epic 2: Create App Frontend
  - Create Web App Using Flask and HTML
    - Create Landing Page
    - Create Player Page
    - Create Team Page
    - Create Comparison Page
  - Improve UX with CSS and Javascript
  - Test Web App
  - Document Web App
- Epic 3: Create Process to Update Current Player Data Nightly
  - Write Python Scripts to Injest Data
  - Automate Scripts
  - Test Ingestion Process
  - Document Data Ingestion Process
- Epic 4: Create Cloud Infrastructure and Move App to Cloud
  - Create Resources in AWS
    - Private S3 bucket
    - Public S3 bucket
    - RDS Instance
    - EC2 Instance
  - Move Models and Data to AWS
  - Move Ingestion Process to AWS
  - Test App in the Cloud
  - Document Cloud Infrastucture
- Epic 5: Create Team Performance Based Model

### Backlog
1. Epic1 - Create Documentation for Models: 2 Points - PLANNED

### Completed
1. Epic1 - Collect Historical Data
2. Epic1 - Clean Historical Data
3. Epic1 - Engineer and Transform Features
4. Epic1 - Create Models with Python
5. Epic1 - Assess Model Performance
6. Epic1 - Tune Models
7. Epic2 - Create Web App Using Flask and HTML: Create Index Page
8. Epic2 - Create Web App Using Flask and HTML: Create Player Page
9. Epic2 - Create Web App Using Flask and HTML: Create Team Page
10. Epic2 - Improve UX with CSS and Javascript
11. Epic3 - Create Python Scripts to Ingest Data
12. Epic3 - Automate Training of model
13. Epic4 - Create Resources in AWS: Private S3 Bucket
14. Epic4 - Create Resources in AWS: Public S3 Bucket
15. Epic4 - Create Resources in AWS: RDS Instance
16. Epic4 - Create Resources in AWS: EC2 Instance

### Icebox
- Epic2 - Create Web App Using Flask and HTML: Create Comparison Page
- Epic2 - Create Web App Using Flask and HTML: Create History Page
- Epic5


## Data Sources
The statisical Major League Baseball data comes from the following API:
`https://appac.github.io/mlb-data-api-docs/`

There is no singup process required to use the API.  However, statistical data can only be pulled for one player and one season at a time.  Because of this, downloading the historical dataset can take quite a while.  A workaround is discussed below.


## Project Initialization
### To initialize this project in a new environemnt, follow these steps

#### 1. Clone Project from Github
Run the following from the command line:

`git clone https://github.com/aburzinski/MSiA-423-Project.git`

#### 2. Create Python Environment
Create the environemnt from the `requirements.txt` file

```
pip install virtual env

virtualenv env_name

source env_name/bin/activate

pip install -r requirements.txt
```

#### 3. Create Environment Variables in New Enviroment
First, create the `PYTHONPATH` variable.  This should be the top level project directory (i.e. `MSiA-423-Project`):

```
export PYTHONPATH='/nfs/home/user/my_project_root'
```

__Note:__ When setting PYTHONPATH, do not use a `~`.  I.e., use 

`export PYTHONPATH='/nfs/home/user/projects/my_project_root'`

rather than 

`export PYTHONPATH='~/projects/my_project_root'`

Next, create the credentials for the AWS S3 bucket that this project will use:

```
export AWS_BUCKET_NAME='my_bucket'

export AWS_ACCESS_KEY_ID='my_access_key'

export AWS_SECRET_ACCESS_KEY='my_access_secret'
```

Finally, create the credentials that will be used for an RDS instance.  This step only needs to be completed if using an RDS database (versus writing to sqlite locally):

```
export MYSQL_HOST='my_db_url'

export MYSQL_USER='my_db_username'

export MYSQL_PASSWORD='my_db_password'
```

#### 4. Update the configuration file
The file `config/config.py` contains configurations for each part of the project.  Key configurations to update are:

- The Flask App Port and Host
- The Yaml file locations (if these are different from the Github defaults)
- The model artifact location (if these are different from the Github defaults)
- The logging file location (if different from the Github defaults)
- The Sql Alchemy database type (this should only be set to either `sqlite` or `mysql`)
- The Sql Alchemy SQLite Host/File Path (if this differs from the Github default)
- The Sql Alchemy database name (if this differs from the Github)


#### 5. Run the script project_init.sh

`bash project_init.sh`

This script will download the historical data from S3, create features, models, and predictions, format the data, create a database in RDS (or SQLite) and populate the database.

__Note:__ Bash scripts rather than makefiles were used for this projects as some of the file dependencies used in makefiles live in S3 rather than the local file system.

__Note:__ By default, the `project_init.sh` script will download historical data that has already been created from S3.  To re-create the historical data from the API, run the following script:

`python src/pull_historical_data.py`

This script pulls the data from an API, but takes over an hour to run.

#### 6. Run the App
After running the `project_init.sh` script, the app is ready to be run.  To run the app, use the following command:

`python app/app.py`

At this point, the app should be running on the host and port specified in the `config/config.py` file.


## Testing
To test many of the functions in this project, run `pytest` from the command line.

The code for the test cases exists in the `test/unit` folder.
