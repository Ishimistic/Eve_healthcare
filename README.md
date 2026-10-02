# Diagnostic Booking System

A backend REST API for managing diagnostic centres, diagnostic tests, user authentication, bookings, mock payments, and payment webhooks.

The system is built using **FastAPI, PostgreSQL, SQLAlchemy, Alembic, and JWT-based authentication**.

---

## Features

- JWT-based authentication
- Access and refresh tokens
- Refresh token rotation
- Password hashing using Argon2
- Role-based access control
- USER and ADMIN roles
- Diagnostic centre management
- Diagnostic test management
- Centre-test many-to-many relationship
- Test-specific pricing for each diagnostic centre
- Diagnostic test booking
- Timestamp-based double-booking prevention
- Booking cancellation
- Mock payment processing
- Payment status tracking
- Idempotent payment webhooks
- Pagination for collection APIs
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Docker-based PostgreSQL setup
- Swagger/OpenAPI documentation

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Alembic | Database migrations |
| JWT | Authentication |
| Argon2 | Password hashing |
| Docker | PostgreSQL containerization |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |

---

# Architecture

The application follows a layered architecture:

```text
Client
  |
  v
FastAPI Router
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
SQLAlchemy
  |
  v
PostgreSQL
```


# Responsibilities
### Router
Responsible for:
- HTTP endpoints
- Request validation
- Authentication dependencies
- Authorization
- HTTP status codes
- Returning API responses

### Service
Contains business logic such as:
- Booking validation
- Payment processing
- Centre-test relationships
- Authentication logic
- Double-booking prevention

### Repository
Responsible for database operations such as:
- Fetching records
- Creating records
- Updating records
- Deleting records
This keeps database access separate from business logic.


# Project Structure
```bash
project-root/
│
├── app/
│   │
│   ├── api/
│   │   ├── router.py
│   │   │
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── centre.py
│   │       ├── test.py
│   │       ├── admin_centre.py
│   │       ├── admin_centre_test.py
│   │       ├── booking.py
│   │       ├── payment.py
│   │       └── webhook.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── refresh_token.py
│   │   ├── diagnostic_centre.py
│   │   ├── diagnostic_test.py
│   │   ├── centre_test.py
│   │   ├── booking.py
│   │   ├── payment.py
│   │   └── webhook_event.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── centre.py
│   │   ├── centre_test.py
│   │   ├── test.py
│   │   ├── booking.py
│   │   ├── payment.py
│   │   └── webhook.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── centre_repository.py
│   │   ├── centre_test_repository.py
│   │   ├── booking_repository.py
│   │   ├── payment_repository.py
│   │   └── webhook_repository.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── centre_service.py
│   │   ├── centre_test_service.py
│   │   ├── booking_service.py
│   │   ├── payment_service.py
│   │   └── webhook_service.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   └── ...
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```


# Database Design

## 1. Overview

The application uses **PostgreSQL** as the primary relational database.

The database is designed to support:

- User registration and authentication
- Role-based access control
- Diagnostic centres
- Diagnostic tests
- Centre-specific test pricing
- Test bookings
- Appointment slot management
- Payments
- Payment webhooks
- Webhook idempotency
- Data integrity and consistency
- Pagination
- Future scalability

The application uses:

- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Alembic** — database migration management

---

## 2. High-Level Database Architecture

```text
                         ┌─────────────────┐
                         │      users      │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌─────────────────┐        ┌─────────────────┐
          │ refresh_tokens  │        │    bookings     │
          └─────────────────┘        └────────┬────────┘
                                               │
                         ┌─────────────────────┼─────────────────────┐
                         │                     │                     │
                         ▼                     ▼                     ▼
               ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
               │ diagnostic_     │   │  centre_tests   │   │    payments     │
               │    centres     │   └────────┬────────┘   └─────────────────┘
               └─────────────────┘            │
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ diagnostic_     │
                                    │     tests       │
                                    └─────────────────┘


                         ┌─────────────────┐
                         │ webhook_events │
                         └─────────────────┘
```

## 3. Main Entities
The database contains the following major entities:

| Table | Purpose |
|---|---|
| `users` | Stores application users and their roles |
| `refresh_tokens` | Stores hashed refresh tokens |
| `diagnostic_centres` | Stores diagnostic centre information |
| `diagnostic_tests` | Stores available diagnostic tests |
| `centre_tests` | Connects diagnostic centres with tests and stores prices |
| `bookings` | Stores user appointment bookings |
| `payments` | Stores payment information |
| `webhook_events` | Stores payment webhook events for idempotency |


