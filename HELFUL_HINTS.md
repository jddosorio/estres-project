ESTRES Streamlit --- Helpful Hints

This document contains the basic commands required to work with the
ESTRES Streamlit application.

1. Open the Project

From Terminal, move to the project directory:

cd /path/to/project
ls

You should see at least app.py, views/, images/, sample_data/,
and requirements.txt.

2. Activate the Python Virtual Environment

The project uses a Python virtual environment named .venv.

source .venv/bin/activate
which python

which python should point to .../project/.venv/bin/python.

3. Install the Dependencies

For a new installation:

python -m pip install -r requirements.txt

If requirements.txt must be regenerated:

python -m pip freeze > requirements.txt

Review it before committing.

4. Run Streamlit Locally

source .venv/bin/activate
python -m streamlit run app.py

Streamlit normally starts at:

http://localhost:8501

To stop it, press Ctrl + C.

5. Local Development Workflow

After modifying Python files, Streamlit normally detects the changes.
Save the file and rerun from the browser if required.

To restart:

Ctrl + C

then:

python -m streamlit run app.py

6. Check the Git Repository

Before committing:

git status

Review all modified and new files.

IMPORTANT: Never upload passwords, API keys, tokens, database
credentials, or other private information.

These files should normally not be committed:

.env
.streamlit/secrets.toml

Include them in .gitignore.

7. Upload Changes to GitHub

git status
git add .
git status
git commit -m "Update ESTRES Streamlit application"
git push origin main
git status

A clean repository should show something similar to:

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

8. Run the Application in Streamlit Community Cloud

The cloud version does not require running Streamlit manually from your
Mac.

Mac
 │
 │ git push
 ▼
GitHub Repository
 │
 │ deployment
 ▼
Streamlit Community Cloud
 │
 ▼
ESTRES Web Application

The application code and required public resources must be available in
the GitHub repository.

9. Deploy to Streamlit Community Cloud

Open Streamlit Community Cloud:

https://share.streamlit.io/

Sign in using the GitHub account associated with the project repository.

Create/deploy an application, select the GitHub repository containing
ESTRES, and configure the application entry point as:

app.py

Streamlit Community Cloud will:

clone the GitHub repository;

create the Python environment;

install packages from requirements.txt;

execute app.py;

publish the application.

10. requirements.txt

Typical dependencies for this project include:

streamlit
pandas
plotly
pydeck
Pillow

The exact requirements.txt should reflect the imports actually used by
the application.

If a module works locally but fails in Streamlit Cloud, first verify
that it is included in requirements.txt.

11. Update the Cloud Application

Normal workflow:

Edit locally
    ↓
Test locally
    ↓
git add .
    ↓
git commit
    ↓
git push origin main
    ↓
GitHub
    ↓
Streamlit Cloud

Commands:

git status
git add .
git commit -m "Update ESTRES"
git push origin main

Streamlit Community Cloud normally detects changes pushed to the
configured GitHub branch and redeploys the application.

There is normally no need to execute streamlit run app.py manually on
the cloud server.

12. Local vs Cloud Execution

Local

source .venv/bin/activate
python -m streamlit run app.py

Access:

http://localhost:8501

Cloud

git add .
git commit -m "Update ESTRES"
git push origin main

Streamlit Community Cloud retrieves the project from GitHub and runs the
application remotely. Access it using the public Streamlit URL assigned
during deployment.

13. Images and Sample Data

Store application images under:

images/

Store experimental datasets under:

sample_data/

Use relative paths:

from pathlib import Path

IMAGE_DIR = Path("images")
DATA_DIR = Path("sample_data")

Do not use absolute Mac paths such as /Users/username/..., because
they will not exist in Streamlit Community Cloud.

14. YouTube Videos

For videos embedded using Streamlit, prefer the standard YouTube URL:

VIDEO = "https://www.youtube.com/watch?v=VIDEO_ID"
st.video(VIDEO)

instead of:

https://www.youtube.com/shorts/VIDEO_ID

The standard watch?v= URL is more suitable for embedded Streamlit
playback.

15. Troubleshooting

Streamlit command not found

source .venv/bin/activate
python -m streamlit run app.py

Application works locally but not in the cloud

Check requirements.txt and verify that all files referenced by the
application were committed:

git status

Image or CSV works locally but not in the cloud

Check that the file is tracked by Git:

git status
git ls-files

Also check filename capitalization. Linux cloud systems may distinguish
filenames such as:

BetoneraGPS.csv
betoneraGPS.csv

Check Streamlit

python -m streamlit --version

Check Python

python --version
which python

16. Recommended Workflow

For normal development:

cd /path/to/estres
source .venv/bin/activate
python -m streamlit run app.py

After testing:

git status
git add .
git status
git commit -m "Update ESTRES"
git push origin main

Then verify the deployed application in Streamlit Community Cloud.

Quick Reference

Run locally

source .venv/bin/activate
python -m streamlit run app.py

Upload to GitHub

git status
git add .
git commit -m "Update ESTRES"
git push origin main

Cloud deployment

Local development → GitHub → Streamlit Community Cloud
