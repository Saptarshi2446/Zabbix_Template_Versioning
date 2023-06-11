import requests
import json
import glob

ZABBIX_API_URL = "http://3.21.37.213/zabbix/api_jsonrpc.php"
UNAME = "Admin"
PWORD = "zabbix"

# Login to Zabbix API and obtain authentication token
r = requests.post(ZABBIX_API_URL, json={
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": UNAME,
        "password": PWORD
    },
    "id": 1
})
AUTHTOKEN = r.json()["result"]

# Find all YAML files in the directory
yaml_files = glob.glob("*.yaml")

# Iterate over each YAML file and perform import operation
for yaml_file in yaml_files:
    with open(yaml_file, 'r') as file:
        yml_data = file.read()

    # Perform import request for the current YAML file
    r = requests.post(ZABBIX_API_URL, json={
        "jsonrpc": "2.0",
        "method": "configuration.import",
        "params": {
            "format": "yaml",
            "rules": {
                "templates": {
                    "createMissing": True,
                    "updateExisting": True
                },
                "items": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True
                },
                "triggers": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": True 
                },
                "valueMaps": {
                    "createMissing": True,
                    "updateExisting": False
                }
            },
            "source": yml_data
        },
        "id": 2,
        "auth": AUTHTOKEN
    })

    # Print the import response for the current YAML file
    print(f"Import response for '{yaml_file}':")
    print(json.dumps(r.json(), indent=4, sort_keys=True))
    print()

# Logout user
r = requests.post(ZABBIX_API_URL, json={
    "jsonrpc": "2.0",
    "method": "user.logout",
    "params": {},
    "id": 3,
    "auth": AUTHTOKEN
})
print("Logout response:")
print(json.dumps(r.json(), indent=4, sort_keys=True))
