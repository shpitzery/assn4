import requests
import pytest

stocks_config = {
    "stock1": {
        "name": "NVIDIA Corporation",
        "symbol": "NVDA",
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    },
    "stock2": {
        "name": "Apple Inc.",
        "symbol": "AAPL",
        "purchase price": 183.63,
        "purchase date": "22-02-2024",
        "shares": 19
    },
    "stock3": {
        "name": "Alphabet Inc.",
        "symbol": "GOOG",
        "purchase price": 140.12,
        "purchase date": "24-10-2024",
        "shares": 14
    },
    "stock4": {
        "name": "Tesla, Inc.",
        "symbol": "TSLA",
        "purchase price": 194.58,
        "purchase date": "28-11-2022",
        "shares": 32
    },
    "stock5": {
        "name": "Microsoft Corporation",
        "symbol": "MSFT",
        "purchase price": 420.55,
        "purchase date": "09-02-2024",
        "shares": 35
    },
    "stock6": {
        "name": "Intel Corporation",
        "symbol": "INTC",
        "purchase price": 19.15,
        "purchase date": "13-01-2025",
        "shares": 10
    },
    "stock7": {
        "name": "Amazon.com, Inc.",
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    },
    "stock8": {
        "name": "Amazon.com, Inc.",
        "symbol": "AMZN",
        "purchase price": 134.66,
        "purchase date": "Tuesday, June 18, 2024",
        "shares": 7
    }
}

'''
    ids[1] = id of stock1
    ids[2] = id of stock2
    ids[3] = id of stock3
'''
ids = []
svs = []

def test_1():
    temp_ids = []
    for stock in [stocks_config['stock1'], stocks_config['stock2'], stocks_config['stock3']]:
        response = requests.post('http://localhost:5001/stocks', json=stock) # json=stock is the payload

        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        temp_ids.append(response.json()['id'])

    assert len(temp_ids) == 3, f"Expected 3 ids, but got {len(temp_ids)}"
    assert len(temp_ids) == len(set(temp_ids)), f"Expected 3 unique ids, but got {len(temp_ids)} with {len(set(temp_ids))} unique IDs"
    
    for id in temp_ids:
        ids.append(id)

def test_2():
    response = requests.get(f'http://localhost:5001/stocks/{ids[0]}')
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json()['symbol'] == 'NVDA', f"Expected symbol to be NVDA, but got {response.json()['symbol']}"

def test_3():
    response = requests.get('http://localhost:5001/stocks')
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    assert isinstance(data, list) and len(data) == 3, f"Expected a list of length 3, but got {data}"

    assert all(isinstance(stock, dict) for stock in data), f"Not all items in the list are JSON objects"

def test_4():
    symbols = []
    for id in ids:
        response = requests.get(f'http://localhost:5001/stock-value/{id}')

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        svs.append(response.json()['stock value'])
        symbols.append(response.json()['symbol'])

    assert symbols == ['NVDA', 'AAPL', 'GOOG'], f"Expected symbols to be NVDA, AAPL, GOOG but got {symbols}"

def test_5():
    response = requests.get('http://localhost:5001/portfolio-value')

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    pv = response.json()['portfolio value']

    assert pv * 0.97 <= svs[0] + svs[1] + svs[2] <= pv * 1.03, f"Expected portfolio value to be within 3% of the sum of stock values"

def test_6():
    response = requests.post('http://localhost:5001/stocks', json=stocks_config['stock7'])

    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

def test_7():
    response = requests.delete(f'http://localhost:5001/stocks/{ids[1]}')

    assert response.status_code == 204, f"Expected status code 204, but got {response.status_code}"

def test_8():
    response = requests.get(f'http://localhost:5001/stocks/{ids[1]}')

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

def test_9():
    response = requests.post('http://localhost:5001/stocks', json=stocks_config['stock8'])

    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"