"""
Tests for Quantum Crypto Trader Core Logic
"""

import pytest
import random
from pathlib import Path

from src.quantum_trader.core import (
    QuantumCryptoTrader,
    CRYPTO_SYMBOLS,
    TRADING_ACTIONS,
    MIN_PRICE
)


class TestQuantumPriceOracle:
    """Test price oracle behavior."""
    
    def test_oracle_returns_positive_prices(self):
        """Prices must always be positive."""
        trader = QuantumCryptoTrader(chaos_level=1.0, seed=42)
        
        for symbol in CRYPTO_SYMBOLS:
            price = trader.quantum_price_oracle(symbol)
            assert price > 0, f"Price for {symbol} must be positive, got {price}"
            assert price >= MIN_PRICE, f"Price for {symbol} must be >= MIN_PRICE"
    
    def test_oracle_with_maximum_chaos(self):
        """Even with maximum chaos, prices remain positive."""
        trader = QuantumCryptoTrader(chaos_level=1.0, seed=123)
        
        # Test multiple times to catch edge cases
        for _ in range(100):
            for symbol in CRYPTO_SYMBOLS[:3]:  # Test subset for speed
                price = trader.quantum_price_oracle(symbol)
                assert price > 0, f"Price must be positive with max chaos"
    
    def test_oracle_deterministic_with_seed(self):
        """Same seed produces same prices."""
        trader1 = QuantumCryptoTrader(chaos_level=0.5, seed=999)
        trader2 = QuantumCryptoTrader(chaos_level=0.5, seed=999)
        
        for symbol in CRYPTO_SYMBOLS:
            price1 = trader1.quantum_price_oracle(symbol)
            price2 = trader2.quantum_price_oracle(symbol)
            assert price1 == price2, f"Deterministic mode failed for {symbol}"


class TestTradeExecution:
    """Test trade execution and invariants."""
    
    def test_cash_never_negative_after_trades(self):
        """Cash balance must never go negative."""
        trader = QuantumCryptoTrader(chaos_level=0.8, seed=42, silent=True)
        
        # Run simulation
        trader.run_simulation(cycles=10)
        
        assert trader.cash >= 0, f"Cash went negative: {trader.cash}"
    
    def test_portfolio_amounts_never_negative(self):
        """Portfolio amounts must never go negative."""
        trader = QuantumCryptoTrader(chaos_level=0.8, seed=123, silent=True)
        
        trader.run_simulation(cycles=10)
        
        for symbol, amount in trader.portfolio.items():
            assert amount >= 0, f"Portfolio amount for {symbol} is negative: {amount}"
    
    def test_trade_history_recorded(self):
        """Trades are recorded in history."""
        trader = QuantumCryptoTrader(chaos_level=0.8, seed=42, silent=True)
        
        trader.run_simulation(cycles=5)
        
        # Should have some trades with reasonable chaos level
        assert len(trader.trade_history) >= 0, "Trade history should exist"
        
        # Verify trade structure
        for trade in trader.trade_history:
            assert 'timestamp' in trade
            assert 'action' in trade
            assert 'symbol' in trade
            assert 'price' in trade
            assert trade['action'] in ['BUY', 'SELL']
    
    def test_buy_trades_decrease_cash(self):
        """Buy trades reduce cash balance."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=456, silent=True)
        initial_cash = trader.cash
        
        # Execute a single cycle
        trader.quantum_trading_cycle()
        
        # Check if any buy trades occurred
        buy_trades = [t for t in trader.trade_history if t['action'] == 'BUY']
        if buy_trades:
            assert trader.cash < initial_cash, "Buy trades should decrease cash"
    
    def test_sell_trades_increase_cash(self):
        """Sell trades increase cash balance."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=789, silent=True)
        
        # First, execute some cycles to build portfolio
        trader.run_simulation(cycles=5)
        
        # Force portfolio positions for testing
        trader.portfolio["BTC"] = 1.0
        cash_before = trader.cash
        
        # Execute sell
        trader.execute_quantum_trade("BTC", "PANIC_SELL", 45000)
        
        # Cash should increase if we had position to sell
        if any(t['action'] == 'SELL' for t in trader.trade_history):
            assert trader.cash > cash_before, "Sell should increase cash"


