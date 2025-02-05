import requests

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

urls = {
    "stocks": "http://localhost:5001/stocks",
    "capital-gains" : "http://localhost:5003/capital-gains"
}

def first_posts():
    for i in range(1,7):
        try:
            requests.post(urls["stocks"], json=stocks_config[f"stock{i}"])

        except Exception as e:
            return f"Error: {e}"
            
def make_request(service: str, query: str):
    if not query.strip():
        url = urls[service]
    else:
        url = f"{urls[service]}?{query}"

    try:
        response = requests.get(url)

        return response.text
    
    except requests.exceptions.RequestException as e:
        return f"Error making request: {str(e)}"

def main():

    first_posts()
    
    # read the query.txt file
    with open('query.txt', "r") as que_file:

        # open response.txt for writing
        with open('response.txt', 'w') as res_file:

            for line in que_file:
                line = line.strip()
                if not line:
                    continue

                # split the line at the first occurrence of :
                service, query_str = line.split(":", 1)

                res_file.write(f"query: {service}:{query_str}\n")
                res_file.write("response:\n")

                # make the request and write the response to response.txt
                json_response = make_request(service, query_str)
                res_file.write(f"{json_response}\n")

if __name__ == "__main__":
    main()