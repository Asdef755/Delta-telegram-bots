MAX_TRADES = 2
TRADE_SIZE = 0.10  # 10% of portfolio per trade


def can_open_trade(open_trades):
    """Check if a new trade can be opened."""
    return len(open_trades) < MAX_TRADES
