import requests

def send_telegram_signal(token, chat_id, pair, signal, accuracy, timeframe, reasons):
    """
    Sends structured live binary options signals to a Telegram channel or chat.
    """
    if not token or not chat_id:
        return False, "Telegram token or Chat ID missing."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    emoji = "🟢" if "CALL" in signal else "🔴"
    
    message = (
        f"🚨 **QUOTEX AI PRO - VIP SIGNAL** 🚨\n\n"
        f"📊 **Asset:** `{pair}`\n"
        f"⏳ **Timeframe:** `{timeframe}`\n"
        f"🎯 **Direction:** `{signal}` {emoji}\n"
        f"📈 **Accuracy:** `{accuracy}`\n\n"
        f"🔍 **Confluence Reasons:**\n"
    )
    
    for r in reasons[:3]:
        message += f"• {r}\n"
        
    message += f"\n⚠️ *Trade responsibly using proper Martingale & Risk Management!*"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            return True, "Signal sent successfully!"
        else:
            return False, f"Failed: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"