## 4. Entity Relationship Diagram

```bash
┌──────────────────────┐
│        users         │
├──────────────────────┤
│ PK id                │
│ name                 │
│ email                │
│ password_hash        │
│ role                 │
│ created_at           │
│ updated_at           │
└──────────┬───────────┘
           │
           │ 1
           │
           ├───────────────────────┐
           │                       │
           │ N                     │ N
           ▼                       ▼
┌──────────────────────┐   ┌──────────────────────┐
│   refresh_tokens     │   │      bookings        │
├──────────────────────┤   ├──────────────────────┤
│ PK id                │   │ PK id                │
│ FK user_id           │   │ FK user_id           │
│ token_hash           │   │ FK centre_test_id    │
│ expires_at           │   │ booking_date         │
│ revoked_at           │   │ booking_time         │
│ created_at           │   │ status               │
└──────────────────────┘   │ created_at           │
                           │ updated_at           │
                           └──────────┬───────────┘
                                      │
                                      │ N
                                      ▼
                           ┌──────────────────────┐
                           │    centre_tests      │
                           ├──────────────────────┤
                           │ PK id                │
                           │ FK centre_id         │
                           │ FK test_id           │
                           │ price                │
                           └─────────┬────────────┘
                                     │
                         ┌───────────┴───────────┐
                         │                       │
                         │ N                     │ N
                         ▼                       ▼
              ┌──────────────────┐   ┌──────────────────┐
              │ diagnostic_      │   │ diagnostic_      │
              │ centres          │   │ tests            │
              ├──────────────────┤   ├──────────────────┤
              │ PK id            │   │ PK id            │
              │ name             │   │ name             │
              │ location         │   │ description      │
              │ is_active        │   │ is_active        │
              │ created_at       │   │ created_at       │
              │ updated_at       │   │ updated_at       │
              └──────────────────┘   └──────────────────┘


                     ┌──────────────────────┐
                     │       payments       │
                     ├──────────────────────┤
                     │ PK id                │
                     │ FK booking_id        │
                     │ provider_payment_id  │
                     │ amount               │
                     │ status               │
                     │ created_at           │
                     │ updated_at           │
                     └──────────────────────┘


                     ┌──────────────────────┐
                     │    webhook_events    │
                     ├──────────────────────┤
                     │ PK id                │
                     │ event_id             │
                     │ payment_id           │
                     │ status               │
                     │ processed_at         │
                     └──────────────────────┘
```


# Environment
Create a .env file in the project root.
Example:
```bash
POSTGRES_USER=app_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=diagnostic_booking
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```
Do not commit .env to Git.
Use .env.example for sharing the required configuration structure.


# Python Environment Setup
Create a virtual environment:
```bash
python -m venv venv
```
Activate it on Windows:
```bash
venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```

# Database Migrations
Alembic is used for database schema management.

Apply all migrations:
```bash
alembic upgrade head
```

Create a new migration after changing models:
```bash
alembic revision --autogenerate -m "describe change"
```
Then apply it:
```bash
alembic upgrade head
```



# Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The API will be available at:
```bash
http://127.0.0.1:8000
```


# API Documentation
FastAPI automatically provides Swagger UI.
Open:
```bash
http://127.0.0.1:8000/docs
```





# Double-Booking Prevention
The booking system prevents two bookings from being created for the same appointment slot.
The booking service checks for an existing booking using the relevant centre/test/time combination before creating a new booking.
Conceptually:
```bash
User A
   |
   | 10:00 AM
   v
Centre 1 + Test 1
   |
   v
Booking created


User B
   |
   | 10:00 AM
   v
Centre 1 + Test 1
   |
   v
Existing booking found
   |
   v
Booking rejected
```

The current implementation uses timestamp-based booking validation.

# Payment APIs
The project uses a mock payment system.
No real payment provider is integrated.
The purpose is to demonstrate:
- Payment creation
- Payment status handling
- Booking state transitions
- Webhook processing
- Webhook idempotency


# Payment Webhook
The webhook simulates a payment provider notifying the backend about a payment status change.
Example webhook payload:
```bash
{
  "event_id": "evt_test_001",
  "payment_id": "pay_123456789",
  "status": "SUCCESS"
}
```

