def remove_duplicate_items(_api_data, _key):
    """
    This function removes duplicate items from a list of dictionaries based on a specified key.

    Args:
        _api_data (list): A list of dictionaries from which duplicates need to be removed.
        _key (str): The key in the dictionaries based on which duplicates are identified.

    Returns:
        list: A list of dictionaries after removing duplicates.
    """
    unique_elements = []
    cleaned_data = []
    keys = []
    for i, j in enumerate(_api_data):
        if _api_data[i][_key] not in unique_elements:
            unique_elements.append(_api_data[i][_key])
            keys.append(i)

    for key in keys:
        cleaned_data.append(_api_data[key])

    # print(
    #     "Total duplicates removed: {}, Total items: {}, Final items:{}".format(
    #         (len(_api_data) - len(unique_elements)),
    #         len(_api_data), len(unique_elements)))
    # print("Final items in list: {}".format(len(cleaned_data)))

    return cleaned_data

def safe_int(val):
    try:
        return int(val)
    except ValueError:
        print("ValueError: Cannot convert to int", val)
        return 1