# Library Management System

A Django REST Framework-based library management system that allows users to borrow and return books, with penalty tracking for overdue returns.

## Features

- **User Management**: Custom user registration and authentication with JWT tokens
- **Book Management**: CRUD operations for books, authors, and categories
- **Borrowing System**: Users can borrow up to 3 books simultaneously
- **Return System**: Book return with automatic penalty calculation for overdue books
- **Penalty Tracking**: Automatic penalty points for late returns (1 point per day late)
- **Admin Controls**: Staff users have full access to manage all resources
- **Filtering**: Search books by author and category

## Tech Stack

- **Backend**: Django 5.2.5 + Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development)
- **Additional Tools**: 
  - Django Silk (profiling)
  - Django Filters (filtering)



## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Oyshik-ICT/library_management_backend.git
   cd library_management_backend
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/api/register/` | User registration | Public |
| POST | `/api/login/` | Get JWT token | Public |
| POST | `/api/login/refresh/` | Refresh JWT token | Public |

### User Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/user/` | List users (own profile for regular users) | Authenticated |
| GET | `/api/user/{id}/` | Get user details | Authenticated (own profile or staff) |
| PUT/PATCH | `/api/user/{id}/` | Update user | Authenticated (own profile or staff) |
| DELETE | `/api/user/{id}/` | Delete user | Authenticated (own profile or staff) |

### Library Management

#### Categories
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/categories/` | List all categories | Admin only |
| POST | `/api/categories/` | Create category | Admin only |
| GET | `/api/categories/{id}/` | Get category details | Admin only |
| PUT/PATCH | `/api/categories/{id}/` | Update category | Admin only |
| DELETE | `/api/categories/{id}/` | Delete category | Admin only |

#### Authors
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/authors/` | List all authors | Admin only |
| POST | `/api/authors/` | Create author | Admin only |
| GET | `/api/authors/{id}/` | Get author details | Admin only |
| PUT/PATCH | `/api/authors/{id}/` | Update author | Admin only |
| DELETE | `/api/authors/{id}/` | Delete author | Admin only |

#### Books
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/books/` | List all books (with filtering) | Authenticated |
| POST | `/api/books/` | Create book | Admin only |
| GET | `/api/books/{id}/` | Get book details | Authenticated |
| PUT/PATCH | `/api/books/{id}/` | Update book | Admin only |
| DELETE | `/api/books/{id}/` | Delete book | Admin only |

**Book Filtering Parameters:**
- `?author=<author_name>` - Filter by author name (case-insensitive)
- `?category=<category_name>` - Filter by category name (case-insensitive)

### Borrowing System

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/api/borrow/` | Borrow a book | Authenticated |
| GET | `/api/borrow/` | List currently borrowed books | Authenticated |
| POST | `/api/return/` | Return a borrowed book | Authenticated |
| GET | `/api/users/{id}/penalties` | Check user penalty points | Authenticated (own or staff) |

## API Usage Examples

### Using Postman

#### Setting up Postman Environment
1. **Create Environment Variables:**
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (will be set after login)

#### Global Postman Setup
1. **Base URL**: Use `{{base_url}}` for all requests
2. **Authorization**: For authenticated endpoints, go to Authorization tab → Type: Bearer Token → Token: `{{access_token}}`

### 1. User Registration

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/register/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**cURL Equivalent:**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### 2. Login (Get JWT Token)

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/login/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Important**: Copy the `access` token and save it in your Postman environment as `access_token`

**cURL Equivalent:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### 3. Create Category (Admin Only)

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/categories/`
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "name": "FICTION"
}
```

### 4. Create Author (Admin Only)

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/authors/`
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "name": "William Shakespeare",
  "bio": "English playwright and poet, widely regarded as the greatest writer in the English language."
}
```

### 5. Create Book (Admin Only)

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/books/`
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "title": "Romeo and Juliet",
  "description": "A tragedy written by William Shakespeare about young star-crossed lovers.",
  "author": 1,
  "category": 1,
  "total_copies": 5
}
```

### 6. List Books with Filtering

**Postman Setup (List All Books):**
- **Method**: GET
- **URL**: `{{base_url}}/api/books/`
- **Authorization**: Bearer Token → `{{access_token}}`

**Postman Setup (Filter by Author):**
- **Method**: GET
- **URL**: `{{base_url}}/api/books/?author=shakespeare`
- **Authorization**: Bearer Token → `{{access_token}}`

**Postman Setup (Filter by Category):**
- **Method**: GET
- **URL**: `{{base_url}}/api/books/?category=fiction`
- **Authorization**: Bearer Token → `{{access_token}}`

**cURL Equivalent:**
```bash
# List all books
curl -X GET http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by author
curl -X GET "http://127.0.0.1:8000/api/books/?author=shakespeare" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by category
curl -X GET "http://127.0.0.1:8000/api/books/?category=fiction" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Borrow a Book

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/borrow/`
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "book_id": 1
}
```

**cURL Equivalent:**
```bash
curl -X POST http://127.0.0.1:8000/api/borrow/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "book_id": 1
  }'
