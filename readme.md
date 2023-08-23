## Track Corporate Asset Management System

#### Goals
- The application might be used by several companies
- Each company might add all or some of its employees
- Each company and its staff might delegate one or more devices to employees for
- a certain period of time
- Each company should be able to see when a Device was checked out and returned
- Each device should have a log of what condition it was handed out and returned

#### Installation Process
- git clone https://github.com/WasekSamin/repliq_asset_management_tracker.git
- To activate virtual environment, on windows: myenv/Scripts/activate.bat and on linux: source myenv/bin/activate
- pip install -r requirements.txt
- python manage.py makemigration
- python manage.py migrate
- python manage.py runserver
- API URL: http://127.0.0.1:8000/api/swagger/
- Doc URL: http://127.0.0.1:8000/api/redoc/
- To test the project: python manage.py test
- Adminpanel URL: http://127.0.0.1:8000/admin/ where username=sam and password=admin12345