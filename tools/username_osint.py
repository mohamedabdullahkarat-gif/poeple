async def username_lookup_raw(username: str) -> dict:
    base = username.strip()

    variations = set()

    variations.add(base)
    variations.add(base.replace("_", ""))
    variations.add(base.replace("_", "."))
    variations.add(base.replace(".", "_"))

    if not base.endswith(("1", "_dev", ".dev")):
        variations.add(base + "1")
        variations.add(base + "_dev")
        variations.add(base + ".dev")

    variations.add(base.lower())
    variations.add(base.upper())

    return {
        "input": username,
        "alias_count": len(variations),
        "aliases": sorted(variations)
    }
