def moving_average_crossover_signal(prices, short_window, long_window,
                                    min_valid_price=1_000, max_valid_price=200_000):
    """
    Calculate a trading signal using a moving average crossover strategy.

    Parameters:
        prices (list of float): Historical closing prices for an asset (e.g., Bitcoin),
            ordered chronologically (oldest first). You must supply at least (long_window + 1)
            data points.
        short_window (int): Number of periods for the short-term moving average.
            Recommended bounds: 1 <= short_window <= 50.
        long_window (int): Number of periods for the long-term moving average.
            Recommended bounds: (short_window + 1) <= long_window <= 200.
        min_valid_price (float): Minimum expected price for BTC/USD (default: 1000).
        max_valid_price (float): Maximum expected price for BTC/USD (default: 200000).

    Returns:
        str: A trading signal: "BUY", "SELL", or "HOLD".
        
    Raises:
        ValueError: If input types or bounds are not met, or if insufficient price data is provided.

    How it works:
        - The function computes simple moving averages (SMA) for both the short and long windows.
        - It calculates the SMA for the most recent period ("today") and for the period immediately prior ("yesterday").
        - A "BUY" signal is returned if yesterday's short SMA was below (or equal to) the long SMA and today it rises above.
        - Conversely, a "SELL" signal is returned if yesterday's short SMA was above (or equal to) the long SMA and today it falls below.
        - If neither crossover condition is met, it returns "HOLD".
    """
    # Validate the input types and data sufficiency
    if not isinstance(prices, (list, tuple)):
        raise ValueError("Prices must be provided as a list or tuple of numbers.")
    if not all(isinstance(p, (int, float)) for p in prices):
        raise ValueError("All elements in prices must be numeric (int or float).")
    if len(prices) < long_window + 1:
        raise ValueError(f"Insufficient data: need at least {long_window + 1} price points.")

    if not (1 <= short_window <= 50):
        raise ValueError("short_window must be between 1 and 50.")
    if not (short_window < long_window <= 200):
        raise ValueError("long_window must be greater than short_window and no more than 200.")

    # Validate that the latest price is within logical bounds for BTC/USD
    latest_price = prices[-1]
    if latest_price < min_valid_price or latest_price > max_valid_price:
        # Price out of expected range; returning "HOLD" to avoid trading on anomalous data.
        return "HOLD"

    # Calculate moving averages using the most recent data points
    short_ma_current = sum(prices[-short_window:]) / short_window
    short_ma_prev = sum(prices[-short_window-1:-1]) / short_window

    long_ma_current = sum(prices[-long_window:]) / long_window
    long_ma_prev = sum(prices[-long_window-1:-1]) / long_window

    # Determine the trading signal based on the moving average crossover
    if short_ma_prev <= long_ma_prev and short_ma_current > long_ma_current:
        return "BUY"
    elif short_ma_prev >= long_ma_prev and short_ma_current < long_ma_current:
        return "SELL"
    else:
        return "HOLD"
