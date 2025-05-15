import subprocess
import sys

required_packages = [
    "rich",
    "paramiko",
    "mysql-connector-python"
]

for package in required_packages:
    try:
        __import__(package.split('-')[0])
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


import socket
from ftplib import FTP
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
import os
import mysql.connector
from mysql.connector import Error
import paramiko  

console = Console()
#this tool was made by snow(xj3j)
red_text = "\033[91m" + r"""

 /$$$$$$$                       /$$           /$$$$$$$  /$$                             /$$                            
| $$__  $$                     | $$          | $$__  $$| $$                            | $$                            
| $$  \ $$ /$$$$$$   /$$$$$$  /$$$$$$        | $$  \ $$| $$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$    /$$$$$$  /$$$$$$/$$$$ 
| $$$$$$$//$$__  $$ /$$__  $$|_  $$_/        | $$$$$$$/| $$__  $$ |____  $$| $$__  $$|_  $$_/   /$$__  $$| $$_  $$_  $$
| $$____/| $$  \ $$| $$  \__/  | $$          | $$____/ | $$  \ $$  /$$$$$$$| $$  \ $$  | $$    | $$  \ $$| $$ \ $$ \ $$
| $$     | $$  | $$| $$        | $$ /$$      | $$      | $$  | $$ /$$__  $$| $$  | $$  | $$ /$$| $$  | $$| $$ | $$ | $$
| $$     |  $$$$$$/| $$        |  $$$$/      | $$      | $$  | $$|  $$$$$$$| $$  | $$  |  $$$$/|  $$$$$$/| $$ | $$ | $$
|__/      \______/ |__/         \___/        |__/      |__/  |__/ \_______/|__/  |__/   \___/   \______/ |__/ |__/ |__/
                                        Made by Snow(xj3j)                                                                                                                                                                                                                                              
""" + "\033[0m"

COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    3306: 'MySQL',
    3389: 'RDP'
}

def try_ssh_login(ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect(ip, port=22, username='root', password='', timeout=3)  
        console.print(f"[yellow][!] SSH login SUCCESSFUL on {ip}[/yellow]")
        ssh.close()
    except Exception:
        console.print(f"[red][-] SSH login FAILED on {ip}[/red]")

def try_ftp_login(ip):
    try:
        ftp = FTP()
        ftp.connect(ip, 21, timeout=3)
        ftp.login('anonymous', 'anonymous')
        console.print(f"[yellow][!] Anonymous FTP login SUCCESSFUL on {ip}[/yellow]")
        ftp.quit()
    except Exception:
        console.print(f"[red][-] Anonymous FTP login FAILED on {ip}[/red]")

def try_telnet(ip):
    try:
        sock = socket.socket()
        sock.settimeout(3)
        sock.connect((ip, 23))
        banner = sock.recv(1024).decode(errors="ignore")
        console.print(f"[yellow][!] Telnet banner: {banner.strip()}[/yellow]")
        sock.close()
    except Exception:
        console.print(f"[red][-] Telnet connection FAILED on {ip}[/red]")

def try_mysql_login(ip):
    try:
        conn = mysql.connector.connect(
            host=ip,
            port=3306,
            user='root',
            password='',
            connection_timeout=3
        )
        if conn.is_connected():
            console.print(f"[yellow][!] MySQL login SUCCESSFUL with root@'' on {ip}[/yellow]")
            conn.close()
    except Error:
        console.print(f"[red][-] MySQL login FAILED with root@'' on {ip}[/red]")

def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        service = COMMON_PORTS.get(port, 'Unknown')
        console.print(f"[green][+] Port {port} OPEN ({service})[/green]")
        sock.close()

        
        if port == 21:
            try_ftp_login(ip)
        elif port == 22:
            try_ssh_login(ip)  
        elif port == 23:
            try_telnet(ip)
        elif port == 3306:
            try_mysql_login(ip)

    except:
        pass

def main():
    print(red_text)
    target = input("Enter target IP address: ")
    console.print(f"[cyan][*] Scanning {target}...[/cyan]")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in COMMON_PORTS:
            executor.submit(scan_port, target, port)

    console.print(f"[cyan][*] Scan completed. Restarting...[/cyan]")

if __name__ == "__main__":
    while True:
        main()
