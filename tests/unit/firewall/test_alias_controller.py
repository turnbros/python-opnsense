import json
import os.path
import unittest
from unittest.mock import call, Mock, MagicMock

from opnsense_api import Opnsense
from opnsense_api.firewall.alias_controller import Alias, FirewallAliasController, AliasType
from opnsense_api.util import ProtocolType
from opnsense_api.util.exceptions import FailedToDeleteException, ItemNotFoundException, FailedToAddItemException, \
    InvalidItemException, FailedToSetItemException

parent_dir = os.path.dirname(os.path.abspath(__file__))


class TestAlias(unittest.TestCase):
    def test_init(self):
        alias_item = Alias(name="Name", type=AliasType.HOST)
        self.assertEqual(alias_item.uuid, None)
        self.assertEqual(alias_item.name, "Name")
        self.assertEqual(alias_item.type, AliasType.HOST)
        self.assertEqual(alias_item.description, "")
        self.assertEqual(alias_item.updatefreq, None)
        self.assertEqual(alias_item.counters, None)
        self.assertEqual(alias_item.proto, None)
        self.assertEqual(alias_item.content, None)
        self.assertEqual(alias_item.enabled, True)
        self.assertListEqual(alias_item.categories_uuids, [])

        alias_item = Alias(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Name",
            type=AliasType.HOST,
            description="tests description",
            updatefreq="2",
            counters="5",
            proto=ProtocolType.IPV6,
            content=["0::0"],
            enabled=False,
            categories_uuids=["11111111-1111-1111-1111-11111111111"]
        )
        self.assertEqual(alias_item.uuid, "11111111-1111-1111-1111-11111111111")
        self.assertEqual(alias_item.name, "Name")
        self.assertEqual(alias_item.type, AliasType.HOST)
        self.assertEqual(alias_item.description, "tests description")
        self.assertEqual(alias_item.updatefreq, "2")
        self.assertEqual(alias_item.counters, "5")
        self.assertEqual(alias_item.proto, ProtocolType.IPV6)
        self.assertListEqual(alias_item.content, ["0::0"])
        self.assertEqual(alias_item.enabled, False)
        self.assertListEqual(alias_item.categories_uuids, ["11111111-1111-1111-1111-11111111111"])


