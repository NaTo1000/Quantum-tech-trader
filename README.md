# 🌀 Quantum-tech-trader 🌀

**⚠️ WARNING: USE AT YOUR OWN RISK! MAXIMUM CHAOS MODE! ⚠️**

An experimental quantum-inspired cryptocurrency trading simulator that brings **CRAZY QUANTUM POWER CRYPTO KAOS** to your terminal!

## 🚨 DISCLAIMER 🚨

**THIS IS NOT FINANCIAL ADVICE!** This is an experimental, educational, and entertainment project. 
- All trades are **SIMULATED** (no real money)
- Extremely high volatility and chaos by design
- Use at your own risk - we warned you! 💀

## 🌟 Features

- **Quantum Superposition**: Multiple trading strategies evaluated simultaneously
- **Quantum Entanglement**: Correlated analysis across crypto pairs
- **Wave Function Collapse**: Probabilistic decision-making
- **Quantum Tunneling**: Breakthrough resistance levels unexpectedly
- **Maximum Chaos Mode**: Adjustable volatility from 0% to 100%
- **Multi-Crypto Support**: BTC, ETH, DOGE, SHIB, ADA, SOL, MATIC, AVAX

### 🚀 Fast Market Data Scraping (NEW!)

- **Multi-Source Aggregation**: Query CoinGecko, Binance, and more in parallel
- **WebSocket-Style Streaming**: Real-time price updates with minimal latency
- **Smart TTL Caching**: LRU cache with time-to-live for optimal performance
- **Price Change Detection**: Configurable alerts for significant market moves
- **Batch Requests**: Efficient multi-symbol queries in a single API call

## 🚀 Quick Start

```bash
# Run the quantum chaos!
python3 quantum_trader.py
```

Follow the prompts to set your chaos level (0.0-1.0) and number of trading cycles.

**Recommended**: Start with chaos level 0.5 to ease into the madness! 🎢

### Market Scraper

```bash
# Run the market scraper demo
python3 market_scraper.py

# Or use it programmatically
python3 scraper_example.py
```

## 💡 How It Works

The Quantum Crypto Trader uses quantum-inspired algorithms:

1. **Superposition Strategy Analysis**: Evaluates multiple strategies at once (Momentum, Mean Reversion, YOLO mode, Quantum Intuition)
2. **Entangled Correlation Analysis**: Detects mysterious correlations between crypto pairs
3. **Wave Function Collapse**: Randomly collapses strategies into trading actions (BUY_THE_DIP, MOON_SHOT, PANIC_SELL, HODL, QUANTUM_LEAP)
4. **Quantum Price Oracle**: Simulates crypto prices with quantum uncertainty and occasional "quantum tunneling" events

## 📊 Example Output

```
🌀 QUANTUM TRADING CYCLE | State: ENTANGLED 🌀

💰 BTC: $52341.23456789
   📊 Strategies in superposition: 4
   ⚡ Collapsed action: MOON_SHOT
🚀 QUANTUM BUY: 0.019234 BTC @ $52341.23

💰 ETH: $2847.91283746
   📊 Strategies in superposition: 4
   ⚡ Collapsed action: PANIC_SELL
📉 QUANTUM SELL: 0.582341 ETH @ $2847.91
```

## 🎮 Trading Actions

- **HODL**: Hold your position (diamond hands! 💎)
- **BUY_THE_DIP**: Buy when the price drops
- **MOON_SHOT**: Aggressive buy for maximum gains 🌙
- **PANIC_SELL**: Sell in fear (paper hands! 📄)
- **QUANTUM_LEAP**: Surprise trade based on quantum randomness

## 📁 Output

The trader saves a complete history of all trades to a JSON file:
- `quantum_trades_YYYYMMDD_HHMMSS.json`

## ⚡ Requirements

- Python 3.6 or higher
- No external dependencies (pure Python standard library!)

## 🎲 Chaos Levels

- **0.0-0.3**: Mild chaos (boring! 😴)
- **0.4-0.6**: Moderate chaos (exciting! 🎢)
- **0.7-0.9**: HIGH CHAOS (wild ride! 🎪)
- **0.9-1.0**: MAXIMUM CHAOS (absolute mayhem! 🌪️💀)

## 🛡️ Safety Features

Despite the chaos, this simulator includes:
- Position sizing limits (5-20% per trade)
- Virtual portfolio tracking
- Complete trade history logging
- No connection to real exchanges
- No real money at risk!

## 🎯 Educational Purpose

This project demonstrates:
- Probabilistic trading strategies
- Portfolio management concepts
- Risk simulation
- Quantum computing metaphors in finance
- The importance of risk management

## 🤝 Contributing

Want to add more chaos? Feel free to contribute! Ideas:
- More quantum-inspired strategies
- Advanced portfolio rebalancing
- Quantum error correction for trades
- Quantum machine learning models
- Integration with real price feeds (simulated only!)

## 📜 License

MIT License - Use at your own risk!

## 🚀 Market Scraper - Fast Data Algorithms

The `market_scraper.py` module implements high-performance scraping algorithms for real-time market data:

### Scraping Strategies

| Strategy | Latency | Best For |
|----------|---------|----------|
| WebSocket Streaming | Sub-500ms | Real-time trading, live dashboards |
| Async HTTP Batch | 100-500ms | Multi-symbol queries, snapshots |
| Cached REST | 0ms (hit) | High-frequency repeated queries |

### Quick Usage

```python
from market_scraper import QuantumMarketScraper

# Create scraper with default settings
scraper = QuantumMarketScraper(
    symbols=["BTC", "ETH", "SOL"],
    cache_ttl=5.0,           # Cache for 5 seconds
    change_threshold=1.0     # Alert on 1% changes
)

# Get current prices
prices = scraper.get_prices()
for symbol, tick in prices.items():
    print(f"{symbol}: ${tick.price:,.2f}")

# Set up price alerts
def on_alert(alert):
    print(f"🚨 {alert['symbol']} moved {alert['change_percent']:.2f}%!")

scraper.subscribe_alerts(on_alert)

# Start streaming (runs in background thread)
scraper.start_streaming()
```

### Available Scrapers

1. **CoinGeckoScraper**: Free API, no key required, includes 24h volume/change
2. **BinanceScraper**: Low latency, includes bid/ask spread, order book access
3. **AsyncMarketAggregator**: Queries multiple sources in parallel
4. **WebSocketPriceStream**: Simulated streaming with callbacks
5. **PriceChangeDetector**: Volatility tracking and threshold alerts

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   QuantumMarketScraper                      │
│  (High-level API with all features integrated)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌──────────────┐ ┌───────────────┐ ┌────────────────┐
│  Aggregator  │ │  WebSocket    │ │  Change        │
│  (Multi-src) │ │  Stream       │ │  Detector      │
└──────┬───────┘ └───────────────┘ └────────────────┘
       │
       ├───────────────┬───────────────┐
       ▼               ▼               ▼
┌──────────────┐ ┌───────────────┐ ┌────────────────┐
│  CoinGecko   │ │   Binance     │ │  TTL Cache     │
│  Scraper     │ │   Scraper     │ │  (LRU + TTL)   │
└──────────────┘ └───────────────┘ └────────────────┘
```

## 🔥 Let It Rip!

Remember: **This is pure chaos by design!** Embrace the quantum uncertainty and enjoy the ride!

```
🌀🌀🌀 QUANTUM CHAOS AWAITS 🌀🌀🌀
```

---

**Made with ⚡ quantum chaos ⚡ and 💀 maximum risk 💀**
