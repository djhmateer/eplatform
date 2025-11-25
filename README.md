# EPlatform

A full-stack web application built with React, TypeScript, and FastAPI.

## Architecture Overview

This is a monorepo-style project with a clear separation between frontend and backend:

```
vite-project-3/
├── client/          # React + TypeScript frontend
├── server/          # Python FastAPI backend
└── README.md
```

### Frontend Architecture (Client)

**Tech Stack:**
- **React 19.2** - UI library with modern hooks
- **TypeScript 5.9** - Type-safe JavaScript
- **Vite 7.2** - Fast build tool and dev server with HMR
- **React Router 7.9** - Client-side routing
- **Tailwind CSS 4.1** - Utility-first CSS framework
- **SWC** - Fast TypeScript/JavaScript compiler (via @vitejs/plugin-react-swc)

**Project Structure:**
```
client/
├── src/
│   ├── pages/          # Route components
│   │   ├── Home.tsx
│   │   ├── Search.tsx
│   │   └── ServerTime.tsx
│   ├── App.tsx         # Main app with layout and routing
│   ├── main.tsx        # Entry point with StrictMode
│   └── index.css       # Global styles
├── vite.config.ts      # Vite configuration with proxy
└── package.json
```

**Key Features:**
- **Development Proxy**: Vite dev server proxies `/api/*` requests to backend (default: `http://localhost:8000`)
- **Client-side Routing**: React Router handles navigation without full page reloads
- **Type Safety**: Full TypeScript coverage with strict mode enabled
- **Fast Refresh**: SWC-powered hot module replacement
- **Production Build**: Optimized static assets served by FastAPI in production

**Dev Proxy Configuration** (`client/vite.config.ts:12-17`):
```typescript
server: {
  proxy: {
    '/api': {
      target: env.VITE_API_URL || 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### Backend Architecture (Server)

**Tech Stack:**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server with hot reload
- **Python 3.12+** - Latest Python with type hints
- **python-dotenv** - Environment-based configuration

**Project Structure:**
```
server/
├── main.py              # FastAPI app with API routes
├── pyproject.toml       # UV/pip dependencies
├── .env.development     # Dev environment config
├── .env.production      # Prod environment config
└── .venv/              # Virtual environment
```

**Key Features:**
- **Environment-based Config**: Loads `.env.development` or `.env.production` based on `ENVIRONMENT` variable
- **API Routes**: RESTful endpoints under `/api/*` prefix
- **Static File Serving**: Serves built React app in production from `client/dist`
- **Health Check**: `/api/health` endpoint for monitoring

**API Endpoints:**
- `GET /api/health` - Health check (returns `{"status": "ok"}`)
- `GET /api/servertime` - Returns current UTC time in ISO format
- `GET /{path:path}` - Serves React frontend (production only)

**Environment Configuration** (`server/main.py:14-31`):
Requires `ENVIRONMENT` variable set to `development` or `production`, then loads corresponding `.env` file with required `PORT` variable.

### Data Flow

**Development Mode:**
1. Vite dev server runs on `http://localhost:5173` (client)
2. FastAPI runs on `http://localhost:8000` (server)
3. Browser hits `localhost:5173`, Vite serves React app
4. React makes API calls to `/api/*`
5. Vite proxy forwards to `localhost:8000/api/*`
6. FastAPI responds with JSON

**Production Mode:**
1. Build frontend: `cd client && npm run build` → outputs to `client/dist`
2. FastAPI serves both:
   - API endpoints at `/api/*`
   - Static files from `client/dist`
3. Single server on one port (e.g., 8000)

### Component Patterns

**Simplified State Management:**
Components use minimal state with pragmatic error handling:

```typescript
// Example: ServerTime.tsx
function ServerTime() {
  const [serverTime, setServerTime] = useState<string>('')

  useEffect(() => {
    fetch('/api/servertime')
      .then(res => res.json())
      .then(data => setServerTime(data.time))
  }, [])

  if (!serverTime) return <div>Loading...</div>
  return <div>{/* render data */}</div>
}
```

**Philosophy:**
- One state variable when possible (not three for loading/error/data)
- Let errors surface in console during development
- Early returns for loading states
- No over-engineering with complex error boundaries

### Development Workflow

**Start Development Servers:**
```bash
# Terminal 1 - Backend
cd server
ENVIRONMENT=development uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd client
npm run dev
```

**Build for Production:**
```bash
# Build frontend
cd client
npm run build

