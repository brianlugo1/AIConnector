# OpenAI

The purpose of this project is to learn about interfacing with
OpenAI's API using the openai python library! The project
currently takes a message entered in stdin and sends the
message to OpenAI. The project then prints the returned
message. Use case for what is learned in this project:
Incorperate OpenAI into your project by creating a
service that takes a message, sends it to OpenAI, and
uses the returned message in your project.

OpenAI Python Library Documentation:
https://pypi.org/project/openai/

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

Step 9:
Enter a prompt to ask ChatGPT: e.g. "What is the meaning of life?"
Enter `exit` to exit out of the program!