"""
SNMPv2c
+++++++

Send SNMP GET request using the following options:

  * with SNMPv2c, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.pysnmp.com:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v2c -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0

"""#
import asyncio
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.smi import builder, compiler, view
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def run():
    slim = Slim()
    mibBuilder = slim.snmpEngine.getMibBuilder()

    # Optionally compile MIBs
    compiler.addMibCompiler(mibBuilder, sources=['/usr/share/snmp/mibs'])

    # mibBuilder.loadModules('SNMPv2-MIB')
    mibBuilder.addMibSources(builder.DirMibSource('/Users/lextm/pysnmp.com/pysnmp/mibs'))
    # mibBuilder.loadModule('LEXTUDIO-MIB')
    mibBuilder.loadModule('CISCO-ENHANCED-IPSEC-FLOW-MIB')

    errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
        'public',
        'localhost',
        161,
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysObjectID", 0)),
        # ObjectType(ObjectIdentity("LEXTUDIO-MIB", "compDescr", 0)), 
        # ObjectType(ObjectIdentity("1.3.6.1.4.1.9999.2.0")),
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
