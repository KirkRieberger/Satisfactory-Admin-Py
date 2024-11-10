import requests
import json
import base64
from sys import exit as sys_ex

# Factor into init and run sections?


def main():
    serverAddr = "192.168.1.17"
    serverPort = "7777"
    baseUrl = "https://" + serverAddr + ":" + serverPort + "/api/v1"
    headers = {"Encoding": "utf-8"}
    print("Contacting " + baseUrl + "...")

    # Do login, get auth token
    auth = passwordlessLogin(baseUrl, headers)
    if not auth[0]:
        print(f"Authorization failed with status code {auth[1]}!")
        sys_ex()

    print(auth[1])
    headers.update({"Authorization": f"Bearer {auth[1]}"})

    # Check auth level
    token = auth[1].split(".")
    tokenPayload = token[0]
    tokenFingerprint = token[1]

    tokenPayload = base64.b64decode(tokenPayload)
    print(tokenPayload)

    # Query server state
    response = postJSONRequest(baseUrl, headers, {"function": "QueryServerState"})
    print(response.status_code)
    print(response.content)


def postJSONRequest(url: str, headers: dict, payload: dict) -> requests.Response:
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response


def passwordlessLogin(url: str, headers: dict) -> tuple:
    payload = json.dumps(
        {
            "function": "PasswordlessLogin",
            "data": {"MinimumPrivilegeLevel": "client"},
        }
    )
    headers.update({"Content-Type": "application/json"})
    print(json.dumps(payload))
    # Uses data=payload not, json=payload
    tempReq = requests.Request(
        method="POST", url=url, headers=headers, data=payload
    ).prepare()

    response = requests.post(url, headers=headers, data=payload, verify=False)
    # response = postJSONRequest(url, headers, payload)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        # Strip out auth token
        respJSON = response.json()
        authToken = respJSON["data"]["authenticationToken"]
        return (1, authToken)
    else:
        return (0, response.status_code)


if __name__ == "__main__":
    # main()
    return "Test"
