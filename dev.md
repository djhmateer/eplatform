# notes on how to start the app normally in dev (not debug which is to use launch.json)


```bash


# CLIENT FRONTEND
# react - vite - port 5173 - custom node webserver
cd client 
pnpm update
pnpm dev

# SERVER BACKEND
cd server
uv lock --upgrade
uv sync

# port 8000 by default
ENVIRONMENT=development uv run uvicorn main:app --reload

## Other front end commands
pnpm build

# port 4173 - prod port
pnpm preview

pnpm lint
```