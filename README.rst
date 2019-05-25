ipgetter2
=========

.. image:: https://img.shields.io/pypi/v/ipgetter2.svg
    :target: https://pypi.python.org/pypi/ipgetter2

.. image:: https://travis-ci.org/starofrainnight/ipgetter2.svg?branch=master
    :target: https://travis-ci.org/starofrainnight/ipgetter2

.. image:: https://ci.appveyor.com/api/projects/status/github/starofrainnight/ipgetter2?svg=true
    :target: https://ci.appveyor.com/project/starofrainnight/ipgetter2

Utility to fetch your external IP address.

This module is designed to fetch your external IP address from the internet.

It is used mostly when behind a NAT.

It picks your IP randomly from a server list to minimize request overhead on a single server

NOTICE: This library is try to act as a replacement of the **ipgetter** library, because that library has disappeared on pypi.org and github.

* License: Apache-2.0
* Documentation: https://ipgetter2.readthedocs.io.

Why there another ipgetter library?
-----------------------------------------

I found ipgetter disappeared at night of 2019-05-11. I don't know precisely when it's disappeared, and don't know what's going on.

So I write this library with same API interface for my projects that depends on it as a replacement, hope it will help people that ran into  the same situation.

Features
---------

* Correctly detect webpage encoding by chardet
* Control the timeout by library `requests` not by signal alarm (Alarm signal will cause problems)
* Smart server fetch algorithm, the get() method will fetch at least 2 IP with the same value in 3 random servers (return the only one valid IP without checking if there have only one server responsed)
* Support IPv6 either (Return both values if the server provided two of them)

Usage
---------

* ipgetter2 usage

::

    >>> from ipgetter2 import IPGetter
    >>> getter = IPGetter()
    >>> getter.get()
    {v4:"8.8.8.8", v6:"::"}
    >>> getter.get_from("http://checkip.dyndns.org/plain")
    {v4:"8.8.8.8", v6:"::"}
    >>> getter.test()
    Numbers of Servers : 46
    [1/46] Testing : http://ip.dnsexit.com
    [2/46] Testing : http://ifconfig.me/ip
    [3/46] Testing : http://ipecho.net/plain
    ......
    [45/46] Testing : http://httpbin.org/ip
    [46/46] Testing : https://api.myip.com
    8 server failed : ['http://checkip.dyndns.org/plain', 'http://www.canyouseeme.org/', 'http://whatsmyip.net/', 'http://www.ip-adress.com/', 'http://ip-lookup.net/', 'https://check.torproject.org/', 'https://www.privateinternetaccess.com/pages/whats-my-ip/', 'http://myexternalip.com/']
    {IPAddress(v4="117.117.117.117", v6="::"): 26, IPAddress(v4="0.0.0.0", v6="::"): 11, IPAddress(v4="117.117.117.116", v6="::"): 1}
    IP's : {v4:"117.117.117.117", v6:"::"} = 26 ocurrencies

* Emulated API interface of ipgetter library

::

    >>> from ipgetter2 import ipgetter1 as ipgetter
    >>> myip = ipgetter.myip()
    >>> myip
    '8.8.8.8'
    >>> ipgetter.IPgetter().test()
    Number of servers: 47
    IP's :
    8.8.8.8 = 47 ocurrencies

Credits
---------

This package was created with Cookiecutter_ and the `PyPackageTemplate`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`PyPackageTemplate`: https://github.com/starofrainnight/rtpl-pypackage

