#!/usr/bin/env python3
"""
Example usage of the Quantum Crypto Trader
⚠️ USE AT YOUR OWN RISK! ⚠️
"""

from quantum_trader import QuantumCryptoTrader

# Example 1: Mild chaos for cautious traders
print("Example 1: MILD CHAOS MODE (Chaos Level: 0.3)")
print("-" * 60)
trader1 = QuantumCryptoTrader(chaos_level=0.3)
trader1.run_quantum_chaos(cycles=2)

print("\n" + "="*60 + "\n")

# Example 2: Moderate chaos for thrill-seekers
print("Example 2: MODERATE CHAOS MODE (Chaos Level: 0.6)")
print("-" * 60)
trader2 = QuantumCryptoTrader(chaos_level=0.6)
trader2.run_quantum_chaos(cycles=2)

print("\n" + "="*60 + "\n")

# Example 3: MAXIMUM CHAOS for absolute mad lads
print("Example 3: MAXIMUM CHAOS MODE (Chaos Level: 1.0)")
print("-" * 60)
trader3 = QuantumCryptoTrader(chaos_level=1.0)
trader3.run_quantum_chaos(cycles=2)

print("\n" + "🎉"*30)
print("ALL EXAMPLES COMPLETE!")
print("🎉"*30)
print("\n⚠️  Remember: All simulated - no real money involved! ⚠️\n")
