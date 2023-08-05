def get_input(config: dict):
    kexes = (
        config.pop("in_kex", [])
        or config.pop("input_kex", [])
        or config.pop("in_kexes", [])
        or config.pop("input_kexes", [])
    )
    if isinstance(kexes, str):
        kexes = [kexes]
    tables = config.pop("input_tables", []) or config.pop("in_tables", [])
    return [*kexes, *tables]
