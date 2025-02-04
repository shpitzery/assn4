import requests
from stocks_config import stocks_config

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