# Banking System API
**Production-ready banking system with secure transactions and JWT authentication**

## Overview
A comprehensive banking API built with FastAPI that handles user registration, authentication, 
  and core banking operations (deposits, withdrawals, transfers) with enterprise-level security.

## Key Features
- **Secure Authentication**: JWT tokens with bcrypt password hashing
- **Banking Operations**: Deposit, withdraw, transfer money between accounts
- **Account Management**: Automatic account creation and balance tracking
- **Transaction History**: Complete audit trail with timestamps
- **Data Security**: Input validation, account ownership verification

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Migrations**: Alembic for database versioning
- **Security**: bcrypt password hashing, CORS enabled

## Database Schema
```
Users → Accounts → Transactions
├── User info & credentials
├── Account numbers & balances  
└── Transaction records & audit trail
```

## API Endpoints
### Authentication
- `POST /register` - Create user and account
- `POST /login` - Get JWT token

### Account Operations
- `GET /account/profile` - User profile
- `GET /account/balance` - Current balance
- `GET /account/details` - Account info

### Transactions
- `POST /transactions/deposit` - Add money
- `POST /transactions/withdraw` - Remove money
- `POST /transactions/transfer` - Send money between accounts
- `GET /transactions/history` - All transactions
- `GET /transactions/mini-statement` - Last 5 transactions

## Security Features
- JWT authentication with 1-hour expiration
- Password hashing with bcrypt
- Account ownership validation
- Balance verification before transactions
- Complete transaction audit logging

## Quick Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
createdb bank_db
cd backend && alembic upgrade head

# Run server
uvicorn main:app --reload
```

**API Documentation**: http://localhost:8000/docs

## Project Deliverables
✅ 12 REST API endpoints  
✅ JWT authentication system  
✅ PostgreSQL database with 3 tables  
✅ Complete transaction processing  
✅ Security implementation  
✅ Interactive API documentation  
✅ Database migration system  

## Technical Achievements
- **Scalable Architecture**: Modular design with separated concerns
- **Production Security**: Industry-standard authentication and validation
- **Data Integrity**: ACID-compliant transactions with foreign key constraints
- **Developer Experience**: Auto-generated API docs and type validation
- **Maintainability**: Clean code structure with comprehensive error handling