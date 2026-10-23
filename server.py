from mcp.server.fastmcp import FastMCP
# --------------------------------
# Create the MCP server
# --------------------------------
mcp = FastMCP("DemoToolServer")
# --------------------------------
# Tool 1: Weather
# --------------------------------
@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    weather_data = {
        "delhi": "32 C, Sunny",
        "mumbai": "29 C, Humid",
        "bangalore": "24 C, Cloudy",
    }
    return weather_data.get(
        city.lower(),
        "Weather data not available for this city.",
    )
# --------------------------------
# Tool 2: Calculator
# --------------------------------
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
# --------------------------------
# Tool 3: Stock Price
# --------------------------------
@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """Get the mock stock price for a ticker symbol."""
    prices = {
        "aapl": "$228.50",
        "tsla": "$248.10",
        "googl": "$172.30",
    }

    return prices.get(
        symbol.lower(),
        "Stock symbol not found.",
    )

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another (mock rates)."""
    rates = {
        ("usd", "inr"): 83.2,
        ("inr", "usd"): 1 / 83.2,
    }
    rate = rates.get(
        (from_currency.lower(), to_currency.lower())
    )
    if rate is None:
        return "Conversion rate not available."
    converted = round(amount * rate, 2)
    return f"{amount} {from_currency.upper()} = {converted} {to_currency.upper()}"
# --------------------------------
# Run the server
# --------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
