import os
from app import app

if __name__ == "__main__":
    import uvicorn
    # Use a single worker to reduce resource pressure on App Service
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), workers=1)
