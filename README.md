# TripWise – Trip Management System

## About the Project

TripWise is a Django REST Framework based trip management application that allows users to create and manage trips and handle trip members.

The project provides REST APIs for managing trip information, user authentication and trip membership.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- REST API
- Basic Authentication

## Features

- User Registration
- User Listing
- User Authentication
- Create and Manage Trips
- View Trip Details
- Update and Delete Trips
- Add Members to Trips
- Manage Trip Members
- Custom Permissions
- Trip Ownership Validation
- Duplicate Member Validation

## Installation and Setup

1. Clone the repository:

   git clone YOUR_GITHUB_REPOSITORY_URL

2. Navigate to the project folder:

   cd TripWise

3. Create a virtual environment:

   python -m venv venv

4. Activate the virtual environment:

   venv\Scripts\activate

5. Install the required packages:

   pip install -r requirements.txt

6. Create a `.env` file in the main project folder and configure your Django SECRET_KEY:

   SECRET_KEY=your_secret_key

7. Apply database migrations:

   python manage.py migrate

8. Run the development server:

   python manage.py runserver

## API Testing

The APIs can be tested using tools such as:

- Postman
- VS Code REST Client

API request examples are available in the `APIDOC.http` file.

## Project Structure

- TripMaster – Django application containing models, serializers, views and permissions.
- TripWise – Main Django project configuration.
- manage.py – Django management utility.
- requirements.txt – Project dependencies.
- .gitignore – Files excluded from Git tracking.