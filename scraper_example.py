#!/usr/bin/env python3
"""
Example usage of the Quantum Market Scraper
Demonstrates fast market data scraping algorithms

⚠️ EDUCATIONAL USE ONLY - RESPECT API RATE LIMITS! ⚠️
"""

from market_scraper import (
    QuantumMarketScraper,
    CoinGeckoScraper,
    BinanceScraper,
    AsyncMarketAggregator,
    WebSocketPriceStream,
    PriceChangeDetector,
    MarketTick,
)

# =============================================================================
# Example 1: Simple Price Fetching
# =============================================================================


def example_simple_fetch():
    """Demonstrates basic price fetching from a single source."""
    print("\n" + "=" * 60)
    print("📊 Example 1: Simple Price Fetching")
    print("=" * 60)

    # Use CoinGecko scraper (free, no API key needed)
    scraper = CoinGeckoScraper(cache_ttl=10.0)

    # Fetch single price
    print("\n🔍 Fetching BTC price from CoinGecko...")
    btc = scraper.get_price("BTC")
    if btc:
        print(f"   💰 BTC: ${btc.price:,.2f}")
        print(f"   📈 24h Change: {btc.change_24h:+.2f}%")
        print(f"   📊 Source: {btc.source}")
    else:
        print("   ⚠️ Could not fetch price (network unavailable)")

    # Batch fetch multiple prices (more efficient!)
    print("\n🔍 Batch fetching multiple prices...")
    prices = scraper.get_prices(["BTC", "ETH", "SOL", "DOGE"])
    for symbol, tick in prices.items():
        print(f"   💰 {symbol}: ${tick.price:,.2f}")


# =============================================================================
# Example 2: Multi-Source Aggregation
# =============================================================================


def example_multi_source():
    """Demonstrates aggregating prices from multiple sources."""
    print("\n" + "=" * 60)
    print("🔗 Example 2: Multi-Source Aggregation")
    print("=" * 60)

    # Create aggregator that uses multiple sources
    aggregator = AsyncMarketAggregator(cache_ttl=5.0)

    print("\n🔍 Getting best prices from all sources...")
    prices = aggregator.get_batch_prices(["BTC", "ETH"])

    for symbol, tick in prices.items():
        print(f"\n   💰 {symbol}: ${tick.price:,.2f}")
        print(f"      Source: {tick.source}")
        print(f"      Age: {tick.age_ms:.0f}ms")

    # Compare prices across sources
    print("\n🔍 Comparing BTC prices across sources...")
    btc_prices = aggregator.get_all_prices("BTC")
    for tick in btc_prices:
        print(f"   {tick.source}: ${tick.price:,.2f}")


# =============================================================================
# Example 3: Real-Time Streaming
# =============================================================================


def example_streaming():
    """Demonstrates real-time price streaming."""
    print("\n" + "=" * 60)
    print("📡 Example 3: Real-Time Price Streaming")
    print("=" * 60)

    # Create a price stream
    stream = WebSocketPriceStream(
        symbols=["BTC", "ETH", "SOL"],
        update_interval=2.0,  # Poll every 2 seconds
        use_binance=True,
    )

    # Set up callback for price updates
    def on_price_update(tick: MarketTick):
        print(f"   📈 {tick.symbol}: ${tick.price:,.2f} (age: {tick.age_ms:.0f}ms)")

    stream.subscribe(on_price_update)

    print("\n🔌 Starting price stream (simulated WebSocket)...")
    print("   Note: In production, use actual WebSocket connections")
    print("   for sub-100ms latency!")
    print("\n   (Press Ctrl+C to stop)\n")

    try:
        stream.start()
        # Let it run for a few seconds in demo
        import time

        time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop()


# =============================================================================
# Example 4: Price Change Detection
# =============================================================================


