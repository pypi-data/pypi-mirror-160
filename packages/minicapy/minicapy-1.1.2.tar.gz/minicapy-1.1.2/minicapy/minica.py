from ctypes import POINTER, c_char_p, c_int, cdll
from enum import Enum
from ipaddress import ip_address as validate_ip
from pathlib import Path

minica = cdll.LoadLibrary(str(Path(__file__).parent / "minica.dll"))

_generate_certificate = minica.generateCertificate
_generate_certificate.argtypes = [c_char_p]

_generate_ip_certificate = minica.generateIPCertificate
_generate_ip_certificate.argtypes = [c_char_p]


def _to_c_str_array(strs: list[str]):
    ptr = (c_char_p * (len(strs)))()
    ptr[:] = [s.encode() for s in strs]
    return ptr


_generate_complex_certificate = minica.generateComplexCertificate
_generate_complex_certificate.argtypes = [
    POINTER(c_char_p),
    c_int,
    POINTER(c_char_p),
    c_int,
]


class DnsType(Enum):
    DOMAIN = 1
    IP_ADDRESS = 2


class NotEnoughPartsException(Exception):
    def __init__(
        self, min_parts: int, domain: str, kind: DnsType = DnsType.DOMAIN
    ) -> None:
        self.min_parts = min_parts
        super().__init__(
            f"This function needs {'a domain' if kind == DnsType.DOMAIN else 'an IP address'} with at least {min_parts} parts, got {domain.split('.')}"
        )


class InvalidIpException(Exception):
    pass


def create_domain_cert(domain: str) -> int:
    """Create an ssl certificate for the given domain.
    Return code meanings:
        0 -> success
        1 -> couldn't create CA files minica-key.pem and minica.pem
        2 -> couldn't create certificate, likely already exists"""
    if len(domain.split(".")) < 2:
        raise NotEnoughPartsException(2, domain)

    return _generate_certificate(c_char_p(domain.encode("utf-8")))


def create_ip_cert(ip_address: str) -> int:
    """Create an ssl certificate for an ip address.
    Return code meanings:
        0 -> success
        1 -> couldn't create CA files minica-key.pem and minica.pem
        2 -> couldn't create certificate, likely already exists"""
    validate_ip(ip_address)
    return _generate_ip_certificate(c_char_p(ip_address.encode("utf-8")))


def create_compound_certificate(
    domains: list[str], ip_addresses: list[str] = []
) -> int:
    """Create a single ssl certificate for a list of domains and ip addresses....
    The first domain will be chosen as the certificate name.
    Return code meanings:
        0 -> success
        1 -> couldn't create CA files minica-key.pem and minica.pem
        2 -> couldn't create certificate, likely already exists"""
    return _generate_complex_certificate(
        _to_c_str_array(domains),
        len(domains),
        _to_c_str_array(ip_addresses),
        len(ip_addresses),
    )


class NotAWildcardException(Exception):
    pass


def create_wildcard_certificate(
    wildcard_domain: str, include_base_domain: bool = False
) -> int:
    """Create a wildcard domain certificate. Optionally include the base domain in the certificate.
    Return code meanings:
        0 -> success
        1 -> couldn't create CA files minica-key.pem and minica.pem
        2 -> couldn't create certificate, likely already exists"""
    if wildcard_domain.find("*.") != 0:
        raise NotAWildcardException('The wildcard domain string must start with "*."')

    if len(wildcard_domain.split(".")) < 3:
        # TODO: sanitize tlds
        raise NotEnoughPartsException(3, wildcard_domain)

    domains = [wildcard_domain]
    if include_base_domain:
        base_domain = ".".join(wildcard_domain.split(".")[1:])
        domains.append(base_domain)

    return create_compound_certificate(domains)
