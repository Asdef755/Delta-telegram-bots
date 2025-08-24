def check_signal(open_, high, low, close, pivots):
    """
    Detect single-candle reversal.
    Returns 'LONG', 'SHORT', or None.
    """

    # Long setup: candle sweeps down through pivots and closes back above
    if low <= min(pivots) and close > pivots[1]:
        return "LONG"

    # Short setup: candle sweeps up through pivots and closes back below
    if high >= max(pivots) and close < pivots[1]:
        return "SHORT"

    return None
