# Troubleshooting

## Frontend Issues

### "Cannot find module" error
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Port 3000 already in use
```bash
npm run dev -- -p 3001
```

### Build fails
```bash
rm -rf .next
npm run build
```

## Backend Issues

### "ModuleNotFoundError"
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Port 8000 already in use
```bash
python -m uvicorn app.main:app --port 8001
```

### Database connection failed
```bash
# Check if database is running
docker ps | grep brand_tracker_db

# View logs
docker logs brand_tracker_db

# Restart
docker-compose restart
```

## Database Issues

### Container won't start
```bash
cd database
docker-compose down
docker-compose up -d
```

### Connection refused
```bash
# Wait 10 seconds for database to start
# Then try connecting
psql -h localhost -U tracker -d trackerdb
```

## Common Solutions

| Problem | Solution |
|---------|----------|
| Nothing works | Restart everything: Stop all, then start fresh |
| Port conflicts | Use different ports with `--port` flag |
| Module errors | Delete node_modules/.venv and reinstall |
| Database errors | Check Docker is running, restart container |

## Get Help

- Check [GETTING_STARTED.md](./GETTING_STARTED.md)
- Read [SETUP.md](./SETUP.md)
- View logs: `docker logs brand_tracker_db`
