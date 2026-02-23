"""
Example Usage Cases for API Integration

This script demonstrates various ways to use the API integration module
for fetching and displaying data from external APIs.
"""

from api_integration import CryptoClient, WeatherClient, display_crypto_prices, display_weather


def example_1_single_crypto():
    """Example 1: Fetch a single cryptocurrency price."""
    print("\n📚 EXAMPLE 1: Getting Bitcoin Price")
    print("-" * 70)

    client = CryptoClient()
    data = client.get_crypto_prices(["bitcoin"])

    if data:
        display_crypto_prices(data)

    client.close()


def example_2_multiple_cryptos():
    """Example 2: Fetch multiple cryptocurrencies in different currencies."""
    print("\n📚 EXAMPLE 2: Getting Multiple Crypto Prices in Different Currencies")
    print("-" * 70)

    client = CryptoClient()
    data = client.get_crypto_prices(
        crypto_ids=["bitcoin", "ethereum", "binancecoin", "ripple", "cardano"],
        vs_currencies=["usd", "gbp"]
    )

    if data:
        display_crypto_prices(data, currencies=["usd", "gbp"])

    client.close()


def example_3_weather():
    """Example 3: Fetch weather for different locations."""
    print("\n📚 EXAMPLE 3: Getting Weather Data for Multiple Locations")
    print("-" * 70)

    locations = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    ]

    client = WeatherClient()

    for location in locations:
        weather_data = client.get_weather(location["lat"], location["lon"])
        if weather_data:
            display_weather(weather_data, location_name=location["name"])

    client.close()


def example_4_error_handling():
    """Example 4: Demonstrating error handling with invalid requests."""
    print("\n📚 EXAMPLE 4: Error Handling with Invalid Requests")
    print("-" * 70)

    client = CryptoClient()

    print("\n❌ Attempting to fetch data with invalid API endpoint...")
    # This will fail gracefully with error handling
    data = client.get_crypto_prices(["invalid-crypto-xyz"])

    if data:
        print("Received data (shouldn't happen with all invalid cryptos)")
    else:
        print("Request failed as expected, but error was handled gracefully.")

    client.close()


def example_5_trending():
    """Example 5: Fetch trending cryptocurrencies."""
    print("\n📚 EXAMPLE 5: Getting Trending Cryptocurrencies")
    print("-" * 70)

    client = CryptoClient()
    data = client.get_trending_cryptos()

    if data and "coins" in data:
        print("\n🔥 TOP 10 TRENDING CRYPTOCURRENCIES")
        print("="*70)

        for i, coin_data in enumerate(data["coins"][:10], 1):
            coin = coin_data["item"]
            name = coin["name"]
            symbol = coin["symbol"].upper()
            market_cap_rank = coin.get("market_cap_rank", "N/A")

            print(f"{i}. {name} ({symbol}) - Market Cap Rank: {market_cap_rank}")

        print("\n" + "="*70 + "\n")

    client.close()


def example_6_retry_logic():
    """Example 6: Manual retry logic for robustness."""
    print("\n📚 EXAMPLE 6: Retry Logic for Network Resilience")
    print("-" * 70)

    max_retries = 3
    retry_count = 0

    client = CryptoClient()

    while retry_count < max_retries:
        print(f"\nAttempt {retry_count + 1}/{max_retries}...")
        data = client.get_crypto_prices(["bitcoin", "ethereum"])

        if data:
            print("✅ Successfully retrieved data on attempt", retry_count + 1)
            display_crypto_prices(data)
            break
        else:
            retry_count += 1
            if retry_count < max_retries:
                print(f"⏳ Retrying in 2 seconds...")
                import time
                time.sleep(2)
            else:
                print("❌ Failed after maximum retries")

    client.close()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎯 API INTEGRATION EXAMPLES")
    print("="*70)

    # Run all examples
    example_1_single_crypto()
    example_2_multiple_cryptos()
    example_3_weather()
    example_4_error_handling()
    example_5_trending()
    example_6_retry_logic()

    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70 + "\n")