# Run production server
cd ../server
ENVIRONMENT=production uvicorn main:app --port 8000
```

**Linting:**
```bash
cd client
npm run lint
```

## Recommendations

### Immediate Improvements

1. **Data Fetching Library**
   - Consider adding **React Query (TanStack Query)** or **SWR**
   - Benefits: Built-in caching, automatic refetching, loading states, error handling
   - Would eliminate manual state management in components
   - Example: `useQuery(['servertime'], () => fetch('/api/servertime').then(r => r.json()))`

2. **Error Boundary**
   - Add a global error boundary component to catch React rendering errors
   - Provides better UX than white screen of death
   - Can be simple: show error message + reload button

3. **API Client Layer**
   - Create a centralized `api/` directory with typed API calls
   - Example: `api/servertime.ts` exports `getServerTime()` function
   - Benefits: Type safety, reusability, easier testing

4. **Environment Variables**
   - Add `.env.example` files for both client and server
   - Document required variables
   - Client: `VITE_API_URL` (optional, defaults to proxy)
   - Server: `ENVIRONMENT`, `PORT`

5. **Logging**
   - Frontend: Add structured logging (e.g., `console.error` with context)
   - Backend: Already has logging, consider adding request IDs

### Future Enhancements

6. **Authentication**
   - The "Login" button in header is currently non-functional
   - Consider: JWT tokens, OAuth, or session-based auth
   - Would need: login/logout endpoints, protected routes, auth state management

7. **Database Layer**
   - Current app has no persistence
   - Consider: PostgreSQL (production) + SQLAlchemy/SQLModel
   - Or: SQLite (development) for simplicity

8. **Testing**
   - Frontend: Add Vitest + React Testing Library
   - Backend: Add pytest with test fixtures
   - E2E: Consider Playwright for critical user flows

9. **Docker Setup**
   - Containerize both frontend and backend
   - `docker-compose.yml` for easy local development
   - Multi-stage build for production images

10. **CI/CD Pipeline**
    - GitHub Actions for: lint, test, build
    - Automated deployments to staging/production
    - Health check monitoring after deploy

11. **API Documentation**
    - FastAPI auto-generates OpenAPI docs at `/docs`
    - Consider adding: API versioning (`/api/v1/*`), rate limiting

12. **Performance**
    - Code splitting in React (lazy loading routes)
    - Backend: Add caching layer (Redis) if needed
    - Database connection pooling when DB is added
    - CDN for static assets in production

13. **Security Hardening**
    - Add CORS configuration (currently not configured)
    - Rate limiting on API endpoints
    - Input validation with Pydantic models (FastAPI)
    - Security headers (helmet equivalent for Python)
    - HTTPS in production

14. **Monitoring & Observability**
    - Application Performance Monitoring (APM)
    - Error tracking (Sentry)
    - Metrics dashboard (Prometheus + Grafana)
    - Log aggregation (ELK stack or cloud equivalent)

### Development Best Practices

- **Keep it simple**: Current architecture is intentionally minimal - only add complexity when needed
- **Type safety**: Leverage TypeScript on frontend and type hints on backend
- **Environment parity**: Keep dev/prod environments as similar as possible
- **Document decisions**: Update this README when making architectural changes
- **Review dependencies**: Keep dependencies up to date, audit security regularly

## Current State

This is a foundational setup suitable for:
- Prototyping and MVP development
- Learning full-stack development
- Small to medium applications

The architecture prioritizes:
- **Simplicity** over complexity
- **Developer experience** with fast HMR and type safety
- **Pragmatic decisions** (e.g., minimal error handling until needed)
- **Clear separation** between frontend and backend

As the application grows, implement recommendations incrementally based on actual needs rather than anticipated requirements.
