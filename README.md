# Online Store — Django Backend

## Description

This project represents the backend of an online store, built using **Django** and **Django REST Framework**. It provides APIs for managing products, shopping cart, orders, users, and more.

## Features

- Product Search by title with price filtering
- Shopping Cart management (add/edit/remove)
- Order Creation with customer details
- User Registration & Authentication (JWT-based)
- Delivery & Services info via API
- Dynamic design data (logos, product names, etc.)

## Technologies

- Python 3.8+
- Django 3.1.2
- Django REST Framework
- SQLite3
- bcrypt
- UUID
- JSON
- CSRF (Cross-Site Request Forgery)


## Quick Start

## Clone the repository

## bash
git clone https://github.com/ваш-профиль/имя-репозитория.git
cd Online_Store_Django-2.0

## bash
python3 -m venv .venv
source .venv/bin/activate
## for Windows:
.venv\Scripts\activate

## Installation and setup

# Installing dependencies
pip install -r requirements.txt

# Applying migrations
python manage.py migrate

# Creating a superuser
python manage.py createsuperuser

# Starting the server
python manage.py runserver


