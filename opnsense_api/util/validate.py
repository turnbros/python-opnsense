def validate_add_filter_rule(action, direction, ipprotocol, protocol) -> bool:
  if action not in ["pass", "block", "reject"]:
    raise ValueError(f"Invalid `action`: {action}, must be `pass`, `block`, or `reject`")

  if direction not in ["in", "out"]:
    raise ValueError(f"Invalid `direction`: {direction}, must be `in` or `out`")

  if ipprotocol not in ["inet","inet6"]:
    raise ValueError(f"Invalid `ipprotocol`: {ipprotocol}, must be `inet` or `inet6`")

  if protocol not in ["any","ICMP","IGMP","GGP","IPENCAP","ST2","TCP","CBT","EGP","IGP","BBN-RCC","NVP","PUP","ARGUS","EMCON","XNET","CHAOS","UDP","MUX","DCN","HMP","PRM","XNS-IDP","TRUNK-1","TRUNK-2","LEAF-1","LEAF-2","RDP","IRTP","ISO-TP4","NETBLT","MFE-NSP","MERIT-INP","DCCP","3PC","IDPR","XTP","DDP","IDPR-CMTP","TP++","IL","IPV6","SDRP","IDRP","RSVP","GRE","DSR","BNA","ESP","AH","I-NLSP","SWIPE","NARP","MOBILE","TLSP","SKIP","IPV6-ICMP","CFTP","SAT-EXPAK","KRYPTOLAN","RVD","IPPC","SAT-MON","VISA","IPCV","CPNX","CPHB","WSN","PVP","BR-SAT-MON","SUN-ND","WB-MON","WB-EXPAK","ISO-IP","VMTP","SECURE-VMTP","VINES","TTP","NSFNET-IGP","DGP","TCF","EIGRP","OSPF","SPRITE-RPC","LARP","MTP","AX.25","IPIP","MICP","SCC-SP","ETHERIP","ENCAP","GMTP","IFMP","PNNI","PIM","ARIS","SCPS","QNX","A/N","IPCOMP","SNP","COMPAQ-PEER","IPX-IN-IP","CARP","PGM","L2TP","DDX","IATP","STP","SRP","UTI","SMP","SM","PTP","ISIS","CRTP","CRUDP","SPS","PIPE","SCTP","FC","RSVP-E2E-IGNORE","UDPLITE","MPLS-IN-IP","MANET","HIP","SHIM6","WESP","ROHC","PFSYNC","DIVERT"]:
    raise ValueError(f"Invalid `protocol`: {protocol}, must be `any`, `ICMP`, `IGMP`, `GGP`, `IPENCAP`, `ST2`, `TCP`, `CBT`, `EGP`, `IGP`, `BBN-RCC`, `NVP`, `PUP`, `ARGUS`, `EMCON`, `XNET`, `CHAOS`, `UDP`, `MUX`, `DCN`, `HMP`, `PRM`, `XNS-IDP`, `TRUNK-1`, `TRUNK-2`, `LEAF-1`, `LEAF-2`, `RDP`, `IRTP`, `ISO-TP4`, `NETBLT`, `MFE-NSP`, `MERIT-INP`, `DCCP`, `3PC`, `IDPR`, `XTP`, `DDP`, `IDPR-CMTP`, `TP++`, `IL`, `IPV6`, `SDRP`, `IDRP`, `RSVP`, `GRE`, `DSR`, `BNA`, `ESP`, `AH`, `I-NLSP`, `SWIPE`, `NARP`, `MOBILE`, `TLSP`, `SKIP`, `IPV6-ICMP`, `CFTP`, `SAT-EXPAK`, `KRYPTOLAN`, `RVD`, `IPPC`, `SAT-MON`, `VISA`, `IPCV`, `CPNX`, `CPHB`, `WSN`, `PVP`, `BR-SAT-MON`, `SUN-ND`, `WB-MON`, `WB-EXPAK`, `ISO-IP`, `VMTP`, `SECURE-VMTP`, `VINES`, `TTP`, `NSFNET-IGP`, `DGP`, `TCF`, `EIGRP`, `OSPF`, `SPRITE-RPC`, `LARP`, `MTP`, `AX.25`, `IPIP`, `MICP`, `SCC-SP`, `ETHERIP`, `ENCAP`, `GMTP`, `IFMP`, `PNNI`, `PIM`, `ARIS`, `SCPS`, `QNX`, `A/N`, `IPCOMP`, `SNP`, `COMPAQ-PEER`, `IPX-IN-IP`, `CARP`, `PGM`, `L2TP`, `DDX`, `IATP`, `STP`, `SRP`, `UTI`, `SMP`, `SM`, `PTP`, `ISIS`, `CRTP`, `CRUDP`, `SPS`, `PIPE`, `SCTP`, `FC`, `RSVP-E2E-IGNORE`, `UDPLITE`, `MPLS-IN-IP`, `MANET`, `HIP`, `SHIM6`, `WESP`, `ROHC`, `PFSYNC`, or `DIVERT`")

  return True
