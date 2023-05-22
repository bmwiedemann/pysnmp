"""
PDU var-binds to MIB objects
++++++++++++++++++++++++++++

This script explains how Python application could turn SNMP PDU
variable-bindings into MIB objects or the other way around.

The code that configures MIB compiler is similar to what
happens inside the pysnmp.hlapi API.
"""#
from pysnmp.proto.rfc1902 import ObjectIdentifier
from pysnmp.smi import builder, view, compiler, rfc1902

# Assemble MIB browser
mibBuilder = builder.MibBuilder()
mibViewController = view.MibViewController(mibBuilder)
compiler.addMibCompiler(mibBuilder, sources=['file:///usr/share/snmp/mibs',
                                             'https://mibs.pysnmp.com/asn1/@mib@'])

mibBuilder.loadTexts = True
# Pre-load MIB modules we expect to work with
mibBuilder.loadModules("SNMPv2-MIB", "SNMP-COMMUNITY-MIB")

# Create an OID object
oid = ObjectIdentifier('1.3.6.1.2.1.1.3')

# Get the MIB name and symbol name for the OID
modName, symName, suffix = mibViewController.getNodeLocation(oid)

# Get the MIB node for the OID
mibNode, = mibBuilder.importSymbols(modName, symName)

# This is what we can get in TRAP PDU
varBinds = [
    ("1.3.6.1.2.1.1.3.0", 12345),
    ("1.3.6.1.6.3.1.1.4.1.0", "1.3.6.1.6.3.1.1.5.2"),
    ("1.3.6.1.6.3.18.1.3.0", "0.0.0.0"),
    ("1.3.6.1.6.3.18.1.4.0", ""),
    ("1.3.6.1.6.3.1.1.4.3.0", "1.3.6.1.4.1.20408.4.1.1.2"),
    ("1.3.6.1.2.1.1.1.0", "my system"),
]

# Run var-binds through MIB resolver
# You may want to catch and ignore resolution errors here
varBinds = [
    rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(
        mibViewController
    )
    for x in varBinds
]

for varBind in varBinds:
    print(varBind.prettyPrint())
