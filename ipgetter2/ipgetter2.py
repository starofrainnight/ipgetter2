# -*- coding: utf-8 -*-

"""Main module."""

import re
import chardet
import requests
import unicodedata
import random
from ipaddress import ip_address, IPv4Address, IPv6Address, AddressValueError
from typing import List

DEFAULT_URLS = [
    "http://ip.dnsexit.com",
    "http://ifconfig.me/ip",
    "http://ipecho.net/plain",
    "http://checkip.dyndns.org/plain",
    "http://ipogre.com/linux.php",
    "http://whatismyipaddress.com/",
    "http://ip.my-proxy.com/",
    "http://websiteipaddress.com/WhatIsMyIp",
    "http://getmyipaddress.org/",
    "http://showmyipaddress.com/",
    "http://www.my-ip-address.net/",
    "http://myexternalip.com/raw",
    "http://www.canyouseeme.org/",
    "http://www.trackip.net/",
    "http://myip.dnsdynamic.org/",
    "http://icanhazip.com/",
    "http://www.iplocation.net/",
    "http://www.howtofindmyipaddress.com/",
    "http://www.ipchicken.com/",
    "http://whatsmyip.net/",
    "http://www.ip-adress.com/",
    "http://checkmyip.com/",
    "http://www.tracemyip.org/",
    "http://checkmyip.net/",
    "http://www.lawrencegoetz.com/programs/ipinfo/",
    "http://www.findmyip.co/",
    "http://ip-lookup.net/",
    "http://www.dslreports.com/whois",
    "http://www.mon-ip.com/en/my-ip/",
    "http://www.myip.ru",
    "http://ipgoat.com/",
    "http://www.myipnumber.com/my-ip-address.asp",
    "http://www.whatsmyipaddress.net/",
    "http://formyip.com/",
    "https://check.torproject.org/",
    "http://www.displaymyip.com/",
    "http://www.bobborst.com/tools/whatsmyip/",
    "http://www.geoiptool.com/",
    "https://www.whatsmydns.net/whats-my-ip-address.html",
    "https://www.privateinternetaccess.com/pages/whats-my-ip/",
    "http://checkip.dyndns.com/",
    "http://myexternalip.com/",
    "http://www.ip-adress.eu/",
    "http://www.infosniper.net/",
    "http://wtfismyip.com/",
    "http://ipinfo.io/",
    "http://httpbin.org/ip",
]
PATTERN_IPV4_SEG = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
PATTERN_IPV4 = ".".join([PATTERN_IPV4_SEG] * 4)

# References to : https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
PATTERN_IPV6_SEG = r"[0-9a-fA-F]{1,4}"
PATTERN_IPV6 = (
    r"("
    r"({ipv6_seg}:){{7,7}}{ipv6_seg}|"  # 1:2:3:4:5:6:7:8
    r"({ipv6_seg}:){{1,7}}:|"  # 1::                                 1:2:3:4:5:6:7::
    r"({ipv6_seg}:){{1,6}}:{ipv6_seg}|"  # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
    r"({ipv6_seg}:){{1,5}}(:{ipv6_seg}){{1,2}}|"  # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
    r"({ipv6_seg}:){{1,4}}(:{ipv6_seg}){{1,3}}|"  # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
    r"({ipv6_seg}:){{1,3}}(:{ipv6_seg}){{1,4}}|"  # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
    r"({ipv6_seg}:){{1,2}}(:{ipv6_seg}){{1,5}}|"  # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
    r"{ipv6_seg}:((:{ipv6_seg}){{1,6}})|"  # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
    r":((:{ipv6_seg}){{1,7}}|:)|"  # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
    r"fe80:(:{ipv6_seg}){{0,4}}%[0-9a-zA-Z]{{1,}}|"  # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
    r"::(ffff(:0{{1,4}}){{0,1}}:){{0,1}}{ipv4}|"  # ::255.255.255.255  ::ffff:255.255.255.255  ::ffff:0:255.255.255.255 (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
    r"({ipv6_seg}:){{1,4}}:{ipv4}"  # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
    r")"
).format(ipv6_seg=PATTERN_IPV6_SEG, ipv4=PATTERN_IPV4)


