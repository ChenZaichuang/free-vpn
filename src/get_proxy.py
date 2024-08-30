import json
import logging
import requests
from pythreadpool.native_thread_pool import NativeThreadPool

from src.logger import init_logging, logger

headers = {
    'accept': '*',
    'accept-language': '*',
    'cache-control': 'no-cache',
    'referer': 'https://www.kuaidaili.com/free/fps/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


@logger
def get_proxies_of_one_page(page):
    response = None
    for i in range(3):
        try:
            response = requests.get(f'https://www.kuaidaili.com/free/fps/{page}', headers=headers, verify=False, timeout=15)
            break
        except Exception as e:
            if i >= 2:
                raise e

    for line in response.iter_lines():
        line = line.decode()
        key_start_str = 'const fpsList = '
        if line.startswith(key_start_str):
            return json.loads(line[len(key_start_str):-1])
    return []


@logger
def get_all_proxies():
    page_num = 16
    pool = NativeThreadPool(total_thread_number=page_num, raise_exception=True)
    for i in range(page_num):
        pool.apply_async(get_proxies_of_one_page, args=(i,))
    return [proxy for proxies in pool.get_results_order_by_index(raise_exception=True) for proxy in proxies]


@logger
def validate_one_proxy(proxy):
    proxy_str = f"http://{proxy['ip']}:{proxy['port']}"
    proxies = {'http': proxy_str, 'https': proxy_str}
    try:
        response = requests.get('https://api64.ipify.org', proxies=proxies, verify=False, timeout=20)
        return proxy if proxy['ip'] in response.text else None
    except Exception as e:
        logging.error(f'fail {proxy_str} | {e}')
        return


@logger
def validate_proxies(proxy_list):
    pool = NativeThreadPool(total_thread_number=16, raise_exception=True)
    for proxy in proxy_list:
        pool.apply_async(validate_one_proxy, args=(proxy,))
    return [proxy for proxy in pool.get_results_order_by_index(raise_exception=True) if proxy is not None]


if __name__ == '__main__':

    init_logging()

    all_proxies = get_all_proxies()

    logging.info(f'all_proxies: {len(all_proxies)}')

    valid_proxies = validate_proxies(all_proxies)

    logging.info(f'valid_proxies: {len(valid_proxies)}')

    for proxy in valid_proxies:
        logging.info(proxy)
