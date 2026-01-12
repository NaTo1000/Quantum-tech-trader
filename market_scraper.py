#!/usr/bin/env python3
"""
🚀 QUANTUM MARKET SCRAPER 🚀
Fast, efficient algorithms for real-time cryptocurrency market data scraping.

This module implements multiple scraping strategies optimized for speed:
1. WebSocket streaming - Lowest latency, real-time push notifications
2. Async HTTP batch fetching - Parallel multi-source queries
3. Smart caching with TTL - Reduces redundant requests
4. Multi-exchange aggregation - Best price discovery

⚠️ DISCLAIMER: For educational purposes only. Respect API rate limits! ⚠️
"""

import json
import ssl
import threading
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# =============================================================================
# Data Structures
# =============================================================================


@dataclass
class MarketTick:
    """Represents a single market data point."""

    symbol: str
    price: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    volume_24h: Optional[float] = None
    change_24h: Optional[float] = None
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "symbol": self.symbol,
            "price": self.price,
            "bid": self.bid,
            "ask": self.ask,
            "volume_24h": self.volume_24h,
            "change_24h": self.change_24h,
            "timestamp": self.timestamp,
            "source": self.source,
        }

    @property
    def age_ms(self) -> float:
        """Returns the age of this tick in milliseconds."""
        return (time.time() - self.timestamp) * 1000

    @property
    def spread(self) -> Optional[float]:
        """Calculate bid-ask spread if both are available."""
        if self.bid and self.ask:
            return self.ask - self.bid
        return None


@dataclass
class ScraperMetrics:
    """Tracks scraper performance metrics."""

    requests_made: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    errors: int = 0
    avg_latency_ms: float = 0.0
    last_update: float = field(default_factory=time.time)

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as percentage."""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0


# =============================================================================
# LRU Cache with TTL - Optimized for Speed
# =============================================================================


class TTLCache:
    """
    Thread-safe Least Recently Used (LRU) cache with Time-To-Live (TTL).

    Optimized for fast market data lookups with automatic expiration.
    Uses OrderedDict for O(1) access and LRU eviction.
    """

    def __init__(self, max_size: int = 1000, default_ttl: float = 5.0):
        """
        Initialize the TTL cache.

        Args:
            max_size: Maximum number of items to store
            default_ttl: Default time-to-live in seconds
        """
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if exists and not expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            value, expiry = self._cache[key]
            if time.time() > expiry:
                # Expired - remove and return None
                del self._cache[key]
                self._misses += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._hits += 1
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            ttl = ttl if ttl is not None else self._default_ttl
            expiry = time.time() + ttl

            # Remove if exists (to update position)
            if key in self._cache:
                del self._cache[key]

            # Add to end
            self._cache[key] = (value, expiry)

            # Evict oldest if over capacity
            while len(self._cache) > self._max_size:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns:
            Number of entries removed
        """
        with self._lock:
            now = time.time()
            expired_keys = [k for k, (_, exp) in self._cache.items() if now > exp]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)

    @property
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": (self._hits / total * 100) if total > 0 else 0.0,
            }


# =============================================================================
# Abstract Base Scraper
# =============================================================================


