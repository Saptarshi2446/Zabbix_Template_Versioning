
import requests
import json
import pandas as pd
ZABBIX_API_URL = "http://3.21.37.213/zabbix/api_jsonrpc.php"
UNAME = "Admin"
PWORD = "zabbix"
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": UNAME,
                          "password": PWORD},
                      "id": 1
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))

AUTHTOKEN = r.json()["result"]

with open('zbx_export_templates_calculated.yaml', 'r') as file:
    yml_data = file.read()
# Retrieve a list of problems
print("\nRetrieve a list of problems")
r = requests.post(ZABBIX_API_URL,
        json= {
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
            }
                     )

json_object = json.dumps(r.json(), indent=4, sort_keys=True)
print(json.dumps(r.json(), indent=4, sort_keys=True))


#Logout user
print("\nLogout user")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.logout",
                      "params": {},
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))
