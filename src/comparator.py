def compare_keywords(all_keywords):
    if not all_keywords:
        return []

    sets = [set(k) for k in all_keywords if k]

    if not sets:
        return []

    common = set.intersection(*sets)
    return list(common)