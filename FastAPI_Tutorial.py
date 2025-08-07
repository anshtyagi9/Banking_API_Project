'''

Table of Contents:
1. Introduction to FastAPI

2. Installation and Setup

3. Creating Your First API with FastAPI

4. Path Operations and HTTP Methods

5. Request and Response Models

6. Query Parameters and Path Parameters

7. Request Body and Validation

8. Dependency Injection

9. Form Data, File Uploads, and Background Tasks

10. Authentication and Authorization

11. Database Integration with FastAPI

12. Middleware, Error Handling, and CORS

13. Testing in FastAPI

14. Swagger UI and ReDoc

15. Deploying FastAPI Applications


      1. Introduction to FastAPI

FastAPI is a modern web framework built on Starlette (for web parts) and Pydantic (for data validation). It’s designed to build APIs quickly and efficiently while ensuring high performance and easy-to-use features like automatic documentation and validation.

Key Features:
Fast: It is very fast, built with asynchronous support.

Pythonic: FastAPI uses Python type hints, making your code more readable and maintainable.

Automatic Interactive Documentation: Automatically generates interactive Swagger UI and ReDoc.

Easy to Use: FastAPI is simple to use for beginners, but also has advanced capabilities for professionals.

Asynchronous Programming: Supports asynchronous routes for non-blocking I/O tasks.


      2. Installation and Setup

To get started, we need to install FastAPI and Uvicorn (the ASGI server to run the application).

pip install fastapi uvicorn
Uvicorn is required to run your FastAPI app since it’s an ASGI server, handling the HTTP requests asynchronously.


       3. Creating Your First API with FastAPI

Now, let’s create a simple FastAPI app.

Create a file main.py

Write the following code:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

In the code above:

We create an instance of FastAPI named app.

We define a route (or path operation) using the @app.get("/") decorator. This will respond to HTTP GET requests at the root ("/") path.

The function read_root() will return a JSON response with the key message.


        4. Path Operations and HTTP Methods

FastAPI allows you to handle various HTTP methods like GET, POST, PUT, DELETE, and more. Here's how to define them:

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
This code defines a GET request at the path /items/{item_id}, where item_id is a path parameter.

Path Operations Supported:
@app.get(): Handle GET requests.

@app.post(): Handle POST requests (used for creating data).

@app.put(): Handle PUT requests (used for updating data).

@app.delete(): Handle DELETE requests (used for deleting data).


           5. Request and Response Models

FastAPI uses Pydantic models for request and response data validation. You define a Pydantic model for structured data and automatic validation.

Example of request and response models:


from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
In this code:

We define a Pydantic model Item with fields name, description, price, and tax.

The create_item() function accepts a POST request with an Item in the body, and FastAPI automatically validates it based on the Pydantic model.


         6. Query Parameters and Path Parameters

Path parameters are included in the URL, while query parameters are part of the URL after the ?.

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
In this example:

item_id is a path parameter.

q is a query parameter (optional).


         7. Request Body and Validation

You can use Pydantic models to automatically validate incoming request bodies.

Example with a POST request:

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "price": item.price}


           8. Dependency Injection

One of FastAPI’s powerful features is dependency injection. Dependencies can be used for things like database connections, authentication, etc.

Example of dependency injection:


from fastapi import Depends

def get_db():
    db = connect_to_database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
Here, get_db() is a dependency that provides a database session.


          9. Form Data, File Uploads, and Background Tasks

You can handle form data and file uploads in FastAPI as well.

Handling file uploads:

from fastapi import UploadFile, File

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
Background tasks allow you to perform tasks in the background while returning a response to the user:

from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(write_log, message)
    return {"message": "Notification sent"}


           10. Authentication and Authorization

FastAPI makes it easy to add authentication and authorization to your app. You can use OAuth2, JWT (JSON Web Tokens), or simple HTTP Basic authentication.

Example using HTTP Basic Authentication:

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.get("/protected/")
def read_protected(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"message": "Welcome, admin!"}


         11. Database Integration with FastAPI

You can easily integrate a database like SQLite, PostgreSQL, or MySQL with FastAPI. You can use SQLAlchemy, Tortoise ORM, or any other ORM of your choice.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

# Creating the database tables
Base.metadata.create_all(bind=engine)


         12. Middleware, Error Handling, and CORS

FastAPI allows you to define middleware for things like logging, CORS, etc.

Example with CORS handling:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


          13. Testing in FastAPI

FastAPI has built-in support for testing using pytest. You can test your app using TestClient from fastapi.testclient.

Example test:

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


     14. Swagger UI and ReDoc

FastAPI automatically generates interactive documentation for your API using Swagger UI and ReDoc. You can access them at /docs and /redoc respectively.


    15. Deploying FastAPI Applications

You can deploy your FastAPI app using Uvicorn and servers like Nginx, Docker, or cloud platforms like AWS, Heroku, and Google Cloud.

uvicorn main:app --host 0.0.0.0 --port 8000


             ## Conclusion ##

   FastAPI is an incredibly fast and efficient framework for building APIs. Its focus on simplicity,
   automatic validation, and documentation makes it great for both beginners and professionals.
   Whether you are building simple or complex applications,
   FastAPI can handle it all, providing you with a scalable and maintainable solution


'''