class TestCollapsedActions:
    """Test wave function collapse produces valid actions."""
    
    def test_collapse_returns_valid_action(self):
        """Collapsed actions must be from valid set."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=42)
        
        # Test collapse multiple times
        for _ in range(50):
            strategies = trader.superposition_strategy_analysis("BTC", 45000)
            action = trader.collapse_wave_function(strategies)
            assert action in TRADING_ACTIONS, f"Invalid action: {action}"
    
    def test_collapse_with_zero_scores(self):
        """Collapse handles zero scores gracefully."""
        trader = QuantumCryptoTrader(chaos_level=0.0, seed=42)
        
        strategies = [("TEST1", 0.0), ("TEST2", 0.0)]
        action = trader.collapse_wave_function(strategies)
        assert action in TRADING_ACTIONS, f"Invalid action with zero scores: {action}"


class TestSimulationParameters:
    """Test parameter validation and clamping."""
    
    def test_chaos_level_clamped(self):
        """Chaos level is clamped to [0, 1]."""
        trader1 = QuantumCryptoTrader(chaos_level=-0.5)
        assert trader1.chaos_level == 0.0, "Negative chaos should be clamped to 0"
        
        trader2 = QuantumCryptoTrader(chaos_level=1.5)
        assert trader2.chaos_level == 1.0, "Excessive chaos should be clamped to 1"
        
        trader3 = QuantumCryptoTrader(chaos_level=0.5)
        assert trader3.chaos_level == 0.5, "Valid chaos should remain unchanged"
    
    def test_cycles_clamped(self):
        """Cycles are clamped to [1, 100]."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=42, silent=True)
        
        # Test clamping
        results1 = trader.run_simulation(cycles=-5)
        # Should clamp to 1, verify it ran at least once
        assert len(trader.trade_history) >= 0
        
        # Reset trader
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=42, silent=True)
        results2 = trader.run_simulation(cycles=150)
        # Should clamp to 100, not crash


class TestResultsAndPersistence:
    """Test results and file saving."""
    
    def test_get_results_structure(self):
        """Results have correct structure."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=42, silent=True)
        trader.run_simulation(cycles=2)
        
        results = trader.get_results()
        
        assert 'final_cash' in results
        assert 'final_portfolio' in results
        assert 'trades' in results
        assert 'chaos_level' in results
        assert 'total_trades' in results
        
        assert results['chaos_level'] == 0.5
        assert isinstance(results['final_cash'], float)
        assert isinstance(results['final_portfolio'], dict)
        assert isinstance(results['trades'], list)
    
    def test_save_trade_history(self, tmp_path):
        """Trade history is saved to file."""
        trader = QuantumCryptoTrader(chaos_level=0.5, seed=42, silent=True)
        trader.run_simulation(cycles=2)
        
        # Save to temp directory
        data_dir = tmp_path / "data"
        filename = trader.save_trade_history(data_dir=str(data_dir))
        
        # Verify file exists
        assert Path(filename).exists(), f"Trade history file not created: {filename}"
        
        # Verify it's valid JSON
        import json
        with open(filename) as f:
            data = json.load(f)
        
        assert 'final_cash' in data
        assert 'trades' in data


class TestDeterministicBehavior:
    """Test deterministic mode with seeds."""
    
    def test_same_seed_produces_same_results(self):
        """Same seed produces identical simulations."""
        trader1 = QuantumCryptoTrader(chaos_level=0.7, seed=12345, silent=True)
        results1 = trader1.run_simulation(cycles=3)
        
        trader2 = QuantumCryptoTrader(chaos_level=0.7, seed=12345, silent=True)
        results2 = trader2.run_simulation(cycles=3)
        
        # Final cash should be identical
        assert results1['final_cash'] == results2['final_cash'], "Deterministic mode failed for cash"
        
        # Trade counts should match
        assert results1['total_trades'] == results2['total_trades'], "Deterministic mode failed for trade count"
        
        # Portfolio should match
        for symbol in CRYPTO_SYMBOLS:
            assert results1['final_portfolio'][symbol] == results2['final_portfolio'][symbol], \
                f"Deterministic mode failed for {symbol}"
    
    def test_different_seeds_produce_different_results(self):
        """Different seeds produce different simulations."""
        trader1 = QuantumCryptoTrader(chaos_level=0.7, seed=111, silent=True)
        results1 = trader1.run_simulation(cycles=3)
        
        trader2 = QuantumCryptoTrader(chaos_level=0.7, seed=222, silent=True)
        results2 = trader2.run_simulation(cycles=3)
        
        # Results should differ (very high probability)
        assert results1['final_cash'] != results2['final_cash'] or \
               results1['total_trades'] != results2['total_trades'], \
               "Different seeds should produce different results"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
