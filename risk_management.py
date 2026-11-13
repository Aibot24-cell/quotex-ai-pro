def check_risk_limits(daily_losses, max_allowed_loss=3, consecutive_losses=2):
    """
    Evaluates risk parameters and warns the user if trading safety limits are reached.
    """
    warnings = []
    can_trade = True

    if daily_losses >= max_allowed_loss:
        can_trade = False
        warnings.append("🛑 **Daily Loss Limit Reached!** Stop trading for today to protect capital.")
    
    if consecutive_losses >= 2:
        warnings.append("⚠️ **Consecutive Loss Warning:** Market volatility might be unpredictable. Consider taking a break.")

    return {
        "can_trade": can_trade,
        "warnings": warnings
    }