def example_change_detection():
    """Demonstrates price change detection with alerts."""
    print("\n" + "=" * 60)
    print("🚨 Example 4: Price Change Detection")
    print("=" * 60)

    # Create a detector with 0.5% threshold
    detector = PriceChangeDetector(
        threshold_percent=0.5, window_size=10  # Alert on 0.5% changes
    )

    # Simulate some price ticks
    import time

    prices = [50000, 50100, 50200, 50500, 50000, 49500, 50000]

    print("\n📊 Processing simulated BTC price ticks...")
    for price in prices:
        tick = MarketTick(symbol="BTC", price=price, source="simulation")
        alert = detector.on_tick(tick)

        if alert:
            print(
                f"   🚨 ALERT: {alert['direction']} by {alert['change_percent']:.2f}%"
            )
            print(f"      Price: ${alert['price']:,.2f}")
        else:
            print(f"   📊 BTC: ${price:,.2f}")

        time.sleep(0.1)

    # Get volatility
    volatility = detector.get_volatility("BTC")
    if volatility:
        print(f"\n   📈 Calculated Volatility: {volatility:.2f}%")


# =============================================================================
# Example 5: Full Integration
# =============================================================================


def example_full_integration():
    """Demonstrates the high-level QuantumMarketScraper API."""
    print("\n" + "=" * 60)
    print("🚀 Example 5: Full Integration (QuantumMarketScraper)")
    print("=" * 60)

    # Create the all-in-one scraper
    scraper = QuantumMarketScraper(
        symbols=["BTC", "ETH", "SOL", "DOGE"],
        cache_ttl=5.0,
        stream_interval=3.0,
        change_threshold=1.0,  # 1% change threshold for alerts
    )

    # Set up alert handler
    def on_alert(alert):
        print(
            f"\n   🚨 PRICE ALERT: {alert['symbol']} {alert['direction']}"
            f" by {alert['change_percent']:.2f}%"
        )

    scraper.subscribe_alerts(on_alert)

    # Get current prices
    print("\n📊 Fetching current market prices...")
    prices = scraper.get_prices()

    for symbol, tick in prices.items():
        print(f"   💰 {symbol}: ${tick.price:,.2f}")

    # Get market summary
    print("\n📊 Getting market summary...")
    summary = scraper.get_market_summary()
    print(f"   Timestamp: {summary['timestamp']}")
    for symbol, data in summary.get("markets", {}).items():
        print(f"   {symbol}: ${data['price']:,.2f} (source: {data['source']})")

    # Show metrics
    print("\n📈 Scraper Metrics:")
    metrics = scraper.get_metrics()
    agg_metrics = metrics.get("aggregator", {})
    print(f"   Total Requests: {agg_metrics.get('total_requests', 0)}")
    print(f"   Cache Hits: {agg_metrics.get('total_cache_hits', 0)}")
    print(f"   Errors: {agg_metrics.get('total_errors', 0)}")


# =============================================================================
# Main
# =============================================================================


def main():
    """Run all examples."""
    print(
        """
    ╔══════════════════════════════════════════════════════════╗
    ║      🚀 QUANTUM MARKET SCRAPER - EXAMPLES 🚀             ║
    ║                                                          ║
    ║  Demonstrating fast market data scraping algorithms      ║
    ║  for real-time cryptocurrency price information          ║
    ╚══════════════════════════════════════════════════════════╝
    
    ⚠️ Note: Network access may be restricted in some environments.
    Examples will show structure even if API calls fail.
    """
    )

    # Run each example
    example_simple_fetch()
    example_multi_source()
    example_change_detection()  # Uses simulated data
    example_full_integration()

    # Skip streaming in automated runs
    print("\n" + "=" * 60)
    print("📡 Streaming Example (skipped in automated mode)")
    print("=" * 60)
    print("   Run: python3 -c 'from scraper_example import example_streaming; example_streaming()'")
    print("   to see the streaming example in action!")

    print("\n" + "🎉" * 30)
    print("ALL EXAMPLES COMPLETE!")
    print("🎉" * 30)
    print("\n⚠️ Remember: Respect API rate limits in production! ⚠️\n")


if __name__ == "__main__":
    main()
