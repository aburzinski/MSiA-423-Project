## Project Charter
### Vision
Provide Major League Baseball MLB with an application that improves fan experience by engaging and sustaining fan interest in MLB teams and players.
### Mission
Build an application incorporating an intuitive user interface, data updated daily, and accurate logistic regression models that predict MLB team and player season outcomes and awards.  This application will assist MLB in driving and sustaining season-long fan engagement. 
### Success Criteria
- The success of the logistic regression models used will be based on achieving an AUC measure and F-score of above .9.
- The success of the application with respect to the business outcome will be improved fan engagement.  A successful application will drive users to attend a higher number of MLB games and purchase a larger amount MLB merchandise and memorabilia.  This will be assessed by analyzing fan user behavior before and after using the application.

## Planning
### MLB Award Prediction App
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
  - Move Models and Data to AWS
  - Move Ingestion Process to AWS
  - Test App in the Cloud
  - Document Cloud Infrastucture
- Epic 5: Create Team Performance Based Model

### Backlog
1. Epic1 - Collect and Clean Data: 2 Points - PLANNED
2. Epic1 - Engineer and Transform Features: 1 Point - PLANNED
3. Epic1 - Create Models with Python: 1 Point - PLANNED
4. Epic1 - Assess Model Performance: 1 Point - PLANNED
5. Epic1 - Tune Models: 4 Points - PLANNED
6. Epic1 - Create Documentation for Models: 2 Points - PLANNED
7. Epic2 - Create Web App Using Flask and HTML: 4 Points
8. Epic2 - Improve UX with CSS and Javascript: 8 Points

### Icebox
- Epic2
- Epic3
- Epic4
- Epic5


## Technical TODOs
- Make sure to add project root to system path