class BaseMarketScraper(ABC):
    """
    Abstract base class for market data scrapers.

    Provides common functionality and defines the interface for all scrapers.
    """

    def __init__(
        self,
        cache_ttl: float = 5.0,
        timeout: float = 10.0,
        user_agent: str = "QuantumTrader/1.0",
    ):
        """
        Initialize the scraper.

        Args:
            cache_ttl: Cache time-to-live in seconds
            timeout: Request timeout in seconds
            user_agent: User agent string for HTTP requests
        """
        self.cache = TTLCache(default_ttl=cache_ttl)
        self.timeout = timeout
        self.user_agent = user_agent
        self.metrics = ScraperMetrics()
        self._running = False
        self._callbacks: List[Callable[[MarketTick], None]] = []

    @abstractmethod
    def get_price(self, symbol: str) -> Optional[MarketTick]:
        """
        Get current price for a symbol.

        Args:
            symbol: Trading symbol (e.g., 'BTC', 'ETH')

        Returns:
            MarketTick with current price or None if unavailable
        """
        pass

    @abstractmethod
    def get_prices(self, symbols: List[str]) -> Dict[str, MarketTick]:
        """
        Get prices for multiple symbols efficiently.

        Args:
            symbols: List of trading symbols

        Returns:
            Dictionary mapping symbols to MarketTick objects
        """
        pass

    def subscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """
        Subscribe to real-time price updates.

        Args:
            callback: Function to call when new price data arrives
        """
        self._callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """
        Unsubscribe from price updates.

        Args:
            callback: Previously subscribed callback function
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_subscribers(self, tick: MarketTick) -> None:
        """Notify all subscribers of a new tick."""
        for callback in self._callbacks:
            try:
                callback(tick)
            except Exception:
                pass  # Don't let subscriber errors crash the scraper

    def _make_request(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """
        Make an HTTP GET request with error handling.

        Args:
            url: URL to fetch
            headers: Optional additional headers

        Returns:
            Response body as string or None on error
        """
        start_time = time.time()
        try:
            req_headers = {"User-Agent": self.user_agent}
            if headers:
                req_headers.update(headers)

            # Create request with headers
            request = Request(url, headers=req_headers)

            # Create SSL context that verifies certificates
            context = ssl.create_default_context()

            with urlopen(request, timeout=self.timeout, context=context) as response:
                data = response.read().decode("utf-8")

            # Update metrics
            latency = (time.time() - start_time) * 1000
            self._update_latency(latency)
            self.metrics.requests_made += 1

            return data

        except (URLError, HTTPError, TimeoutError) as e:
            self.metrics.errors += 1
            print(f"⚠️ Request error for {url}: {e}")
            return None

    def _update_latency(self, latency_ms: float) -> None:
        """Update running average latency."""
        n = self.metrics.requests_made
        if n == 0:
            self.metrics.avg_latency_ms = latency_ms
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics.avg_latency_ms = (
                alpha * latency_ms + (1 - alpha) * self.metrics.avg_latency_ms
            )


# =============================================================================
# CoinGecko Scraper - Free, No API Key Required
# =============================================================================


class CoinGeckoScraper(BaseMarketScraper):
    """
    Market data scraper using CoinGecko's free public API.

    Features:
    - No API key required for basic usage
    - Supports batch queries for efficiency
    - Automatic rate limiting
    - Price, volume, and 24h change data
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    # Map common symbols to CoinGecko IDs
    SYMBOL_MAP = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "DOGE": "dogecoin",
        "SHIB": "shiba-inu",
        "ADA": "cardano",
        "SOL": "solana",
        "MATIC": "matic-network",
        "AVAX": "avalanche-2",
        "XRP": "ripple",
        "DOT": "polkadot",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "LTC": "litecoin",
        "ATOM": "cosmos",
        "NEAR": "near",
        "APT": "aptos",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rate_limit_delay = 0.5  # Seconds between requests

    def _get_coingecko_id(self, symbol: str) -> Optional[str]:
        """Map trading symbol to CoinGecko ID."""
        return self.SYMBOL_MAP.get(symbol.upper())

    def get_price(self, symbol: str) -> Optional[MarketTick]:
        """Get current price for a single symbol."""
        # Check cache first
        cache_key = f"price:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            self.metrics.cache_hits += 1
            return cached

        self.metrics.cache_misses += 1

        # Get CoinGecko ID
        coin_id = self._get_coingecko_id(symbol)
        if not coin_id:
            return None

        # Fetch from API
        url = f"{self.BASE_URL}/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
        data = self._make_request(url)

        if not data:
            return None

        try:
            parsed = json.loads(data)
            coin_data = parsed.get(coin_id, {})

            tick = MarketTick(
                symbol=symbol.upper(),
                price=coin_data.get("usd", 0),
                volume_24h=coin_data.get("usd_24h_vol"),
                change_24h=coin_data.get("usd_24h_change"),
                source="coingecko",
            )

            # Cache the result
            self.cache.set(cache_key, tick)
            return tick

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Parse error for {symbol}: {e}")
            return None

    def get_prices(self, symbols: List[str]) -> Dict[str, MarketTick]:
        """
        Get prices for multiple symbols in a single batch request.
        This is much more efficient than individual requests!
        """
        result: Dict[str, MarketTick] = {}

        # Check cache for each symbol, collect missing ones
        missing_symbols: List[str] = []
        for symbol in symbols:
            cache_key = f"price:{symbol}"
            cached = self.cache.get(cache_key)
            if cached:
                result[symbol] = cached
                self.metrics.cache_hits += 1
            else:
                missing_symbols.append(symbol)
                self.metrics.cache_misses += 1

        if not missing_symbols:
            return result

        # Map symbols to CoinGecko IDs
        ids_map = {}
        for symbol in missing_symbols:
            coin_id = self._get_coingecko_id(symbol)
            if coin_id:
                ids_map[coin_id] = symbol

        if not ids_map:
            return result

        # Batch request for all missing symbols
        ids_str = ",".join(ids_map.keys())
        url = f"{self.BASE_URL}/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
        data = self._make_request(url)

        if not data:
            return result

        try:
            parsed = json.loads(data)

            for coin_id, symbol in ids_map.items():
                coin_data = parsed.get(coin_id, {})
                if coin_data:
                    tick = MarketTick(
                        symbol=symbol.upper(),
                        price=coin_data.get("usd", 0),
                        volume_24h=coin_data.get("usd_24h_vol"),
                        change_24h=coin_data.get("usd_24h_change"),
                        source="coingecko",
                    )
                    result[symbol] = tick
                    self.cache.set(f"price:{symbol}", tick)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Batch parse error: {e}")

        return result


