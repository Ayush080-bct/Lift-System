# Getting Started - Quick Setup

## First-time database (single lift, floors 1–10)

```bash
cd /home/ayush/LiftSystem
cp .env.example .env   # edit DB_PASS
psql -U ayush -d lift_system -f backend/database/Schema.sql
```

If you already had an old schema, reset tables first (see `backend/database/Queries.sql`).

## 🚀 Start Everything

### Terminal 1: Start PostgreSQL
```bash
sudo service postgresql start
```

### Terminal 2: Start Backend (FastAPI)
```bash
cd /home/ayush/LiftSystem
source Lvenv/bin/activate
fastapi dev backend/app/main.py
```

Should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 3: Start Frontend (Vite)
```bash
cd /home/ayush/LiftSystem/frontend
npm run dev
```

Should show:
```
VITE v... ready in XXX ms
➜  Local:   http://localhost:5173/
```

**Open browser:** http://localhost:5173/

---

## ✅ How to Know It's Working

✓ Header appears with gradient background
✓ Request Lift form visible
✓ Lifts display with data (NOT "Failed to fetch")
✓ Can create requests
✓ Logs update in real-time

---

## 🔧 Troubleshooting

**Backend shows error?**
```bash
# Check if PostgreSQL is running
sudo service postgresql status

# Restart it
sudo service postgresql restart
```

**Frontend won't start?**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Still getting "Failed to fetch"?**
- Backend must run on http://127.0.0.1:8000
- Frontend must run on http://localhost:5173/
- Check that both are running in separate terminals