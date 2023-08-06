from embit.script import Script
from embit.liquid.networks import NETWORKS
from embit.liquid.addresses import addr_decode
from embit import base58, bech32
from collections import OrderedDict

KEYWORDS = ["address", "amount", "asset", "label"]


def detect_network(addr):
    """Detects what networks the address belongs to"""
    # check if it's bech32
    for net in NETWORKS.values():
        hrp = addr.lower().split("1")[0]
        if hrp == net.get("bech32"):
            return net
        if "blech32" in net and hrp == net.get("blech32"):
            return net
    # if not - it's base58
    data = base58.decode_check(addr)
    for net in NETWORKS.values():
        if data[:2] in [net.get("bp2sh"), net.get("p2sh")]:
            return net


def checkaddr(addr):
    sc, pub = addr_decode(addr)
    net = detect_network(addr)
    for chain, n in NETWORKS.items():
        if n == net:
            return chain, net, sc
    raise ParsingError("Unknown network")
    # # try with base58 address
    # try:
    #     data = base58.decode_check(addr)
    #     prefix = data[:1]
    #     for chain, net in NETWORKS.items():
    #         if prefix == net["p2pkh"]:
    #             return chain, net, Script(b"\x76\xa9\x14" + data[1:] + b"\x88\xac")
    #         elif prefix == net["p2sh"]:
    #             return chain, net, Script(b"\xa9\x14" + data[1:] + b"\x87")
    # except:
    #     # fail - then it's bech32 address
    #     hrp = addr.lower().split("1")[0]
    #     ver, data = bech32.decode(hrp, addr)
    #     if ver not in [0, 1] or len(data) not in [20, 32]:
    #         raise ValueError("Invalid bech32 address")
    #     if ver == 1 and len(data) != 32:
    #         raise ValueError("Invalid bech32 address")
    #     # OP_1..OP_N
    #     if ver > 0:
    #         ver += 0x50
    #     sc = Script(bytes([ver, len(data)] + data))
    #     for chain, net in NETWORKS.items():
    #         if net["bech32"] == hrp:
    #             return chain, net, sc


class ParsingError(Exception):
    pass


def parse_header(line):
    arr = [e.strip() for e in line.split(",")]
    # check if address is there - then it's not a header
    for el in arr:
        try:
            checkaddr(el)
            return None
        except:
            pass
    # find keywords
    arr = [e.lower() for e in arr]
    header = {}
    for keyword in KEYWORDS:
        if keyword in arr:
            header[keyword] = arr.index(keyword)
    if "serial number" in arr:
        header["label"] = arr.index("serial number")
    return header


def parse_csv(data):
    lines = [
        line.strip()
        for line in data.strip().replace("\r", "").split("\n")
        if line.strip()
    ]
    header = None
    if len(lines) > 0:
        header = parse_header(lines[0])
        if header is not None:
            lines = lines[1:]
    invalid_lines = []
    addresses = OrderedDict()
    for line in lines:
        found = False
        arr = [e.strip() for e in line.split(",")]
        if header:
            obj = {}
            addr_pos = header.get("address")
            for keyword, pos in header.items():
                if len(arr) > pos:
                    if keyword == "address":
                        el = arr[pos]
                        chain, net, sc = checkaddr(el)
                        obj["chain"] = chain
                        found = True
                    obj[keyword] = arr[pos]
                    if el in addresses:
                        raise ParsingError(f"Address {el} is found twice!")
            if ("address" not in obj) and (addr_pos is None):
                for i, el in enumerate(arr):
                    if i in header.values():
                        continue
                    try:
                        chain, net, sc = checkaddr(el)
                        if el in addresses:
                            raise ParsingError(f"Address {el} is found twice!")
                        if found:
                            raise ParsingError(
                                f"Two addresses in the same line: {line}"
                            )
                        obj.update({"address": el, "chain": chain})
                        found = True
                    # propogate parsing error
                    except ParsingError as e:
                        raise e
                    except Exception as e:
                        pass
            if found or ("address" in obj):
                addresses[obj["address"]] = obj
        else:
            for el in arr:
                try:
                    chain, net, sc = checkaddr(el)
                    if el in addresses:
                        raise ParsingError(f"Address {el} is found twice!")
                    if found:
                        raise ParsingError(f"Two addresses in the same line: {line}")
                    addresses[el] = {"address": el, "chain": chain}
                    found = True
                # propogate parsing error
                except ParsingError as e:
                    raise e
                except Exception as e:
                    pass
        if not found:
            invalid_lines.append(line)
    # detect chain
    chain = {el["chain"] for el in addresses.values()}
    if len(chain) > 1:
        raise ParsingError("Addresses belong to different chains!")
    if len(chain) == 0:
        raise ParsingError("No addresses found")
    chain = chain.pop()
    for obj in addresses.values():
        obj["amount"] = int(obj.get("amount", 0) or 0)
        obj["label"] = obj.get("label", "")
    return list(addresses.values()), chain, invalid_lines
