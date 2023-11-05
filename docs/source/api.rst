
API Reference
=============


.. _proxyhub-api-broker:

Broker
------

.. autoclass:: proxyhub.api.Broker
    :members: grab, find, serve, stop, show_stats


.. _proxyhub-api-proxy:

Proxy
-----

.. autoclass:: proxyhub.proxy.Proxy
    :members: create, types, is_working, avg_resp_time, geo, error_rate, get_log
    :member-order: groupwise


.. _proxyhub-api-provider:

Provider
--------

.. autoclass:: proxyhub.providers.Provider
    :members: proxies, get_proxies
    :member-order: groupwise
