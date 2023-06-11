import argparse
import requests
import json

ZABBIX_API_URL = "http://3.21.37.213/zabbix/api_jsonrpc.php"
UNAME = "Admin"
PWORD = "zabbix"

def import_yaml_file(file_path):
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

    with open(file_path, 'r') as file:
        yml_data = file.read()

    # Perform import request for the YAML file
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

    # Print the import response for the YAML file
    print(f"Import response for '{file_path}':")
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import a YAML file to Zabbix")
    parser.add_argument("file_path", help="Path to the YAML file to be imported")
    args = parser.parse_args()
    import_yaml_file(args.file_path)

