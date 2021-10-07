# Wykop Tags

Repozytorum do tekstu [Wyciąganie danych przez REST API](https://dsinaction.pl/index.php/2021/10/07/wyciaganie-danych-przez-rest-api/)

## Wykop API

```python
from wykop.api import WykopAPI

api_key = os.environ.get('WYKOP_API_KEY')
api = WykopAPI(api_key)

links = api.get_hits_month(year=2020, month=10, page=1)
```