class AddressNotFoundError(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IPAddress(object):
    """Use for store our external v4 and v6 addresses
    """

    DEFAULT_IPV4_ADDRESS = IPv4Address("0.0.0.0")
    DEFAULT_IPV6_ADDRESS = IPv6Address("::")

    def __init__(self, v4=None, v6=None):
        if v4:
            self._v4 = v4
        else:
            self._v4 = self.DEFAULT_IPV4_ADDRESS

        if v6:
            self._v6 = v6
        else:
            self._v6 = self.DEFAULT_IPV6_ADDRESS

    @property
    def v4(self):
        return self._v4

    @property
    def v6(self):
        return self._v6

    def is_valid(self):
        return bool(self.v4 or self.v6)

    def __repr__(self):
        return '%s(v4="%s", v6="%s")' % (
            self.__class__.__name__,
            self.v4,
            self.v6,
        )

    def __str__(self):
        return '{v4:"%s", v6:"%s"}' % (self.v4, self.v6)

    def __eq__(self, other):
        return (self.v4 == other.v4) and (self.v6 == other.v6)


class IPGetter(object):
    def __init__(self, urls: List[str] = DEFAULT_URLS):
        self._urls = urls
        self._timeout = 30

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def get_from(self, url: str):
        """Gets your IP from a specific server
        """

        user_agent = " ".join(
            [
                "Mozilla/5.0",
                "(Windows NT 10.0; Win64; x64)",
                "AppleWebKit/537.36",
                "(KHTML, like Gecko)",
                "Chrome/70.0.3538.77",
                "Safari/537.36",
            ]
        )
        # Request raise timeout on connection or read operation after 30s if not
        # received any data
        params = {
            "url": url,
            "verify": False,
            "headers": {"user-agent": user_agent},
        }

        if self.timeout:
            params["timeout"] = self.timeout
        r = requests.get(**params)

        # Guess context with correct encoding
        guessed = chardet.detect(r.content)
        # Fixed Chinese encoding by latest standard
        if guessed["encoding"].upper() == "GB2312":
            guessed["encoding"] = "GB18030"

        text = r.content.decode(guessed["encoding"])
        # Normalize unicode text
        text = unicodedata.normalize("NFKC", text)

        # Analyse the ip patterns
        v6 = None
        matched = re.search(PATTERN_IPV6, text)
        if matched is not None:
            try:
                v6 = ip_address(matched.group(0))
            except AddressValueError:
                pass

        v4 = None
        matched = re.search(PATTERN_IPV4, text)
        if matched is not None:
            try:
                v4 = ip_address(matched.group(0))
            except AddressValueError:
                pass

        if v4 and v6:
            raise AddressNotFoundError(
                "Not found any valid IP address at server : %s" % url
            )

        return IPAddress(v4, v6)

    def get(self):
        """Get the external IP address from servers.

        This method will pick 3 random server from list and then request IP
        address from them. If there have 2 servers have the same IP address,
        we will return it, otherwise raise an exception"""

        # 2 for checking, 1 more for backup if there have any server do not
        # repsond
        pick_count = 3
        if len(self._urls) < pick_count:
            pick_count = len(self._urls)

        urls = random.choices(self._urls, k=pick_count)
        addresses = []
        for url in urls:
            try:
                address = self.get_from(url)
            except (AddressNotFoundError, ConnectionError) as e:
                addresses.append((None, url, e))
                continue

            for check_address, check_url, _ in addresses:
                if address and (
                    address.v4 == check_address.v4
                    or address.v6 == check_address.v6
                ):
                    return address

            addresses.append((address, url, None))

        # If there have only one valid address in list, we should return it
        if (len(urls) <= 1) and (len(addresses) == 1):
            address, url, _ = addresses[0]
            if address is not None:
                return address

        raise AddressNotFoundError(
            "Can't found any valid IP address : %s" % addresses
        )

