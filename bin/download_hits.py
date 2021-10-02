#!/usr/bin/env python3

from pathlib import Path
import logging
import argparse
import time
import json
import sys
import os

from wykop.api import WykopAPI, WykopAPIError
from wykop.api.wrappers import WykoAPIWrapper, WykoAPICollection

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


DELAY_AFTER_EXCEPTION = 1
DELAY_BETWEEN_REQUESTS = 2


def download_links(apis, year, month, dest):
    dest = Path(dest) / str(year) / str(month)

    if os.path.exists(dest / '_complete'):
        print(f'Links for {year}-{month} has been already downloaded.', 
              file=sys.stderr)
        return 1

    os.makedirs(dest, exist_ok=True)

    page = 1
    delay_between_requests = DELAY_BETWEEN_REQUESTS

    while True:
        time.sleep(delay_between_requests)
        api = apis.get()
        try:
            log.info(f'Fetching links for {year}-{month} and {page} page ...')
            response = api.get_hits_month(year=year, month=month, page=page)
        except WykopAPIError as e:
            log.error(str(e))
            if e.code == 5:
                api.block()
                log.info(f'Blocking api to {api.blocked_to}')
                time.sleep(DELAY_AFTER_EXCEPTION)
            else:
                raise e
        except Exception as e:
            log.error(str(e))
            delay_between_requests += 1
            log.info(f'Increased time between requests to {delay_between_requests}.')
            time.sleep(DELAY_AFTER_EXCEPTION)
        else:
            saved_links = save_links(dest, response['data'])
            log.info(f'Saved {saved_links} new links.')
            if saved_links == 0:
                (dest / '_complete').touch()
                break
            delay_between_requests = max(delay_between_requests - 1, 1)
            page += 1



def save_links(dest, links):
    return sum([ save_link(dest, link) for link in links ])


def save_link(dest, link):
    file_path = dest / (str(link['id']) + '.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(json.dumps(link))
        return 1
    return 0


def get_cmd_args():
    parser = argparse.ArgumentParser(description='Download wykop.pl monthly hits links.')
    parser.add_argument('year', type=int, help='Year')
    parser.add_argument('month', type=int, help='Month')
    parser.add_argument('dest', type=str, help='Destination directory')
    parser.add_argument('apikeys', type=str, nargs='+', help='Application keys')
    return parser.parse_args()
    

def main():
    args = get_cmd_args()
    apis = [ WykoAPIWrapper(WykopAPI(key)) for key in args.apikeys ]
    api = WykoAPICollection(apis)
    download_links(api, args.year, args.month, Path(args.dest))


if __name__ == '__main__':
    main()