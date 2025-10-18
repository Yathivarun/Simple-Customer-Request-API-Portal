# Simple Customer Request API & Portal
This project is a simplified Customer Request System built using FastAPI, vanilla JavaScript, HTML, CSS, and SQLite. It allows customers to submit requests (text or optional audio), manage solutions, and track the status of their requests through a simple web portal and REST API.  

# Video link for a quick project demonstration and working:  
________________________________________
# Table of Contents  
•	[Project Overview](#Project-overview)  
•	[Tech Stack](#Tech Stack)  
•	[Folder Structure](#Folder Structure)  
•	[Getting Started](#Getting Started)  
•	[Setup & Installation](#Setup & Installation)  
•	[Usage](#Usage)  
•	[API Endpoints](#API Endpoints, Using curl (PowerShell))  
•	[Notes](Notes)  
•	[Timeline](#Project Timeline/ Estimation)  
________________________________________  
# Project Overview  
The system has 2 main components:  
1.	Backend REST API (FastAPI)  
Handles customer requests, solutions, and file uploads. Stores all data in a simple SQLite database.  
2.	Frontend Web Portal  
A single-page HTML form where customers can submit requests with text and optional audio files.  
The backend and frontend are integrated so that the portal directly communicates with the API for creating and viewing requests.  
________________________________________  
# Tech Stack  
•	Backend: FastAPI, Python 3.8+  
•	Frontend: HTML, CSS, JavaScript (vanilla)  
•	Database: SQLite  
•	Server: Uvicorn (ASGI server)  
________________________________________  
# Folder Structure  
```
customer_request_api/  
├── app/                  - Backend code  
│   ├── __init__.py  
│   ├── main.py           - FastAPI app entry point  
│   ├── models.py         - Database models  
│   ├── schemas.py        - Pydantic schemas  
│   ├── crud.py           - CRUD operations  
│   └── database.py       - Database connection  
├── templates/            - Frontend HTML files  
│   └── index.html  
├── uploads/              - audio uploads from customers  
├── venv/                 - Python virtual environment (not included in repo)  
├── requests.db           - SQLite database  
├── requirements.txt      - Python dependencies  
└── README.md             - Project documentation
```
________________________________________  
# Getting Started  
These instructions help to run the project locally for development or testing.  
Prerequisites  
•	Python 3.8+  
•	pip (Python package installer)  
________________________________________  
# Setup & Installation  
1. Clone the Repository
```
git clone <your-repository-url>  
cd customer_request_api
```
2. Create and Activate Virtual Environment  
Windows (PowerShell):
``` 
python -m venv venv  
.\venv\Scripts\activate
```
  (note: if execution of scripts is disabled on system, use the below command to temporarly run the virtual environment:  
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process )
```
  macOS/Linux: 
```
python3 -m venv venv  
source venv/bin/activate
```
3. Install Dependencies
```
pip install -r requirements.txt
``` 
________________________________________  
# Usage  
1. Initialize the Database  
The database initializes automatically when the server is started for the first time.  
A file named requests.db will be created in the project root. (to see the content of database use SQLite view extension for VScode or any other SQLite software)  
2. Start the FastAPI Server
```
uvicorn app.main:app --reload
```
Access the portal in your browser at:  
http://127.0.0.1:8000
________________________________________  
# API Endpoints, Using curl (PowerShell)  
make sure the server is running. Try submitting a sample request from the web portal at http://127.0.0.1:8000 (this will also give you some data to work with)  
For the examples below, let’s assume the request created has an ID of 1.  

1. Create a New Request  
This endpoint is used by the web form to create a new customer request.  
•	How to Test: Go to http://127.0.0.1:8000 in your browser and submit the form.

2. View All Requests  
This endpoint fetches a list of every request in the database.  
o	To get all requests:
```  
curl "[http://127.0.0.1:8000/requests/](http://127.0.0.1:8000/requests/)"
```
  o	To get only the "open" requests:  
```
curl "[http://127.0.0.1:8000/requests/?status=open](http://127.0.0.1:8000/requests/?status=open)"
```

4. View a Single Request  
This endpoint fetches the details for one specific request.  
(This command gets the request with an ID of 1.)
```
curl "[http://127.0.0.1:8000/requests/1](http://127.0.0.1:8000/requests/1)"
```

6. Listen to an Audio File  
This endpoint lets you listen to the audio file attached to a request.  
•	How to Test:  
  o	First, get the details of a request that has an audio file (using the step above).  
  o	Open this URL directly in your web browser, replacing 1 with the correct ID: http://127.0.0.1:8000/requests/1/audio  
  o	Your browser should start playing the audio file.

7. Add a Solution to a Request  
This endpoint adds a solution from a volunteer to an existing request.   
(This command adds a solution to the request with ID 1.)
```
curl -Method POST -Uri "[http://127.0.0.1:8000/requests/1/solutions](http://127.0.0.1:8000/requests/1/solutions)" -Headers @{"Content-Type"="application/json"} -Body '{"volunteer_name": "Alice", "solution_text": "Please try restarting your computer."}'
```
  
9. Close a Request  
This endpoint marks a request as "closed."  
(command close to request with ID 1.)
```
curl -Method PUT -Uri "[http://127.0.0.1:8000/requests/1/close](http://127.0.0.1:8000/requests/1/close)"
```

________________________________________  
# Notes  
•	Audio files uploaded by customers are stored in the uploads/ folder.  
•	The portal is a single-page application.  
•	This project is designed to be iterative and scalable.
________________________________________  
# Project Timeline/ Estimation  

Day 1     :- Backend setup & database creation [15-OCT]  
Day 2     :- Implement API endpoints [16-OCT]  
Day 3     :- Frontend form & integration with backend [17-Oct]  
Day 4     :- Testing, bug fixes, and documentation [18-OCT]  
