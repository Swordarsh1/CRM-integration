# CRM–Inventory Mini Integration


This is a super simple demo project with two FastAPI services that talk to each other. It’s mainly built for interview/testing purposes – nothing production-grade here (yet!).

---


There are two tiny services:

- **`clients.py`** (CRM): runs on port **9000**
- **`shipments.py`** (Inventory): runs on port **9001**

When you add a new client, it automatically triggers a shipment. Kind of like a handshake between the two.

---

## Project Structure

```
.
├── clients.py          # CRM service
├── shipments.py        # Inventory service
├── clients.json        # Stores client data
├── shipments.json      # Stores shipment data
├── README.md
```

---

## Setup & Running the Project


1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install fastapi uvicorn requests pydantic[email]
```

3. Run the services

```bash
# Start CRM service
uvicorn clients:app --reload --port 9000

# Start Inventory service
uvicorn shipments:app --reload --port 9001
```

---

## API Endpoints

### CRM – `localhost:9000`

- `POST /clients` → Add a new client
- `GET /clients` → List all clients

### Inventory – `localhost:9001`

- `POST /shipments` → (Called internally when a client registers)
- `GET /shipments` → List all shipments

---

## Notes

- It’s using local `.json` files for storing data – nothing fancy.
- Communication between the services is done using `requests`.
- No database or Docker setup yet (could be cool to add!)
- Logging is just basic `print()` for now.

---

## TODOs(later)

- Replace JSON with a real database (SQLAlchemy?)
- Add proper error handling & logging
- Maybe Dockerize both services
- Expand API validation a bit more

---

Feel free to fork, break, or improve it!
