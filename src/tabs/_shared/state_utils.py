from copy import deepcopy


def deep_merge_missing(dst, src):
    """Recursively merge `src` into `dst` without overwriting existing keys."""
    for key, value in src.items():
        if isinstance(value, dict):
            cur = dst.get(key)
            if not isinstance(cur, dict):
                cur = {}
                dst[key] = cur
            deep_merge_missing(cur, value)
        elif key not in dst:
            dst[key] = deepcopy(value)


def ensure_dict(root, key):
    cur = root.get(key)
    if not isinstance(cur, dict):
        cur = {}
        root[key] = cur
    return cur
