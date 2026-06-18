# SUBSCRIPTION MONITOR
#### Video Demo: https://youtu.be/fFDCxR-pl3s?si=LKbuiPo_zaQNq84Q

#### Description:
Subscription Monitor is a user-friendly desktop application built using Python. It helps everyday users track their recurring subscriptions, software licenses, and utility bills in one clean, centralized dashboard. 

Unlike a standard Excel spreadsheet or static text list, this application does all the difficult date calculations for you automatically. When you run the application, it looks at your subscription's original start date and checks your computer's live calendar time to tell you exactly when your next payment is due and how many days you have left to prepare.

### Key Features:
- **Bulletproof Date Selection:** Uses clean dropdown menus for Year, Month, and Day to make entering start dates completely error-free.
- **Multi-Currency Support:** Allows you to log costs using different global currencies like Dollars ($), Rupees (₹), Euros (€), Pounds (£), or Yuan (¥).
- **10-Day Critical Alerts:** A dedicated sidebar panel highlights any subscription billing dates landing within the next 10 days in red text so you never get surprised by a charge.
- **Financial Analytics Summary:** Automatically sums up your total active accounts and calculates your total yearly and monthly costs grouped cleanly by currency.
- **Subscription Cancellation Support:** Features a "Cancel / Delete Selected" button that allows you to click any row in your table to wipe out a cancelled subscription from your tracker and update your CSV database file instantly.

### File Breakdown:
1. **`project.py`**: This is the main file containing the Tkinter Dark Mode desktop interface layout, the delete entry system, and the core calendar processing code.
2. **`test_project.py`**: This file contains the automated testing functions used by `pytest` to verify that the app's data validation, date shifting, and row filtering logic are 100% correct.
3. **`requirements.txt`**: A simple text file that lists external packages (`tabulate`) needed to keep text panels organized.
4. **`subscriptions.csv`**: The local database file where all your entries are saved securely so you never lose your data when closing the window.

### What I Learned Outside the Course:
While the CS50P course taught me excellent foundational coding, loops, and file handling, I wanted to learn how to build real desktop software. I independently researched and learned how to build graphical layouts using **Tkinter**. I also learned how to use the **Clam Style Engine** to create a custom dark theme so that all dropdown text elements are perfectly visible, readable, and professional.
