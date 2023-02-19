from typing import List
from typing import Union

from deprecation import deprecated

from opnsense_api.util.parse import parse_firewall_filter_rule, parse_firewall_filter_search_results
from opnsense_api.util.validate import validate_add_filter_rule


class Filter(object):

    def __init__(self, device):
        self.device = device

    def apply_changes(self):
        response = self.device._authenticated_request("POST", f"firewall/filter/apply")
        if response["status"] == "error":
            raise Exception(f"Failed to apply changes. Reason {response}")

    def get(self, uuid: str = None) -> Union[dict, None]:
        """
        Returns a specific filter rule
        :param uuid: The UUID of the filter rule to get
        :type uuid: str
        :return: A parsed filter rule
        :rtype: dict
        """
        return self.get_rule(uuid)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use get instead")
    def get_rule(self, uuid: str = None) -> Union[dict, None]:
        """
        Returns a specific filter rule
        :param uuid: The UUID of the filter rule to get
        :type uuid: str
        :return: A parsed filter rule
        :rtype: dict
        """
        query_results = self.device._authenticated_request("GET", f"firewall/filter/getRule/{uuid}")
        if 'rule' in query_results:
            return parse_firewall_filter_rule(uuid, query_results['rule'])
        return None

    def list(self) -> list:
        """
        Returns a list of filter rules that exist on the device
        :return: A brief list of parsed filter rules
        :rtype: list
        """
        return self.list_rules()

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use list instead")
    def list_rules(self) -> list:
        """
        Returns a list of filter rules that exist on the device
        :return: A brief list of parsed filter rules
        :rtype: list
        """
        query_results = self.device._authenticated_request("GET", f"firewall/filter/searchRule")
        if 'rows' in query_results:
            return parse_firewall_filter_search_results(query_results['rows'])
        return []

    def match_rule_by_attributes(self, **kwargs) -> Union[dict, None]:
        """
        Matches and returns firewall filter rules. The match is based on attribute values provided as kwargs.
        :param kwargs: { "description": "a filter rule description", "log": True }
        :return: A list of matched firewall filter rules
        :rtype: dict
        """
        return self.match_rule_by_attributes(**kwargs)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use match_by_attribute instead")
    def match_rule_by_attributes(self, **kwargs) -> List[dict | None]:
        """
        Matches and returns firewall filter rules. The match is based on attribute values provided as kwargs.
        :param kwargs: { "description": "a filter rule description", "log": True }
        :return: A list of matched firewall filter rules
        :rtype: dict
        """
        all_rules = self.list_rules()
        matched_rules = []
        for rule in all_rules:
            rule_uuid = rule.get("uuid")
            rule = self.get_rule(rule_uuid)
            rule["uuid"] = rule_uuid
            rule_matched = True
            for key in kwargs.keys():
                if rule.get(key) != kwargs.get(key):
                    rule_matched = False
                    break
            if rule_matched:
                matched_rules.append(rule)
        return matched_rules

    def add(self,
            direction: str = "in",
            interface: List[str] = ["lan"],
            source_net: str = "any",
            destination_net: str = "any",
            action: str = 'pass',
            protocol: str = "any",
            source_port: int = 0,
            destination_port: int = 0,
            gateway: Union[str, None] = None,
            source_not: bool = False,
            destination_not: bool = False,
            sequence: int = 1,
            description: str = "",
            enabled: bool = False,
            quick: bool = True,
            log: bool = False,
            ipprotocol: str = "inet"):
        """
        Adds a new firewall filter rule.
        Note: This will function does not apply the change. A separate call is needed.
        :param action:
        :param direction:
        :param interface:
        :param protocol:
        :param source_net:
        :param source_port:
        :param destination_net:
        :param destination_port:
        :param gateway:
        :param source_not:
        :param destination_not:
        :param sequence:
        :param description:
        :param enabled:
        :param quick:
        :param log:
        :param ipprotocol:
        :return: A parsed filter rule
        :rtype: dict
        """
        return self.add_rule(
            direction=direction,
            interface=interface,
            source_net=source_net,
            destination_net=destination_net,
            action=action,
            protocol=protocol,
            source_port=source_port,
            destination_port=destination_port,
            gateway=gateway,
            source_not=source_not,
            destination_not=destination_not,
            sequence=sequence,
            description=description,
            enabled=enabled,
            quick=quick,
            log=log,
            ipprotocol=ipprotocol
        )

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use add instead")
    def add_rule(self,
                 direction: str = "in",
                 interface: List[str] = ["lan"],
                 source_net: str = "any",
                 destination_net: str = "any",
                 action: str = 'pass',
                 protocol: str = "any",
                 source_port: int = 0,
                 destination_port: int = 0,
                 gateway: Union[str, None] = None,
                 source_not: bool = False,
                 destination_not: bool = False,
                 sequence: int = 1,
                 description: str = "",
                 enabled: bool = False,
                 quick: bool = True,
                 log: bool = False,
                 ipprotocol: str = "inet"):
        """
        Adds a new firewall filter rule.
        Note: This will function does not apply the change. A separate call is needed.
        :param action:
        :param direction:
        :param interface:
        :param protocol:
        :param source_net:
        :param source_port:
        :param destination_net:
        :param destination_port:
        :param gateway:
        :param source_not:
        :param destination_not:
        :param sequence:
        :param description:
        :param enabled:
        :param quick:
        :param log:
        :param ipprotocol:
        :return: A parsed filter rule
        :rtype: dict
        """

        # This will raise an exception if a bad input is provided.
        validate_add_filter_rule(action, direction, ipprotocol, protocol)

        if gateway is None:
            gateway = ""

        if source_port == 0:
            source_port = ""
        else:
            source_port = str(source_port)

        if destination_port == 0:
            destination_port = ""
        else:
            destination_port = str(destination_port)

        rule_body = {
            "sequence": str(sequence),
            "description": description,
            "enabled": str(int(enabled)),
            "quick": str(int(quick)),
            "log": str(int(log)),
            "source_net": source_net,
            "source_not": str(int(source_not)),
            "source_port": source_port,
            "destination_net": destination_net,
            "destination_not": str(int(destination_not)),
            "destination_port": destination_port,
            "action": action,
            "interface": ",".join(interface),
            "direction": direction,
            "ipprotocol": ipprotocol,
            "protocol": protocol,
            "gateway": gateway
        }

        response = self.device._authenticated_request("POST", "firewall/filter/addRule", body={"rule": rule_body})
        if response['result'] == "saved":
            self.apply_changes()
            return self.get_rule(response['uuid'])
        else:
            raise Exception(f"Failed to add filter rule. Reason: {response}")

    def set(self,
            uuid: str,
            action: Union[str, None] = None,
            direction: Union[str, None] = None,
            interface: Union[List[str], None] = None,
            protocol: Union[str, None] = None,
            source_net: Union[str, None] = None,
            source_port: Union[int, None] = None,
            destination_net: Union[str, None] = None,
            destination_port: Union[int, None] = None,
            gateway: Union[str, None] = None,
            source_not: Union[bool, None] = None,
            destination_not: Union[bool, None] = None,
            sequence: Union[int, None] = None,
            description: Union[str, None] = None,
            enabled: Union[bool, None] = None,
            quick: Union[bool, None] = None,
            log: Union[bool, None] = None,
            ipprotocol: Union[str, None] = None) -> dict:
        return self.set_rule(
            uuid=uuid,
            action=action,
            direction=direction,
            interface=interface,
            protocol=protocol,
            source_net=source_net,
            source_port=source_port,
            destination_net=destination_net,
            destination_port=destination_port,
            gateway=gateway,
            source_not=source_not,
            destination_not=destination_not,
            sequence=sequence,
            description=description,
            enabled=enabled,
            quick=quick,
            log=log,
            ipprotocol=ipprotocol
        )

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use set instead")
    def set_rule(self,
                 uuid: str,
                 action: Union[str, None] = None,
                 direction: Union[str, None] = None,
                 interface: Union[List[str], None] = None,
                 protocol: Union[str, None] = None,
                 source_net: Union[str, None] = None,
                 source_port: Union[int, None] = None,
                 destination_net: Union[str, None] = None,
                 destination_port: Union[int, None] = None,
                 gateway: Union[str, None] = None,
                 source_not: Union[bool, None] = None,
                 destination_not: Union[bool, None] = None,
                 sequence: Union[int, None] = None,
                 description: Union[str, None] = None,
                 enabled: Union[bool, None] = None,
                 quick: Union[bool, None] = None,
                 log: Union[bool, None] = None,
                 ipprotocol: Union[str, None] = None) -> dict:
        """
        Update one or more attributes of a firewall filter rule.
        Only values require updating need to be specified.
        :param uuid:
        :param action:
        :param direction:
        :param interface:
        :param protocol:
        :param source_net:
        :param source_port:
        :param destination_net:
        :param destination_port:
        :param gateway:
        :param source_not:
        :param destination_not:
        :param sequence:
        :param description:
        :param enabled:
        :param quick:
        :param log:
        :param ipprotocol:
        :return: A parsed filter rule
        :rtype: dict
        """

        existing_rule = self.get_rule(uuid)
        if existing_rule is None:
            raise Exception(f"Firewall rule with UUID {uuid} not found")

        if action is None: action = existing_rule.get("action")
        if direction is None: direction = existing_rule.get("direction")
        if interface is None: interface = existing_rule.get("interface")
        if protocol is None: protocol = existing_rule.get("protocol")
        if source_net is None: source_net = existing_rule.get("source_net")
        if source_port is None: source_port = existing_rule.get("source_port")
        if destination_net is None: destination_net = existing_rule.get("destination_net")
        if destination_port is None: destination_port = existing_rule.get("destination_port")
        if gateway is None: gateway = existing_rule.get("gateway")
        if source_not is None: source_not = existing_rule.get("source_not")
        if destination_not is None: destination_not = existing_rule.get("destination_not")
        if sequence is None: sequence = existing_rule.get("sequence")
        if description is None: description = existing_rule.get("description")
        if enabled is None: enabled = existing_rule.get("enabled")
        if quick is None: quick = existing_rule.get("quick")
        if log is None: log = existing_rule.get("log")
        if ipprotocol is None: ipprotocol = existing_rule.get("ipprotocol")

        # This will raise an exception if a bad input is provided.
        validate_add_filter_rule(action, direction, ipprotocol, protocol)

        if gateway is None: gateway = ""

        if source_port == 0:
            source_port = ""
        else:
            source_port = str(source_port)

        if destination_port == 0:
            destination_port = ""
        else:
            destination_port = str(destination_port)

        rule_body = {
            "sequence": str(sequence),
            "description": description,
            "enabled": str(int(enabled)),
            "quick": str(int(quick)),
            "log": str(int(log)),
            "source_net": source_net,
            "source_not": str(int(source_not)),
            "source_port": source_port,
            "destination_net": destination_net,
            "destination_not": str(int(destination_not)),
            "destination_port": destination_port,
            "action": action,
            "interface": ",".join(interface),
            "direction": direction,
            "ipprotocol": ipprotocol,
            "protocol": protocol,
            "gateway": gateway
        }

        response = self.device._authenticated_request("POST", f"firewall/filter/setRule/{uuid}",
                                                      body={"rule": rule_body})
        if response['result'] == 'saved':
            self.apply_changes()
            return self.get_rule(uuid)
        else:
            raise Exception(f"Failed to update filter rule with uuid {uuid}. Reason: {response}")

    def toggle(self, uuid: str = None) -> dict:
        """
            Toggles the enabled state of a filter rule.
            :param uuid: The UUID of the filter rule to toggle
            :type uuid: str
            :return: A parsed filter rule
            :rtype: dict
            """
        return self.toggle_rule(uuid)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use toggle instead")
    def toggle_rule(self, uuid: str = None) -> dict:
        """
        Toggles the enabled state of a filter rule.
        :param uuid: The UUID of the filter rule to toggle
        :type uuid: str
        :return: A parsed filter rule
        :rtype: dict
        """
        response = self.device._authenticated_request("POST", f"firewall/filter/toggleRule/{uuid}")
        if response["changed"]:
            self.apply_changes()
            return self.get_rule(uuid)
        raise Exception(f"Failed to toggle filter rule. Reason: {response}")

    def delete(self, uuid: str = None) -> bool:
        return self.delete_rule(uuid)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use delete instead")
    def delete_rule(self, uuid: str = None) -> bool:
        """
        Deletes a rule. Returns a bool or throws an exception since we don't really care about the UUID once it's gone.
        :param uuid: The UUID of the filter rule to delete
        :type uuid: str
        :return: A bool that indicates operation result
        :rtype: bool
        """
        query_results = self.device._authenticated_request("POST", f"firewall/filter/delRule/{uuid}")
        if query_results['result'] == "deleted":
            self.apply_changes()
            return True
        raise Exception(f"Failed to delete filter rule with UUID {uuid} with reason: {query_results['result']}  ")

    def add_or_se(self,
                  uuid: str = None,
                  action: Union[str, None] = None,
                  direction: Union[str, None] = None,
                  interface: Union[List[str], None] = None,
                  protocol: Union[str, None] = None,
                  source_net: Union[str, None] = None,
                  source_port: Union[int, None] = None,
                  destination_net: Union[str, None] = None,
                  destination_port: Union[int, None] = None,
                  gateway: Union[str, None] = None,
                  source_not: Union[bool, None] = None,
                  destination_not: Union[bool, None] = None,
                  sequence: Union[int, None] = None,
                  description: Union[str, None] = None,
                  enabled: Union[bool, None] = None,
                  quick: Union[bool, None] = None,
                  log: Union[bool, None] = None,
                  ipprotocol: Union[str, None] = None) -> dict:
        return self.add_or_set_rule(
            uuid=uuid,
            action=action,
            direction=direction,
            interface=interface,
            protocol=protocol,
            source_net=source_net,
            source_port=source_port,
            destination_net=destination_net,
            destination_port=destination_port,
            gateway=gateway,
            source_not=source_not,
            destination_not=destination_not,
            sequence=sequence,
            description=description,
            enabled=enabled,
            quick=quick,
            log=log,
            ipprotocol=ipprotocol
        )

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use add_or_set instead")
    def add_or_set_rule(self,
                        uuid: str = None,
                        action: Union[str, None] = None,
                        direction: Union[str, None] = None,
                        interface: Union[List[str], None] = None,
                        protocol: Union[str, None] = None,
                        source_net: Union[str, None] = None,
                        source_port: Union[int, None] = None,
                        destination_net: Union[str, None] = None,
                        destination_port: Union[int, None] = None,
                        gateway: Union[str, None] = None,
                        source_not: Union[bool, None] = None,
                        destination_not: Union[bool, None] = None,
                        sequence: Union[int, None] = None,
                        description: Union[str, None] = None,
                        enabled: Union[bool, None] = None,
                        quick: Union[bool, None] = None,
                        log: Union[bool, None] = None,
                        ipprotocol: Union[str, None] = None) -> dict:
        if uuid is None:
            filter_rule = self.add_rule()
        else:
            filter_rule = self.get_rule(uuid)

        return self.set_rule(filter_rule["uuid"],
                             action,
                             direction,
                             interface,
                             protocol,
                             source_net,
                             source_port,
                             destination_net,
                             destination_port,
                             gateway,
                             source_not,
                             destination_not,
                             sequence,
                             description,
                             enabled,
                             quick,
                             log,
                             ipprotocol)
