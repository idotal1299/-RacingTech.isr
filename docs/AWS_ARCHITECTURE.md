# 🏁 RaceTech AWS Architecture

This document outlines the recommended cloud architecture for the RaceTech platform, deployed on AWS.

---

## 🧱 System Overview

RaceTech is a telemetry platform for iRacing that includes:
- A secure desktop Client
- A cloud-based API backend
- A web frontend for users to explore driver data
- Integration with Google OAuth for secure identity

---

## ☁️ AWS Components

| Component                | AWS Service               | Purpose                                                                 |
|--------------------------|----------------------------|-------------------------------------------------------------------------|
| Client Authentication    | Google OAuth               | User identity verification via desktop login                            |
| API Entry Point          | API Gateway (REST + WS)    | Secure entry point for all client and web requests                      |
| Application Logic        | AWS Lambda (or EC2/FastAPI)| Handles business logic – login, token exchange, lap data intake         |
| Main Database            | Amazon RDS (PostgreSQL)    | Stores users, purchases, metadata                                       |
| Telemetry Storage        | Amazon DocumentDB / DynamoDB | Flexible JSON telemetry storage per lap                                 |
| File Storage             | Amazon S3                  | Stores large replay files, lap exports, images                          |
| Task Queue (optional)    | Amazon SQS                 | Buffers high-volume telemetry before processing                         |
| Secrets and Tokens       | AWS Secrets Manager / IAM  | Secure handling of auth keys and JWT signing secrets                    |

---

## 🔐 Security Architecture

- All communication is over HTTPS/WSS.
- JWT tokens are used for client–server and web–server authentication.
- IAM policies restrict Lambda/S3/DB access.
- S3 buckets are private, access is tokenized or signed.

---

## 🧭 Architecture Flow

1. User logs in via Google OAuth in the **RaceTech Client**
2. Client sends Google `id_token` to API: `POST /auth/google`
3. Backend validates token, creates internal **RaceTech JWT**
4. Client uses that JWT to stream lap data via WebSocket
5. API stores metadata in PostgreSQL and telemetry in DocumentDB
6. Data is available to users via Web frontend (with the same JWT)

---

## 🔧 Suggested Folder Structure in Backend


│
├── main.py # FastAPI or Lambda handler
├── auth/
│ └── google_auth.py # Google token verification
├── models/
│ └── user.py # SQLAlchemy or Pydantic models
├── services/
│ └── telemetry_service.py # Mongo insertions
└── db/
├── postgres.py # PostgreSQL connection
└── mongo.py # Mongo connection


---

## 🛠️ Next Steps

- [ ] Build `POST /auth/google` endpoint
- [ ] Setup AWS RDS instance with `users`, `laps`, `purchases`
- [ ] Configure DocumentDB or DynamoDB for telemetry
- [ ] Deploy with IAM roles + Secrets Manager
- [ ] (Optional) Setup CI/CD with GitHub Actions and Terraform

---

