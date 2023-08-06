# proxynova_scraper

Get free proxies for your projects from [proxinova.com](https://proxinova.com)

## Getting started


**Installing the package**

```text
pip install proxynova-scrapper
```

**Use**

You have two ways to get the proxies:

- Get the latest ones
- Get proxies by country

**Get the latest ones from different countries**

It will scrap the [main page](https://www.proxynova.com/proxy-server-list) from proxynova 

```python
from proxynova_scraper import get_proxies
proxies = get_proxies()
```

**Get proxies by country**

It will scrap [proxynova by specifying the country](https://www.proxynova.com/proxy-server-list/country-mx) (2 char code), if the table from proxynova doesn't contain any proxy it will return an empty array

```python
from proxynova_scraper import get_proxies_by_country
mexico_proxies = get_proxies_by_country('mx')
```

**Proxy item** 

This is an example of the content returned by `get_proxies` or `get_proxies_by_country`

```python
{
    'proxyIp': '45.174.77.241', 
    'proxyPort': '999', 
    'lastCheck': '2022-07-23 22:32:03Z', 
    'proxySpeed': 2735, 
    'Uptime': '5114', 
    'proxyCountry': 'Mexico - Chihuahua City', 
    'anonymity': 'Transparent'
}

```