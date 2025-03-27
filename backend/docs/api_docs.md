API Documentation

Authentication Endpoints

1. User Signup

Endpoint: POST /auth/signup

Request Body:
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "securepassword"
}

Response (Success):
{
  "message": "User registered successfully"
}

Response (Error):
{
  "error": "User already exists"
}

2. User Login
Endpoint: POST /auth/login

Request Body:
{
  "email": "user@example.com",
  "password": "securepassword"
}

Response (Success):
{
  "access_token": "your.jwt.token"
}

Response (Error):
{
  "error": "Invalid credentials"
}


3. Test Protected Route
Endpoint: GET /auth/test-protected

Headers:
Authorization: Bearer <your.jwt.token>

Response (Success):
{
  "message": "Access granted"
}

Response (Error - Invalid Token):
{
  "error": "Missing or invalid token"
}

Mood Tracking Endpoints


4. Submit Mood Entry

Endpoint: POST /mood/submit

Headers:
Authorization: Bearer <your.jwt.token>

Request Body:
{
  "text": "I'm feeling great!",
  "mood_score": 8.0,
  "sentiment": "positive"
}

Response (Success):
{
  "message": "Mood entry submitted successfully"
}


5. Get Mood History
Endpoint: GET /mood/mood-history

Headers:
Authorization: Bearer <your.jwt.token>

Response (Success):
{
  "mood_history": [
    {
      "id": 1,
      "text": "Feeling happy!",
      "mood_score": 8.0,
      "sentiment": "positive",
      "timestamp": "Mon, 24 Mar 2025 17:01:44 GMT"
    }
  ]
}

Response (Error - Unauthorized):
{
  "error": "Missing or invalid token"
}


Error Cases

Expired Token
{
  "error": "Token has expired"
}

Invalid Request Body
{
  "error": "Missing required fields"
}

Unauthorized Access
{
  "error": "Missing or invalid token"
}

Notes:
All protected endpoints require an Authorization header with a valid JWT token.
Ensure Postman is set to use Bearer <token> for authentication when testing protected routes.
