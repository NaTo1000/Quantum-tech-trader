#!/bin/bash
# Quick start script for Quantum Crypto Trader
# ⚠️ USE AT YOUR OWN RISK! ⚠️

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       🌀 QUANTUM CRYPTO TRADER - QUICK START 🌀         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Select your chaos level:"
echo ""
echo "  1) 🟢 Mild Chaos (0.3) - For cautious traders"
echo "  2) 🟡 Moderate Chaos (0.6) - For thrill-seekers"
echo "  3) 🟠 High Chaos (0.8) - For risk-takers"
echo "  4) 🔴 MAXIMUM CHAOS (1.0) - For absolute mad lads"
echo "  5) 🎮 Run examples (all chaos levels)"
echo "  6) 🎲 Custom (enter your own values)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "0.3\n5" | python3 quantum_trader.py
        ;;
    2)
        echo -e "0.6\n5" | python3 quantum_trader.py
        ;;
    3)
        echo -e "0.8\n5" | python3 quantum_trader.py
        ;;
    4)
        echo -e "1.0\n5" | python3 quantum_trader.py
        ;;
    5)
        python3 example_usage.py
        ;;
    6)
        python3 quantum_trader.py
        ;;
    *)
        echo "Invalid choice. Defaulting to moderate chaos..."
        echo -e "0.6\n5" | python3 quantum_trader.py
        ;;
esac

echo ""
echo "✨ Thanks for riding the quantum chaos wave! ✨"
