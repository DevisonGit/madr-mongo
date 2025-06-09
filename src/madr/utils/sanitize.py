def name_in(name: str):
    return ' '.join(name.strip().lower().split())


def name_out(name: str):
    return name.title()


def name_in_out(name: str):
    return name_out(name_in(name))
