def remove_duplicate_items(_api_data, _key):
    print("Initial items in list: {}".format(len(_api_data)))
    unique_elements = []
    cleaned_data = []
    keys = []
    for i, j in enumerate(_api_data):
        if _api_data[i][_key] not in unique_elements:
            unique_elements.append(_api_data[i][_key])
            keys.append(i)

    for key in keys:
        cleaned_data.append(_api_data[key])

    print(
        "Total duplicates removed: {}, Total items: {}, Final items:{}".format(
            (len(_api_data) - len(unique_elements)),
            len(_api_data), len(unique_elements)))
    print("Final items in list: {}".format(len(cleaned_data)))

    return cleaned_data