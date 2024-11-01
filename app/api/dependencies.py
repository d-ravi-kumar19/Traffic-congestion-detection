# Example of a security dependency that can be added in the future
from fastapi import Depends, HTTPException

async def verify_api_key(api_key: str):
    # Placeholder for API key verification logic
    if api_key != "your_secret_api_key":
        raise HTTPException(status_code=403, detail="Forbidden")
