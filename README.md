# Expense Splitting System

## Overview

The Expense Splitting System is a Django-based web application that allows users to split expenses among multiple participants. It provides an API endpoint for splitting expenses based on different methods such as EQUAL, EXACT, and PERCENT. This README file provides an overview of the system's design, including its API contracts, class structure, installation, usage, and license information.


## API Contracts

### Endpoint: http://localhost:8000/api/

#### Request

- Method: POST
- Description: Split expenses among users based on different methods.
- Body:
  ```json
  {
    "paid_by_user": <user_id>,
    "total_amount": <total_amount>,
    "split_method": "<split_method>",
    "participants": [<participant1_id>, <participant2_id>, ...],
    "exact_amounts": {
      "<participant1_id>": <exact_amount1>,
      "<participant2_id>": <exact_amount2>,
      ...
    },
    "percent_splits": {
      "<participant1_id>": <percent_share1>,
      "<participant2_id>": <percent_share2>,
      ...
    }
  }

### Response
- Status: 201 Created
- Body:
{
  "message": "Expense split successfully",
  "participants": [<participant1_name>, <participant2_name>, ...],
  "total_amount": <total_amount>,
  "split_method": "<split_method>"
}

### Class Structure
### SplitExpenseAPIView
- Description: API endpoint for splitting expenses among users.
- Methods:
    - post: Handles POST requests to split expenses among users.
#### send_email_async
- Description: Asynchronous method to send email notifications to participants.
- Parameters:
   - participants: List of participant IDs.
   - total_amount: Total amount of the expense.
   - split_method: Method used to split the expense.

## Installation and Usage
1.Clone the repository:
 git clone <repository_url>

2.Install requirements:
pip install -r requirements.txt

3.Run the Django development server:
python manage.py runserver

4.Access the API endpoint at http://localhost:8000/api/




