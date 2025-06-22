
def normalize_data(data_json):
    for item in data_json:
        if item.get("dispensas") is None:
            item["dispensas"] = "N"
        else:
            item["dispensas"] = "S"
    return data_json