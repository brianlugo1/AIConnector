# OpenAI
Step 1:
Login to your OpenAI account at the following link:
https://platform.openai.com/

Step 2:
Create an API KEY at the following link after logging in:
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
Copy and Paste the api_key value you created after `OPEN_API_KEY=`
e.g. `OPEN_API_KEY=generated_api_key_value_from_openai`
e.g. `OPEN_API_KEY=sh-121afhdsjaklqtqrquiopreuwxx`

Note:
MacOS/Linux use `pip3` and `python3`
Windows use `pip` and `python`

Step 7:
Run the command `pip3 install --upgrade pip`
Run the command `pip3 install -r requirements.txt`

Step 8:
Run the command `python3 OpenAIConnector.py`

Step 9:
Enter a prompt to ask ChatGPT: e.g. "What is the meaning of life?"
Enter `exit` to exit out of the program!