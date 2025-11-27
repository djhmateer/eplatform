# EPlatform

A full-stack web application with React frontend and Python FastAPI backend, deployed to Azure.

## Quick Start

### Prerequisites

- Node.js 20+ (via nvm)
- pnpm
- Python 3.12+
- uv (Python package manager)
- MySQL

### Development

**1. Start MySQL and create database:**

```bash
sudo mysql < infra/create_db.sql
```

**2. Start backend (Terminal 1):**

```bash
cd server
ENVIRONMENT=development uv run uvicorn main:app --reload --port 8000
```

**3. Start frontend (Terminal 2):**

```bash
cd client
pnpm install
pnpm dev
```

**4. Open browser:** http://localhost:5173

Sample login: `davemateer@gmail.com` / `2`

### Production (Azure VM)

Deploy a new Azure VM with everything configured:

```bash
cd infra
./infra.azcli
```

This script:
- Creates Azure resource group, VM, networking
- Copies source code to VM
- Runs `create_webserver.sh` which installs all dependencies
- Sets up systemd service for the API
- Configures nginx as reverse proxy
- Updates DNS

## Project Structure

```
├── client/              # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/       # Route components
│   │   └── App.tsx      # Main app with routing
│   └── public/          # Static assets (images, favicon)
├── server/              # Python FastAPI backend
│   ├── main.py          # API routes and auth
│   ├── logs/            # Application logs
│   └── .env.*           # Environment configs
└── infra/               # Deployment scripts
    ├── infra.azcli      # Azure deployment script
    ├── create_webserver.sh  # VM provisioning
    ├── create_db.sql    # Database schema
    └── nginx.conf       # Nginx configuration
```

## Tech Stack

**Frontend:**
- React 19 + TypeScript
- Vite (build tool)
- React Router (client-side routing)
- Tailwind CSS

**Backend:**
- FastAPI + Uvicorn
- MySQL + PyMySQL
- Argon2 (password hashing)
- Session-based authentication

**Infrastructure:**
- Azure VM (Ubuntu 24.04)
- Nginx (reverse proxy, SSL)
- systemd (process management)
- DNSimple (DNS)

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | No | Health check |
| `/api/servertime` | GET | No | Current UTC time |
| `/api/register` | POST | No | Create account |
| `/api/login` | POST | No | Login (sets session cookie) |
| `/api/logout` | POST | No | Logout (clears session) |
| `/api/me` | GET | Yes | Current user info |
| `/api/users` | GET | Yes | List all users |

## Authentication

Session-based auth with secure cookies:

1. User logs in with email/password
2. Password verified with Argon2
3. Session token stored in MySQL, sent as HTTP-only cookie
4. Subsequent requests validated against session table
5. Sessions expire after 7 days

## Environment Configuration

**Development** (`server/.env.development`):
```
ENVIRONMENT=development
MYSQL_HOST=localhost
MYSQL_USER=charlie
MYSQL_PASSWORD=password
MYSQL_DATABASE=eplatform
```

**Production** (`server/.env.production`):
```
ENVIRONMENT=production
MYSQL_HOST=localhost
MYSQL_USER=doug
MYSQL_PASSWORD=password2
MYSQL_DATABASE=eplatform
```

## Logging

Application logs are written to `server/logs/1debug.log` with rotation (10MB max, 5 backups).

**View logs on production:**
```bash
# Application logs
tail -f /home/dave/server/logs/1debug.log

# systemd logs
sudo journalctl -u evidenceplatform -f
```

## Useful Commands

**Development:**
```bash
# Frontend
cd client && pnpm dev          # Start dev server
cd client && pnpm build        # Build for production

# Backend
cd server
ENVIRONMENT=development uv run uvicorn main:app --reload
```

**Production (on VM):**
```bash
# Service management
sudo systemctl status evidenceplatform
sudo systemctl restart evidenceplatform
sudo systemctl stop evidenceplatform

# View logs
sudo journalctl -u evidenceplatform -f
tail -f /home/dave/server/logs/1debug.log

# Nginx
sudo systemctl restart nginx
sudo nginx -t  # Test config
```

**Database:**
```bash
sudo mysql eplatform
# Then: SELECT * FROM user;
```

## Data Flow

**Development:**
```
Browser (localhost:5173)
    ↓
Vite Dev Server (serves React, proxies /api/*)
    ↓
FastAPI (localhost:8000)
    ↓
MySQL
```

**Production:**
```
Browser (https://evidenceplatform.org)
    ↓
Nginx (SSL termination, serves static files)
    ↓
FastAPI (localhost:3000, via systemd)
    ↓
MySQL
```
