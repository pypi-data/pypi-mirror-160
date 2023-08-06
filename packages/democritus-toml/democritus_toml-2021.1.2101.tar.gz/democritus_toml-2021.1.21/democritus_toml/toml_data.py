def toml_read(toml_data: str):
    import toml

    parsed_toml_data = toml.loads(toml_data)
    return parsed_toml_data


def is_toml(possible_toml_data: str) -> bool:
    try:
        toml_read(possible_toml_data)
    except:
        return False
    else:
        return True


# todo: are there other input types possible?
# TODO: can we do this using atomic/safe writing?
def toml_write(data: dict) -> str:
    import toml

    result = toml.dumps(data)
    return result
