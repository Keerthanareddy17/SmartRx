import pywhatkit
import time

def send_whatsapp_message(receiver_number: str, message: str):
    """
    Sends a WhatsApp message using pywhatkit.
    Requires WhatsApp Web login.
    """
    try:
        print(f"Sending message to {receiver_number}...")
        pywhatkit.sendwhatmsg_instantly(receiver_number, message, wait_time=10, tab_close=True)
        time.sleep(5)  
        return True
    except Exception as e:
        print(f" Failed to send message: {e}")
        return False
