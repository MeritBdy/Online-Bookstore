BookStream: My Online Bookstore Project

Welcome to BookStream! This is a full-stack web application I built for my Web Technology project. It’s a complete digital bookstore where users can browse a catalog, search for their favorite books, and manage a shopping cart, while admins have full control over the inventory.

Project Overview
I built this project to solve the challenge of managing a physical book collection digitally. It features a modern, responsive frontend and a powerful Flask-based backend with a relational MySQL database.


Key Features
* User Authentication: Secure Sign-up and Login system with protected routes.
* Real-time Search: A smart search bar that filters books by title or author instantly.
* Admin Dashboard (CRUD): A private area for admins to *Create, Read, Update, and Delete* books from the store.
* Shopping Cart: Users can add books to their cart and manage their selections.
* Fully Responsive: The site looks great on mobile, tablet, and desktop thanks to Bootstrap 5.


Tech Stack
* Frontend: HTML5, CSS3, Bootstrap 5, JavaScript (jQuery).
* Backend: Flask (Python) with Jinja2 Templating.
* Database: MySQL (interconnected tables for Users, Books, and Orders).
* Version Control: Git & GitHub.


 Repository Structure
```text
BookStream/
├── app.py              # Main Flask application logic
├── bookstream_db.sql   # Database export (SQL Dump)
├── requirements.txt    # Python dependencies
├── .gitignore          # Files ignored by Git
├── static/             # CSS, JS, and Book Images
└── templates/          # HTML pages (Home, Login, Admin, etc.)
