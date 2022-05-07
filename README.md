# Chattucino

## Description
Chattucino is a web-based application that can be used to organise coffee-catch-ups with friends.

The application has been deployed to Heroku and can be found at:
    https://chattucino-app.herokuapp.com/

Known issues with the applicaiton are also listed at the bottom of this page.

## Design
---
### **Current Status**
Currently a user can:
    Create an account/Sign Up
    Login/Logout
    Post a new "Chattucino" meet-up
        Location
        Date
        Purpose
    Update user profile details
    Show interest in attending a meet-up
    Approve request of other users to join a meet-up

### **Future Features**
There is scope to implement AWS S3 to upload and display photos of a meet-up after it has been completed.

Javascript is not currently utilised but can be added to improve usability of the webpages.

Chattucino can be expanded for use outside of Australia however, currently Australia is hardcoded in the app.py file when calling map.py functions.

### Approach Taken
Broke project down to phases:
1. Initial Design Concept: core concept mock-up diagram and pseudocode
2. PostgreSQL Tables: Mock up of 5 tables to achieve functionality outlined in phase 1 with INNER JOINs experimented conceptually
3. Home Page Front End: Created basic HTML, CSS for layout
4. Implemented user profiles and signup/login functionality
5. Jinja Conditionals/Loops: Implemented conditionals and loops in Jinja to display correct data depending on user login
6. Javascript Implementation: Use of javascript to apply smoother UI experience
7. Test, Bug-fix & fine-tune: Test several scenarios, fix bugs found in testing and user feedback, fine-tune user experience.

## Languages & Libraries
---
Chattucino utilises Python, HTML, CSS and SQL (postgreSQL) languages. 

Python 3.6 is required.

**Libraries**:
* flask
* psycopg2
* bcrypt
* requests
* datetime

## APIs
---
Chattucino leverages the Open Weather Map and Bing Maps free tier APIs.

A unique API Key will be required by signing up. 

    Open Weather Map
        Portal: https://openweathermap.org/api
        Documentation: https://openweathermap.org/price#weather

    Bing Maps 
        Portal: https://www.bingmapsportal.com/
        Documentation: https://docs.microsoft.com/en-us/documentation/


_NOTE: Bing Maps will require a Microsoft account_
_NOTE: API keys are stored in weather.py and map.py files_

## Usage
---
Create a database in psql named chattucino and load the schema to generate necessary tables

    CREATE DATABASE chattucino;
    psql -d library < schema.sql

Install required libraries for use:

    source venv/bin/activate
    pip install -r requirements.txt

## Image Attribution
---
The application logo was obtained from https://pixabay.com/

## Known Issues
---
When creating a new post ('Brew a new Chattucino') the user must enter a street, suburb and state. The application does not check if this is a real location and can sometimes fail to find the location using the Bing Maps API. By giving a street, suburb AND state the problem is minimised so that duplicate suburbs etc. are less of a problem.

Currently there is no check for duplicate names (an input to the sign-up form). This will lead to problems where users with duplicate names may have admin privileges in some features of the program. The extent of this has been minimised by utilising the user_id from the users table in postgreSQL for most of the admin checks. 