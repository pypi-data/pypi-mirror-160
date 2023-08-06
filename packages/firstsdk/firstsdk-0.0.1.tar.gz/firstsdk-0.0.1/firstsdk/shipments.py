import requests

def get_shipments_rates():
    try:
        rates = requests.get('http://127.0.0.1:8000/shipments/')
        return rates.json()
    except requests.exceptions.RequestException as e:
        print("Ocurrio un error al solicitar las tarifas -> ")
        print(e)
    
