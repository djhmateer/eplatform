# notes on how to start the app normally in dev (not debug which is to use launch.json)
# python
cd server 
uv run uvicorn main:app --reload

# react - vite - port 5173 - custom node webserver
cd client 
pnpm dev


## Other front end commands
pnpm build

# port 4173 - prod port
pnpm preview

pnpm lint