"""
Set string value
++++++++++++++++

Send a SNMP SET request with the following options:

* with SNMPv3 with user 'usr-sha-none', SHA auth and no privacy protocols
* over IPv4/UDP
* to an Agent at 127.0.0.1:161
* for an OID in tuple form and a string-typed value

This script performs similar to the following Net-SNMP command:

| $ snmpset -v3 -l authNoPriv -u usr-sha-none -a SHA -A authkey1 -ObentU demo.pysnmp.com:161 1.3.6.1.2.1.1.9.1.3.1 s 'my new value'

"""#

import asyncio
from pysnmp.hlapi.asyncio import *

async def run():
    snmpEngine = SnmpEngine()
    set_result = await setCmd(
        snmpEngine,
        UsmUserData('usr-sha-none', 'authkey1',
                    authProtocol=usmHMACSHAAuthProtocol),
        UdpTransportTarget(('demo.pysnmp.com', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.9.1.3.1'), OctetString('my new value')))

    errorIndication, errorStatus, errorIndex, varBinds = await set_result
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