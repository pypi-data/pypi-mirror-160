from .__init__ import *
signature_key = "f8e7a61ac3f725941e3ac7cae2d688be97f30b93"
device_key = b"\x02\xb2X\xc65Y\xd8\x80C!\xc5\xd5\x06Z\xf3 5\x8d6o"
session = httpx()

def generate_device_id() -> str:
    infinite = sha1(str(''.join(choice(ascii_letters + digits) for _ in range(32))).encode('utf-8')).digest()
    return "42" + infinite.hex() + hmac(device_key, b"\x42" + infinite, sha1).digest().hex()

def generate_signature(DATA: dict) -> str:
    return b64encode(bytes.fromhex("42") + hmac(bytes.fromhex(signature_key), str(DATA).encode("utf-8"), sha1).digest()).decode("utf-8")

async def get_device_id_from_api(self) -> str:
    #NOTE: This is a temporary fix for device generator.
    #      API is currently down.
    r = await session.get("https://cynical.gg/device")
    return loads(r.text)["deviceID"]

async def get_signature(self, DATA) -> str:
    #NOTE: This is a temporary fix for the signature generator.
    #      API is currently down.
    r = await session.get("https://cynical.gg/signature?data=" + DATA)
    return loads(r.text)["signature"]

def sid2uid(sid: str) -> str:
    return loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + " = " * (-len(sid) % 4)).encode())[1:-20].decode())["2"]

def printr(text: str):
    print(stylize(text, fg("dark_gray") + bg("black")))
    print(stylize("", attr("reset")))

def printwr(text: str):
    print(stylize(text, fg("blue") + bg("black")))
    print(stylize("", attr("reset")))

def printrb(text: str):
    print(stylize(text, fg("red") + bg("black")))
    print(stylize("", attr("reset")))

def APICodes(statuscode: int) -> str:
    """
    || Returns solution to common errors. ||
    """
    statuscodes = {
        105: "Invalid session ID. Please login again and obtain a new session ID.",
        106: "Access denied. You are not authorized to use this service.",
        110: "Change IP address to a new one.",
        200: "Make sure password is correct.",
        216: "Check the email address. It may be incorrect.",
        218: "Change your device_id to a valid one.",
        219: "Change your device_id to a new one and try again.",
    }
    if statuscode in statuscodes:
        return statuscodes[statuscode]
    else:
        return None

def _get_entity_(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    res = _get_entity_(v, key)
                    if res:
                        return res
                elif isinstance(v, list):
                    for item in v:
                        res = _get_entity_(item, key)
                        if res:
                            return res
    elif isinstance(data, list):
        for item in data:
            res = _get_entity_(item, key)
            if res:
                return res
    return None

def _get_entities_(data, key):
    if isinstance(data, dict):
        if key in data:
            return [data[key]]
        else:
            res = []
            for k, v in data.items():
                if isinstance(v, dict):
                    res += _get_entities_(v, key)
                elif isinstance(v, list):
                    for item in v:
                        res += _get_entities_(item, key)
            return res
    elif isinstance(data, list):
        res = []
        for item in data:
            res += _get_entities_(item, key)
        return res
    return []