```

### 8. List Currently Borrowed Books

**Postman Setup:**
- **Method**: GET
- **URL**: `{{base_url}}/api/borrow/`
- **Authorization**: Bearer Token → `{{access_token}}`

**Response Example:**
```json
[
  {
    "borrow_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "user": 1,
    "book": 1,
    "borrow_date": "2025-01-15",
    "due_date": "2025-01-29",
    "return_date": null
  }
]
```

### 9. Return a Book

**Postman Setup:**
- **Method**: POST
- **URL**: `{{base_url}}/api/return/`
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "borrow_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**cURL Equivalent:**
```bash
curl -X POST http://127.0.0.1:8000/api/return/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "borrow_id": "uuid-of-borrow-record"
  }'
```

### 10. Check Penalty Points

**Postman Setup:**
- **Method**: GET
- **URL**: `{{base_url}}/api/users/1/penalties` (replace 1 with actual user ID)
- **Authorization**: Bearer Token → `{{access_token}}`

**cURL Equivalent:**
```bash
curl -X GET http://127.0.0.1:8000/api/users/1/penalties \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 11. Update User Profile

**Postman Setup:**
- **Method**: PATCH
- **URL**: `{{base_url}}/api/user/1/` (replace 1 with actual user ID)
- **Authorization**: Bearer Token → `{{access_token}}`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "username": "newusername"
}
```

## Postman Tips

### Testing Workflow in Postman:
1. **Register** a new user
2. **Login** to get access token (save to environment)
3. **Create categories** (admin required)
4. **Create authors** (admin required)  
5. **Create books** (admin required)
6. **List books** to see available inventory
7. **Borrow books** as regular user
8. **List borrowed books** to get borrow_id
9. **Return books** using the borrow_id
10. **Check penalty points** if returned late

## Core System Logic

### Borrowing System Logic

The borrowing system implements several business rules and safety measures:

#### 1. **Book Borrowing Process**

When a user requests to borrow a book:

1. **Validation Checks:**
   - Verify the book exists and is available (`available_copies > 0`)
   - Check if user hasn't exceeded the 3-book limit
   - Ensure user is authenticated

2. **Atomic Transaction:**
   - Uses database transactions to prevent race conditions
   - Locks the book record with `select_for_update()` during the borrowing process
   - Creates a `Borrow` record with:
     - Unique UUID as primary key
     - Current user and selected book
     - Borrow date (automatic - today's date)
     - Due date (14 days from borrow date)
     - Return date (initially null)

3. **Book Inventory Update:**
   - Decrements the book's `available_copies` by 1
   - Uses `update_fields` for optimized database operations

4. **Constraints:**
   - Maximum 3 books per user at any time
   - Books must have available copies
   - Each borrow gets a 14-day lending period

#### 2. **Book Return Process**

When a user returns a book:

1. **Validation:**
   - Verify the borrow_id is a valid UUID
   - Ensure the borrow record exists and belongs to the user
   - Check that the book hasn't been returned already (`return_date` is null)

2. **Atomic Transaction:**
   - Locks the borrow record during processing
   - Sets the `return_date` to today's date
   - Increments the book's `available_copies` by 1

3. **Penalty Calculation:**
   - Checks if the book is overdue using `is_overdue()` method
   - Calculates days late using `days_late()` method
   - Adds penalty points equal to the number of days late
   - Updates user's `penalty_points` field

### Penalty Points System

#### How Penalty Points are Calculated:

1. **Due Date Determination:**
   - Every book has a 14-day lending period
   - Due date = borrow_date + 14 days

2. **Overdue Detection:**
   ```python
   def is_overdue(self):
       return date.today() > self.due_date
   ```

3. **Penalty Calculation:**
   ```python
   def days_late(self):
       return (date.today() - self.due_date).days
   ```

4. **Point Assignment:**
   - 1 penalty point per day late
   - Points are added to the user's cumulative `penalty_points`
   - Example: Book due on Jan 15, returned on Jan 20 = 5 penalty points

#### Penalty Point Features:

- **Automatic Calculation:** No manual intervention required
- **Cumulative:** Points accumulate over time across all late returns
- **Persistent:** Penalty points remain on the user's record
- **Viewable:** Users can check their own penalty points, staff can view any user's points


### Security Features

1. **Authentication:** JWT-based authentication for all endpoints
2. **Authorization:** Role-based permissions (regular users vs. staff)
3. **Data Protection:** Users can only access their own borrowing records
4. **Race Condition Prevention:** Database locks during critical operations
5. **Input Validation:** Proper validation for all user inputs

### Error Handling

The system includes comprehensive error handling:

- **Logging:** All errors are logged with detailed information
- **User-Friendly Messages:** Clear error messages returned to clients
- **Database Integrity:** Atomic transactions ensure data consistency
- **Graceful Degradation:** System continues operating even if individual operations fail

## Development Tools

### Django Silk Profiling

Access the Silk profiling interface at `http://127.0.0.1:8000/silk/` to monitor:
- Request/response times
- SQL queries
- Performance bottlenecks

### Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` with superuser credentials to:
- Manage users, books, authors, and categories
- View borrowing records
- Monitor system data

## Available Book Categories

The system supports the following predefined categories:

- Fiction
- Non-Fiction
- Science
- History
- Biography
- Mystery
- Fantasy
- Romance
- Technology
- Art
- Children's Books
- Self-Help
- Travel

## Database Schema

### Key Models:

1. **CustomUser**: Extends Django's AbstractUser with penalty_points
2. **Category**: Book categories with predefined choices
3. **Author**: Author information with biography
4. **Book**: Book details with inventory tracking
5. **Borrow**: Borrowing records with UUID primary keys