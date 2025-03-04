# Remote-keylogger

## Objective  
The **Remote-keylogger** project was developed to create an advanced remote keylogger for learning purposes only and is not intended for malicious use.

## Skills Learned  
- **Python Programming** – General scripting and automation.
- **Cybersecurity & Ethical Hacking** – Understanding keylogging techniques, encryption, and data exfiltration.
- **Networking & System Information Gathering** – Collecting system details (IP, hostname, OS, etc.).
- **File Handling** – Reading, writing, and encrypting files.
- **Clipboard Interception** – Accessing and extracting clipboard data.
- **Email Automation** – Sending logs via SMTP.

## Tools Used  
- **Python** – Core language.
- **smtplib & email.mime** – Sending logs via email.
- **socket & platform** – Gathering system and network details.
- **win32clipboard** – Accessing clipboard data.
- **pynput.keyboard** – Logging keystrokes.
- **cryptography.fernet** – Encrypting logs before exfiltration.
- **requests** – Fetching public IP address.
- **multiprocessing** – Running processes in parallel.
- **PIL (Pillow)** – Capturing screenshots.
- **os & time** – File operations and timing execution.

## Notes

For this keylogger to work in a real environment, it should be converted into an executable. The thing is that any antivirus would detect it as a virus, so you should see a way around.
