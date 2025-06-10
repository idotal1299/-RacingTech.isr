# 🏎️ RaceTech

**RaceTech** is a real-time telemetry analysis platform for *iRacing*, consisting of a desktop client, an API server, and a TypeScript-based frontend for visualizing driving data.

---


RaceTech.isr/
├── BackEnd/
│   ├── API/                    # WebSocket and REST endpoint logic
│   ├── auth/                   # Authentication and token handling
│   ├── config.py               # Environment and settings
│   ├── database/               # DB connection & session (postgres.py)
│   ├── models/                 # SQLAlchemy models (user.py etc.)
│   ├── routes/                 # FastAPI routers
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic (user_service.py, laps.py)
│   └── server/
│       └── main.py             # FastAPI app definition
│
├── Client/
│   ├── auth/                   # Google OAuth login
│   ├── cache/                  # token.pickle
│   ├── config/                 # config.json, loader, Google secrets
│   ├── dist/                   # Installer setup (setup.iss, license, policy)
│   ├── iracing/                # SDK wrapper, session manager
│   ├── network/                # WebSocket client
│   ├── utils/                  # Logging, cache fallback, process
│   ├── main.py                 # Main PySide GUI + socket app
│   ├── .env                    # Env vars
│   └── requirements.txt
│
├── Shared/                     # Shared schemas (future)
│
├── web/
│   ├── src/
│   │   ├── components/
│   │   ├── entities/           # TypeScript models
│   │   ├── pages/              # React pages (Home, Profile, Checkout)
│   │   └── Layout.tsx
│   └── README.md
│
├── docs/
│   ├── RoadMap.md
│   ├── AWS_ARCHITECTURE.md
│   ├── clientdocs.md
│   └── Tech_use
│
├── GitIgnore/
│   └── .gitignore_template
├── README.md
└── Licence.txt



## 🧠 Core Components

### 1. `client/`
- Runs locally on the driver's machine
- Captures telemetry data via the iRacing SDK
- Sends data every 200ms via WebSocket
- Configured via `.env` file

### 2. `backend/`
- FastAPI server that receives and stores telemetry
- Provides REST API and WebSocket endpoints for the frontend
- Includes user management, authentication, logging, and security

### 3. `web/`
- Frontend built with **TypeScript** using Visual Studio Code
- Displays telemetry, lap comparisons, and driver data
- Communicates with backend via REST and WebSocket

### 4. `shared/`
- Common data models (e.g., enums, Pydantic schemas)
- Used by both client and backend to maintain consistency

### 5. `docs/`
- Contains system architecture, development roadmap, and changelogs

---

## 🚀 Running the Project Locally

### Client
```bash


cd client
pip install -r requirements.txt
python main.py


cd backend
pip install -r requirements.txt
uvicorn main:app --reload


cd web
npm install
tsc --watch


npm run dev



🔐 Security Highlights
JWT token-based authentication

secure communication via wss:// and https://

Environment variables stored in .env (never pushed to Git)

Rate limiting and server-side logging



📄 License
Copyright (c) 2025 Ido Tal

All rights reserved.

This software and all associated files are the proprietary property of the author.
Unauthorized copying, distribution, modification, or use of any part of this software 
without explicit written permission from the author is strictly prohibited.

Only authorized users are permitted to access and work with this software.

For inquiries, contact: racingtech.isr@gmail.com


✍️ Credits
Development: Ido Tal




 Client skeleton completed

 Initial API setup

 Full user authentication system

 GUI for desktop client

 Advanced telemetry graphs & lap comparison

 Closed-group beta release

