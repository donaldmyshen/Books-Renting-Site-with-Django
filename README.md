# Books-Renting-Site-with-Django
An online books renting system built with python Django Framework.

---
# Manual
Don't know how to start? Check offcial Manual here.
https://docs.djangoproject.com/en/2.2/intro/tutorial01/

```sh
$ python manage.py migrate
```
```sh
$ python manage.py runserver
```

Then you can open the site with your local server:
http://127.0.0.1:8000/homepage/

Or check the database from:
http://127.0.0.1:8000/admin/login/?next=/admin/

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
---
# Demo
![image](https://raw.githubusercontent.com/donaldmyshen/Books-Renting-Site-with-Django/master/Screenshot/1.png)
![image](https://raw.githubusercontent.com/donaldmyshen/Books-Renting-Site-with-Django/master/Screenshot/2.png)
![image](https://raw.githubusercontent.com/donaldmyshen/Books-Renting-Site-with-Django/master/Screenshot/3.png)
![image](https://raw.githubusercontent.com/donaldmyshen/Books-Renting-Site-with-Django/master/Screenshot/4.png)
