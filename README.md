# AIConnector

The purpose of this project is to learn about interfacing with
Chatgpt and Perplexity's API using the openai python library
and using postgresql as the database to store conversations
using the postgresql python library! The project not only sends
questions to ChatGPT or Perplexity, but also stores asked
questions and returned responses. Additionally, extra
information is stored about when the question was asked and
how many times the question has been asked overall. If a
question has been asked already, the stored response is
printed to save unnecessary api calls to Chatgpt and
Perplexity's API.

DISCLAIMER: Every api call made is charged by Chatgpt and Perplexity!

OpenAI Python Library Documentation:
https://pypi.org/project/openai/

Perplexity API Documentation:
https://docs.perplexity.ai/

Perplexity API Tutorial in Python:
https://blog.perplexity.ai/blog/introducing-pplx-api

Link for Available Models for Perplexity:
https://docs.perplexity.ai/docs/model-cards

Datetime Documentation:
https://docs.python.org/3/library/datetime.html

Postgresql Documentation:
https://postgresapp.com/documentation/

Textwrap Documentation:
https://docs.python.org/3/library/textwrap.html

Colorama Documentation:
https://pypi.org/project/colorama/

Levenshtein Python Library Documentation:
https://pypi.org/project/python-Levenshtein/


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
Run the command `createdb ai` to create the new database in postgresql.

Step 3:
Run the command `psql ai` to open a connection to the database.

Step 4:
Run the command `\q` to quit session.

To dump the PostgreSQL openai db:
Run `pg_dump ai >> file_name.sql`

Follow the instructions for setting up and running the project!

Step 1:
Login to your OpenAI account at the following link:
https://platform.openai.com/

Step 2:
Create the API KEY with the name `CHATGPT_API_KEY` at the following link after logging in:
https://platform.openai.com/api-keys

Step 3:
Add your credit card information to your account here:
https://platform.openai.com/account/billing/payment-methods

Step 4:
Add a credit balance of $5 to your account here:
https://platform.openai.com/account/billing/overview

Step 5:
Login to your Perplexity account at the following link:
https://www.perplexity.ai/

Step 6:
Add your credit card information to your account here:
https://www.perplexity.ai/settings/api

Step 7:
Add a credit balance of $5 to your account here:
https://www.perplexity.ai/settings/api

Step 8:
Create an API KEY at the following link by clicking the button generate:
https://www.perplexity.ai/settings/api

Step 9:
Create a .env file and add the enviornment variables `CHATGPT_API_KEY=` and `PERPLEXITY_API_KEY`

Step 10:
Copy and Paste the api_key values you created from Step 2 and 8 after `CHATGPT_API_KEY=` and `PERPLEXITY_API_KEY=`
e.g. `CHATGPT_API_KEY=generated_api_key_value_from_openai`
e.g. `PERPLEXITY_API_KEY=generated_api_key_value_from_perplexity`

NOTE:
Ensure that you have python installed.

If not, follow the instructions in the following link for installing python:
https://www.python.org/downloads/

For the rest of the instructions:
MacOS/Linux use `pip3` and `python3`
Windows use `pip` and `python`

Step 11:
Run `pip3 install --upgrade pip`
Run `pip3 install -r requirements.txt`

Step 12:
Run `python3 AIConnector.py`

To easily access AIConnector from anywhere, fill in the path to the file and create the following alias:
`alias aicp=python3 /full/path/to/OpenAI/AIConnector.py`

To get the path to where you have AIConnector, open a terminal and change the directory to where
you cloned the AIConnector git repo.

Then run the command:
`pwd`

Copy and paste the output to where `full/path/to` is.
e.g. `/Users/your_user_name/OpenAI/AIConnector.py`
