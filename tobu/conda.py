import yaml


def merge(a, b):
    def assignments(d: list):
        return dict(i.partition("=")[::2] for i in d)

    def from_assignments(assign: dict):
        return [f"{k}={v}" if v else k for k, v in assign.items()]

    def get_pip(d: list):
        res, pip = [], []
        for i in d:
            if isinstance(i, str):
                res.append(i)
            else:
                (name, pip), = i.items()
                assert name == "pip", i

        return res, pip

    # destructively merge b into a
    assert type(a) is type(b) is dict

    if ch := b.pop('channels', None):
        a['channels'] = ch

    dep_b = b.pop('dependencies', [])
    dep_a = a['dependencies']

    dep_a[:], pip_a = get_pip(dep_a)
    dep_b[:], pip_b = get_pip(dep_b)

    assign = assignments(dep_a) | assignments(dep_b)

    if remove := b.pop("-dependencies", None):
        for r in remove:
            assign.pop(r)
        dep_a[:] = from_assignments(assign)

    dep_a[:] = from_assignments(assign)
    if pip := pip_a + pip_b:
        dep_a.append({"pip": pip})

    assert not b, b
    return a


if __name__ == '__main__':
    import sys

    _, first, *rest = sys.argv
    with open(first) as fp:
        result = yaml.safe_load(fp.read())

    for f in rest:
        with open(f) as fp:
            merge(result, yaml.safe_load(fp.read()))

    print(yaml.safe_dump(result))
