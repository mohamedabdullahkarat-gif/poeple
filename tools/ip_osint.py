import requests

async def ip_lookup_raw(target):
    r = requests.get(f"http://ip-api.com/json/{target}").json()
    return {"country": r.get("country"), "isp": r.get("isp"), "asn": r.get("as")}
