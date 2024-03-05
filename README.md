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

- brew install pipx
- pipx ensurepath
- pipx install poetry
- poetry new flask-api-book-store
- poetry add flask flask-sqlalchemy flask-smorest psycopg2 python-dotenv
- touch .env .flaskenv .gitignore
- DEVELOP THE API
- poetry shell => activate the virtual environment
- flask run

- login to elephantSQL and create a new database
- copy the database URL to .env file, BUT rename `postgres` to `postgresql`
- install DBeaver

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

### Environment

- Local
- Production

### Validation

- client-side validation
- server-side validation
- database-level validation

### Docker

- docker build -t pojan-flask-api-book-store .
- docker run -p 5000:5000 -w /app -v "$(pwd):/app" pojan-flask-api-book-store sh -c "flask run --host 0.0.0.0"

### Unit test

- poetry add pytest pytest-cov
- pytest
- pytest --cov
- pytest --cov-report term-missing --cov=resources tests/
- pytest --cov-report term-missing --cov=models tests/

### Migration

- poetry add flask-migrate
- modify app.py
- flask db init
- flask db migrate
- flask db upgrade

### Table Relationship

- User
- Book
- Review

- User-Book (Many-to-Many)
    - User-Review (One-to-Many)
    - Book-Review (One-to-Many)

- https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/
- https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef

## Authentication

- Basic Authentication
- Token Authentication (Stateful)
    - `Session` based
    - Flask-Login
- Token Authentication (Stateless)
    - JWT (JSON Web Token)
    - Flask-JWT-Extended
- API Key Authentication
- OAuth2 Authentication

- lets-go-further/html/15.01-authentication-options.html
- https://blog.bytebytego.com/p/password-session-cookie-token-jwt
- https://blog.bytebytego.com/p/password-session-cookie-token-jwt-ec1
- http://cryto.net/%7Ejoepie91/blog/2016/06/13/stop-using-jwt-for-sessions/

- poetry add flask-login flask-jwt-extended passlib