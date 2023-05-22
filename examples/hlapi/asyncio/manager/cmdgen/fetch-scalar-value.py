"""
Fetch scalar MIB variables (SNMPv1)
+++++++++++++++++++++++++++++++++++

Perform SNMP GET operation with the following options:

* with SNMPv1, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OIDs in tuple form

This script performs similar to the following Net-SNMP command:

| $ snmpget -v1 -c public -ObentU demo.pysnmp.com 1.3.6.1.2.1.1.1.0 1.3.6.1.2.1.1.3.0

"""#

import asyncio
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def run():
    slim = Slim(1)
    errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
        'public',
        'demo.pysnmp.com',
        161,
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    slim.close()


asyncio.run(run())
