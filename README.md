# multiverse_agents
This is a project which has capability to create a simple agent from frontend
with pub/sub ability

# AI Agent Platform — FastAPI Auth

## Project Structure
```
auth-app/
├── main.py              # App entry point, routers, CORS
├── database.py          # MongoDB connection
├── auth.py              # Password hashing, JWT creation, auth dependency
├── models.py            # Pydantic request/response models
├── routes/
│   ├── auth_routes.py   # POST /auth/register, POST /auth/login
│   └── user_routes.py   # GET /users/me (protected)
├── .env                 # Environment variables
└── requirements.txt     # Dependencies
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB locally
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo

# Or if MongoDB is installed locally
mongod
```

### 3. Configure .env
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=agent_platform
JWT_SECRET=your_super_secret_key_change_this_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

Server runs at: http://localhost:8000
Swagger docs at: http://localhost:8000/docs

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Register new user | ❌ |
| POST | /auth/login | Login, get JWT token | ❌ |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /users/me | Get current user | ✅ Bearer token |

---

## How to Test

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@test.com", "password": "password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@test.com", "password": "password123"}'
```

### Get current user (use token from login response)
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## MongoDB Document Structure

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "password": "$2b$12$hashed_password",
  "created_at": "2024-01-01T00:00:00"
}
```

---

## Next Steps
- Add agents routes (create, publish, list)
- Add conversations and chat routes
- Add Redis pub/sub for real-time events