The important field is:
```bash
event_id
```

The event_id identifies a particular webhook event.
It should normally be generated by the payment provider, not by the end user.
Because this project uses a mock payment provider, an event ID can be manually supplied while testing the webhook.


# Webhook Idempotency
Webhook processing is idempotent.
If the same webhook is received multiple times:
```bash
Request 1
event_id = evt_test_001
       |
       v
Process event
       |
       v
Store event_id


Request 2
event_id = evt_test_001
       |
       v
Event already exists
       |
       v
Do not process again
```
This prevents duplicate payment processing when a payment provider retries the same webhook.

# Payment Flow
The complete payment flow is:
```bash
User
 |
 | Create booking
 v
Booking
 |
 | Create mock payment
 v
Payment
 |
 | Payment provider processes payment
 v
Webhook
 |
 | event_id
 v
Webhook validation
 |
 | SUCCESS
 v
Payment updated
 |
 v
Booking CONFIRMED
```

Pagination
Collection endpoints support pagination.
Example:
```bash
GET /api/v1/centres/?page=1&limit=10
```
The pagination response contains the collection data along with pagination information according to the application's PaginatedResponse schema.
Pagination is used to avoid returning an unnecessarily large number of records in a single request.


# Admin Setup
A newly registered user is created as a normal USER.
To promote a user to ADMIN, update the role directly in PostgreSQL.
Example:
```bash
UPDATE users
SET role = 'ADMIN'
WHERE email = 'admin@example.com';
```

Verify:
```bash
SELECT id, name, email, role
FROM users
WHERE email = 'admin@example.com';
```

After changing the role, log in again to obtain a fresh access token.



# API Documentation

Base URL:

```text
http://127.0.0.1:8000/api/v1
```
Interactive Swagger documentation:
```bash
http://127.0.0.1:8000/docs
```
For protected endpoints, use:
```bash
Authorization: Bearer <access_token>
```

## Authentication APIs
### Register User
Creates a new user account.
Endpoint
```bash
POST /api/v1/auth/register
```
Request
```bash
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Password123!"
}
```

Response
```bash
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "USER"
}
```


### Login
Authenticates a user and returns an access token and refresh token.
Endpoint
```bash
POST /api/v1/auth/login
```
Request
```bash
{
  "email": "john@example.com",
  "password": "Password123!"
}
```

Response
```bash
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "USER"
  }
}
```

Status Codes
- 200 OK
- 401 Unauthorized
- 422 Validation Error

### Refresh Token
Generates a new access token and refresh token using a valid refresh token.
Refresh token rotation is used, meaning the old refresh token is revoked when a new token pair is issued.
Endpoint
```bash
POST /api/v1/auth/refresh
```
Request
```bash
{
  "refresh_token": "<refresh_token>"
}
```

Response
```bash
{
  "access_token": "<new_access_token>",
  "refresh_token": "<new_refresh_token>",
  "token_type": "bearer"
}
```

Status Codes
- 200 OK
- 401 Unauthorized
- 422 Validation Error

### Get Current User
Returns information about the currently authenticated user.
Endpoint
```bash
GET /api/v1/auth/me
```
Headers
```bash
Authorization: Bearer <access_token>
```
Example
```bash
GET /api/v1/auth/me
Authorization: Bearer eyJ...
```
Response
```bash
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "USER"
}
```

Status Codes
- 200 OK
- 401 Unauthorized

### Logout
Revokes the supplied refresh token.
Endpoint
```bash
POST /api/v1/auth/logout
```
Request
```bash
{
  "refresh_token": "<refresh_token>"
}
```

Response
```bash
204 No Content
```
Status Codes
- 204 No Content
- 401 Unauthorized
- 422 Validation Error

## Diagnostic Centre APIs
These endpoints are publicly accessible.
### List Diagnostic Centres
Returns a paginated list of diagnostic centres.
Endpoint
```bash
GET /api/v1/centres/
```

