import time
import requests

def respectful_requester(url, delay_interval=1):
    response = requests.get(url)
    # If the status code indicates rate limiting, sleep then retry
    if response.status_code == 429:
        print('Rate limit reached. Sleeping...')
        time.sleep(delay_interval)
        return respectful_requester(url, delay_interval)
    elif response.status_code != 200:
        print(f'Error: {response.status_code}. Try a different proxy or user-agent')

    return response

respectful_requester("https://jp.louisvuitton.com/jpn-jp/products/noa-compact-wallet-monogram-nvprod5590056v/M83476",delay_interval=1)
