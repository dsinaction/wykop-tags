from datetime import datetime, timedelta
import logging
import time

from wykop.api.client import WykopAPI

DELAY_BEFORE_GET_API_ATTEMPT = 120
API_BLOCK_LENGTH = 900

log = logging.getLogger(__name__)


class WykoAPIWrapper:

    def __init__(self, api):
        self.api = api
        self.blocked_to = None

    def __getattr__(self, name):
        return getattr(self.api, name)
    
    @property
    def is_block(self):
        return self.blocked_to is not None and self.blocked_to > datetime.now()

    def block(self, seconds = API_BLOCK_LENGTH):
        self.blocked_to = datetime.now() + timedelta(seconds=seconds)


class WykoAPICollection:
    
    def __init__(self, apis, next_attempt_time = DELAY_BEFORE_GET_API_ATTEMPT):
        self.apis = apis
        self._next_attempt_time = next_attempt_time

    def get(self):
        while True:
            try:
                return next(api for api in self.apis if not api.is_block )
            except StopIteration:
                log.warning(f'Unable to access wykop API. Waiting for the next attempt.')
                time.sleep(self._next_attempt_time)
