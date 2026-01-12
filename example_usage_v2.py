#!/usr/bin/env python3
"""
Example usage of the Quantum Crypto Trader V2 - Advanced Edition
⚠️ USE AT YOUR OWN RISK! ⚠️

This demonstrates the advanced features of the V2 trader including:
- Multi-exchange simulation
- Technical indicators (RSI, MACD, Bollinger Bands)
- Sector-based trading
- Risk management configurations
"""

from quantum_trader_v2 import (
    QuantumCryptoTraderV2,
    CRYPTO_ASSETS,
    EXCHANGES,
    MarketSector,
)

print("=" * 80)
print("🌀 QUANTUM CRYPTO TRADER V2 - EXAMPLE USAGE 🌀")
print("=" * 80)

# ============================================================================
# Example 1: Conservative Trader on Coinbase
# ============================================================================
print("\n" + "="*60)
print("Example 1: CONSERVATIVE MODE (Low Risk, Low Chaos)")
print("Exchange: Coinbase | Risk: 0.2 | Chaos: 0.3")
print("="*60)

trader1 = QuantumCryptoTraderV2(
    chaos_level=0.3,
    starting_capital=50000.0,
    primary_exchange="coinbase",
    risk_tolerance=0.2
)
trader1.run_quantum_chaos(cycles=3)

# ============================================================================
# Example 2: Balanced Trader on Binance
# ============================================================================
print("\n" + "="*60)
print("Example 2: BALANCED MODE (Moderate Risk & Chaos)")
print("Exchange: Binance | Risk: 0.5 | Chaos: 0.5")
print("="*60)

trader2 = QuantumCryptoTraderV2(
    chaos_level=0.5,
    starting_capital=100000.0,
    primary_exchange="binance",
    risk_tolerance=0.5
)
trader2.run_quantum_chaos(cycles=3)

# ============================================================================
# Example 3: Aggressive Trader on Bybit
# ============================================================================
print("\n" + "="*60)
print("Example 3: AGGRESSIVE MODE (High Risk, High Chaos)")
print("Exchange: Bybit | Risk: 0.8 | Chaos: 0.8")
print("="*60)

trader3 = QuantumCryptoTraderV2(
    chaos_level=0.8,
    starting_capital=200000.0,
    primary_exchange="bybit",
    risk_tolerance=0.8
)
trader3.run_quantum_chaos(cycles=3)

# ============================================================================
# Example 4: Degen Mode on MEXC (Maximum Chaos!)
# ============================================================================
print("\n" + "="*60)
print("Example 4: DEGEN MODE (Maximum Chaos, Maximum Risk!)")
print("Exchange: MEXC | Risk: 1.0 | Chaos: 1.0")
print("="*60)

trader4 = QuantumCryptoTraderV2(
    chaos_level=1.0,
    starting_capital=500000.0,
    primary_exchange="mexc",
    risk_tolerance=1.0
)
trader4.run_quantum_chaos(cycles=3)

# ============================================================================
# Summary
# ============================================================================
print("\n" + "🎉"*40)
print("ALL V2 EXAMPLES COMPLETE!")
print("🎉"*40)

print("\n📊 AVAILABLE CRYPTO ASSETS:")
for sector in MarketSector:
    sector_assets = [a for a in CRYPTO_ASSETS.values() if a.sector == sector]
    if sector_assets:
        symbols = ", ".join(a.symbol for a in sector_assets)
        print(f"   {sector.value:15s}: {symbols}")

print("\n🏦 AVAILABLE EXCHANGES:")
for key, ex in EXCHANGES.items():
    print(f"   {ex.name:12s} | Fee: {ex.taker_fee:4.2f}% | Coins: {ex.supported_coins:4d}+ | Region: {ex.region}")

print("\n⚠️  Remember: All simulated - no real money involved! ⚠️\n")
