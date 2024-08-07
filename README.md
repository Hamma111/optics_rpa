# Project Overview
This Django project is designed to manage optical and IEHP orders efficiently. It includes functionalities to handle order submissions, process CSV data, and automate form submissions using Selenium.

## Features
### Optical Orders Management:

Handles optical PIA orders with details such as subscriber information, prescription details, and frame specifications.
Allows order creation from CSV data.
### IEHP Orders Management:

Manages IEHP orders with appointment details and medical codes.
Provides automation for vision referral requests using Selenium.
### Dashboards:

Provides user-specific dashboards for viewing and managing order submissions.

## Models
OpticalPIAOrder: Manages optical order details including prescription and frame information.
IEHPOrder: Manages IEHP order details including appointment and medical information.

## Views
PIASubmissionsDashboardView: Displays a dashboard for Optical PIA order submissions.
IEHPSubmissionsDashboardView: Displays a dashboard for IEHP order submissions.


## Installation
1. Clone the repository.
2. Install the required dependencies.
3. Set up your database.
4. Configure the necessary environment variables.
5. Run the development server.

## Usage
Navigate to the respective dashboards to view and manage orders.
Use the automated processes to handle CSV uploads and form submissions.


# Technical Documentation

## Tech Stack

### Backend

- Language: Python
- Backend: Django Rest Framework
- Task Management Queue: Redis
- Asynchronous Task: Celery w/ Flower
- Scheduled Task: Celery Beats

### Cloud

- Cloud: Dockerized. Have Docker and Docker Compose file.
- Backend WSGI serving: Gunicorn
- Traffic Handler: NGINX


