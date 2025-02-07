# Project: Domain Auto-Switch System
# Main script to detect blocked domains and trigger auto-switching

import os
import requests
import time
from namecheap import Api
from cloudflare import Cloudflare
from nginx import load, dumps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
CHECK_DOMAIN = "your-old-domain.com"
DOMAIN_PREFIX = "yourapp"
TLD = "com"
LOG_FILE = "domain_switch.log"
NAMECHEAP_API_USER = "your_api_user"
NAMECHEAP_API_KEY = "your_api_key"
NAMECHEAP_USERNAME = "your_nc_username"
CLIENT_IP = "your_ip_address"
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
NGINX_CONF_PATH = "/etc/nginx/sites-enabled/default"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your-email@example.com"
SMTP_PASSWORD = "your-password"
EMAIL_RECIPIENT = "recipient@example.com"

# Initialize Cloudflare client
cf_client = Cloudflare()

# Function to check if domain is blocked
def is_domain_blocked(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code in [403, 404, 503]:
            return True
    except requests.exceptions.RequestException:
        return True
    return False

# Function to check domain availability
def check_domain_availability(domain):
    api = Api(NAMECHEAP_USERNAME, NAMECHEAP_API_KEY, NAMECHEAP_USERNAME, CLIENT_IP, sandbox=True)
    return api.domains_check(domain)

# Function to register a new domain using Namecheap API
def register_new_domain(domain_name):
    api = Api(NAMECHEAP_USERNAME, NAMECHEAP_API_KEY, NAMECHEAP_USERNAME, CLIENT_IP, sandbox=True)
    try:
        response = api.domains_create(
            DomainName=domain_name,
            FirstName='John',
            LastName='Doe',
            Address1='123 Example Street',
            City='Example City',
            StateProvince='Example State',
            PostalCode='12345',
            Country='US',
            Phone='+1.123456789',
            EmailAddress='admin@example.com'
        )
        print(f"[+] Successfully registered domain: {domain_name}")
        return response
    except Exception as e:
        print(f"[!] Failed to register domain {domain_name}: {e}")
        return None

# Function to update Cloudflare DNS
def update_cloudflare_dns(new_domain, new_ip):
    if CLOUDFLARE_ZONE_ID is None:
        print("[!] CLOUDFLARE_ZONE_ID is not defined")
        return False
    record = cf_client.dns.records.create(
        zone_id=CLOUDFLARE_ZONE_ID,
        type="A",
        name=new_domain,
        content=new_ip,
        proxied=True,
    )
    if record is not None:
        print(f"[+] Cloudflare DNS updated for {new_domain} -> {new_ip}")
        return True
    return False

# Function to send email alert
def send_email_alert(new_domain, old_domain):
    subject = f"Domain Switched: {new_domain}"
    body = f"The domain {old_domain} has been switched to {new_domain}.\nCloudflare and NGINX have been updated."
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()
        print(f"[+] Email alert sent to {EMAIL_RECIPIENT}")
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")

# Main execution loop
def main():
    if is_domain_blocked(CHECK_DOMAIN):
        print(f"[!] Domain {CHECK_DOMAIN} is blocked. Initiating switch...")
        new_domain = f"{DOMAIN_PREFIX}{int(time.time())}.{TLD}"
        new_ip = "your_new_ip_address"
        if register_new_domain(new_domain):
            if update_cloudflare_dns(new_domain, new_ip):
                os.system('systemctl reload nginx')
                send_email_alert(new_domain, CHECK_DOMAIN)
                with open(LOG_FILE, "a") as log:
                    log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Switched from {CHECK_DOMAIN} to {new_domain}\n")
                print(f"[+] Successfully switched to {new_domain}")
            else:
                print("[!] Failed to update Cloudflare DNS. Aborting switch.")
        else:
            print("[!] Failed to register new domain. Aborting switch.")
    else:
        print(f"[+] {CHECK_DOMAIN} is working fine. No action needed.")

if __name__ == "__main__":
    main()
