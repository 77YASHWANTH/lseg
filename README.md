
# INFO
APPLICATIONS:

1.STOCKDATA - Returns the parsed data from csv file in json format downloaded using ./stockdata.sh
2.OUTLIER - Calculate & Returns the Standarddeviation,mean data in json format using the data returned from STOCKDATA application 
3.OUTPUT - Requests the data from STOCKDATA & OUTLIER ,Returns the csv attachment

### TO RUN IN LOCAL ###

#### PREREQUISITES

1.Install python3
2.Install pip 
3.Install flask
4.Install AWSCLI 


####  STEP 1: ####

Upload the files in standard s3 bucket 

FOLDER ALIGNMENT : `/EXCHANGENAME/STOCKID/**.CSV `

#### Execute the script ####

Scriptfile present in `/APP/stockdata/stockdatafiles/`

`stockdata.sh`

Files will be downloaded to local folder 


### STEP 2 ###

Ignore the step 1 if the files are going to be placed directly in local.

Update the base path (folder location) variable in `/APP/stockdata/app.py`

### STEP 3 ###

Configure ENvironment variables 

`export STOCKDATA_APP_URL="127.0.0.1:5000"`

`export OUTLIER_APP_URL="127.0.0.1:5001"`


TO run the application with command `CD` to each applications

FOLDERS `/APP/stockdata/ ,/APP/outlier/ ,/APP/output/`

Run the command `PYTHON3 app.py` ,update unique ports to `app.py `(currently all app ports are configured to 5000 )
```
### ENDPOINTS ###

** Endpoint 1 : Retrieve 30 Days stock price **

* OUTPUT application running in port 5003 *
`
http:127.0.0.1:5003/EXCHANGENAME/STOCKID/NOOFFILES/DATE
ex: http:127.0.0.1:5003/NASDAQ/TSLA/5/01-09-2023
`
** Endpoint 2: Retrieve Outlier data **

http:127.0.0.1:5003/EXCHANGENAME/STOCKID/outliers/NOOFFILES/DATE
ex: http:127.0.0.1:5003/NASDAQ/TSLA/outliers/5/01-09-2023
```

--------------------------------------------------------------------------------------------

NOTE:
1.CI pipeline is already implemented with github actions , pipeline files are present in `.github` folder
2. (INPROGRESS) Container orchestrations is initiated using EKS. Deployment file present in `CONTAINERIZATION` folder 


