def add_remaining_to_populated_args(populated, remaining):
    i = 0
    while i < len(remaining):
        if "=" in remaining[i]:
            name, value = remaining[i].split("=")
            i += 1
        else:
            name = remaining[i]
            value = remaining[i + 1]
            i += 2
        name = name[2:]
        setattr(populated, name, value)