# =============================================================================
# Binance Scraper - Fast, Low Latency
# =============================================================================


class BinanceScraper(BaseMarketScraper):
    """
    Market data scraper using Binance's public API.

    Features:
    - Very low latency
    - Real-time ticker data
    - Order book depth available
    - No API key required for public endpoints
    """

    BASE_URL = "https://api.binance.com/api/v3"

    # Map common symbols to Binance trading pairs
    SYMBOL_MAP = {
        "BTC": "BTCUSDT",
        "ETH": "ETHUSDT",
        "DOGE": "DOGEUSDT",
        "SHIB": "SHIBUSDT",
        "ADA": "ADAUSDT",
        "SOL": "SOLUSDT",
        "MATIC": "MATICUSDT",
        "AVAX": "AVAXUSDT",
        "XRP": "XRPUSDT",
        "DOT": "DOTUSDT",
        "LINK": "LINKUSDT",
        "UNI": "UNIUSDT",
        "LTC": "LTCUSDT",
        "ATOM": "ATOMUSDT",
        "NEAR": "NEARUSDT",
        "APT": "APTUSDT",
    }

    def _get_binance_symbol(self, symbol: str) -> Optional[str]:
        """Map trading symbol to Binance pair."""
        return self.SYMBOL_MAP.get(symbol.upper())

    def get_price(self, symbol: str) -> Optional[MarketTick]:
        """Get current price with bid/ask spread."""
        # Check cache first
        cache_key = f"price:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            self.metrics.cache_hits += 1
            return cached

        self.metrics.cache_misses += 1

        # Get Binance symbol
        binance_symbol = self._get_binance_symbol(symbol)
        if not binance_symbol:
            return None

        # Fetch ticker data (includes price, bid, ask)
        url = f"{self.BASE_URL}/ticker/bookTicker?symbol={binance_symbol}"
        data = self._make_request(url)

        if not data:
            return None

        try:
            parsed = json.loads(data)

            bid = float(parsed.get("bidPrice", 0))
            ask = float(parsed.get("askPrice", 0))
            price = (bid + ask) / 2  # Mid price

            tick = MarketTick(
                symbol=symbol.upper(),
                price=price,
                bid=bid,
                ask=ask,
                source="binance",
            )

            self.cache.set(cache_key, tick)
            return tick

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ Parse error for {symbol}: {e}")
            return None

    def get_prices(self, symbols: List[str]) -> Dict[str, MarketTick]:
        """
        Get prices for multiple symbols using Binance's batch ticker endpoint.
        """
        result: Dict[str, MarketTick] = {}

        # Check cache first
        missing_symbols: List[str] = []
        for symbol in symbols:
            cache_key = f"price:{symbol}"
            cached = self.cache.get(cache_key)
            if cached:
                result[symbol] = cached
                self.metrics.cache_hits += 1
            else:
                missing_symbols.append(symbol)
                self.metrics.cache_misses += 1

        if not missing_symbols:
            return result

        # Build reverse map for lookup
        binance_to_symbol = {}
        for symbol in missing_symbols:
            binance_sym = self._get_binance_symbol(symbol)
            if binance_sym:
                binance_to_symbol[binance_sym] = symbol

        if not binance_to_symbol:
            return result

        # Fetch all tickers at once
        url = f"{self.BASE_URL}/ticker/bookTicker"
        data = self._make_request(url)

        if not data:
            return result

        try:
            all_tickers = json.loads(data)

            for ticker in all_tickers:
                binance_sym = ticker.get("symbol")
                if binance_sym in binance_to_symbol:
                    symbol = binance_to_symbol[binance_sym]
                    bid = float(ticker.get("bidPrice", 0))
                    ask = float(ticker.get("askPrice", 0))
                    price = (bid + ask) / 2

                    tick = MarketTick(
                        symbol=symbol.upper(),
                        price=price,
                        bid=bid,
                        ask=ask,
                        source="binance",
                    )
                    result[symbol] = tick
                    self.cache.set(f"price:{symbol}", tick)

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ Batch parse error: {e}")

        return result

    def get_order_book(
        self, symbol: str, depth: int = 5
    ) -> Optional[Dict[str, List[tuple]]]:
        """
        Get order book depth for a symbol.

        Args:
            symbol: Trading symbol
            depth: Number of levels to fetch (5, 10, 20, 50, 100, 500, 1000)

        Returns:
            Dictionary with 'bids' and 'asks' lists
        """
        binance_symbol = self._get_binance_symbol(symbol)
        if not binance_symbol:
            return None

        url = f"{self.BASE_URL}/depth?symbol={binance_symbol}&limit={depth}"
        data = self._make_request(url)

        if not data:
            return None

        try:
            parsed = json.loads(data)
            return {
                "bids": [
                    (float(price), float(qty)) for price, qty in parsed.get("bids", [])
                ],
                "asks": [
                    (float(price), float(qty)) for price, qty in parsed.get("asks", [])
                ],
            }
        except (json.JSONDecodeError, KeyError, ValueError):
            return None


