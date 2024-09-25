def flatten_dict(d, parent_key='', sep='_'):
    items = []
    acceptable = (str, int, float, bool)
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        # If the key is "Text", don't flatten further, just return the content
        if k == "Text":
            if isinstance(v, acceptable):
                items.append((parent_key, v))
            else:
                items.append((parent_key, str(v)))
        elif isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Ensure all items in the list are strings
            if all(isinstance(item, str) for item in v):
                items.append((new_key, v))
            else:
                # Convert all items to strings
                items.append((new_key, [str(item) for item in v]))
        else:
            if isinstance(v, acceptable):
                items.append((new_key, v))
            else:
                # Convert the value to a string
                items.append((new_key, str(v)))
    return dict(items)