'''
             ##  Advance topics  ##

        1. OAuth2, JWT, and HTTP Basic Authentication :
        
Authentication is a process to verify the identity of a user. 
Authorization is the process of verifying what actions the authenticated user can perform. 
FastAPI supports a wide variety of authentication mechanisms.

       1.1 HTTP Basic Authentication:

This is the simplest form of authentication. 
It requires a username and password to be sent with each request.

How it works:

The client sends a username and password with the Authorization header.

The server validates this information before allowing access to protected resources.

Example: Basic Authentication

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

# A simple mock of user data
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret"
    }
}

# Basic Auth Dependency
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/protected/")
def read_protected(username: str = Depends(authenticate_user)):
    return {"message": f"Hello, {username}, you're authenticated!"}
Explanation:

HTTPBasicCredentials is used to extract credentials from the Authorization header.

The authenticate_user function checks whether the username and password are correct, otherwise returns a 401 Unauthorized error.


         1.2 OAuth2 Authentication :
         
OAuth2 is a token-based authentication protocol. 
It allows clients to authenticate without using their username and password directly. 
Instead, they use access tokens that are provided by an authorization server.

How it works:

The client first obtains an OAuth2 token (after authenticating with the provider).

The client includes this token in the header of requests to access protected resources.

Example: OAuth2 Password Flow (for simplicity)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# A mock database for user authentication
fake_users_db = {
    "user1": {
        "username": "user1",
        "password": "password123",
        "full_name": "John Doe"
    }
}

# Mock function to get a user
def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return user
    return None

# Token model (a simple placeholder, replace with actual OAuth2 implementation)
class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordBearer = Depends(oauth2_scheme)):
    user = get_user(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": "mock_token_123", "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    # In a real scenario, you would validate the token and extract user data
    return {"username": "user1", "full_name": "John Doe"}
Explanation:

OAuth2PasswordBearer is used to extract the OAuth2 token from the request.

In a real OAuth2 flow, you'd use libraries like Authlib or OAuthlib for token validation, but here, we’ve used a simple placeholder for token generation.


       1.3 JSON Web Tokens (JWT) Authentication :
       
JWT is an open standard for securely transmitting information between parties as a JSON object.
It’s often used in OAuth2 flows. JWT contains three parts: the header, payload, and signature.

How it works:

The server generates a JWT after the user logs in.

The client stores the JWT (usually in local storage or cookies) and includes it in subsequent requests.

The server validates the JWT on each request to authenticate the user.

Example: JWT Authentication

import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

app = FastAPI()

# OAuth2 Password flow (simplified for demo)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key to encode the JWT token
SECRET_KEY = "mysecretkey"

# JWT Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Mock User DB
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret"
    }
}

# Token creation route (User logs in)
@app.post("/token", response_model=Token)
def login_for_access_token(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_jwt_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route (requires JWT token)
@app.get("/protected/")
def read_protected(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Hello {username}, you're authenticated!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
Explanation:

The create_jwt_token function generates a JWT token that includes the user’s username (sub claim) and an expiration time.

The /protected/ route extracts and validates the JWT token from the Authorization header.


       2. Authentication and Authorization in FastAPI 
       
               2.1 Authentication :
Authentication verifies who the user is, typically through username/password, OAuth2, or JWT tokens.

               2.2 Authorization :
Authorization checks what the authenticated user is allowed to do. For example, role-based access control (RBAC) or permissions checks can be used.

Example: Role-based Authorization

from fastapi import Depends, HTTPException

# Mock of user data with roles

fake_users_db = {
    "admin": {"username": "admin", "password": "admin", "role": "admin"},
    "user": {"username": "user", "password": "user", "role": "user"},
}

def get_current_user(username: str):
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user

def check_role(required_role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
        return user
    return role_dependency

@app.get("/admin/")
def read_admin_data(user: dict = Depends(check_role("admin"))):
    return {"message": f"Hello {user['username']}, you have access to admin data."}

@app.get("/user/")
def read_user_data(user: dict = Depends(check_role("user"))):
    return {"message": f"Hello {user['username']}, you have access to user data."}


            3. Database Integration with FastAPI :
            
FastAPI supports various databases like SQLite, PostgreSQL, MySQL, and others.

            3.1 SQLAlchemy Integration Example :
            
Let’s set up an example with SQLAlchemy and SQLite.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define a simple User model
class User(Base):
    __tablename__ = "users"
    id = Column


ChatGPT said:
(Integer, primary_key=True, index=True)
username = Column(String, unique=True, index=True)
full_name = Column(String)

Create the tables
Base.metadata.create_all(bind=engine)

Dependency to get DB session
def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()

from fastapi import Depends

@app.post("/users/")
def create_user(username: str, full_name: str, db=Depends(get_db)):
user = User(username=username, full_name=full_name)
db.add(user)
db.commit()
db.refresh(user)
return user

@app.get("/users/{user_id}")
def read_user(user_id: int, db=Depends(get_db)):
user = db.query(User).filter(User.id == user_id).first()
if not user:
raise HTTPException(status_code=404, detail="User not found")
return user


- **Explanation**:
  - SQLAlchemy handles database interactions.
  - `get_db()` provides a database session via dependency injection.
  - `create_user()` adds a user, and `read_user()` fetches user details.

---

### 4. Middleware, Error Handling, and CORS

         4.1 Middleware :
         
Middleware is a function that runs before or after each request. You can use it for logging, authentication, or modifying requests/responses.

Example of simple logging middleware:

```python
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request URL: {request.url}")
    response = await call_next(request)
    print(f"Response Status Code: {response.status_code}")
    return response


       4.2 Error Handling :
You can create custom exception handlers for your application.

Example: Handle 404 errors with a custom message:


from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Oops! Error: {exc.detail}"}
    )


         4.3 CORS (Cross-Origin Resource Sharing) :
When your frontend and backend are hosted on different domains, browsers block requests due to the same-origin policy. CORS middleware allows you to configure which domains can access your API.

Example enabling CORS:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Only allow this domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)


                                                 Summary :
                                                 
               
       Topic	                              What It Is	                          Example Usage
       
HTTP Basic Authentication	      Simple username/password authentication	     Protect simple endpoints
OAuth2	                          Token-based authentication protocol	         Secure APIs with OAuth providers
JWT	                              JSON Web Tokens for stateless auth	         Issue and validate JWT tokens for auth
Authentication & Authorization	  Verify identity and permissions                Role-based access control
Database Integration              Connect FastAPI with databases	             SQLAlchemy with SQLite/PostgreSQL
Middleware	                      Code executed on every request/response	     Logging, authentication, headers modification
Error Handling	                  Custom responses for errors	                 Custom 404 or validation errors
CORS	                          Enable cross-origin requests	                 Allow frontend to talk to backend on different domain


'''

