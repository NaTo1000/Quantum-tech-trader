#!/usr/bin/env python3
"""
FastAPI Service for Quantum Crypto Trader
Provides REST API endpoints for running simulations.
"""

import logging
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from .core import QuantumCryptoTrader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Quantum Crypto Trader API",
    description="Quantum-inspired cryptocurrency trading simulator API",
    version="2.0.0"
)


class SimulationRequest(BaseModel):
    """Request model for simulation endpoint."""
    chaos_level: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Chaos level (0.0-1.0). Higher = more volatility"
    )
    cycles: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Number of trading cycles (1-100)"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for deterministic behavior (optional)"
    )


class SimulationResponse(BaseModel):
    """Response model for simulation endpoint."""
    final_cash: float
    final_portfolio: dict
    trades: list
    chaos_level: float
    total_trades: int
    message: str


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Quantum Crypto Trader API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/healthz",
            "simulate": "/simulate",
            "docs": "/docs"
        }
    }


@app.get("/healthz")
async def health_check():
    """Health check endpoint for monitoring and orchestration."""
    return {
        "status": "healthy",
        "service": "quantum-crypto-trader",
        "version": "2.0.0"
    }


@app.post("/simulate", response_model=SimulationResponse)
async def simulate(
    chaos_level: float = Query(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Chaos level (0.0-1.0)"
    ),
    cycles: int = Query(
        default=5,
        ge=1,
        le=100,
        description="Number of trading cycles (1-100)"
    ),
    seed: Optional[int] = Query(
        default=None,
        description="Random seed for deterministic behavior"
    )
):
    """
    Run a quantum trading simulation.
    
    Returns portfolio state and trade history.
    """
    try:
        logger.info(f"Starting simulation: chaos_level={chaos_level}, cycles={cycles}, seed={seed}")
        
        # Create trader in silent mode (API doesn't need console output)
        trader = QuantumCryptoTrader(
            chaos_level=chaos_level,
            seed=seed,
            silent=True
        )
        
        # Run simulation
        results = trader.run_simulation(cycles=cycles)
        
        # Save trade history to data directory
        data_dir = "./data"
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        filename = trader.save_trade_history(data_dir=data_dir)
        
        logger.info(f"Simulation complete: {results['total_trades']} trades executed")
        
        return SimulationResponse(
            final_cash=results['final_cash'],
            final_portfolio=results['final_portfolio'],
            trades=results['trades'],
            chaos_level=results['chaos_level'],
            total_trades=results['total_trades'],
            message=f"Simulation complete! Trade history saved to {filename}"
        )
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@app.get("/info")
async def info():
    """Get API and trading system information."""
    return {
        "api_version": "2.0.0",
        "system": "Quantum Crypto Trader",
        "description": "Quantum-inspired cryptocurrency trading simulator",
        "warning": "⚠️ SIMULATED ONLY - NOT FINANCIAL ADVICE - USE AT YOUR OWN RISK",
        "features": [
            "Quantum superposition strategy analysis",
            "Entangled correlation analysis",
            "Wave function collapse decision making",
            "Deterministic mode with seed support",
            "Configurable chaos levels"
        ],
        "supported_cryptos": ["BTC", "ETH", "DOGE", "SHIB", "ADA", "SOL", "MATIC", "AVAX"]
    }


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI server.
    
    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: 8000)
    """
    import uvicorn
    logger.info(f"Starting Quantum Trader API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
