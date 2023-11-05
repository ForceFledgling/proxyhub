"""
Copyright © 2023 ForceFledgling <pvenv@icloud.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__title__ = 'proxyhub'
__package__ = 'proxyhub'
__version__ = '0.0.1a1'
__short_description__ = 'An advanced [Finder | Checker | Server] tool for proxy servers, supporting both HTTP(S) and SOCKS protocols.'
__author__ = 'ForceFledgling'
__author_email__ = 'pvenv@icloud.com'
__url__ = 'https://github.com/ForceFledgling/proxyhub'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2023 ForceFledgling'


import logging  # noqa
import warnings  # noqa

from .api import Broker  # noqa
from .checker import Checker  # noqa
from .judge import Judge  # noqa
from .providers import Provider  # noqa
from .proxy import Proxy  # noqa
from .server import ProxyPool, Server  # noqa

logger = logging.getLogger('asyncio')
logger.addFilter(logging.Filter('has no effect when using ssl'))

warnings.simplefilter('always', UserWarning)
warnings.simplefilter('once', DeprecationWarning)


__all__ = (Proxy, Judge, Provider, Checker, Server, ProxyPool, Broker)
