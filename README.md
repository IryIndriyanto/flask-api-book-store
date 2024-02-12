### Concepts

- API (Application Programming Interface)
    - Allows different software applications to communicate with each other
- HTTP Methods
    - GET: Retrieve data
    - POST: Create data
    - PUT: Update data
    - DELETE: Delete data
- Database
- ORM (Object-Relational Mapping)
    - Allows to interact with the database without writing SQL queries
- Resources

### Files

- db.py
    - Database configuration
- app.py
    - Application configuration
- models
    - Database models
    - database-level validation
- schemas.py
    - Request validation (api-level validation)
    - Response formatting
- resources
    - API endpoints
    - Request parsing and validation
    - Response formatting
    - Error handling

### Commands

- poetry new flask-api-book-store
- poetry add flask flask-sqlalchemy flask-smorest python-dotenv
- poetry shell
- flask run

### Libraries

- flask: Python web framework
- flask-SQLAlchemy: ORM
- flask-Smorest: Simplify API development
    - Request parsing and validation
    - Response formatting
    - Documentation
    - Error handling
- python-dotenv: Load environment variables from .env file
- psycopg2: PostgreSQL adapter
