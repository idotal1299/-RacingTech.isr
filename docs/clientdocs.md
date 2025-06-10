# RaceTech Client – Feature Specification

## 🎯 Goal
A lightweight desktop application that runs silently in the background, detects when iRacing is active, and sends lap and telemetry data to the RaceTech server. The user installs once and forgets – no manual interaction needed.

---

## 🧩 Main Modules

### 1. iRacing Session Detection
- Automatic connection to iRacing SDK
- Runs only when iRacing is active
- Detects session start and stop
- Auto-disconnect if session closes

### 2. Session & Lap Management
- Unique session ID (UUID)
- Each lap tied to a session
- Lap details: fuel, weather, setup, telemetry

### 3. Telemetry Collection
- Real-time telemetry per lap
- Sent via secure WebSocket
- Sent only if connection is allowed

### 4. Cache/Fallback Mechanism
- If offline – save locally
- Resend on reconnect
- No data loss

### 5. Security
- Token-authenticated access
- Config stored in `.env` only
- No access to source code post-compilation
- No data sent without valid token

### 6. Always-on Background Operation
- Background operation (no console)
- Auto-start with OS boot
- No user visibility

### 7. Logging System
- Logs each session to file
- Tracks errors, connections, transmissions
- Useful for diagnostics

### 8. Deployment & Updates
- Signed EXE with installer
- Installer includes TOS and Privacy Policy
- Future silent updates supported
- Git access not required

---

## ✅ Core Development Principles

| Principle              | Implementation |
|------------------------|----------------|
| Open/Closed Principle  | Extendable components (Lap, Session) without structural changes |
| Single Responsibility  | One class = one task (e.g., Cache, WebSocket) |
| Secure by Design       | No data sent without permission |
| Performance-aware      | Minimal CPU/RAM usage |
| User Invisible         | Transparent to user |

---

## 🏆 Competitive Advantage
- Fully automated
- Enables driver comparison via RaceTech web
- Secure and modular architecture
