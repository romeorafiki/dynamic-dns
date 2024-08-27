import requests
import json

# Path to JSON file that contains all values
json_values = json.load(open('C:\\Users\\jasonp\\Documents\\API Keys\\cloudflare-keys.json'))

# Authentication variables and URL
EMAIL = json_values["email"]
API_KEY = json_values["api_key"]
ZONE_ID = json_values["zone_id"]
DNS_RECORD = json_values["dns_record"]
URL = ('https://api.cloudflare.com/client/v4/zones/{}/dns_records').format(ZONE_ID)
# Get Current IP address
CURRENT_IP = requests.get('https://api.ipify.org').text                             

# Set the Authentication headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": EMAIL,
    "X-Auth-Key": API_KEY
}

# Fucntion for getting the DNS ID of DNS Record
def get_dns_id(url, headers, record):
    results = requests.get(url, headers=headers).json()["result"]
    for result in results:
        if (result['name'] == record):
            return result['id']

# Set the DNS ID
DNS_RECORD_ID = get_dns_id(URL, headers, DNS_RECORD)

# Set the new URL for updating the DNS Record
UPDATE_URL = ('https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}').format(ZONE_ID, DNS_RECORD_ID)

# Data required for changing the IP address in the record
data = {
  "content": CURRENT_IP,
  "name": DNS_RECORD,
  "proxied": False,
  "type": "A",
  "comment": "Dynamic AWS DNS Record",
  "id": DNS_RECORD_ID,
  "tags": [],
  "ttl": "Auto"
}

# Publish the record
response = requests.patch(UPDATE_URL, headers=headers, json=data)

#test