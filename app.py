"""
CryptoHub Backend - Real-time Cryptocurrency Dashboard
Free CoinGecko API - Unlimited calls, no key needed!
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Dict
import os

app = FastAPI(
    title="CryptoHub API",
    description="Real-time cryptocurrency data from CoinGecko",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

@app.get("/")
async def root():
    return {
        "name": "CryptoHub API",
        "status": "active",
        "data_source": "CoinGecko (Free)",
        "endpoints": {
            "top_coins": "/api/coins/top?limit=100",
            "coin_details": "/api/coins/{coin_id}",
            "trending": "/api/trending",
            "global": "/api/global",
            "search": "/api/search?q={query}"
        }
    }

@app.get("/api/coins/top")
async def get_top_coins(limit: int = 100):
    """Get top cryptocurrencies by market cap"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{COINGECKO_BASE}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": True,
                    "price_change_percentage": "1h,24h,7d"
                }
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "count": len(response.json())
                }
            
            raise HTTPException(status_code=response.status_code, detail="CoinGecko API error")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/coins/{coin_id}")
async def get_coin_details(coin_id: str):
    """Get detailed information about a specific coin"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{COINGECKO_BASE}/coins/{coin_id}",
                params={
                    "localization": False,
                    "tickers": False,
                    "community_data": True,
                    "developer_data": False,
                    "sparkline": True
                }
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            
            raise HTTPException(status_code=404, detail="Coin not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trending")
async def get_trending():
    """Get trending coins"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{COINGECKO_BASE}/search/trending")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            
            raise HTTPException(status_code=response.status_code, detail="Error fetching trending")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/global")
async def get_global_data():
    """Get global cryptocurrency market data"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{COINGECKO_BASE}/global")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()["data"]
                }
            
            raise HTTPException(status_code=response.status_code, detail="Error fetching global data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_coins(q: str):
    """Search for coins by name or symbol"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{COINGECKO_BASE}/search",
                params={"query": q}
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            
            raise HTTPException(status_code=response.status_code, detail="Search error")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "api": "coingecko"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
