# Ecommerce Template

This is a robust and scalable Django-based API template for building an ecommerce application. It provides essential features such as user authentication, product management, cart functionality, order processing, wishlist management, and more. The project is designed with modularity and extensibility in mind, making it easy to customize and expand.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Authentication**: Custom user model with email-based authentication and JWT support.
- **Product Management**: Manage products, categories, subcategories, and sizes.
- **Cart Functionality**: Add, update, and remove items from the cart.
- **Order Processing**: Place and manage orders with detailed order items.
- **Wishlist Management**: Add products to a wishlist for future reference.
- **Pagination**: Custom pagination for API responses.
- **Swagger Documentation**: Auto-generated API documentation using Swagger.
- **Environment-Specific Settings**: Separate configurations for development, staging, and production.
- **Email Notifications**: Email-based OTP verification and notifications.
- **Docker Support**: Dockerized setup for easy deployment.
- **Admin Panel**: Enhanced admin interface using Jazzmin.

---

## Project Structure

```
.
├── api/
│   ├── urls.py
│   └── v1/
├── apps/
│   ├── authentication/
│   ├── cart/
│   ├── orders/
│   ├── payment/
│   ├── products/
│   └── wishlist/
├── config/
│   ├── settings/
│   ├── asgi.py
│   ├── schemas.py
│   ├── urls.py
│   └── wsgi.py
├── deployment/
│   ├── docker-compose.yml
│   └── Dockerfile
├── media/
├── .env
├── .env.examples
├── .gitignore
├── db.sqlite3
├── LICENSE
├── Makefile
├── manage.py
├── README.md
└── requirements.txt
```

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL (for production/staging)
- Docker (optional, for containerized setup)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EcommerceTemplate
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file:
   Copy `.env.examples` to `.env` and update the values as needed.

5. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Environment Variables

The project uses environment variables for configuration. Below are the required variables:

```env
DJANGO_ENV=development  # Options: development, production, staging
BASE_ROUTE=http://127.0.0.1:8000
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL=your-email
PASSWORD=your-email-app-password
FLW_SEC_KEY=your-flutterwave-secret-key

# For production/staging only
NAME=db-name
USER=db-user
DB_PASSWORD=db-password
HOST=db-host
PORT=db-port
```

---

## Usage

### Running with Docker

1. Build and start the containers:
   ```bash
   make up
   ```

2. Stop the containers:
   ```bash
   make down
   ```

3. View logs:
   ```bash
   make logs
   ```

### Running Locally

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Documentation

The project includes auto-generated API documentation using Swagger and Redoc. Access the documentation at:

- Swagger UI: [http://localhost:8000/](http://localhost:8000/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).