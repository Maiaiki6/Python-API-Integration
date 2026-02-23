# Python API Integration Project

A comprehensive Python project demonstrating how to interact with external APIs, fetch data, handle errors gracefully, and display results in a user-friendly format.

## 📋 Overview

This project showcases best practices for API integration in Python, including:

- ✅ **GET requests** using the `requests` library
- ✅ **Error handling** for network issues, timeouts, and invalid responses
- ✅ **Data parsing** from JSON responses
- ✅ **User-friendly output** with formatted display functions
- ✅ **Reusable client classes** for different APIs
- ✅ **Type hints** for better code clarity
- ✅ **Session management** for connection pooling

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\users\Mustapha MaiAiki\documents\Python-API-Integration
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `requests` - HTTP library for making API requests

## 🚀 Quick Start

### Run the Main Demo
```bash
python api_integration.py
```

This will:
1. Fetch Bitcoin, Ethereum, and Cardano prices
2. Fetch weather data for Lagos, Nigeria
3. Display all data in a formatted table

### Run Examples
```bash
python examples.py
```

This runs 6 different example scenarios:
1. Single cryptocurrency price
2. Multiple cryptocurrencies in different currencies
3. Weather for multiple locations
4. Error handling demonstration
5. Trending cryptocurrencies
6. Retry logic implementation

## 📚 Project Structure

```
├── api_integration.py    # Main module with API clients
├── examples.py           # Example usage scenarios
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🔧 Key Components

### APIClient (Base Class)
Handles generic HTTP GET requests with comprehensive error handling.

**Features:**
- Timeout handling
- Connection error detection
- HTTP error status code handling (404, 429, 401, etc.)
- JSON parsing with error handling
- Session management for connection pooling

**Methods:**
```python
APIClient.get(url, params, headers) -> Optional[Dict]
```

### CryptoClient (Cryptocurrency Prices)
Fetches cryptocurrency data from the CoinGecko API (free, no authentication required).

**APIs Used:**
- `GET /simple/price` - Get current prices
- `GET /search/trending` - Get trending cryptocurrencies

**Methods:**
```python
CryptoClient.get_crypto_prices(crypto_ids, vs_currencies) -> Optional[Dict]
CryptoClient.get_trending_cryptos() -> Optional[Dict]
```

**Example:**
```python
client = CryptoClient()
data = client.get_crypto_prices(
    crypto_ids=["bitcoin", "ethereum"],
    vs_currencies=["usd", "eur"]
)
client.close()
```

### WeatherClient (Weather Data)
Fetches weather information from the Open-Meteo API (free, no authentication required).

**APIs Used:**
- `GET /v1/forecast` - Get current weather

**Methods:**
```python
WeatherClient.get_weather(latitude, longitude) -> Optional[Dict]
```

**Example:**
```python
client = WeatherClient()
data = client.get_weather(latitude=40.7128, longitude=-74.0060)
client.close()
```

## 🛡️ Error Handling

The project demonstrates comprehensive error handling for:

### 1. **Timeout Errors**
```
❌ Error: Request timed out after 10 seconds.
   The server took too long to respond. Try again later.
```

### 2. **Connection Errors**
```
❌ Error: Connection failed.
   Please check your internet connection and try again.
```

### 3. **HTTP Status Errors**
- **404:** Resource not found
- **429:** Rate limit exceeded (too many requests)
- **401:** Unauthorized (invalid API key)
- **5xx:** Server errors

### 4. **JSON Parsing Errors**
```
❌ Error: Failed to parse response as JSON.
   The API returned invalid data.
```

### 5. **Generic Request Exceptions**
```
❌ Error: An unexpected error occurred: {details}
```

## 📊 Display Functions

### display_crypto_prices(data, currencies)
Formats cryptocurrency data into a readable table:

```
======================================================================
💰 CRYPTOCURRENCY PRICES
======================================================================

📍 BITCOIN
----------------------------------------------------------------------
  Price (USD):              55000.00
  Market Cap:        1,050,000,000,000
  24h Volume:          15,000,000,000
  24h Change:          📈   2.50%
```

### display_weather(data, location_name)
Formats weather data with emoji indicators:

```
======================================================================
🌤️  WEATHER FOR LAGOS, NIGERIA
======================================================================

  Temperature:     28°C
  Wind Speed:      12 km/h
  Condition:       Partly cloudy ⛅

======================================================================
```

## 🔑 API Endpoints Used

### CoinGecko API
- **Base URL:** `https://api.coingecko.com/api/v3`
- **Authentication:** Not required (free tier)
- **Rate Limit:** 10-50 calls/minute (check official docs)

### Open-Meteo API
- **Base URL:** `https://api.open-meteo.com/v1`
- **Authentication:** Not required (free tier)
- **Rate Limit:** Unlimited for personal use

## 💡 Best Practices Demonstrated

### 1. **Type Hints**
```python
def get_crypto_prices(self, crypto_ids: List[str], vs_currencies: List[str] = ["usd"]) -> Optional[Dict]:
```

### 2. **Session Reuse**
```python
self.session = requests.Session()
# Reuses connections for multiple requests
```

### 3. **Configurable Timeouts**
```python
response = self.session.get(url, timeout=self.timeout)
```

### 4. **User-Friendly Output**
Using emojis and formatted text for better readability.

### 5. **Proper Resource Management**
```python
try:
    # Use client
finally:
    client.close()  # Always clean up

# Or use context managers (can be extended)
```

### 6. **Graceful Degradation**
Returns `None` instead of raising exceptions for better UX.

## 🔄 Usage Patterns

### Pattern 1: Simple Query
```python
client = CryptoClient()
data = client.get_crypto_prices(["bitcoin"])
if data:
    # Process data
finally:
    client.close()
```

### Pattern 2: Multiple Queries with One Client
```python
client = CryptoClient()
for crypto_id in ["bitcoin", "ethereum", "cardano"]:
    data = client.get_crypto_prices([crypto_id])
    if data:
        # Process data
client.close()  # Single cleanup
```

### Pattern 3: Error Handling with Retries
```python
max_retries = 3
for attempt in range(max_retries):
    data = client.get_crypto_prices(["bitcoin"])
    if data:
        break
    print(f"Retry {attempt + 1}/{max_retries}")
```

## 🧪 Testing

To verify the setup works:

```bash
# Test if requests library is properly installed
python -c "import requests; print('✅ requests library is installed')"

# Run main demo
python api_integration.py

# Run examples
python examples.py
```

## 📝 Common Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'requests'
**Solution:**
```bash
pip install requests
```

### Issue: Connection timeout
**Possible causes:**
- No internet connection
- API server is down
- Firewall blocking requests

**Solution:**
- Check internet connection
- Try again later
- Use a VPN if needed

### Issue: JSON decode error
**Cause:** API returned unexpected format

**Solution:**
- Check if the API endpoint is correct
- Verify parameters are valid
- Check API documentation

## 🔗 External Resources

- **Requests Library:** https://requests.readthedocs.io/
- **CoinGecko API:** https://www.coingecko.com/api/documentations/v3
- **Open-Meteo API:** https://open-meteo.com/en/docs
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes

## 📄 License

This project is provided as an educational example.

## 🎯 Learning Objectives Achieved

✅ Used the `requests` library to make GET requests  
✅ Parsed and displayed fetched data in user-friendly format  
✅ Handled errors including failed requests and invalid responses  
✅ Implemented proper error messages for different failure scenarios  
✅ Created reusable client classes for different APIs  
✅ Demonstrated session management and resource cleanup  
✅ Added comprehensive documentation and examples  

---

**Happy API integrating! 🚀**
