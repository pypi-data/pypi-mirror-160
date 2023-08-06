import asyncio
from bs4 import BeautifulSoup
import unidecode
import traceback
from pyppeteer import launch
from .scrapper import _generic_row_parser, _get_soup_instance, _get_table_by_id, _get_table_columns, _get_table_content
from .utils import _replace_chars

PROXY_TABLE_ID = "tbl_proxy_list"
PROXY_PROVIDER_BASE_URL = "https://www.proxynova.com"
LATEST_PROXIES = "proxy-server-list"


def _extract_ip(column: BeautifulSoup):
    """
        Extracts the ip value from the column
        Arguments:
            column: BeautifulSoup instance
        Returns:
            the value of the ip (str)
    """
    abbr = column.find('abbr')
    raw_ip = ""
    if abbr is not None:
        raw_ip = abbr.text
    else:
        raw_ip = column.text
    return str(unidecode.unidecode(raw_ip.strip()))


def _proxy_row_parser(column: BeautifulSoup, index: int):
    """
        Allows to extract the information needed from each column
        Arguments:
            column: BeautifulSoup instance
            index: an integer to determine the column and how to extract the value
        Returns:
            A parsed value
    """
    if index == 0:
        return _extract_ip(column)
    elif index == 2:
        return column.find('time').get('datetime')
    elif index == 3:
        return int(_replace_chars(str(column.text)).replace('ms', ''))
    elif index == 5:
        return " ".join(str(column.text).split())
    else:
        return _replace_chars(str(column.text))


def _extract_proxies(table: BeautifulSoup):
    """
        Read the html table and transforms the content into a dictionary 
        Arguments:
            table: BeautifulSoup instance
        Returns:
            An array containing each table row transformed into a python dictionary
    """
    columns = _get_table_columns(table)
    table_content = _get_table_content(table)
    proxies = []
    for row in table_content:
        parsed_info = _generic_row_parser(row, _proxy_row_parser)
        if len(parsed_info) > 1:
            parsed_content = dict(zip(columns, parsed_info))
            proxies.append(parsed_content)
    return proxies


async def _get_page_content(url: str):
    """
        Function used to get the html from a webpage
        Arguments:
            url: web page url (a string)
        Returns:
            a string containing the html code
    """
    browser = await launch(headless=True)
    page = await browser.newPage()
    try:
        await page.goto(url, {"waitUntil": "load"})
    except Exception:
        traceback.print_exc()
    else:
        html = await page.content()
        return html
    finally:
        await page.close()
        await browser.close()


def _get_proxies(country_code: str = None):
    """
        Common method to scrap the proxy table by country or all proxies availables (mixed countries)
        Arguments:
            country_code: the country code format (ISO code of two chars), example: us
        Returns:
            An array of proxies (dictionary of proxy info)
    """
    url: str
    if country_code is None:
        url = "{}/{}/".format(PROXY_PROVIDER_BASE_URL, LATEST_PROXIES)
    else:
        url = "{}/{}/country-{}".format(PROXY_PROVIDER_BASE_URL,
                                        LATEST_PROXIES, country_code)
    loop = asyncio.get_event_loop()
    content = loop.run_until_complete(_get_page_content(url))
    table = _get_table_by_id(_get_soup_instance(content), PROXY_TABLE_ID)
    return _extract_proxies(table)


def get_proxies():
    """
        Wrapper to get proxies availables from proxy-server-list url
        Returns:
            An array of proxies
    """
    return _get_proxies()


def get_proxies_by_country(country_code: str):
    """
        Wrapper to get proxies by country
        Arguments:
            country_code: ISO (two chars) country code, example: us
        Returns:
            An array of proxies filtered by country
    """
    return _get_proxies(country_code)
