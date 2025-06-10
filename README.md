## Purpose
A streamlined and intuitive web application designed to help users manage their personal finances by tracking income and expenses, visualizing spending patterns, and generating insightful financial summaries. 

# Features

## 1. User-Friendly Dashboard
- Displays real-time expense and income data with interactive bar graphs.
- Offers graph type and date range customization.
- Highlights spending trends and over-budget warnings.
- Includes dark mode and light mode toggle for accessibility.
- Set monthly budgets per category.
- View budget progress bars with green for under budget and red for over budget.
- Display real-time spending vs. budget.
- Easily delete budget entries.
![image](https://github.com/user-attachments/assets/b3e28a18-9169-429e-a824-71145f6d0221)
![image](https://github.com/user-attachments/assets/49311ca3-d666-4dfd-a400-4dd67bd3c194)


### 2. Login/Sign-Up
- Simple and clean login and registration interfaces using Django authentication.
- Custom error messages for invalid login attempts or incorrect credentials.
- Password reset support via email (Django-compatible if email backend is configured).
- Set/Reset Password page to define a new password securely.
- Built-in session management — users stay logged in across pages and can securely log out.
![image](https://github.com/user-attachments/assets/832015c0-c67d-41f4-bb73-0e345f0213f9)

## 3. Expenses Page
- View a table of recorded expenses with clear columns for amount, category, description, and date.
- Search expenses using keywords.
- Filter by 1 month, 6 months, 1 year, or lifetime
- Inline edit and delete functionality for each record.
![image](https://github.com/user-attachments/assets/90fc0007-c95b-4ea1-bd91-d2c818168982)


## 4. Income Page
- View a table of recorded incomes with clear columns for amount, category, description, and date.
- Search incomes using keywords.
- Filter by 1 month, 6 months, 1 year, or lifetime
- Inline edit and delete functionality for each record.
![image](https://github.com/user-attachments/assets/12025405-2f56-46c7-87b1-4e45989e7812)

## 5. Summary
- Visualize spending by category across selectable time ranges.
- Choose different graph types: Bar, Pie, Line, etc.
- Dynamically fetches and plots category-wise totals.
- Responsive and animated for better UX.
![image](https://github.com/user-attachments/assets/83c3159c-bf32-44e8-ba6d-e3e5883ad887)
![image](https://github.com/user-attachments/assets/5aa0a570-78a2-4f8c-ba22-b677315bc093)

### 6. Export
- PDF
  ![image](https://github.com/user-attachments/assets/2cd51d2e-9e9c-4c11-b6d2-0e375fc3cb2b)
  
- Excel
  ![image](https://github.com/user-attachments/assets/7b11c500-5072-4157-bd4b-8f705eac8392)

- CSV
  ![image](https://github.com/user-attachments/assets/3d829122-0581-45e6-b860-a1bf7076169f)

 
## 7. General Settings
- Set preferred currency (e.g., CAD).
- Add custom income sources and expense categories.
- Instantly reflects changes throughout the app.
- Edit or remove sources/categories as needed.
![image](https://github.com/user-attachments/assets/6100024b-8c19-4112-ad9f-5831ec5f2f03)



## Installation
Follow these steps to set up FinanceTracker locally:

```bash

# 1. Clone the repository
git clone https://github.com/Richard-Xu-86/FinanceTracker.git
cd FinanceTracker

# 2. (Optional but recommended) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Set up the database
python manage.py makemigrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver

```If you encounter environment variable errors (e.g. related to SECRET_KEY, EMAIL_HOST_USER, etc.), make sure to:

Rename or copy env.txt to .env
Open .env and fill in the following variables with your values:

SECRET_KEY=your_django_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_app_password
DEBUG=True

Make sure this .env file is located at the root of the project (FinanceTracker/) and is listed in .gitignore.

## For any query feel free to contact 
richardxubusiness@gmail.com

