#!/usr/bin/env python
"""
Simple runner script for the application
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting E-Commerce Recommendation System...")
    print("📍 Running on: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

