# Fetch Responses from LimeSurvey API
This python script allows you to fetch responses from the LimeSurvey API and save them to a file. Before running the script, you'll need to set some environment variables and install the necessary Python packages. Here's how:

## Environment Variables
Create a file named .env in the root directory of the project, and add the following environment variables:

```
LS_USER=<your LimeSurvey username>
LS_PWD=<your LimeSurvey password>
LS_API_URL=<the base URL for your LimeSurvey installation, e.g. https://your-limesurvey-installation.com/index.php/admin/remotecontrol>
```
## Installing Dependencies
To install the required Python packages, run the following command:

```
pip install -r requirements.txt
```

## Running the Script
Once you've set the environment variables and installed the dependencies, you can run the script by running:
```
python3 main.py
```
The script will fetch responses from the LimeSurvey API and save them to a file named responses.json. If responses.json does not exist, the script will create it. If responses.json does exist, the script will only add new responses to the file on subsequent runs.

That's it! If you have any questions or issues, feel free to open an issue in this repository.

**Note:** This is my first public script and it may not look professional or efficient, but it works and does the job at least for me.