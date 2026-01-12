#!/bin/bash
# Quick start script for Quantum Crypto Trader
# ⚠️ USE AT YOUR OWN RISK! ⚠️

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       🌀 QUANTUM CRYPTO TRADER - QUICK START 🌀         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Select your trading mode:"
echo ""
echo "  === V2 ADVANCED EDITION (NEW!) ==="
echo "  1) 🟢 Conservative (Chaos: 0.3, Risk: 0.2)"
echo "  2) 🟡 Balanced (Chaos: 0.5, Risk: 0.5)"
echo "  3) 🟠 Aggressive (Chaos: 0.8, Risk: 0.8)"
echo "  4) 🔴 DEGEN MODE (Chaos: 1.0, Risk: 1.0)"
echo "  5) 🎮 Custom V2 (enter your own values)"
echo ""
echo "  === ORIGINAL EDITION ==="
echo "  6) 🟢 Mild Chaos (0.3)"
echo "  7) 🟡 Moderate Chaos (0.6)"
echo "  8) 🟠 High Chaos (0.8)"
echo "  9) 🔴 MAXIMUM CHAOS (1.0)"
echo "  10) 🎲 Custom Original"
echo ""
echo "  === EXAMPLES ==="
echo "  11) 📚 Run V2 examples (all modes)"
echo "  12) 📚 Run Original examples"
echo ""
read -p "Enter your choice (1-12): " choice

case $choice in
    1)
        echo -e "0.3\n0.2\n100000\n2\n10" | python3 quantum_trader_v2.py
        ;;
    2)
        echo -e "0.5\n0.5\n100000\n1\n10" | python3 quantum_trader_v2.py
        ;;
    3)
        echo -e "0.8\n0.8\n100000\n5\n10" | python3 quantum_trader_v2.py
        ;;
    4)
        echo -e "1.0\n1.0\n500000\n8\n10" | python3 quantum_trader_v2.py
        ;;
    5)
        python3 quantum_trader_v2.py
        ;;
    6)
        echo -e "0.3\n5" | python3 quantum_trader.py
        ;;
    7)
        echo -e "0.6\n5" | python3 quantum_trader.py
        ;;
    8)
        echo -e "0.8\n5" | python3 quantum_trader.py
        ;;
    9)
        echo -e "1.0\n5" | python3 quantum_trader.py
        ;;
    10)
        python3 quantum_trader.py
        ;;
    11)
        python3 example_usage_v2.py
        ;;
    12)
        python3 example_usage.py
        ;;
    *)
        echo "Invalid choice. Defaulting to V2 Balanced mode..."
        echo -e "0.5\n0.5\n100000\n1\n10" | python3 quantum_trader_v2.py
        ;;
esac

echo ""
echo "✨ Thanks for riding the quantum chaos wave! ✨"
