import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from opnsense_api import Opnsense

domain_ip_override = os.getenv("TEST_DOMAIN_IP")
test_alias = os.getenv("TEST_ALIAS")
test_domain = os.getenv("TEST_DOMAIN")
opnsense = Opnsense()


def test_route_controller():
    print(opnsense.routing.route_controller.list())


test_route_controller()