'''
                                ##  Some common HTTP status codes.  ##

1. 4xx - Client-Side Errors
These errors occur when the problem is on the client’s side. The server can't process the request due to an issue with the request itself (e.g., a malformed URL or missing data).

404 - Not Found
Explanation: The server can't find the requested resource. This usually happens when the user tries to access a page that doesn’t exist on the server.

Example: If you type http://example.com/nonexistent-page, you'll likely see a 404 error if that page doesn't exist.

403 - Forbidden
Explanation: The server understands the request but refuses to authorize it. This could be due to insufficient permissions or restrictions on the server (e.g., trying to access a private resource).

Example: Trying to access an admin page without being logged in.

400 - Bad Request
Explanation: The server cannot understand the request due to malformed syntax or invalid parameters. It’s usually an issue with the request sent by the client.

Example: Sending an incomplete or broken query string like http://example.com/?id=123& where the id parameter is missing a value.

401 - Unauthorized
Explanation: The request requires user authentication. This occurs when you try to access a resource that requires a login but you haven't provided valid credentials.

Example: Trying to access a restricted page without logging in.

405 - Method Not Allowed
Explanation: The request method (GET, POST, PUT, DELETE, etc.) is not allowed for the requested resource. For example, trying to POST data to a page that only allows GET requests.

Example: A form that only accepts GET requests, but you're trying to POST to it.

408 - Request Timeout
Explanation: The server timed out waiting for the request from the client. This can happen if the client takes too long to send data, or the server is too busy.

Example: Sending a request from a slow or unreliable internet connection.

2. 5xx - Server-Side Errors
These errors occur when the problem is on the server side. They indicate that the server failed to fulfill a valid request.

500 - Internal Server Error
Explanation: A generic error message when something goes wrong on the server, but the server can't provide more specific information.

Example: A bug in the server-side code or an unexpected crash.

502 - Bad Gateway
Explanation: The server acting as a gateway or proxy received an invalid response from the upstream server.

Example: The server tries to access another server to fulfill the request (e.g., a reverse proxy), but that server is down or returning errors.

503 - Service Unavailable
Explanation: The server is temporarily unable to handle the request due to being overloaded or undergoing maintenance.

Example: High traffic to a website or maintenance downtime.

504 - Gateway Timeout
Explanation: Similar to 502, this error occurs when a server acting as a gateway or proxy times out waiting for a response from another server.

Example: A backend server takes too long to respond to a request from the frontend server.

505 - HTTP Version Not Supported
Explanation: The server does not support the HTTP protocol version that was used in the request.

Example: A server that only supports HTTP/1.1 but the client is sending a request using HTTP/2.

3. 1xx - Informational Responses
These codes indicate that the request was received and is being processed.

100 - Continue
Explanation: The server has received the request headers and the client should proceed to send the request body (if applicable).

Example: A client sends a large file, and the server says it’s OK to continue uploading.

101 - Switching Protocols
Explanation: The server is switching protocols according to the client's request (e.g., switching from HTTP/1.1 to WebSocket).

Example: A server switching to WebSocket for real-time communication.

4. 2xx - Success
These codes indicate that the request was successfully processed.

200 - OK
Explanation: The request was successful, and the server has returned the requested data or performed the requested action.

Example: A webpage loads correctly.

201 - Created
Explanation: The request was successful, and a new resource has been created (often used in POST requests).

Example: A new record is created in the database via a POST request.

204 - No Content
Explanation: The request was successful, but there’s no content to send in the response. Often used for operations that don’t return data.

Example: Deleting a resource from the server.

5. 3xx - Redirection
These codes indicate that further action is needed to fulfill the request, usually involving redirecting the client to a different location.

301 - Moved Permanently
Explanation: The resource has been permanently moved to a new URL. Any future requests should use the new URL.

Example: A website URL changes, and visitors are automatically redirected to the new location.

302 - Found (Temporarily Moved)
Explanation: The resource is temporarily located at a different URL. Future requests should still use the original URL.

Example: A site temporarily redirects to a maintenance page.

304 - Not Modified
Explanation: The resource hasn’t been modified since the last request, so the server doesn’t need to send the data again.

Example: A browser checks if a cached image is still valid.

307 - Temporary Redirect
Explanation: Similar to a 302, but it specifies that the request method should not be changed.

Example: Temporary redirects that keep the HTTP method the same (e.g., POST).

308 - Permanent Redirect
Explanation: A permanent redirect, similar to 301, but keeps the method (e.g., POST).

Example: A permanent redirect from an old URL to a new URL.

Summary
4xx errors generally indicate problems with the client’s request (e.g., missing files, bad syntax).

5xx errors mean something went wrong on the server (e.g., server overload, misconfigurations).

1xx errors provide informational responses.

2xx errors indicate successful processing of the request.

3xx errors involve redirects to other URLs

'''

