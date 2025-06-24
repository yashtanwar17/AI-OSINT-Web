import socket

# for info
DANGEROUS_PORTS = {
    21: "FTP - anonymous login",
    22: "SSH - brute force",
    23: "Telnet - plaintext login (Mirai)",
    25: "SMTP - open relay",
    53: "DNS - amplification",
    80: "HTTP - web exploits",
    110: "POP3 - old mail creds",
    139: "NetBIOS - LAN attack",
    143: "IMAP - info disclosure",
    161: "SNMP - default creds",
    389: "LDAP - info leak",
    443: "HTTPS - SSL issues",
    445: "SMB - EternalBlue, SMBGhost",
    512: "rexec - trust abuse",
    513: "rlogin - trust abuse",
    514: "rsh - trust abuse",
    3306: "MySQL - weak pass",
    3389: "RDP - BlueKeep",
    5900: "VNC - open remote desktop",
    6379: "Redis - RCE via config",
    7001: "WebLogic - deserialization RCE",
    8080: "HTTP-alt - admin panels",
    9200: "Elasticsearch - no auth",
    27017: "MongoDB - no auth",
    5000: "Flask debug - RCE",
    11211: "Memcached - DDoS amp",
    4444: "Metasploit - reverse shell"
}

def scan_port(host, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except:
        return False

def scan_host(host):
    print(f"\n🔍 Scanning {host} for exploited or dangerous ports...\n")
    for port, reason in DANGEROUS_PORTS.items():
        if scan_port(host, port):
            print(f"[OPEN]  Port {port} - {reason}")

