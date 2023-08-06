import numpy as np


def read_record(data, fmt):
    """Parse string to data given format."""
    token_to_type = {
        "s": str,
        "S": str,
        "d": int,
        "f": to_float,
        "e": to_float,
    }

    i = 0
    out = []
    for token in fmt.split(","):
        n = int(token[:-1].split(".")[0])
        tmp = data[i : i + n]
        tmp = tmp if token[-1] == "S" else tmp.strip()
        out.append(token_to_type[token[-1]](tmp) if tmp else None)
        i += n

    return out


def write_record(data, fmt, multi=False):
    """Return a list of record strings given format."""
    if not multi:
        data = [to_str(d, f) for d, f in zip(data, fmt)]
        out = ["{:80}\n".format("".join(data))]

    else:
        n = len(data)
        ncol = len(fmt)
        data = [
            data[ncol * i : min(ncol * i + ncol, n)]
            for i in range(int(np.ceil(n / ncol)))
        ]

        out = []
        for d in data:
            d = [to_str(dd, f) for dd, f in zip(d, fmt)]
            out += ["{:80}\n".format("".join(d))]

    return out


def to_float(s):
    """Convert variable string to float."""
    try:
        return float(s.replace("d", "e"))

    except ValueError:
        # It's probably something like "0.0001-001"
        significand, exponent = s[:-4], s[-4:]
        return float("{}e{}".format(significand, exponent))


def to_str(x, fmt):
    """Convert variable to string."""
    x = "" if x is None else x

    if not isinstance(x, str):
        # Special handling for floating point numbers
        if "f" in fmt:
            # Number of decimals is specified
            if "." in fmt:
                n = int(fmt[3:].split(".")[0])
                tmp = fmt.format(x)

                if len(tmp) > n:
                    return fmt.replace("f", "e").format(x)

                else:
                    return tmp

            # Let Python decides the format
            else:
                n = int(fmt[3:].split("f")[0])
                tmp = str(float(x))

                if len(tmp) > n:
                    fmt = "{{:>{}.{}e}}".format(n, n - 7)

                    return fmt.format(x)

                else:
                    fmt = "{{:>{}}}".format(n)

                    return fmt.format(tmp)

        else:
            return fmt.format(x)

    else:
        return fmt.replace("g", "").replace("e", "").replace("f", "").format(x)


def prune_nones_dict(data):
    """Remove None key/value pairs from dict."""
    return {k: v for k, v in data.items() if v is not None}


def prune_nones_list(data):
    """Remove trailing None values from list."""
    return [x for i, x in enumerate(data) if any(xx is not None for xx in data[i:])]
