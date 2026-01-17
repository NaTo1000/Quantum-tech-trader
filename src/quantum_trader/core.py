#!/usr/bin/env python3
"""
Core Quantum Crypto Trader Logic
Refactored for production use with deterministic seeding and structured logging.
"""

import random
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json

# Simulated quantum states
QUANTUM_STATES = ["SUPERPOSITION", "ENTANGLED", "COLLAPSED", "DECOHERENT"]
CRYPTO_SYMBOLS = ["BTC", "ETH", "DOGE", "SHIB", "ADA", "SOL", "MATIC", "AVAX"]
TRADING_ACTIONS = ["HODL", "BUY_THE_DIP", "MOON_SHOT", "PANIC_SELL", "QUANTUM_LEAP"]

# Trading configuration constants
MIN_PRICE = 0.01  # Minimum price threshold to prevent negative/zero prices
MIN_TRADE_SIZE = 0.05  # Minimum 5% of cash per trade
MAX_TRADE_SIZE = 0.2  # Maximum 20% of cash per trade
MIN_SELL_PERCENT = 0.3  # Minimum 30% to sell on panic
MAX_SELL_PERCENT = 0.8  # Maximum 80% to sell on panic

logger = logging.getLogger(__name__)


class QuantumCryptoTrader:
    """
    A quantum-inspired crypto trading system that uses:
    - Superposition: Multiple strategies evaluated simultaneously
    - Entanglement: Correlated analysis across crypto pairs
    - Wave function collapse: Decision making through probabilistic collapse
    - Quantum tunneling: Breakthrough resistance/support levels unexpectedly
    
    ⚠️ MAXIMUM CHAOS MODE - TRADE AT YOUR OWN RISK! ⚠️
    """
    
    def __init__(self, chaos_level: float = 0.8, seed: Optional[int] = None, 
                 silent: bool = False):
        """
        Initialize the quantum trader with specified chaos level.
        
        Args:
            chaos_level: Float between 0-1. Higher = more chaotic trading! (default: 0.8)
            seed: Optional random seed for deterministic behavior
            silent: If True, suppresses console output (for API/service mode)
        """
        # Clamp chaos_level to valid range
        self.chaos_level = max(0.0, min(1.0, chaos_level))
        self.silent = silent
        
        # Set random seed for deterministic mode
        if seed is not None:
            random.seed(seed)
            logger.info(f"Deterministic mode enabled with seed: {seed}")
        
        self.quantum_state = "SUPERPOSITION"
        self.portfolio = {symbol: 0.0 for symbol in CRYPTO_SYMBOLS}
        self.cash = 10000.0  # Starting with $10k (virtual!)
        self.trade_history: List[Dict] = []
        self.price_cache: Dict[str, float] = {}  # Cache prices within a trading cycle
        
        logger.info(f"Quantum Crypto Trader initialized with chaos_level={self.chaos_level}")
        if not silent:
            print("⚡ QUANTUM CRYPTO TRADER INITIALIZED ⚡")
            print(f"💀 CHAOS LEVEL: {self.chaos_level * 100}% 💀")
            print("⚠️  REMEMBER: THIS IS EXPERIMENTAL - TRADE AT YOUR OWN RISK! ⚠️\n")
    
    def quantum_price_oracle(self, symbol: str) -> float:
        """
        Generate a quantum-inspired price using wave functions and uncertainty.
        In reality, this simulates crypto prices with high volatility.
        
        ⚠️ NOT REAL PRICES - SIMULATED CHAOS! ⚠️
        """
        base_prices = {
            "BTC": 45000, "ETH": 3000, "DOGE": 0.15, 
            "SHIB": 0.00001, "ADA": 0.50, "SOL": 100,
            "MATIC": 0.80, "AVAX": 35
        }
        
        base = base_prices.get(symbol, 1.0)
        # Quantum uncertainty creates wild price swings!
        quantum_noise = random.uniform(-self.chaos_level, self.chaos_level)
        quantum_spike = random.random()
        
        # Occasional quantum tunneling through price barriers!
        if quantum_spike > 0.95:
            quantum_noise *= 3  # MEGA PUMP OR DUMP!
            logger.info(f"Quantum wave detected for {symbol}")
            if not self.silent:
                print(f"🌊 QUANTUM WAVE DETECTED FOR {symbol}! 🌊")
        
        # Ensure price remains positive even with maximum chaos
        price = max(MIN_PRICE, base * (1 + quantum_noise))
        return price
    
    def superposition_strategy_analysis(self, symbol: str, price: float) -> List[Tuple[str, float]]:
        """
        Evaluate multiple trading strategies in quantum superposition.
        All strategies exist simultaneously until observation collapses them!
        """
        strategies = []
        
        # Strategy 1: Momentum (chaotic)
        momentum_score = random.uniform(0, 1) * self.chaos_level
        strategies.append(("MOMENTUM", momentum_score))
        
        # Strategy 2: Mean reversion (slightly less chaotic)
        mean_reversion_score = random.uniform(0, 1) * (1 - self.chaos_level * 0.5)
        strategies.append(("MEAN_REVERSION", mean_reversion_score))
        
        # Strategy 3: YOLO mode (maximum chaos!)
        yolo_score = random.uniform(0, 1) * self.chaos_level * 1.5
        strategies.append(("YOLO", yolo_score))
        
        # Strategy 4: Quantum intuition (pure randomness)
        quantum_score = random.random()
        strategies.append(("QUANTUM_INTUITION", quantum_score))
        
        return strategies
    
    def entangled_correlation_analysis(self, symbols: List[str]) -> Dict[str, float]:
        """
        Analyze quantum entanglement between crypto pairs.
        When one moves, entangled pairs move in mysterious ways!
        """
        if not symbols:
            return {}
        
        correlations = {}
        reference_symbol = symbols[0]
        
        for symbol in symbols:
            if symbol == reference_symbol:
                correlations[symbol] = 1.0
            else:
                # Entanglement strength depends on quantum chaos
                entanglement = random.uniform(-1, 1) * self.chaos_level
                correlations[symbol] = entanglement
        
        return correlations
    
    def collapse_wave_function(self, strategies: List[Tuple[str, float]]) -> str:
        """
        Collapse the quantum superposition to a single trading decision.
        This is where the magic (chaos) happens!
        """
        # Weighted random selection based on strategy scores
        total_score = sum(score for _, score in strategies)
        if total_score == 0:
            return random.choice(TRADING_ACTIONS)
        
        rand = random.uniform(0, total_score)
        cumulative = 0
        
        for strategy, score in strategies:
            cumulative += score
            if rand <= cumulative:
                # Map strategy to action with quantum randomness
                if score > 0.7:
                    return random.choice(["BUY_THE_DIP", "MOON_SHOT"])
                elif score < 0.3:
                    return random.choice(["PANIC_SELL", "HODL"])
                else:
                    return random.choice(TRADING_ACTIONS)
        
        return "QUANTUM_LEAP"
    
    def execute_quantum_trade(self, symbol: str, action: str, price: float):
        """
        Execute a trade based on quantum-collapsed decision.
        ⚠️ SIMULATED TRADES ONLY - NO REAL MONEY! ⚠️
        """
        trade_amount = self.cash * random.uniform(MIN_TRADE_SIZE, MAX_TRADE_SIZE)
        
        if action in ["BUY_THE_DIP", "MOON_SHOT", "QUANTUM_LEAP"]:
            if self.cash >= trade_amount:
                coins = trade_amount / price
                self.portfolio[symbol] += coins
                self.cash -= trade_amount
                
                trade = {
                    "timestamp": datetime.now().isoformat(),
                    "action": "BUY",
                    "symbol": symbol,
                    "price": price,
                    "amount": coins,
                    "cost": trade_amount,
                    "quantum_state": self.quantum_state
                }
                self.trade_history.append(trade)
                
                logger.info(f"BUY: {coins:.6f} {symbol} @ ${price:.2f} | Action: {action}")
                if not self.silent:
                    print(f"🚀 QUANTUM BUY: {coins:.6f} {symbol} @ ${price:.2f} | Action: {action}")
                
        elif action == "PANIC_SELL":
            if self.portfolio[symbol] > 0:
                coins = self.portfolio[symbol] * random.uniform(MIN_SELL_PERCENT, MAX_SELL_PERCENT)
                revenue = coins * price
                self.portfolio[symbol] -= coins
                self.cash += revenue
                
                trade = {
                    "timestamp": datetime.now().isoformat(),
                    "action": "SELL",
                    "symbol": symbol,
                    "price": price,
                    "amount": coins,
                    "revenue": revenue,
                    "quantum_state": self.quantum_state
                }
                self.trade_history.append(trade)
                
                logger.info(f"SELL: {coins:.6f} {symbol} @ ${price:.2f} | Action: {action}")
                if not self.silent:
                    print(f"📉 QUANTUM SELL: {coins:.6f} {symbol} @ ${price:.2f} | Action: {action}")
        
        # HODL does nothing, as true believers do
    
    def quantum_trading_cycle(self):
        """
        Execute one cycle of quantum crypto trading chaos!
        """
        if not self.silent:
            print("\n" + "="*60)
            print(f"🌀 QUANTUM TRADING CYCLE | State: {self.quantum_state} 🌀")
            print("="*60 + "\n")
        
        logger.info(f"Starting trading cycle with quantum state: {self.quantum_state}")
        
        # Clear price cache at start of new cycle for consistent pricing
        self.price_cache.clear()
        
        # Randomly shift quantum state
        self.quantum_state = random.choice(QUANTUM_STATES)
        
        # Analyze entanglement across all cryptos
        correlations = self.entangled_correlation_analysis(CRYPTO_SYMBOLS)
        
        # Trade on a random subset of cryptos (more chaos!)
        active_symbols = random.sample(CRYPTO_SYMBOLS, k=random.randint(2, 5))
        
        for symbol in active_symbols:
            # Cache price for consistency within this cycle
            price = self.quantum_price_oracle(symbol)
            self.price_cache[symbol] = price
            
            if not self.silent:
                print(f"\n💰 {symbol}: ${price:.8f}")
            
            # Evaluate strategies in superposition
            strategies = self.superposition_strategy_analysis(symbol, price)
            if not self.silent:
                print(f"   📊 Strategies in superposition: {len(strategies)}")
            
            # Collapse wave function to make decision
            action = self.collapse_wave_function(strategies)
            if not self.silent:
                print(f"   ⚡ Collapsed action: {action}")
            
            # Execute trade
            if action != "HODL":
                self.execute_quantum_trade(symbol, action, price)
        
        self.display_portfolio_status()
    
    def display_portfolio_status(self):
        """Display current portfolio and performance."""
        if not self.silent:
            print("\n" + "-"*60)
            print("📊 QUANTUM PORTFOLIO STATUS 📊")
            print("-"*60)
            print(f"💵 Cash: ${self.cash:.2f}")
        
        total_crypto_value = 0
        for symbol, amount in self.portfolio.items():
            if amount > 0:
                # Use cached price if available for consistent valuation within cycle
                if symbol not in self.price_cache:
                    self.price_cache[symbol] = self.quantum_price_oracle(symbol)
                current_price = self.price_cache[symbol]
                value = amount * current_price
                total_crypto_value += value
                if not self.silent:
                    print(f"   {symbol}: {amount:.6f} (≈${value:.2f})")
        
        total_value = self.cash + total_crypto_value
        profit_loss = total_value - 10000
        profit_pct = (profit_loss / 10000) * 100
        
        logger.info(f"Portfolio value: ${total_value:.2f}, P/L: ${profit_loss:.2f} ({profit_pct:+.2f}%)")
        
        if not self.silent:
            print(f"\n💎 Total Portfolio Value: ${total_value:.2f}")
            print(f"{'📈' if profit_loss >= 0 else '📉'} P/L: ${profit_loss:.2f} ({profit_pct:+.2f}%)")
            print(f"🎲 Total Trades: {len(self.trade_history)}")
            print("-"*60)
    
    def run_simulation(self, cycles: int = 5):
        """
        Run the quantum trader for specified number of cycles.
        MAXIMUM CHAOS MODE! 🌪️
        
        Args:
            cycles: Number of trading cycles to execute (default: 5, clamped 1-100)
        
        Returns:
            dict: Final portfolio state with cash, portfolio, and trades
        """
        # Clamp cycles to valid range
        cycles = max(1, min(100, cycles))
        
        if not self.silent:
            print("\n" + "🌟"*30)
            print("⚠️  QUANTUM CRYPTO CHAOS MODE ACTIVATED! ⚠️")
            print("🚨 REMEMBER: TRADE AT YOUR OWN RISK! 🚨")
            print("🌟"*30 + "\n")
        
        logger.info(f"Starting simulation with {cycles} cycles")
        
        for i in range(cycles):
            if not self.silent:
                print(f"\n{'🔥'*20} CYCLE {i+1}/{cycles} {'🔥'*20}\n")
            logger.info(f"Executing cycle {i+1}/{cycles}")
            self.quantum_trading_cycle()
        
        if not self.silent:
            print("\n" + "🏁"*30)
            print("QUANTUM TRADING SIMULATION COMPLETE!")
            print("🏁"*30 + "\n")
        
        logger.info("Simulation complete")
        
        return self.get_results()
    
    def get_results(self) -> dict:
        """Get current portfolio state and trade history."""
        return {
            "final_cash": self.cash,
            "final_portfolio": self.portfolio,
            "trades": self.trade_history,
            "chaos_level": self.chaos_level,
            "total_trades": len(self.trade_history)
        }
    
    def save_trade_history(self, data_dir: str = "./data"):
        """
        Save trade history to JSON file in specified directory.
        
        Args:
            data_dir: Directory to save trade history (default: ./data)
        """
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        # Add microseconds to prevent filename collisions
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = Path(data_dir) / f"quantum_trades_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.get_results(), f, indent=2)
        
        logger.info(f"Trade history saved to: {filename}")
        if not self.silent:
            print(f"💾 Trade history saved to: {filename}")
        
        return str(filename)
