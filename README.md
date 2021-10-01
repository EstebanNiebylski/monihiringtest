# monihiringtest

Use python 3.8.10

1) Clone the repository
2) Requirements: Go to the root of the project and run: pip install -r requirements.txt
3) In moni_loans/settings.py: Add django secret key (SECRET_KEY line 26) and moni credential (MONI_API_KEY line 34)
4) Models: Go to /moni_loans/ and excecute in the console: python manage.py migrate
5) Admin user: 
  You can create it, run: python manage.py createsuperuser
  or,
  Import the fixture in moni_loan/user/fixture.json
  6) Start App: In /moni_loans/ run "python manage.py runserver".
    The server run in http://127.0.0.1:8000/
    
The app run in DEBUG=True, for test it with the front end go to: The server run in http://127.0.0.1:8000/

A postman collection is provided for use too.

  
