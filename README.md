# AI SaaS Backend API

A secure and scalable **AI SaaS Backend API** built with **Python, FastAPI, and MongoDB** as part of the **Sqrock IT Solutions Backend Development Internship – Phase 2, Task 1**.

The project provides authentication, subscription plans, AI tool access control, mock AI request processing, usage tracking, API key management, subscription management, and an admin panel.

## 🚀 Live Demo

- **Live API:** https://ai-saas-backend-yjfh.onrender.com
- **Swagger API Documentation:** https://ai-saas-backend-yjfh.onrender.com/docs
- **GitHub Repository:** https://github.com/pchauhan24-dev/ai-saas-backend

---

## 📌 Project Overview

This project demonstrates the backend architecture of an AI-powered SaaS platform where users can:

- Create an account and log in securely
- Receive JWT-based authentication tokens
- View available subscription plans
- Subscribe to a plan
- Access AI tools according to their subscription
- Send prompts to AI tools
- Receive mock AI responses
- View and manage AI request history
- Save favorite AI responses
- Track daily and monthly AI usage
- Generate and manage API keys
- Upgrade, downgrade, or cancel subscriptions

Administrators can manage users, subscription plans, AI tools, subscriptions, and usage analytics.

---

## ✨ Features

### 🔐 Authentication & Security

- User registration
- User login
- JWT authentication
- Password hashing using bcrypt
- Protected API endpoints
- User profile endpoint
- Logout endpoint
- Active/blocked user status
- Role-based admin access
- Environment-based configuration for secrets

### 💳 Subscription Plans

The system supports four subscription plans:

| Plan | Daily Requests | AI Models | File Upload Limit |
|---|---:|---|---:|
| Free | 20 | GPT-3.5 | 0 |
| Starter | 200 | GPT-3.5, GPT-4 | 5 |
| Pro | Unlimited | GPT-3.5, GPT-4, Image Generation | 20 |
| Enterprise | Unlimited | GPT-3.5, GPT-4, Image Generation | 100 |

Plans also contain:

- Monthly price
- Available AI models
- Features
- Plan status

### 🤖 AI Tools

The backend supports five AI tools:

1. **AI Chat**
2. **AI Code Generator**
3. **AI Text Summarizer**
4. **AI Image Prompt Generator**
5. **AI Email Writer**

Tool access is controlled according to the user's subscription plan.

### 🧠 AI Request System

Users can:

- Send prompts
- Receive mock AI responses
- View prompt history
- Delete request history
- Save favorite responses
- Track tokens used

The current project uses **mock AI responses**, so an external AI API key is not required.

### 📊 Usage Tracking

The system tracks:

- Daily AI requests
- Monthly AI requests
- Daily request limits
- Remaining requests
- Daily tokens used
- Monthly tokens used
- AI tool usage

### 🔑 API Key Management

Users can:

- Generate an API key
- View their active API key
- Regenerate an API key
- Delete/deactivate an API key
- View API usage information

### 📦 Subscription Management

Users can:

- Subscribe to a plan
- View their current subscription
- Change their subscription plan
- Upgrade or downgrade
- Cancel their subscription

### 👨‍💼 Admin Panel

Administrators can:

- View all users
- Block users
- Unblock users
- View all subscription plans
- Manage plans
- View all AI tools
- Manage AI tools
- View AI usage analytics
- View API usage analytics
- View subscriptions

All admin endpoints are protected by admin authorization.

---

## 🛠️ Tech Stack

### Backend

- **Python**
- **FastAPI**
- **Uvicorn**

### Database

- **MongoDB**
- **PyMongo**

### Authentication & Security

- **JWT**
- **python-jose**
- **bcrypt**
- **Passlib**

### Validation & Configuration

- **Pydantic**
- **Email Validator**
- **python-dotenv**

### Deployment

- **Render**

### API Testing

- **Swagger UI / OpenAPI**

---

## 🏗️ Project Structure

