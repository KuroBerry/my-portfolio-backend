import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    # Run the app instance from the app package
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