Query Parameters
```bash
page       = 1
page_size  = 20
```
page_size can be between 1 and 100.
Example
```bash
GET /api/v1/centres/?page=1&page_size=20
```
Response
```bash
{
  "items": [
    {
      "id": 1,
      "name": "City Diagnostic Centre",
      "location": "Delhi",
      "is_active": true,
      "created_at": "2026-10-02T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

Status Codes
- 200 OK
- 422 Validation Error

### Get Diagnostic Centre
Returns a diagnostic centre by ID.
Endpoint
```bash
GET /api/v1/centres/{centre_id}
```
Example
```bash
GET /api/v1/centres/1
```
Response
```bash
{
  "id": 1,
  "name": "City Diagnostic Centre",
  "location": "Delhi",
  "is_active": true,
  "created_at": "2026-10-02T10:00:00"
}

```

Status Codes
- 200 OK
- 404 Not Found

## Diagnostic Test APIs
These endpoints are publicly accessible.
### List Diagnostic Tests
Returns a paginated list of diagnostic tests.
Endpoint
```bash
GET /api/v1/tests/
```
Query Parameters
```text
page       = 1
page_size  = 20
```
page_size can be between 1 and 100.
Example
```bash
GET /api/v1/tests/?page=1&page_size=20
```
Response
```bash
{
  "items": [
    {
      "id": 1,
      "name": "Complete Blood Count",
      "description": "Measures different components of blood.",
      "is_active": true
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

Status Codes
- 200 OK
- 422 Validation Error

### Get Diagnostic Test
Returns a diagnostic test by ID.
Endpoint
```bash
GET /api/v1/tests/{test_id}
```
Example
```bash
GET /api/v1/tests/1
```
Response
```bash
{
  "id": 1,
  "name": "Complete Blood Count",
  "description": "Measures different components of blood.",
  "is_active": true
}
```

Status Codes
- 200 OK
- 404 Not Found

## Admin APIs

Admin APIs require an authenticated user with the ADMIN role.
All admin requests must include:
Authorization: Bearer <ADMIN_ACCESS_TOKEN>

A normal USER receives:
```bash
403 Forbidden
```
when attempting to access admin-only endpoints.
## Admin Diagnostic Centre APIs
### Create Diagnostic Centre
Creates a new diagnostic centre.
Endpoint
```bash
POST /api/v1/admin/centres/
```
Headers
```bash
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
Content-Type: application/json
```
Request
```bash
{
  "name": "City Diagnostic Centre",
  "location": "Delhi"
}
```

Response
```bash
{
  "id": 1,
  "name": "City Diagnostic Centre",
  "location": "Delhi",
  "is_active": true,
  "created_at": "2026-10-02T10:00:00"
}
```

Status Codes
- 201 Created
- 401 Unauthorized
- 403 Forbidden
- 422 Validation Error

### Update Diagnostic Centre
Updates one or more fields of a diagnostic centre.
Endpoint
```bash
PATCH /api/v1/admin/centres/{centre_id}
```
Headers
```bash
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
Content-Type: application/json
```
Request
```bash
{
  "name": "Updated Diagnostic Centre",
  "location": "Gurgaon",
  "is_active": true
}
```

Partial updates are supported.
```bash
For example:
{
  "location": "Noida"
}
```

Response
```bash
{
  "id": 1,
  "name": "Updated Diagnostic Centre",
  "location": "Gurgaon",
  "is_active": true,
  "created_at": "2026-10-02T10:00:00"
}
```

Status Codes
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error

### Delete Diagnostic Centre
Deletes a diagnostic centre according to the service implementation.
Endpoint
DELETE /api/v1/admin/centres/{centre_id}

Headers
Authorization: Bearer <ADMIN_ACCESS_TOKEN>

Example
DELETE /api/v1/admin/centres/1

Response
204 No Content

Status Codes
204 No Content
401 Unauthorized
403 Forbidden
404 Not Found

## Admin Centre-Test APIs
A diagnostic centre can offer multiple tests, and a diagnostic test can be available at multiple centres.
The relationship between a centre and a test is represented by CentreTest.
The CentreTest relationship also stores the price of the test at that particular centre.
### Add Test to Centre
Adds a diagnostic test to a centre with a specified price.
Endpoint
```bash
POST /api/v1/admin/centres/{centre_id}/tests/
```
Headers
```bash
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
Content-Type: application/json
```

Request
```bash
{
  "test_id": 1,
  "price": 750.00
}
```

Response
```bash
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "price": 750.00
}
```

Status Codes
- 201 Created
- 401 Unauthorized
- 403 Forbidden
- 409 Conflict
- 422 Validation Error

Possible conflicts include:
- Diagnostic centre not found
- Diagnostic centre is inactive
- Diagnostic test not found
- Diagnostic test is inactive
- Test is already available at this centre

### Update Test Price at Centre
Updates the price of a test at a particular diagnostic centre.
Endpoint
```bash
PATCH /api/v1/admin/centres/{centre_id}/tests/{test_id}/
```

Headers
```bash
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
Content-Type: application/json
```

Request
```bash
{
  "price": 800.00
}
```

Response
```bash
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "price": 800.00
}
```

Status Codes
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error

### Remove Test from Centre
Removes a test from a diagnostic centre.
Endpoint
```bash
DELETE /api/v1/admin/centres/{centre_id}/tests/{test_id}/
```
Headers
```bash
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
```
Example
```bash
DELETE /api/v1/admin/centres/1/tests/1/
```
Response
```bash
204 No Content
```

Status Codes
- 204 No Content
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

## Booking APIs
Booking endpoints require an authenticated user.
Authorization: Bearer <ACCESS_TOKEN>

### Create Booking
Creates a diagnostic test booking for the selected centre and time slot.
Endpoint
```bash
POST /api/v1/bookings/
```

Headers
```bash
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

Example Request
```bash
{
  "centre_id": 1,
  "test_id": 1,
  "booking_time": "2026-10-05T10:00:00"
}
```

Example Response
```bash
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "booking_time": "2026-10-05T10:00:00",
  "status": "PENDING"
}
```

The booking process validates:
- The diagnostic centre exists.
- The diagnostic centre is active.
- The diagnostic test exists.
- The diagnostic test is active.
- The selected test is available at the selected centre.
- The requested time slot is not already booked.
The current implementation uses timestamp-based double-booking prevention.

### Get Booking
Returns a booking belonging to the authenticated user.
Endpoint
```bash
GET /api/v1/bookings/{booking_id}
```
Headers
Authorization: Bearer <ACCESS_TOKEN>

Example
```bash
GET /api/v1/bookings/1
```
Response
```bash
{
  "id": 1,
  "centre_id": 1,
  "test_id": 1,
  "booking_time": "2026-10-05T10:00:00",
  "status": "PENDING"
}
```

### List User Bookings
Returns bookings belonging to the authenticated user.
Endpoint
```bash
GET /api/v1/bookings/
```

Headers
```bash
Authorization: Bearer <ACCESS_TOKEN>
```
Example
```bash
GET /api/v1/bookings/?page=1&page_size=20
```


### Cancel Booking
Cancels an existing booking.
Endpoint
```bash
PATCH /api/v1/bookings/{booking_id}/cancel/
```

Headers
```bash
Authorization: Bearer <ACCESS_TOKEN>
```
Example
```bash
PATCH /api/v1/bookings/1/cancel/
```

Example Response
```bash
{
  "id": 1,
  "status": "CANCELLED"
}
```

## Payment APIs
The project currently uses a mock payment implementation.
No real payment gateway is integrated.
### Create Mock Payment
Creates a payment for a booking.
Endpoint
```bash
POST /api/v1/payments/
```

Headers
```bash
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```
Request
```bash
{
  "booking_id": 1
}
```

Response
```bash
{
  "id": 1,
  "booking_id": 1,
  "provider_payment_id": "pay_123456789",
  "status": "PENDING"
}
```

The provider_payment_id represents the payment ID that would normally be generated by an external payment provider.


### Get Payment
Returns payment information.
Endpoint
```bash
GET /api/v1/payments/{payment_id}
```
Headers
```bash
Authorization: Bearer <ACCESS_TOKEN>
```
Example
```bash
GET /api/v1/payments/1
```
Response
```bash
{
  "id": 1,
  "booking_id": 1,
  "provider_payment_id": "pay_123456789",
  "status": "SUCCESS"
}
```

## Payment Webhook APIs
The webhook simulates a payment provider notifying the application about a payment status.
The normal user does not generate the webhook event_id.
In a real payment system, the payment provider generates the event_id.
For local testing, the webhook request can simulate the provider.

### Payment Webhook
Endpoint
```bash
POST /api/v1/webhooks/payment
```
Example Request
```bash
{
  "event_id": "evt_test_001",
  "payment_id": "pay_123456789",
  "status": "SUCCESS"
}
```

 Response
 ```bash
{
  "message": "Webhook processed successfully"
}
```

When a successful payment webhook is processed:
```bash
Payment
   |
   | SUCCESS
   v
Booking
   |
   | CONFIRMED
   v
Confirmed Booking
```

### Webhook Idempotency
The event_id is used to make webhook processing idempotent.
For example, if the same event is received twice:
```bash
{
  "event_id": "evt_test_001",
  "payment_id": "pay_123456789",
  "status": "SUCCESS"
}
```

the application recognizes that evt_test_001 has already been processed and prevents the same payment event from being processed twice.
The application stores processed webhook event IDs in the database.
The event_id belongs to the payment-provider/webhook side, not to the normal user payment request.


# Example API Flow
A typical system flow is:
```bash
1. Register user
       |
       v
2. Login
       |
       v
3. Receive access token
       |
       v
4. Browse diagnostic centres
       |
       v
5. Browse diagnostic tests
       |
       v
6. Select centre + test
       |
       v
7. Create booking
       |
       v
8. Create mock payment
       |
       v
9. Payment webhook
       |
       v
10. Booking becomes CONFIRMED
```

# Admin API Flow
An administrator can manage the diagnostic catalogue:
```bash
Admin Login
     |
     v
Create Centre
     |
     v
Create/Manage Diagnostic Tests
     |
     v
Add Test to Centre
     |
     v
Set Test Price
     |
     v
Update Centre/Test
     |
     v
Remove Centre/Test
```


# Security Considerations
The application implements the following security measures:
- Passwords are never stored as plain text
- Passwords are hashed using Argon2
- JWT secrets are loaded through environment variables
- Access tokens are short-lived
- Refresh tokens have expiration
- Refresh tokens are stored as hashes
- Refresh tokens can be revoked
- Admin endpoints require ADMIN authorization
- Protected endpoints require authentication
- Database credentials are stored through environment configuration
- .env should not be committed to source control


# Running the Project
1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create virtual environment
```bash
python -m venv venv
```

3. Activate virtual environment
Windows:
```bash
venv\Scripts\activate
``
Linux/macOS:
```bash
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Configure environment variables
Create:
```bash
.env
```
using .env.example as a reference.

6. Start PostgreSQL
```bash
docker compose up -d
``

7. Run database migrations
```bash
alembic upgrade head
```
8. Start FastAPI
```bash
uvicorn app.main:app --reload
```
9. Open Swagger
```bash
http://127.0.0.1:8000/docs

```


# API Testing
The APIs can be tested using:
- Swagger UI
- Postman
- Any HTTP client
Recommended testing order:
```bash
1. Register
      ↓
2. Login
      ↓
3. Authorize using access token
      ↓
4. Create/administer diagnostic centres
      ↓
5. Create/manage diagnostic tests
      ↓
6. Map tests to centres
      ↓
7. Set test prices
      ↓
8. Create user booking
      ↓
9. Create mock payment
      ↓
10. Send payment webhook
      ↓
11. Verify payment status
      ↓
12. Verify booking status
```


# Important Assumptions Made

1. PostgreSQL is used as the primary database and source of truth for application data.

2. The system supports two roles: `USER` and `ADMIN`, with admin-only operations protected by role-based authorization.

3. User email addresses are unique, and passwords are stored as secure hashes rather than plain text.

4. Access tokens are short-lived JWTs, while refresh tokens are stored securely as hashes and rotated when refreshed.

5. Diagnostic centres and diagnostic tests have a many-to-many relationship through the `centre_tests` table.

6. Test prices are centre-specific, so the price is stored in `centre_tests` rather than directly in `diagnostic_tests`.

7. Centres and tests can be marked inactive instead of being immediately removed, allowing existing records to remain consistent.

8. A booking belongs to a user and a specific centre-test combination, with appointment date and time identifying the selected slot.

9. The database is assumed to prevent duplicate bookings for the same centre, test, date, and time, providing protection against concurrent booking requests.

10. Payment processing is mocked, and payment webhook events are assumed to contain a provider-generated unique `event_id` so duplicate webhook requests can be detected and processed only once.


# Future Enhancements
Possible future improvements include:
- Redis-based rate limiting
- Webhook retry mechanism
- Structured application logging
- Automated integration/unit tests
- Real payment gateway integration
- Background task processing
- Email/SMS booking notifications
- Advanced appointment slot management
- Monitoring and observability