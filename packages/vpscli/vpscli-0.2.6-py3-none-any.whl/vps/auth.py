#!/usr/bin/env python
from typing import Tuple
from authc import authc


class AccountLoader:
    @classmethod
    def query_secrets(cls) -> Tuple[str]:
        accs = authc()
        return accs['redis_host'], accs['redis_port'], accs['redis_pass']
