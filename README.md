# OpenAIConnector

The purpose of this project is to learn about interfacing with
OpenAI's API using the openai python library and using postgresql
as the database to store conversations using the postgresql python
library! The project not only sends questions to ChatGPT, but also
stores asked questions and returned responses. Additionally, extra
information is stored about when the question was asked and how
many times the question has been asked overall. If a question has
been asked already, the stored response is printed to save
unnecessary api calls to OpenAI's API.

DISCLAIMER: Every api call made is charged by OpenAI!

OpenAI Python Library Documentation:
https://pypi.org/project/openai/

Postgresql Documentation:
https://postgresapp.com/documentation/


Follow the instructions for downloading postgres:
https://postgresapp.com/downloads.html


Follow the instructions for setting up postgres:

Step 1:
To check if you correctly installed postgres, open a new terminal session.

Run the command `psql`.

If you get a message saying command not found, you have not correctly
installed postgress. You will not be able to continue with the
instructions until you correctly install postgres.

Go to the link for help on troubleshooting:
https://postgresapp.com/documentation/troubleshooting.html

Step 2:
Run the command `createdb openai` to create the new database in postgresql.

Step 3:
Run the command `psql openai` to open a connection to the database.

Step 4:
Run the command `\q` to quit session.

Follow the instructions for setting up and running the project!

Step 1:
Login to your OpenAI account at the following link:
https://platform.openai.com/

Step 2:
Create the API KEY with the name `OPEN_API_KEY` at the following link after logging in:
https://platform.openai.com/api-keys

Step 3:
Add your credit card information to your account here:
https://platform.openai.com/account/billing/payment-methods

Step 4:
Add a credit balance of $5 to your account here:
https://platform.openai.com/account/billing/overview

Step 5:
Create a .env file and add the enviornment variable `OPEN_API_KEY=`

Step 6:
Copy and Paste the api_key value you created from Step 2 after `OPEN_API_KEY=`
e.g. `OPEN_API_KEY=generated_api_key_value_from_openai`
e.g. `OPEN_API_KEY=sh-121afhdsjaklqtqrquiopreuwxx`

NOTE:
Ensure that you have python installed.

If not, follow the instructions in the following link for installing python:
https://www.python.org/downloads/

For the rest of the instructions:
MacOS/Linux use `pip3` and `python3`
Windows use `pip` and `python`

Step 7:
Run `pip3 install --upgrade pip`
Run `pip3 install -r requirements.txt`

Step 8:
Run `python3 OpenAIConnector.py`