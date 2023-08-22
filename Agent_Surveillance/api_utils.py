import requests
import datetime
import json



def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def notify_api_about_change(change):

    api_endpoint = "http://127.0.0.1:5000/notify_change"
    
    # Convert the data to a JSON string
    data_as_json = json.dumps(change, default=datetime_converter)

    try:
        headers = {'Content-type': 'application/json'}
        response = requests.post(api_endpoint, data=data_as_json, headers=headers)
        
        if response.status_code == 200:
            print("Notification à l'API réussie!")
        else:
            print(f"Erreur lors de la notification à l'API: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erreur lors de la notification à l'API: {e}")