from typing import List
from typing import Union
from opnsense_api.util.validate import validate_add_filter_rule
from opnsense_api.util.parse import parse_firewall_filter_rule, parse_firewall_filter_search_results

class Filter(object):

  def __init__(self, device):
    self.device = device

  def get_rule(self, uuid: str=None) -> Union[dict, None]:
    """
    Returns a specific filter rule
    :param uuid: The UUID of the filter rule to get
    :type uuid: str
    :return: A parsed filter rule
    :rtype: dict
    """
    query_results = self.device.authenticated_request("GET", f"firewall/filter/getRule/{uuid}")
    if 'rule' in query_results:
      return parse_firewall_filter_rule(uuid, query_results['rule'])
    return None


  def list_rules(self) -> list:
    """
    Returns a list of filter rules that exist on the device
    :return: A brief list of parsed filter rules
    :rtype: list
    """
    query_results = self.device.authenticated_request("GET", f"firewall/filter/searchRule")
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
    all_rules = self.list_rules()
    matched_rules = []
    for rule in all_rules:
      for key in kwargs.keys():
        if rule.get(key) != kwargs.get(key):
          return None
      matched_rules.append(rule)
    return matched_rules


  def add_rule(self,
               action: str,
               direction: str,
               interface: List[str],
               protocol: str,
               source_net: str,
               source_port: int,
               destination_net: str,
               destination_port: int,
               gateway: Union[str,None],
               source_not: bool = False,
               destination_not: bool = False,
               sequence: int = 1,
               description: str = "",
               enabled: bool = True,
               quick: bool = True,
               log: bool = True,
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
    :return: {'result': 'saved', 'uuid': 'd244216a-0483-4090-897a-2f2dbd6c7f8d'}
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

    return self.device.authenticated_request("POST", "firewall/filter/addRule", body={"rule": rule_body})


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
    :return: {'result': 'saved'}
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

    if source_port == 0: source_port = ""
    else: source_port = str(source_port)

    if destination_port == 0: destination_port = ""
    else: destination_port = str(destination_port)

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

    return self.device.authenticated_request("POST", f"firewall/filter/setRule/{uuid}", body={"rule": rule_body})


  def toggle_rule(self, uuid: str=None, enabled: Union[bool,None]=None) -> dict:
    """
    Toggles the enabled state of a filter rule. Alternativly, a desired enabled state can be supplied with a bool
    :param uuid: The UUID of the filter rule to toggle
    :param enabled: An optional parameter that if set will become the enabled state of the filter rule
    :type uuid: str
    :type enabled: bool
    :return: {"result": string,"changed": bool}
    :rtype: dict
    """
    if enabled is None:
      enabled = bool(int(self.get_rule(uuid)['enabled']))
    return self.device.authenticated_request("POST", f"firewall/filter/toggleRule/{uuid}?enabled={not enabled}")


  def delete_rule(self, uuid: str=None) -> bool:
    """
    Deletes a rule.
    :param uuid: The UUID of the filter rule to delete
    :type uuid: str
    :return: A bool that indicates operation result
    :rtype: bool
    """
    query_results = self.device.authenticated_request("POST", f"firewall/filter/delRule/{uuid}")
    if query_results['result'] == "deleted":
      return True
    return False
