from pysnmp.hlapi import *
from pysnmp.hlapi.asyncio.cmdgen import setCmd
from pysnmp.hlapi.asyncio.transport import UdpTransportTarget

def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(ObjectType(ObjectIdentity(key), value))
    return pairs, print(pairs)


def set(target, value_pairs, CommunityData=CommunityData('public', mpModel=0), port=1883, engine=SnmpEngine(), context=ContextData()):

    handler = setCmd(
        engine,
        CommunityData,
        UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs(value_pairs)
    )
    return fetch(handler, 1)[0]

def cast(value):

    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):

    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def runset(TCIPAddress):

    threading.Timer(1, runget, [TCIPAddress]).start()
    set(TCIPAddress, {"1.3.6.1.4.1.1206.4.2.1.1.5.1.6.1": "8"})

if name == "main":
    ListTCID = []
    ListTCID.append('192.168.10.108')
    for siginfo in ListTCID:
        runset(siginfo)
