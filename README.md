# MediSync

You can check out the project in Project.pdf file

##  Setup Instructions

### 1. IMP
create new .env file and add API_KEY="groqcloud api key"
Python 3.12 version required



### 2. Create a Virtual Environment

To isolate project dependencies, create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # For Unix/Mac
```

### 3. Command to download required libraries

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Command to run Fast API

```
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 5. Command to run ngrok server

```
ngrok http 8001
```

### 6. Note

keep all scrap.py files in new folder inside main folder named scarp
keep all url.txt files in new folder inside main folder named urls
dont keep extra lines in urls.txt file as it will cause error as following: An error occurred: fact_sheet Invalid URL '': No scheme supplied. Perhaps you meant https://?
first do scraping by running individual scrap files and then host it
