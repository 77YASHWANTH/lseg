Here’s an updated version of your `README.md` with the correct format and structure for clarity and readability:

```markdown
# INFO

## APPLICATIONS:

1. **STOCKDATA**  
   Parses data from a CSV file and returns it in JSON format. The CSV file is downloaded using `./stockdata.sh`.

2. **OUTLIER**  
   Calculates and returns the standard deviation and mean data in JSON format using the data returned from the STOCKDATA application.

3. **OUTPUT**  
   Requests data from both STOCKDATA and OUTLIER, then returns the data as a CSV attachment.

---

## TO RUN IN LOCAL

### PREREQUISITES

Before running the application, ensure the following dependencies are installed:

1. Install **python3**
2. Install **pip**
3. Install **Flask**
4. Install **AWSCLI**

---

### STEP 1: Upload Files to S3 Bucket

1. Upload the required CSV files to your S3 bucket with the following folder alignment:

   ```
   /EXCHANGENAME/STOCKID/**.CSV
   ```

2. **Execute the script** to download the files:

   - The script is located in `/APP/stockdata/stockdatafiles/`.
   - Execute the script `stockdata.sh` to download the files to your local folder.

---

### STEP 2: (Optional) Use Local Files

If the files are going to be placed directly in your local environment (i.e., skipping S3 upload), follow these steps:

1. Update the base path (folder location) variable in `/APP/stockdata/app.py` to point to your local directory.

---

### STEP 3: Configure Environment Variables

Set up the necessary environment variables by running the following commands:

```bash
export STOCKDATA_APP_URL="127.0.0.1:5000"
export OUTLIER_APP_URL="127.0.0.1:5001"
```

---

## RUNNING THE APPLICATION

To run the application, navigate to each application's folder and run the Python app:

1. Change directory to each of the following folders:

   - `/APP/stockdata/`
   - `/APP/outlier/`
   - `/APP/output/`

2. Run the following command in each folder:

   ```bash
   python3 app.py
   ```

   **Note:** Ensure the ports are configured properly for each app. By default, all apps are set to use port 5000. You may need to update the ports in `app.py` files if they need to run on different ports.

---

## ENDPOINTS

### 1. Retrieve 30 Days Stock Price

- **Application**: OUTPUT (running on port 5003)  
- **Endpoint**:  
  `http://127.0.0.1:5003/EXCHANGENAME/STOCKID/NOOFFILES/DATE`

  Example:  
  `http://127.0.0.1:5003/NASDAQ/TSLA/5/01-09-2023`

### 2. Retrieve Outlier Data

- **Application**: OUTPUT (running on port 5003)  
- **Endpoint**:  
  `http://127.0.0.1:5003/EXCHANGENAME/STOCKID/outliers/NOOFFILES/DATE`

  Example:  
  `http://127.0.0.1:5003/NASDAQ/TSLA/outliers/5/01-09-2023`

---

## ADDITIONAL NOTES

1. **CI Pipeline**  
   A CI pipeline is already set up using GitHub Actions. The pipeline configuration files are located in the `.github` folder.

2. **Container Orchestration (IN PROGRESS)**  
   Container orchestration has been initiated using **Amazon EKS**. Deployment files can be found in the `CONTAINERIZATION` folder. Cluster setup steps will be added at a later stage.

---

```git 