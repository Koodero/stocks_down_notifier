from send_email import send_gmail
from dotenv import load_dotenv
import requests
import json
import os

# A list of the stock symbols you want to monitor, have to be a US based stock that alphavantage supports
stock_symbols = ["AAPL", "NVDA"]

# Loading environment variables from .env -- make sure to make own .env file with needed passkeys
load_dotenv()


def main():

    # Load existing stocks.json file and get the contents
    with open("stocks.json", "r") as file:
        data = file.read()
        json_data = json.loads(data)


    # For each symbol in given symbol list, find out the previous days market value and compare it to the stock.json file content
    for symbol in stock_symbols:
        url = 'https://www.alphavantage.co/query'
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": os.getenv("AV_KEY")    # from .env file, give alphavantage key
        }

        # Doing the calculation and updating json file
        try:
            response = requests.get(url=url, params=params)
            response.raise_for_status()
            symbol_data = response.json()

            # Getting closing price
            daily_data = symbol_data['Time Series (Daily)'] 
            most_recent_day= next(iter(daily_data))
            latest_data = daily_data[most_recent_day]
            day_closing_value = float(latest_data['4. close'])

            # Checking if json file is empty, json needs empty brackets to work
            if symbol not in json_data:
                json_data[symbol] = {'updated': most_recent_day, 'highest_value': day_closing_value}
            # Else checking if stock price has gone up or down, if up update stock highest value to json
            else:
                starting_price = float(json_data[symbol]["highest_value"])
                if starting_price < day_closing_value:
                    json_data[symbol] = {'updated': most_recent_day, 'highest_value': day_closing_value}
                else:
                    # If the stock has gone down a specified percentile, send email notification
                    prcents = (((starting_price - day_closing_value)/(abs(starting_price))) * 100)
                    if prcents >= 15:
                        send_gmail(symbol, json_data[symbol]["updated"], prcents)

        # Cheking for errors
        except requests.RequestException as e:
            print(f"Request failed for {symbol}: {e}")
        except KeyError as e:
            print(f"Missing key in response for {symbol}: {e}")
        except ValueError as e:
            print(f"Value error for {symbol}: {e}")


    # Update json file
    with open("stocks.json", "w") as file:
        json.dump(json_data, file, indent=4)



if __name__ == "__main__":
    main()