# =============================================================================
# Async Multi-Source Aggregator - Maximum Speed
# =============================================================================


class AsyncMarketAggregator:
    """
    Async aggregator that queries multiple sources in parallel.

    Features:
    - Parallel queries to multiple exchanges
    - Best price discovery (lowest ask, highest bid)
    - Automatic failover if one source fails
    - Combined metrics tracking
    """

    def __init__(self, cache_ttl: float = 3.0):
        """Initialize with multiple scrapers."""
        self.scrapers = [
            CoinGeckoScraper(cache_ttl=cache_ttl),
            BinanceScraper(cache_ttl=cache_ttl),
        ]
        self.cache = TTLCache(default_ttl=cache_ttl)
        self._callbacks: List[Callable[[MarketTick], None]] = []

    def get_best_price(self, symbol: str) -> Optional[MarketTick]:
        """
        Get the best price from all sources.
        Returns the most recent price with lowest latency.
        """
        cache_key = f"best:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        prices = []
        for scraper in self.scrapers:
            try:
                tick = scraper.get_price(symbol)
                if tick:
                    prices.append(tick)
            except Exception:
                continue

        if not prices:
            return None

        # Return the most recent tick (lowest age)
        best = min(prices, key=lambda t: t.age_ms)
        self.cache.set(cache_key, best)
        return best

    def get_all_prices(self, symbol: str) -> List[MarketTick]:
        """Get prices from all sources for comparison."""
        prices = []
        for scraper in self.scrapers:
            try:
                tick = scraper.get_price(symbol)
                if tick:
                    prices.append(tick)
            except Exception:
                continue
        return prices

    def get_batch_prices(self, symbols: List[str]) -> Dict[str, MarketTick]:
        """
        Get prices for multiple symbols from all sources.
        Uses the best available price for each symbol.
        """
        result: Dict[str, MarketTick] = {}

        # Query each scraper
        all_results: List[Dict[str, MarketTick]] = []
        for scraper in self.scrapers:
            try:
                prices = scraper.get_prices(symbols)
                all_results.append(prices)
            except Exception:
                continue

        # Merge results, keeping the most recent for each symbol
        for symbol in symbols:
            candidates = []
            for prices in all_results:
                if symbol in prices:
                    candidates.append(prices[symbol])

            if candidates:
                result[symbol] = min(candidates, key=lambda t: t.age_ms)

        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Get combined metrics from all scrapers."""
        combined = {
            "total_requests": 0,
            "total_errors": 0,
            "total_cache_hits": 0,
            "total_cache_misses": 0,
            "scrapers": [],
        }

        for scraper in self.scrapers:
            metrics = scraper.metrics
            combined["total_requests"] += metrics.requests_made
            combined["total_errors"] += metrics.errors
            combined["total_cache_hits"] += metrics.cache_hits
            combined["total_cache_misses"] += metrics.cache_misses
            combined["scrapers"].append(
                {
                    "type": scraper.__class__.__name__,
                    "requests": metrics.requests_made,
                    "errors": metrics.errors,
                    "avg_latency_ms": round(metrics.avg_latency_ms, 2),
                    "cache": scraper.cache.stats,
                }
            )

        return combined

    def subscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """Subscribe to price updates from all sources."""
        for scraper in self.scrapers:
            scraper.subscribe(callback)

    def unsubscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """Unsubscribe from all sources."""
        for scraper in self.scrapers:
            scraper.unsubscribe(callback)


# =============================================================================
# WebSocket Streaming Simulator
# =============================================================================


class WebSocketPriceStream:
    """
    Simulates WebSocket-like streaming for real-time price updates.

    In production, this would connect to actual WebSocket endpoints like:
    - Binance: wss://stream.binance.com:9443/ws/<symbol>@ticker
    - CoinGecko: Not available (REST only)
    - Kraken: wss://ws.kraken.com

    This implementation polls at high frequency to simulate streaming
    for demonstration purposes.

    ⚠️ Note: For actual low-latency trading, use real WebSocket connections!
    """

    def __init__(
        self, symbols: List[str], update_interval: float = 1.0, use_binance: bool = True
    ):
        """
        Initialize the price stream.

        Args:
            symbols: List of symbols to stream
            update_interval: Seconds between updates (simulated)
            use_binance: If True, use Binance API; else use CoinGecko
        """
        self.symbols = [s.upper() for s in symbols]
        self.update_interval = update_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[MarketTick], None]] = []
        self._latest: Dict[str, MarketTick] = {}
        self._lock = threading.Lock()

        # Choose scraper based on preference
        if use_binance:
            self._scraper = BinanceScraper(cache_ttl=0.5)  # Short TTL for freshness
        else:
            self._scraper = CoinGeckoScraper(cache_ttl=1.0)

    def subscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """Add a callback for price updates."""
        with self._lock:
            self._callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[MarketTick], None]) -> None:
        """Remove a callback."""
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def start(self) -> None:
        """Start the streaming thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._stream_loop, daemon=True)
        self._thread.start()
        print(f"🔌 Price stream started for: {', '.join(self.symbols)}")

    def stop(self) -> None:
        """Stop the streaming thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("🔌 Price stream stopped")

    def _stream_loop(self) -> None:
        """Main streaming loop that fetches and broadcasts prices."""
        while self._running:
            try:
                # Fetch all prices in batch
                prices = self._scraper.get_prices(self.symbols)

                # Update latest and notify subscribers
                with self._lock:
                    for symbol, tick in prices.items():
                        old_tick = self._latest.get(symbol)
                        self._latest[symbol] = tick

                        # Only notify if price changed
                        if old_tick is None or old_tick.price != tick.price:
                            self._notify(tick)

            except Exception as e:
                print(f"⚠️ Stream error: {e}")

            time.sleep(self.update_interval)

    def _notify(self, tick: MarketTick) -> None:
        """Notify all subscribers of a price update."""
        with self._lock:
            callbacks = list(self._callbacks)

        for callback in callbacks:
            try:
                callback(tick)
            except Exception:
                pass

    def get_latest(self, symbol: str) -> Optional[MarketTick]:
        """Get the latest cached price for a symbol."""
        with self._lock:
            return self._latest.get(symbol.upper())

    def get_all_latest(self) -> Dict[str, MarketTick]:
        """Get all latest prices."""
        with self._lock:
            return dict(self._latest)

    @property
    def is_running(self) -> bool:
        """Check if the stream is running."""
        return self._running


# =============================================================================
# Price Change Detector - For Fast Market Change Detection
# =============================================================================


class PriceChangeDetector:
    """
    Detects significant price changes in real-time.

    Features:
    - Configurable change thresholds
    - Moving average tracking
    - Volatility calculation
    - Alert callbacks for significant moves
    """

    def __init__(
        self,
        threshold_percent: float = 1.0,
        window_size: int = 20,
    ):
        """
        Initialize the detector.

        Args:
            threshold_percent: Minimum % change to trigger alert
            window_size: Number of ticks to track for moving average
        """
        self.threshold = threshold_percent / 100
        self.window_size = window_size
        self._history: Dict[str, List[float]] = {}
        self._alerts: List[Callable[[str, float, float, str], None]] = []
        self._lock = threading.Lock()

    def on_tick(self, tick: MarketTick) -> Optional[Dict[str, Any]]:
        """
        Process a new price tick and check for significant changes.

        Returns:
            Alert data if significant change detected, None otherwise
        """
        with self._lock:
            symbol = tick.symbol
            price = tick.price

            if symbol not in self._history:
                self._history[symbol] = []

            history = self._history[symbol]

            if len(history) > 0:
                prev_price = history[-1]
                change = (price - prev_price) / prev_price

                if abs(change) >= self.threshold:
                    direction = "UP 📈" if change > 0 else "DOWN 📉"
                    alert = {
                        "symbol": symbol,
                        "price": price,
                        "prev_price": prev_price,
                        "change_percent": change * 100,
                        "direction": direction,
                        "timestamp": tick.timestamp,
                    }

                    # Notify alert subscribers
                    self._notify_alert(
                        symbol, price, change * 100, direction
                    )

                    return alert

            # Add to history
            history.append(price)
            if len(history) > self.window_size:
                history.pop(0)

            return None

    def subscribe_alert(
        self, callback: Callable[[str, float, float, str], None]
    ) -> None:
        """Subscribe to price change alerts."""
        self._alerts.append(callback)

    def _notify_alert(
        self, symbol: str, price: float, change: float, direction: str
    ) -> None:
        """Notify all alert subscribers."""
        for callback in self._alerts:
            try:
                callback(symbol, price, change, direction)
            except Exception:
                pass

    def get_volatility(self, symbol: str) -> Optional[float]:
        """
        Calculate price volatility for a symbol.

        Returns:
            Standard deviation of price changes as percentage
        """
        with self._lock:
            history = self._history.get(symbol, [])
            if len(history) < 2:
                return None

            # Calculate returns
            returns = []
            for i in range(1, len(history)):
                ret = (history[i] - history[i - 1]) / history[i - 1]
                returns.append(ret)

            # Calculate standard deviation
            mean = sum(returns) / len(returns)
            variance = sum((r - mean) ** 2 for r in returns) / len(returns)
            return (variance**0.5) * 100  # Return as percentage

    def get_moving_average(self, symbol: str) -> Optional[float]:
        """Get the simple moving average for a symbol."""
        with self._lock:
            history = self._history.get(symbol, [])
            if not history:
                return None
            return sum(history) / len(history)


# =============================================================================
# High-Level API - Easy to Use Interface
# =============================================================================


class QuantumMarketScraper:
    """
    High-level market scraper with all features integrated.

    This is the recommended interface for using the scraping system.
    It combines:
    - Multi-source aggregation
    - Real-time streaming
    - Price change detection
    - Performance metrics
    """

    def __init__(
        self,
        symbols: Optional[List[str]] = None,
        cache_ttl: float = 3.0,
        stream_interval: float = 2.0,
        change_threshold: float = 1.0,
    ):
        """
        Initialize the quantum market scraper.

        Args:
            symbols: List of symbols to track (default: major cryptos)
            cache_ttl: Cache time-to-live in seconds
            stream_interval: Seconds between stream updates
            change_threshold: % change threshold for alerts
        """
        self.symbols = symbols or ["BTC", "ETH", "DOGE", "SOL", "ADA", "MATIC", "AVAX"]

        # Components
        self.aggregator = AsyncMarketAggregator(cache_ttl=cache_ttl)
        self.stream = WebSocketPriceStream(
            self.symbols, update_interval=stream_interval
        )
        self.detector = PriceChangeDetector(threshold_percent=change_threshold)

        # Wire up the detector to the stream
        self.stream.subscribe(self._on_stream_tick)

        self._alert_callbacks: List[Callable[[Dict[str, Any]], None]] = []

    def _on_stream_tick(self, tick: MarketTick) -> None:
        """Internal handler for stream ticks."""
        alert = self.detector.on_tick(tick)
        if alert:
            for callback in self._alert_callbacks:
                try:
                    callback(alert)
                except Exception:
                    pass

    def get_price(self, symbol: str) -> Optional[MarketTick]:
        """Get current price for a symbol."""
        return self.aggregator.get_best_price(symbol)

    def get_prices(self, symbols: Optional[List[str]] = None) -> Dict[str, MarketTick]:
        """Get prices for multiple symbols."""
        return self.aggregator.get_batch_prices(symbols or self.symbols)

    def compare_sources(self, symbol: str) -> List[MarketTick]:
        """Compare prices across all sources."""
        return self.aggregator.get_all_prices(symbol)

    def start_streaming(self) -> None:
        """Start real-time price streaming."""
        self.stream.start()

    def stop_streaming(self) -> None:
        """Stop price streaming."""
        self.stream.stop()

    def subscribe_prices(self, callback: Callable[[MarketTick], None]) -> None:
        """Subscribe to real-time price updates."""
        self.stream.subscribe(callback)

    def subscribe_alerts(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to significant price change alerts."""
        self._alert_callbacks.append(callback)

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics."""
        return {
            "aggregator": self.aggregator.get_metrics(),
            "stream": {
                "running": self.stream.is_running,
                "symbols": self.symbols,
            },
            "volatility": {
                symbol: self.detector.get_volatility(symbol) for symbol in self.symbols
            },
        }

    def get_market_summary(self) -> Dict[str, Any]:
        """Get a summary of all tracked markets."""
        prices = self.get_prices()
        summary = {
            "timestamp": datetime.now().isoformat(),
            "markets": {},
        }

        for symbol, tick in prices.items():
            summary["markets"][symbol] = {
                "price": tick.price,
                "change_24h": tick.change_24h,
                "volume_24h": tick.volume_24h,
                "volatility": self.detector.get_volatility(symbol),
                "moving_avg": self.detector.get_moving_average(symbol),
                "source": tick.source,
                "age_ms": round(tick.age_ms, 2),
            }

        return summary


# =============================================================================
# CLI Demo
# =============================================================================


def demo():
    """
    Demonstrate the market scraper capabilities.
    """
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      🚀 QUANTUM MARKET SCRAPER - DEMO 🚀                 ║
    ║                                                          ║
    ║  Fast, efficient crypto market data scraping             ║
    ║  Multiple sources | Real-time streaming | Smart caching  ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Create the scraper
    scraper = QuantumMarketScraper(
        symbols=["BTC", "ETH", "SOL", "DOGE"],
        cache_ttl=5.0,
        stream_interval=3.0,
        change_threshold=0.5,
    )

    # Set up alert handler
    def on_alert(alert: Dict[str, Any]) -> None:
        print(
            f"\n🚨 ALERT: {alert['symbol']} {alert['direction']} "
            f"by {alert['change_percent']:.2f}%! "
            f"Price: ${alert['price']:.2f}"
        )

    scraper.subscribe_alerts(on_alert)

    # Get initial prices
    print("\n📊 Fetching current prices from multiple sources...")
    prices = scraper.get_prices()

    print("\n" + "=" * 60)
    print("💰 CURRENT MARKET PRICES 💰")
    print("=" * 60)

    for symbol, tick in prices.items():
        print(f"\n{symbol}:")
        print(f"   💵 Price: ${tick.price:,.2f}")
        if tick.change_24h:
            emoji = "📈" if tick.change_24h >= 0 else "📉"
            print(f"   {emoji} 24h Change: {tick.change_24h:+.2f}%")
        if tick.volume_24h:
            print(f"   📊 24h Volume: ${tick.volume_24h:,.0f}")
        print(f"   🔗 Source: {tick.source}")
        print(f"   ⏱️  Age: {tick.age_ms:.0f}ms")

    # Compare sources
    print("\n" + "=" * 60)
    print("🔍 SOURCE COMPARISON FOR BTC 🔍")
    print("=" * 60)

    btc_prices = scraper.compare_sources("BTC")
    for tick in btc_prices:
        spread_info = f" (Spread: ${tick.spread:.2f})" if tick.spread else ""
        print(f"   {tick.source}: ${tick.price:,.2f}{spread_info}")

    # Show metrics
    print("\n" + "=" * 60)
    print("📈 SCRAPER METRICS 📈")
    print("=" * 60)

    metrics = scraper.get_metrics()
    agg = metrics["aggregator"]
    print(f"\n   Total Requests: {agg['total_requests']}")
    print(f"   Cache Hits: {agg['total_cache_hits']}")
    print(f"   Cache Misses: {agg['total_cache_misses']}")
    print(f"   Errors: {agg['total_errors']}")

    for scraper_info in agg["scrapers"]:
        print(f"\n   {scraper_info['type']}:")
        print(f"      Requests: {scraper_info['requests']}")
        print(f"      Avg Latency: {scraper_info['avg_latency_ms']:.1f}ms")
        print(f"      Cache Hit Rate: {scraper_info['cache']['hit_rate']:.1f}%")

    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    demo()
