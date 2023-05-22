"""
Broadcast SNMP message (IPv4)
+++++++++++++++++++++++++++++

Send SNMP GET request to broadcast address and wait for respons(es):

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to all Agents via broadcast address 255.255.255.255:161
* for OIDs in tuple form

Here we send out a single SNMP request and wait for potentially many SNMP 
responses from multiple SNMP Agents listening in local broadcast domain.
Since we can't predict the exact number of Agents responding, this script 
just waits for arbitrary time for collecting all responses. This technology
is also known as SNMP-based discovery.

This script performs similar to the following Net-SNMP command:

| $ snmpget -v2c -c public -ObentU 255.255.255.255 1.3.6.1.2.1.1.1.0 1.3.6.1.2.1.1.3.0

"""#

# TODO: need to convert to low level API

import asyncio
from pysnmp.hlapi.asyncio import *

async def run():
    snmpEngine = SnmpEngine()
    target = UdpTransportTarget(('255.255.255.255', 161), allow_broadcast=True)
    get_result = await getCmd(
        snmpEngine,
        CommunityData("public"),
        target,
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')))

    errorIndication, errorStatus, errorIndex, varBinds = await get_result
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

    snmpEngine.transportDispatcher.closeDispatcher()

asyncio.run(run())

