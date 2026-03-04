## Inventory Management System

A small microservices-based demo app for managing manufacturing inventory and stock alerts.  
It has three parts:
- **Inventory service** (FastAPI, SQLite)
- **Alert service** (FastAPI, SQLite)
- **Frontend** (simple HTML + JavaScript)

---

## 1. Prerequisites

- Python 3.11 (or 3.10+)
- `git`
- A terminal (macOS: Terminal or iTerm)

---

## 2. Clone the project

```bash
git clone https://github.com/nikhilww3/Inventory-Management-System.git
cd Inventory-Management-System
```

---

## 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate     # Windows PowerShell: .venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

For the alert service, also install its requirements (they are the same but kept separate):

```bash
cd alert-service
pip install -r requirements.txt
cd ..
```

---

## 4. Run the backend services

### 4.1 Inventory service (port 8000)

From the project root (`Inventory-Management-System`):

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

The inventory API docs will be at:
- `http://127.0.0.1:8000/docs`

### 4.2 Alert service (port 8001)

Open a **second terminal**, then:

```bash
cd Inventory-Management-System
source .venv/bin/activate
cd alert-service
uvicorn app.main:app --reload --port 8001
```

Alert API docs:
- `http://127.0.0.1:8001/docs`

---

## 5. Run the frontend

Open `frontend/index.html` in a browser (Chrome, Edge, etc.).

The frontend expects the inventory API at:

```javascript
const API = "http://127.0.0.1:8000";
```

So make sure the **inventory service is running on port 8000**.

---

## 6. How the system works

- **Add item**
  - Frontend calls `POST /items/` on the inventory service.
  - Item is stored in `inventory.db`.

- **List items**
  - Frontend calls `GET /items/` to show all inventory items.

- **Update quantity**
  - Frontend calls `PUT /items/{item_id}`.
  - Inventory service updates quantity.
  - It then calls `POST /check-alert` on the alert service (port 8001) with:
    - `item_id`, `quantity`, `threshold`.
  - Alert service:
    - Creates an alert if `quantity < threshold` and no active alert exists.
    - Resolves an existing alert if `quantity >= threshold`.

- **View alerts**
  - Call `GET /alerts` on the alert service to see all alerts.

---

## 7. Useful API endpoints

### Inventory service (port 8000)

- `GET /` – Health check message.
- `GET /items/` – List all items.
- `POST /items/` – Create an item.
- `PUT /items/{item_id}` – Update quantity for an item.
- `DELETE /items/{item_id}` – Delete an item.
- `GET /summary` – Inventory summary (totals, low stock count, etc.).

### Alert service (port 8001)

- `POST /check-alert` – Check quantity vs threshold and create/resolve alerts.
- `GET /alerts` – List all alerts.

---

## 8. Resetting local databases (optional)

If you want a clean start:

```bash
rm inventory.db
rm alert-service/alerts.db
```

Then restart both services; the databases will be recreated automatically.

---

## 9. Notes

- This project is for learning microservices + FastAPI basics.
- SQLite is used for simplicity; in production you would replace it with PostgreSQL or another database.
