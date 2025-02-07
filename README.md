# Domain Auto-Switch System

## Overview
The **Domain Auto-Switch System** is an automated solution to detect blocked domains, register a new domain using Namecheap API, update DNS records via Cloudflare API, modify NGINX configurations dynamically, and send email alerts via SMTP.

## Features
- **Automatic Domain Status Check**: Detects blocked domains (403, 404, 503 errors).
- **Namecheap API Integration**: Registers a new domain automatically.
- **Cloudflare API Integration**: Updates DNS records to point to the new domain.
- **NGINX Configuration Update**: Dynamically modifies the server block and reloads NGINX.
- **SMTP Email Alerts**: Notifies the admin whenever a domain switch occurs.

## Installation
### Prerequisites
- Python 3.8+
- NGINX installed on your server
- Namecheap API credentials
- Cloudflare API credentials
- SMTP server credentials for email alerts

### Install Required Packages
Run the following command to install required dependencies:
```bash
pip install python-nginx cloudflare PyNamecheap
```

## Configuration
### Environment Variables
Set up the required credentials as environment variables:
```bash
export NAMECHEAP_API_USER="your_api_user"
export NAMECHEAP_API_KEY="your_api_key"
export NAMECHEAP_USERNAME="your_nc_username"
export CLIENT_IP="your_ip_address"
export CLOUDFLARE_ZONE_ID="your_cloudflare_zone_id"
export SMTP_SERVER="smtp.example.com"
export SMTP_USER="your-email@example.com"
export SMTP_PASSWORD="your-password"
export EMAIL_RECIPIENT="recipient@example.com"
```

## Usage
Run the script manually:
```bash
python main.py
```

Or set up a cron job to run every 10 minutes:
```bash
*/10 * * * * /usr/bin/python3 /path/to/domain_switch_manager.py
```

## How It Works
1. **Check Domain Status**: The script checks if the current domain is blocked.
2. **Register a New Domain**: If blocked, a new domain is registered via Namecheap.
3. **Update Cloudflare DNS**: The script updates the Cloudflare DNS records to reflect the new domain.
4. **Modify NGINX Configuration**: The NGINX configuration is updated and reloaded.
5. **Send Email Alert**: The admin is notified via email about the domain switch.

## Troubleshooting
- If the Namecheap API is not working, ensure that the API key is correctly set and your IP is whitelisted.
- If NGINX does not reload, check the `nginx.conf` syntax using:
  ```bash
  nginx -t
  ```
- If emails are not received, verify the SMTP credentials and logs.

## License
This project is licensed under the  [MIT License](./LICENSE.md).

## Author
Hassan Ali