'''
🧠 What is Error Handling in Python?
When something goes wrong during code execution (like dividing by zero, or accessing a file that doesn't exist), Python raises an exception. If you don’t handle it, your program will crash.

🔥 Common Runtime Errors (Exceptions)
Here are some frequent exceptions in Python:

Exception	When it Occurs
ZeroDivisionError	Division by zero
ValueError	Wrong value type (e.g., converting "abc" to int)
TypeError	Invalid operation between different types
FileNotFoundError	Trying to open a file that doesn’t exist
IndexError	Accessing an invalid list index
KeyError	Accessing a missing dictionary key

🧱 Basic Syntax of Error Handling
try:
    # code that might cause an error
except SomeException:
    # code that runs if that error occurs
else:
    # runs only if there is no error
finally:
    # always runs, error or not
🧪 Example 1: Handling a ValueError
try:
    num = int(input("Enter a number: "))  # Could raise ValueError
    print(f"Square is: {num ** 2}")
except ValueError:
    print("That was not a valid number.")
Explanation:
If the user inputs text instead of a number (like "abc"), Python raises a ValueError. The program doesn’t crash because we catch it.

🧪 Example 2: Handling Multiple Exceptions
try:
    x = int(input("Enter a number: "))
    y = 10 / x
    print(f"Result: {y}")
except ValueError:
    print("Please enter a valid integer.")
except ZeroDivisionError:
    print("Cannot divide by zero!")
Explanation:

If input is "abc" → ValueError

If input is "0" → ZeroDivisionError

🔄 Using else and finally
try:
    num = int(input("Enter a positive number: "))
    assert num > 0
except ValueError:
    print("Invalid input. Please enter a number.")
except AssertionError:
    print("Number must be greater than zero.")
else:
    print(f"Thank you! You entered: {num}")
finally:
    print("Execution complete.")
else runs if there's no exception.

finally always runs, even if an error occurs or the program exits early.

📁 Example 3: File Handling with Error Management
try:
    with open("data.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("The file was not found.")
finally:
    print("Done reading the file.")
🔧 Creating Custom Exceptions
You can define your own error types:

class MyCustomError(Exception):
    pass

def check_value(x):
    if x < 0:
        raise MyCustomError("Negative value not allowed!")

try:
    check_value(-10)
except MyCustomError as e:
    print(f"Custom Error: {e}")
🔁 Real-world Pattern: Retrying on Error

while True:
    try:
        num = int(input("Enter a number: "))
        break  # success!
    except ValueError:
        print("Invalid input. Please try again.")
        
'''