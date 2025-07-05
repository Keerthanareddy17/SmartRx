import pywhatkit
import time

number = "+91............"
message = "This is a test message from SmartRx!"

pywhatkit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=False)
time.sleep(10)
