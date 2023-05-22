"""
Waive MIB lookup
++++++++++++++++

Perform SNMP GETNEXT operation with the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for an OID in string form
* do not resolve request/response OIDs and values from/toto human-friendly form

The `lookupMib=False` keyword argument makes pysnmp NOT resolving 
request and response variable-bindings from/to human-friendly form.

Functionally similar to:

| $ snmpgetnext -v2c -c public -ObentU demo.pysnmp.com 1.3.6.1.2.1

"""#
import asyncio
from pysnmp.hlapi import *
from pysnmp.hlapi.asyncio.cmdgen import nextCmd
from pysnmp.hlapi.asyncio.transport import UdpTransportTarget

async def run():
    next_result = await nextCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('localhost', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1')),
        lookupMib=False
    )

    errorIndication, errorStatus, errorIndex, varBinds = await next_result
    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

asyncio.run(run())
