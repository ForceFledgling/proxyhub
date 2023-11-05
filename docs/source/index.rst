.. proxyhub documentation master file, created by
   sphinx-quickstart on Thu May 26 13:04:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

proxyhub
===========

[Finder | Checker | Server]

.. image:: https://img.shields.io/pypi/v/proxyhub.svg?style=flat-square
    :target: https://pypi.python.org/pypi/proxyhub/
.. image:: https://img.shields.io/travis/ForceFledgling/proxyhub.svg?style=flat-square
    :target: https://travis-ci.org/ForceFledgling/proxyhub
.. image:: https://img.shields.io/pypi/wheel/proxyhub.svg?style=flat-square
    :target: https://pypi.python.org/pypi/proxyhub/
.. image:: https://img.shields.io/pypi/pyversions/proxyhub.svg?style=flat-square
    :target: https://pypi.python.org/pypi/proxyhub/
.. image:: https://img.shields.io/pypi/l/proxyhub.svg?style=flat-square
    :target: https://pypi.python.org/pypi/proxyhub/

proxyhub is an open source tool that asynchronously finds public proxies from multiple sources and concurrently checks them.

.. image:: _static/index_find_example.gif


Features
--------

* Finds more than 7000 working proxies from ~50 sources.
* Support protocols: HTTP(S), SOCKS4/5. Also CONNECT method to ports 80 and 23 (SMTP).
* Proxies may be filtered by type, anonymity level, response time, country and status in DNSBL.
* Work as a proxy server that distributes incoming requests to external proxies. With automatic proxy rotation.
* All proxies are checked to support Cookies and Referer (and POST requests if required).
.. * Save found proxies to a file in custom format.
* Automatically removes duplicate proxies.
* Is asynchronous.


Requirements
------------

* Python **3.5** or higher
* `aiohttp <https://pypi.python.org/pypi/aiohttp>`_
* `aiodns <https://pypi.python.org/pypi/aiodns>`_
* `maxminddb <https://pypi.python.org/pypi/maxminddb>`_


Installation
------------

To install last stable release from pypi:

.. code-block:: bash

    $ pip install proxyhub

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install -U git+https://github.com/ForceFledgling/proxyhub.git


Usage
-----


CLI Examples
~~~~~~~~~~~~


Find
""""

Find and show 10 HTTP(S) proxies from United States with the high level of anonymity:

.. code-block:: bash

    $ proxyhub find --types HTTP HTTPS --lvl High --countries US --strict -l 10

.. image:: _static/cli_find_example.gif


Grab
""""

Find and save to a file 10 US proxies (without a check):

.. code-block:: bash

    $ proxyhub grab --countries US --limit 10 --outfile ./proxies.txt

.. image:: _static/cli_grab_example.gif


Serve
"""""

Run a local proxy server that distributes incoming requests to a pool
of found HTTP(S) proxies with the high level of anonymity:

.. code-block:: bash

    $ proxyhub serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High


.. image:: _static/cli_serve_example.gif

.. note::

    Run ``proxyhub --help`` for more information on the options available.

    Run ``proxyhub <command> --help`` for more information on a command.


Basic code example
~~~~~~~~~~~~~~~~~~

Find and show 10 working HTTP(S) proxies:

.. literalinclude:: ../../examples/basic.py
    :lines: 3-

:doc:`More examples <examples>`.


TODO
----

* Check the ping, response time and speed of data transfer
* Check site access (Google, Twitter, etc) and even your own custom URL's
* Information about uptime
* Checksum of data returned
* Support for proxy authentication
* Finding outgoing IP for cascading proxy
* The ability to specify the address of the proxy without port (try to connect on defaulted ports)


Contributing
------------

* Fork it: https://github.com/ForceFledgling/proxyhub/fork
* Create your feature branch: git checkout -b my-new-feature
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-feature
* Submit a pull request!


License
-------

Licensed under the Apache License, Version 2.0

*This product includes GeoLite2 data created by MaxMind, available from* `http://www.maxmind.com <http://www.maxmind.com>`_.



Contents:

.. toctree::

   api
   examples
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
