#!/usr/bin/env python3
"""
CLI Entry Point for Quantum Crypto Trader
Non-interactive command-line interface with configurable parameters.
"""

import argparse
import logging
import sys
from pathlib import Path

from .core import QuantumCryptoTrader


def setup_logging(log_file: str = None, json_format: bool = False):
    """
    Configure structured logging.
    
    Args:
        log_file: Optional file path for log output
        json_format: If True, use JSON format (currently outputs standard format)
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quantum Crypto Trader - Quantum-inspired trading simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python -m quantum_trader.cli
  
  # Run with custom chaos level and cycles
  python -m quantum_trader.cli --chaos-level 0.5 --cycles 10
  
  # Run in deterministic mode with seed
  python -m quantum_trader.cli --seed 42 --cycles 5
  
  # Save logs to file
  python -m quantum_trader.cli --log-file ./data/app.log
        """
    )
    
    parser.add_argument(
        '--chaos-level',
        type=float,
        default=0.8,
        help='Chaos level (0.0-1.0, default: 0.8). Higher = more volatility'
    )
    
    parser.add_argument(
        '--cycles',
        type=int,
        default=5,
        help='Number of trading cycles (1-100, default: 5)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for deterministic behavior (optional)'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='./data',
        help='Directory for trade history files (default: ./data)'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='Optional log file path (logs to stdout by default)'
    )
    
    parser.add_argument(
        '--silent',
        action='store_true',
        help='Suppress console output (logs only)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_file=args.log_file)
    
    logger = logging.getLogger(__name__)
    
    # Display banner if not silent
    if not args.silent:
        print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      🌀 QUANTUM CRYPTO TRADER - CHAOS EDITION 🌀        ║
    ║                                                          ║
    ║  ⚠️  WARNING: EXPERIMENTAL SYSTEM - MAXIMUM CHAOS! ⚠️   ║
    ║  🚨 NOT FINANCIAL ADVICE - USE AT YOUR OWN RISK! 🚨     ║
    ║  💀 EXTREME VOLATILITY - PREPARE FOR WILD RIDES! 💀     ║
    ║                                                          ║
    ║  This is a simulated quantum-inspired trading system    ║
    ║  for educational and entertainment purposes only!       ║
    ╚══════════════════════════════════════════════════════════╝
        """)
    
    logger.info(f"Starting Quantum Trader CLI - chaos_level={args.chaos_level}, cycles={args.cycles}, seed={args.seed}")
    
    try:
        # Create trader with validated parameters
        trader = QuantumCryptoTrader(
            chaos_level=args.chaos_level,
            seed=args.seed,
            silent=args.silent
        )
        
        # Run simulation
        results = trader.run_simulation(cycles=args.cycles)
        
        # Save trade history
        filename = trader.save_trade_history(data_dir=args.data_dir)
        
        if not args.silent:
            print("\n✨ Simulation complete! ✨")
            print(f"📊 Final Portfolio Value: ${results['final_cash'] + sum(results['final_portfolio'].values()):.2f}")
            print(f"🎲 Total Trades: {results['total_trades']}")
            print("⚠️  Remember: This was all simulated - always do your own research! ⚠️\n")
        
        logger.info(f"Simulation successful - {results['total_trades']} trades executed")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("Simulation interrupted by user")
        if not args.silent:
            print("\n\n⚠️  Quantum trading interrupted by user!")
        return 130
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        if not args.silent:
            print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
