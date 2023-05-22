"""
SET string and integer scalars
++++++++++++++++++++++++++++++

Send SNMP SET request with the following options:

* with SNMPv1 with community name 'private'
* over IPv4/UDP
* to an Agent at 127.0.0.1:161
* for OIDs in tuple form and an integer and string-typed values

This script performs similar to the following Net-SNMP command:

| $ snmpset -v1 -c private -ObentU demo.pysnmp.com:161 1.3.6.1.2.1.1.9.1.3.1 s 'my value'  1.3.6.1.2.1.1.9.1.4.1 t 123 

"""#

import asyncio
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.proto.rfc1902 import OctetString, TimeTicks
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def run():
    slim = Slim(1)
    errorIndication, errorStatus, errorIndex, varBinds = await slim.set(
        'public',
        'demo.pysnmp.com',
        161,
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.9.1.3.1'), OctetString('my value')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.9.1.4.1'), TimeTicks(123)),
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
