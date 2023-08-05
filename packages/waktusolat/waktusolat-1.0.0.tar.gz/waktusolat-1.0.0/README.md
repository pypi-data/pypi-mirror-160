# python-waktu-solat
A simple API wrapper for [waktu-solat-api](https://zaimramlan.github.io/waktu-solat-api/). (Malaysia only)

# Installation
```sh
pip install waktusolat
```

# Basic usage
List all states:
```python
from waktusolat import WaktuSolat

client = WaktuSolat()
print(client.states())
```

List all zones:
```python
from waktusolat import WaktuSolat

client = WaktuSolat()
print(client.zones())
```

List all prayer times:
```python
from waktusolat import WaktuSolat

client = WaktuSolat()
print(client.prayer_times())
```

# License
[MIT](./LICENSE)