class TestFirewallAliasController(unittest.TestCase):
    alias_controller: FirewallAliasController
    apply_call = call('POST', 'firewall/alias/reconfigure', body=None)

    @classmethod
    def setUpClass(cls) -> None:
        cls.alias_controller = FirewallAliasController(device=Mock(spec=Opnsense))

    def test_init(self):
        self.assertEqual(TestFirewallAliasController.alias_controller._module, 'firewall')
        self.assertEqual(TestFirewallAliasController.alias_controller._controller, 'alias')

    def test_opnsense_item_class(self):
        self.assertEqual(TestFirewallAliasController.alias_controller._opnsense_item_class, Alias)

    def test_list(self):
        with open(os.path.join(parent_dir, 'json_src', 'alias_list_response.json')) as f:
            list_response = json.loads(f.read())

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            return_value=list_response)
        aliases = TestFirewallAliasController.alias_controller.list()

        TestFirewallAliasController.alias_controller._device._authenticated_request.assert_called_once_with(
            'POST', 'firewall/alias/searchItem',
            body=None)

        self.assertListEqual(aliases, [
            Alias(
                uuid="bogons",
                enabled=True,
                name="bogons",
                description="bogon networks (internal)",
                type=AliasType.EXTERNAL,
                content=[""],
                categories_uuids=[]
            ), Alias(
                uuid="bogonsv6",
                enabled=True,
                name="bogonsv6",
                description="bogon networks IPv6 (internal)",
                type=AliasType.EXTERNAL,
                content=[""],
                categories_uuids=[]
            ), Alias(
                uuid="a3a1d19e-be99-43de-99de-b2cd4947359c",
                enabled=True,
                name="net_alias",
                description="",
                type=AliasType.NETWORK,
                content=["192.168.1.0/24"],
                categories_uuids=[]
            ), Alias(
                uuid="87be7a20-d3b8-481d-adfa-c3eb35ce0d24",
                enabled=True,
                name="new_alias",
                description="",
                type=AliasType.PORT,
                content=["80", "443"],
                categories_uuids=[]
            ), Alias(
                uuid="e0a70cde-cfbc-4ce0-bc57-6d85149ba696",
                enabled=True,
                name="URL_Table",
                description="",
                type=AliasType.URL_TABLE,
                content=["9.9.9.9", "10.10.10.10", "1.1.1.1"],
                categories_uuids=[]
            ), Alias(
                uuid="sshlockout",
                enabled=True,
                name="sshlockout",
                description="abuse lockout table (internal)",
                type=AliasType.EXTERNAL,
                content=[""],
                categories_uuids=[]
            ), Alias(
                uuid="__LAN_GROUP_network",
                enabled=True,
                name="__LAN_GROUP_network",
                description="LAN_GROUP net",
                type=AliasType.INTERNAL,
                content=[""],
                categories_uuids=[]
            )
        ])

    def test_get(self):
        with open(os.path.join(parent_dir, 'json_src', 'alias_get_response.json')) as f:
            get_response = json.loads(f.read())

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            return_value=get_response)
        alias = TestFirewallAliasController.alias_controller.get("11111111-1111-1111-1111-11111111111")

        TestFirewallAliasController.alias_controller._device._authenticated_request.assert_called_once_with(
            'GET',
            "firewall/alias/getItem/11111111-1111-1111-1111-11111111111",
            body=None)

        self.assertEqual(alias, Alias(
            uuid="11111111-1111-1111-1111-11111111111",
            name="tests",
            enabled=True,
            type=AliasType.DYNAMIC_IPV6_HOST,
            counters="0",
            updatefreq="",
            content=[""],
            categories_uuids=["521b4779-a493-4790-b1a2-92738f4c85c0"]
        )
                         )

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(return_value={})
        with self.assertRaises(ItemNotFoundException):
            TestFirewallAliasController.alias_controller.get("11111111-1111-1111-1111-11111111111")

    def test_delete(self):
        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            side_effect=[{'result': 'deleted'}, {'status': 'ok'}])

        alias = Alias(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Name",
            type=AliasType.HOST
        )

        TestFirewallAliasController.alias_controller.delete(alias)

        TestFirewallAliasController.alias_controller._device._authenticated_request.assert_has_calls([
            call('POST',
                 'firewall/alias/delItem/11111111-1111-1111-1111-11111111111',
                 body=None),
            TestFirewallAliasController.apply_call
        ])

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'not found'}
        )
        with self.assertRaises(FailedToDeleteException):
            TestFirewallAliasController.alias_controller.delete(alias)

    def test_add(self):
        with open(os.path.join(parent_dir, 'json_src', 'alias_add_request.json')) as f:
            add_request = json.loads(f.read())

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            side_effect=[{'result': 'saved', 'uuid': '11111111-1111-1111-1111-11111111111'}, {'status': 'ok'}]
        )

        alias = Alias(
            name="Name",
            type=AliasType.PORT,
            content=["80", "443"]
        )
        TestFirewallAliasController.alias_controller.add(alias)

        TestFirewallAliasController.alias_controller._device._authenticated_request.assert_has_calls([
            call('POST',
                 'firewall/alias/addItem',
                 body=add_request),
            TestFirewallAliasController.apply_call
        ])
        self.assertEqual('11111111-1111-1111-1111-11111111111', alias.uuid)

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'failed'}
        )

        with self.assertRaises(FailedToAddItemException):
            TestFirewallAliasController.alias_controller.add(alias)

    def test_set(self):
        with open(os.path.join(parent_dir, 'json_src', 'alias_get_response.json')) as f:
            get_response = json.loads(f.read())

        with open(os.path.join(parent_dir, 'json_src', 'alias_set_request.json')) as f:
            set_request = json.loads(f.read())

        alias = Alias(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Name",
            type=AliasType.PORT,
            content=["80", "443"]
        )

        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            side_effect=[get_response, {'result': 'saved'}, {'status': 'ok'}])

        TestFirewallAliasController.alias_controller.set(alias)
        TestFirewallAliasController.alias_controller._device._authenticated_request.assert_has_calls([
            call('GET',
                 'firewall/alias/getItem/11111111-1111-1111-1111-11111111111',
                 body=None),
            call('POST',
                 'firewall/alias/setItem/11111111-1111-1111-1111-11111111111',
                 body=set_request),
            TestFirewallAliasController.apply_call
        ])

        # missing uuid
        alias.uuid = ""
        with self.assertRaises(InvalidItemException):
            TestFirewallAliasController.alias_controller.set(alias)

        # failed response
        alias.uuid = "11111111-1111-1111-1111-11111111111"
        TestFirewallAliasController.alias_controller._device._authenticated_request = MagicMock(
            side_effect=[get_response, {'result': 'failed'}])

        with self.assertRaises(FailedToSetItemException):
            TestFirewallAliasController.alias_controller.set(alias)


if __name__ == '__main__':
    unittest.main()
