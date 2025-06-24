import ssl
import socket
from datetime import datetime

def check_ssl(domain, port=443):
    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED  # Default and safe



    try:
        with socket.create_connection((domain, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

                # Expiry
                expires = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (expires - datetime.utcnow()).days

                # Issuer
                issuer = dict(x[0] for x in cert['issuer'])
                subject = dict(x[0] for x in cert['subject'])

                print(f"\n🔒 {domain}")
                print(f"  > Issued by: {issuer.get('organizationName', 'Unknown')}")
                print(f"  > Common name: {subject.get('commonName', 'N/A')}")
                print(f"  > Expires in: {days_left} days")
                print(f"  > TLS version: {ssock.version()}")


                if days_left < 0:
                    print("  ❌ Certificate EXPIRED!")
                if issuer.get('commonName', '') == subject.get('commonName', ''):
                    print("  ⚠️ Self-signed certificate detected!")
    except ssl.SSLError as e:
        print(f"\n❌ SSL error on {domain}: {e}")
    except Exception as e:
        print(f"\n❌ Error connecting to {domain}: {e}")

