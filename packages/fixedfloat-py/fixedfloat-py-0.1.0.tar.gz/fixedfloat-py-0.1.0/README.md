# Python module for FixedFloat.com API

Implements the following API methods:

- Get currencies: `Getting a list of all currencies that are available on FixedFloat.com`;
- Get price: `Information about a currency pair with a set amount of funds`;
- Get order: `Receiving information about the order`;
- Set emergency: `Emergency Action Choice`;
- Create order: `Creating exchange orders`;


## How to use: 

```python3
from FixedFloat import FixedFloat

api = FixedFloat("API_PUBLIC","API_SECRET")

# Get all currencies:
print(api.get_currencies())

# Create exchange order:

test_btc_address = "test_btc_address_here"
order = api.create_order("ETH", "BTC", 0.5, test_btc_address, "fixed")
print(order)

# Get order:

print(api.get_order("ORDER_ID", "TOKEN")) # you can get TOKEN after creating an order

# Get pair exchange price:

print(api.get_price("ETH", 0.5, "BTC", "fixed"))

# Setting emergency: 

print(api.set_emergency("ORDER_ID", "TOKEN", "EXCHANGE"))
```

## Reference: 

https://fixedfloat.com/api
