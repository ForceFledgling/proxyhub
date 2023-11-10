*Porting to Python3.10+ is painful and the progress is moving slowly.*  
*We need more volunteers to join. PRs welcome! :joy:*

ProxyHub
===========

![logo](https://github.com/ForceFledgling/proxyhub/blob/main/docs/img/logo_transparent.png)

ProxyHub is an open source tool that asynchronously finds public proxies from multiple sources and concurrently checks them.

[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg)](docs)
[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache2-brightgreen.svg)](https://choosealicense.com/licenses/apache-2.0/)
[![pypi Version](https://img.shields.io/pypi/v/proxyhub.svg?style=flat-square&logo=proxyhub&logoColor=white)](https://pypi.org/project/proxyhub/)
[![PyPi downloads](https://static.pepy.tech/personalized-badge/proxyhub?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/proxyhub/)

Features 🌟
--------

-   Finds more than 7000 working proxies from \~50 sources.
-   Support protocols: HTTP(S), SOCKS4/5. Also CONNECT method to ports 80 and 23 (SMTP).
-   Proxies may be filtered by type, anonymity level, response time, country and status in DNSBL.
-   Work as a proxy server that distributes incoming requests to external proxies. With automatic proxy rotation.
-   All proxies are checked to support Cookies and Referer (and POST requests if required).
-   Automatically removes duplicate proxies.
-   Is asynchronous.

Requirements 📋
------------

-   Python 3.8+
-   [aiohttp](https://pypi.python.org/pypi/aiohttp)
-   [aiodns](https://pypi.python.org/pypi/aiodns)
-   [maxminddb](https://pypi.python.org/pypi/maxminddb)

Installation 🚀
------------

### Install locally

To install last stable release from pypi:

``` {.sourceCode .bash}
$ pip install proxyhub
```

To install the latest development version from GitHub:

``` {.sourceCode .bash}
$ pip install -U git+https://github.com/ForceFledgling/proxyhub.git
```

### Use pre-built Docker image

``` {.sourceCode .bash}
$ docker pull ForceFledgling/proxyhub
```

### Build bundled one-file executable with pyinstaller

#### Requirements
Supported Operating System: Windows, Linux, MacOS

*On UNIX-like systems (Linux / macOSX / BSD)*

Install these tools
 - upx
 - objdump (this tool is usually in the binutils package)
``` {.sourceCode .bash}
$ sudo apt install -y upx-ucl binutils # On Ubuntu / Debian
```

#### Build

```
pip install pyinstaller \
&& pip install . \
&& mkdir -p build \
&& cd build \
&& pyinstaller --onefile --name proxyhub --add-data "../proxyhub/data:data" --workpath ./tmp --distpath . --clean ../py2exe_entrypoint.py \
&& rm -rf tmp *.spec
```

The executable is now in the build directory

Usage 💡
-----

### CLI Examples

#### Find

Find and show 10 HTTP(S) proxies from United States with the high level of anonymity:

``` {.sourceCode .bash}
$ proxyhub find --types HTTP HTTPS --lvl High --countries US --strict -l 10
```

#### Grab

Find and save to a file 10 US proxies (without a check):

``` {.sourceCode .bash}
$ proxyhub grab --countries US --limit 10 --outfile ./proxies.txt
```

#### Serve

Run a local proxy server that distributes incoming requests to a pool of found HTTP(S) proxies with the high level of anonymity:

``` {.sourceCode .bash}
$ proxyhub serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High --min-queue 5
```

Run `proxyhub --help` for more information on the options available.
Run `proxyhub <command> --help` for more information on a command.

### Basic code example

Find and show 10 working HTTP(S) proxies:

``` {.sourceCode .python}
import asyncio
from proxyhub import Broker

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        print('Found proxy: %s' % proxy)

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=10),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
```

[More examples](https://proxyhub.readthedocs.io/en/latest/examples.html).

### Proxy information per requests
#### HTTP
Check `X-Proxy-Info` header in response.
```
$ http_proxy=http://127.0.0.1:8888 https_proxy=http://127.0.0.1:8888 curl -v http://httpbin.org/get
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> GET http://httpbin.org/get HTTP/1.1
> Host: httpbin.org
> User-Agent: curl/7.58.0
> Accept: */*
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 200 OK
< X-Proxy-Info: 174.138.42.112:8080
< Date: Mon, 04 May 2020 03:39:40 GMT
< Content-Type: application/json
< Content-Length: 304
< Server: gunicorn/19.9.0
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
< X-Cache: MISS from ADM-MANAGER
< X-Cache-Lookup: MISS from ADM-MANAGER:880
< Connection: keep-alive
<
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Cache-Control": "max-age=259200",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.58.0",
    "X-Amzn-Trace-Id": "Root=1-5eaf8e7c-6a1162a1387a1743a49063f4"
  },
  "origin": "...",
  "url": "http://httpbin.org/get"
}
* Connection #0 to host 127.0.0.1 left intact
```

#### HTTPS
We are not able to modify HTTPS traffic to inject custom header once they start being encrypted. A `X-Proxy-Info` will be sent to client after `HTTP/1.1 200 Connection established` but not sure how clients can read it.
```
(env) username@host:~/workspace/proxyhub2$ http_proxy=http://127.0.0.1:8888 https_proxy=http://127.0.0.1:8888 curl -v https://httpbin.org/get
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
* allocate connect buffer!
* Establish HTTP proxy tunnel to httpbin.org:443
> CONNECT httpbin.org:443 HTTP/1.1
> Host: httpbin.org:443
> User-Agent: curl/7.58.0
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 200 Connection established
< X-Proxy-Info: 207.148.22.139:8080
<
* Proxy replied 200 to CONNECT request
* CONNECT phase completed!
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
...
*  SSL certificate verify ok.
* Using HTTP2, server supports multi-use
* Connection state changed (HTTP/2 confirmed)
* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
* Using Stream ID: 1 (easy handle 0x5560b2e93580)
> GET /get HTTP/2
> Host: httpbin.org
> User-Agent: curl/7.58.0
> Accept: */*
>
* Connection state changed (MAX_CONCURRENT_STREAMS updated)!
< HTTP/2 200
< date: Mon, 04 May 2020 03:39:35 GMT
< content-type: application/json
< content-length: 256
< server: gunicorn/19.9.0
< access-control-allow-origin: *
< access-control-allow-credentials: true
<
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.58.0",
    "X-Amzn-Trace-Id": "Root=1-5eaf8e77-efcb353b0983ad6a90f8bdcd"
  },
  "origin": "...",
  "url": "https://httpbin.org/get"
}
* Connection #0 to host 127.0.0.1 left intact
```

### HTTP API
#### Get info of proxy been used for retrieving specific url
For HTTP, it's easy.
```
$ http_proxy=http://127.0.0.1:8888 https_proxy=http://127.0.0.1:8888 curl -v http://proxycontrol/api/history/url:http://httpbin.org/get
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> GET http://proxycontrol/api/history/url:http://httpbin.org/get HTTP/1.1
> Host: proxycontrol
> User-Agent: curl/7.58.0
> Accept: */*
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 34
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
<
{"proxy": "..."}
```

For HTTPS, we're not able to know encrypted payload (request), so only hostname can be used.
```
$ http_proxy=http://127.0.0.1:8888 https_proxy=http://127.0.0.1:8888 curl -v http://proxycontrol/api/history/url:httpbin.org:443
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> GET http://proxycontrol/api/history/url:httpbin.org:443 HTTP/1.1
> Host: proxycontrol
> User-Agent: curl/7.58.0
> Accept: */*
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 34
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
<
{"proxy": "..."}
* Connection #0 to host 127.0.0.1 left intact
```

#### Remove specific proxy from queue
```
$ http_proxy=http://127.0.0.1:8888 https_proxy=http://127.0.0.1:8888 curl -v http://proxycontrol/api/remove/PROXY_IP:PROXY_PORT
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> GET http://proxycontrol/api/remove/... HTTP/1.1
> Host: proxycontrol
> User-Agent: curl/7.58.0
> Accept: */*
> Proxy-Connection: Keep-Alive
>
< HTTP/1.1 204 No Content
<
* Connection #0 to host 127.0.0.1 left intact
```

TODO 🛠️
----

-   Check the ping, response time and speed of data transfer
-   Check site access (Google, Twitter, etc) and even your own custom URL's
-   Information about uptime
-   Checksum of data returned
-   Support for proxy authentication
-   Finding outgoing IP for cascading proxy
-   The ability to specify the address of the proxy without port (try to connect on defaulted ports)

Contributing 🤝
------------

-   Fork it: <https://github.com/ForceFledgling/proxyhub/fork>
-   Create your feature branch: `git checkout -b my-new-feature`
-   We use [Poetry](https://python-poetry.org/) to manage dependencies. If need, install dependencies: `poetry install`
-   Commit your changes: `git commit -am 'Add some feature'`
-   Push to the branch: `git push origin my-new-feature`
-   Submit a pull request!
-   [Contributor workflow](https://github.com/ForceFledgling/proxyhub/issues/)
