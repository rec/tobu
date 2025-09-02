import yaml


def merge(a, b):
    def assignments(d: list):
        return dict(i.partition("=")[::2] for i in d)

    def from_assignments(assign: dict):
        return [f"{k}={v}" if v else k for k, v in assign.items()]

    # destructively merge b into a
    assert type(a) is type(b) is dict

    if ch := b.pop('channels', None):
        a['channels'] = ch

    dep_b = b.pop('dependencies', None)
    dep_a = a['dependencies']

    if dep_a and dep_b:
        pip = dep_a.pop("pip", []) + dep_b.pop("pip", [])

        assign = assignments(dep_a) | assignments(dep_b)
        dep_a[:] = from_assignments(assign)

        if pip:
            dep_a.append({"pip": pip})

    elif dep_b:
        dep_a[:] = dep_b

    if remove := b.pop("-dependencies", None):
        assign = assignments(dep_a)
        for r in remove:
            assign.pop(r)
        dep_a[:] = from_assignments(assign)

    assert not b, b
    return a
