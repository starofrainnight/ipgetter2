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

