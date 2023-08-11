# BudgetTracking_CreditAgricole_Gsheets

Here's the first Python project that I did back in 2020. This repository houses a Python script aimed at collecting diverse banking transactions from an account using the third-party package python-creditagricole-particuliers, developed by [dmachard](https://github.com/dmachard/python-creditagricole-particuliers). The acquired transaction data is then seamlessly integrated into a designated Google Sheets worksheet, which acts as an efficient budget tracking tool. The script makes use of a variety of tools and technologies to accomplish its objectives:

python-creditagricole-particuliers: A Python package created by dmachard, which facilitates access to Credit Agricole account details and transaction records.

gspread: A package that streamlines interactions with Google Sheets, enabling the addition of transaction information into a specified worksheet.

dotenv: A module that loads environment variables from a '.env' file, enhancing security and configuration flexibility.

ServiceAccountCredentials: Enables authentication via a service account JSON keyfile to access Google APIs.

AWS Lambda & EventBridge: The project is hosted on AWS Lambda and triggered at daily intervals through EventBridge, ensuring automated and scheduled execution.

For comprehensive insights, please consult the [Google Sheets Template](https://docs.google.com/spreadsheets/d/1NvhKyCqQK515gzzyhcQUO0TfHJLnYhUB1hptQ-sZAT0/edit?usp=sharing) along with the included code within this repository.

Please be aware that specific packages, credentials, paths, and environment variables must be appropriately configured to ensure the proper functionality of the script within your specific environment.
