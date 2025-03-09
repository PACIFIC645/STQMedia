import requests

class CurrencyConverter:
    @staticmethod
    def get_exchange_rate(from_currency="ZAR", to_currency="ZAR"):
        """
        Fetches the exchange rate from an API.
        
        Parameters:
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
        
        Returns:
        float: The exchange rate from `from_currency` to `to_currency`.
        """
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            return data['rates'].get(to_currency, 1)
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return 1  # Default to 1 if the API fails