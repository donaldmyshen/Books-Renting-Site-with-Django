# Books-Renting-Site-with-Django
An online books renting system built with python Django Framework.

---
# Structure
- Fullstack framework: Django
- Langurage: Python
- Databse: SQLite
---
# Function List
- Account management
    - User login
    - User logout
    - User register
- Book management
    - Borrow books
        - The books have been borrowed will not be shown in library 
        - The books have been borrowed can be check in personal profile
    - Return books
        - The books have been returned will be shown in library again
        - The books have been returned will not be shown in personal profile 
    - Each user will have a limit of borrowing number of books
    - User can search books by name
    - Can filter books by tags/borrow times
    - Can filter books by max cost
    - User can share their own books in libraries, and can get some bonus for this
    - System will charge some fee when return books
    - User can add comments to the books
- Database contains users/books/comments/balance
