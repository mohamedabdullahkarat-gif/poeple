import whois

async def domain_lookup_raw(domain):
    try:
        data = whois.whois(domain)
        return {"registrar": data.registrar, "created": str(data.creation_date)}
    except:
        return {"registrar": None, "created": None}
