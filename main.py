import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents, db
from schemas import Lead, ContactMessage, Subscriber

app = FastAPI(title="ChatImmo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ChatImmo backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# -----------------------------
# Leads endpoints
# -----------------------------
@app.post("/api/leads", status_code=201)
async def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"id": lead_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leads")
async def list_leads(limit: int = 50):
    try:
        docs = get_documents("lead", limit=limit)
        # Convert ObjectId to string
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Contact messages endpoints
# -----------------------------
@app.post("/api/contact", status_code=201)
async def send_contact(msg: ContactMessage):
    try:
        msg_id = create_document("contactmessage", msg)
        return {"id": msg_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Newsletter subscribers
# -----------------------------
@app.post("/api/subscribe", status_code=201)
async def subscribe(sub: Subscriber):
    try:
        sub_id = create_document("subscriber", sub)
        return {"id": sub_id, "status": "subscribed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
