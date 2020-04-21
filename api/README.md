## Web API - Flask
This directory holds the codebase for the web API.

### First-time Setup (macOS)
1. Create a Python virtual environment with `virtualenv farm-stack` after navigating to that directory.
2. Activate it with `source farm-stack/bin/activate`
3. Navigate to `api/` and run `pip3 install -r requirements.txt` to install all Python modules necessary for the API.
4. Open `dbcreds.py` in the `api/` directory and edit database credentials as needed.

### Running the API
1. Activate the virtual environment from above.
2. Run `python3 app.py` to run the API on `http://localhost:8080`.
