"""
API Integration Module

This module demonstrates how to interact with external APIs, handle errors,
and display data in a user-friendly format. It includes functions for fetching
cryptocurrency prices and weather data.
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class APIClient:
    """A client for making API requests with error handling."""

    def __init__(self, timeout: int = 10):
        """
        Initialize the API client.

        Args:
            timeout (int): Request timeout in seconds. Default is 10.
        """
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a GET request to an API endpoint with error handling.

        Args:
            url (str): The API endpoint URL.
            params (Dict, optional): Query parameters for the request.
            headers (Dict, optional): Custom headers for the request.

        Returns:
            Dict: Parsed JSON response, or None if the request failed.

        Raises:
            Prints error messages instead of raising exceptions for better UX.
        """
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            # Check if the response status code indicates success
            response.raise_for_status()

            # Try to parse JSON
            return response.json()

        except requests.exceptions.Timeout:
            print(f"❌ Error: Request timed out after {self.timeout} seconds.")
            print(f"   The server took too long to respond. Try again later.")
            return None

        except requests.exceptions.ConnectionError:
            print("❌ Error: Connection failed.")
            print("   Please check your internet connection and try again.")
            return None

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print("❌ Error: The requested resource was not found (404).")
            elif status_code == 429:
                print("❌ Error: Too many requests. Please wait before trying again (429).")
            elif status_code == 401:
                print("❌ Error: Unauthorized. Invalid API key or credentials (401).")
            else:
                print(f"❌ Error: HTTP Error {status_code} - {e}")
            return None

        except json.JSONDecodeError:
            print("❌ Error: Failed to parse response as JSON.")
            print("   The API returned invalid data.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Error: An unexpected error occurred: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()


class CryptoClient(APIClient):
    """Client for fetching cryptocurrency data from CoinGecko API."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_crypto_prices(self, crypto_ids: List[str], vs_currencies: List[str] = ["usd"]) -> Optional[Dict]:
        """
        Fetch cryptocurrency prices.

        Args:
            crypto_ids (List[str]): List of cryptocurrency IDs (e.g., ["bitcoin", "ethereum"]).
            vs_currencies (List[str]): List of currencies to display prices in. Default is ["usd"].

        Returns:
            Dict: Cryptocurrency price data, or None if the request failed.
        """
        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": ",".join(crypto_ids),
            "vs_currencies": ",".join(vs_currencies),
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }

        return self.get(url, params=params)

    def get_trending_cryptos(self) -> Optional[Dict]:
        """
        Fetch trending cryptocurrencies.

        Returns:
            Dict: Trending cryptocurrency data, or None if the request failed.
        """
        url = f"{self.BASE_URL}/search/trending"
        return self.get(url)


class WeatherClient(APIClient):
    """Client for fetching weather data using Open-Meteo API (no auth required)."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Fetch weather data for a specific location.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Returns:
            Dict: Weather data, or None if the request failed.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "temperature_unit": "celsius"
        }

        return self.get(self.BASE_URL, params=params)


def display_crypto_prices(data: Dict, currencies: List[str] = ["usd"]) -> None:
    """
    Display cryptocurrency prices in a user-friendly format.

    Args:
        data (Dict): Cryptocurrency price data from API.
        currencies (List[str]): List of currencies to display.
    """
    if not data:
        return

    print("\n" + "="*70)
    print("💰 CRYPTOCURRENCY PRICES")
    print("="*70)

    for crypto, prices in data.items():
        print(f"\n📍 {crypto.upper()}")
        print("-" * 70)

        for currency in currencies:
            if currency in prices:
                price = prices[currency]
                market_cap = prices.get(f"{currency}_market_cap", "N/A")
                volume = prices.get(f"{currency}_24h_vol", "N/A")
                change = prices.get(f"{currency}_24h_change", "N/A")

                print(f"  Price ({currency.upper()}):        ${price:>15,.2f}" if isinstance(price, (int, float)) else f"  Price ({currency.upper()}):        {price}")

                if market_cap != "N/A" and isinstance(market_cap, (int, float)):
                    print(f"  Market Cap:      ${market_cap:>15,.0f}")

                if volume != "N/A" and isinstance(volume, (int, float)):
                    print(f"  24h Volume:      ${volume:>15,.0f}")

                if change != "N/A" and isinstance(change, (int, float)):
                    emoji = "📈" if change >= 0 else "📉"
                    print(f"  24h Change:      {emoji} {change:>14.2f}%")

    print("\n" + "="*70 + "\n")


def display_weather(data: Dict, location_name: str = "Location") -> None:
    """
    Display weather data in a user-friendly format.

    Args:
        data (Dict): Weather data from API.
        location_name (str): Name of the location.
    """
    if not data or "current" not in data:
        return

    print("\n" + "="*70)
    print(f"🌤️  WEATHER FOR {location_name.upper()}")
    print("="*70)

    current = data["current"]
    print(f"\n  Temperature:     {current.get('temperature_2m', 'N/A')}°C")
    print(f"  Wind Speed:      {current.get('wind_speed_10m', 'N/A')} km/h")

    weather_code = current.get("weather_code", None)
    if weather_code is not None:
        weather_descriptions = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Foggy 🌫️",
            48: "Foggy with rime 🌫️",
            51: "Light drizzle 🌧️",
            53: "Moderate drizzle 🌧️",
            55: "Dense drizzle 🌧️",
            61: "Slight rain 🌧️",
            63: "Moderate rain 🌧️",
            65: "Heavy rain ⛈️",
            71: "Slight snow ❄️",
            73: "Moderate snow ❄️",
            75: "Heavy snow ❄️",
            77: "Snow grains ❄️",
            80: "Slight rain showers 🌧️",
            81: "Moderate rain showers 🌧️",
            82: "Violent rain showers ⛈️",
            85: "Slight snow showers ❄️",
            86: "Heavy snow showers ❄️",
            95: "Thunderstorm ⛈️",
            96: "Thunderstorm with hail ⛈️",
            99: "Thunderstorm with hail ⛈️"
        }
        description = weather_descriptions.get(weather_code, f"Unknown ({weather_code})")
        print(f"  Condition:       {description}")

    print("\n" + "="*70 + "\n")


def main():
    """Main function demonstrating API integration."""

    print("\n🚀 API Integration Demo")
    print("="*70)

    # Example 1: Fetch cryptocurrency prices
    print("\n1️⃣  Fetching cryptocurrency prices...")
    crypto_client = CryptoClient()
    crypto_data = crypto_client.get_crypto_prices(
        crypto_ids=["bitcoin", "ethereum", "cardano"],
        vs_currencies=["usd", "eur"]
    )

    if crypto_data:
        display_crypto_prices(crypto_data, currencies=["usd", "eur"])

    # Example 2: Fetch weather data
    print("\n2️⃣  Fetching weather data...")
    print("   Location: Lagos, Nigeria (6.5244°N, 3.3792°E)")

    weather_client = WeatherClient()
    weather_data = weather_client.get_weather(latitude=6.5244, longitude=3.3792)

    if weather_data:
        display_weather(weather_data, location_name="Lagos, Nigeria")

    # Clean up
    crypto_client.close()
    weather_client.close()

    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
