from typing import List
import collections
import dns.resolver
import os


def compare(list_x, list_y):
    return collections.Counter(list_x) == collections.Counter(list_y)


def query_opnsense_device_dns(record_name: str, record_type: str = "NS") -> List[str]:
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [os.getenv("OPN_API_HOST")]
    answer = resolver.resolve(record_name, record_type)

    records = []
    for record in answer:
        records.append(record.to_text())
    return records