```text
ai-saas-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── plan.py
│   │   ├── subscription.py
│   │   ├── ai_tool.py
│   │   ├── ai_request.py
│   │   └── api_key.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── plan.py
│   │   ├── subscription.py
│   │   ├── ai_tool.py
│   │   ├── ai_request.py
│   │   ├── api_key.py
│   │   └── usage.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── plans.py
│   │   ├── subscriptions.py
│   │   ├── ai_tools.py
│   │   ├── ai_requests.py
│   │   ├── api_keys.py
│   │   ├── usage.py
│   │   └── admin.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       ├── dependencies.py
│       ├── ai_engine.py
│       └── usage.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Collections

The application uses MongoDB with the following collections:

```text
ai_saas
│
├── users
├── plans
├── subscriptions
├── ai_tools
├── ai_requests
└── api_keys
```

---

## 🔗 Main API Endpoints

### Authentication

```text
POST   /auth/signup
POST   /auth/login
GET    /auth/profile
POST   /auth/logout
```

### Subscription Plans

```text
GET    /plans/
GET    /plans/{plan_id}
POST   /plans/
PUT    /plans/{plan_id}
DELETE /plans/{plan_id}
```

### AI Tools

```text
GET    /ai-tools/
GET    /ai-tools/{tool_id}
POST   /ai-tools/
PUT    /ai-tools/{tool_id}
DELETE /ai-tools/{tool_id}
```

### AI Requests

```text
POST   /ai-requests/
GET    /ai-requests/
DELETE /ai-requests/{request_id}
PUT    /ai-requests/{request_id}/favorite
```

### Subscriptions

```text
POST   /subscriptions/
GET    /subscriptions/current
PUT    /subscriptions/change-plan
PUT    /subscriptions/cancel
```

### Usage

```text
GET    /usage/
```

### API Keys

```text
POST   /api-keys/
GET    /api-keys/
PUT    /api-keys/regenerate
DELETE /api-keys/
GET    /api-keys/usage
```

### Admin

```text
GET    /admin/users
PUT    /admin/users/{user_id}/block
PUT    /admin/users/{user_id}/unblock

GET    /admin/plans
GET    /admin/ai-tools
GET    /admin/usage
GET    /admin/api-usage
GET    /admin/subscriptions
```

For complete request/response documentation, use the live Swagger documentation:

**https://ai-saas-backend-yjfh.onrender.com/docs**

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/pchauhan24-dev/ai-saas-backend.git
cd ai-saas-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```powershell
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_secret_key
```

Do **not** commit `.env` or any secret credentials to GitHub.

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing & Verification

The deployed API was tested through the live Swagger interface.

Verified functionality includes:

- User signup
- User login
- JWT authentication
- User profile
- Logout
- Subscription plans
- Plan access control
- AI tools
- AI request creation
- AI request history
- Favorite responses
- Request deletion
- Subscription creation
- Current subscription
- Subscription plan changes
- Usage tracking
- API key generation
- API key regeneration
- API key deletion
- Admin user management
- Admin plan management
- Admin AI tool management
- Admin usage analytics
- Admin API usage analytics
- Admin subscription viewing

---

## 🚀 Deployment

The application is deployed on **Render**.

### Live API

https://ai-saas-backend-yjfh.onrender.com

### Swagger Documentation

https://ai-saas-backend-yjfh.onrender.com/docs

The deployed application uses environment variables for MongoDB and JWT configuration.

---

## 🔒 Security Notes

- Passwords are stored as bcrypt hashes.
- JWT is used for protected endpoints.
- Admin routes require admin authorization.
- Blocked users cannot access protected resources.
- MongoDB credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- Virtual environment files are excluded from Git.
- Admin credentials are not stored in the repository.

The logout endpoint is stateless and instructs the client to remove its JWT token.

---

## 📚 Internship Project

**Program:** Backend Development Internship  
**Organization:** Sqrock IT Solutions  
**Phase:** Phase 2  
**Task:** Task 1 – AI SaaS Backend

This project was developed to demonstrate practical backend development skills including REST API development, authentication, authorization, database integration, subscription management, usage tracking, API design, and cloud deployment.

---

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Designing RESTful APIs
- Building APIs with FastAPI
- Working with MongoDB and PyMongo
- Implementing JWT authentication
- Password hashing with bcrypt
- Implementing role-based access control
- Designing subscription-based access
- Building usage tracking systems
- Managing API keys
- Creating admin functionality
- Testing APIs using Swagger
- Deploying backend applications to Render
- Managing environment variables and secrets
- Using Git and GitHub for version control

---

## 🔮 Future Improvements

Possible future improvements include:

- Integration with real AI APIs
- Real token usage from AI providers
- Payment gateway integration
- File upload and document processing
- Email notifications
- Advanced analytics dashboards
- API-key authenticated AI requests with usage counting
- Server-side JWT token revocation
- Team management for Enterprise users
- Rate limiting and caching

---

## 📄 License

This project was developed as an internship project for educational and demonstration purposes.