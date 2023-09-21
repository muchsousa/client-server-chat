tags = {
    # field: tag
    "type": "01",
    "datetime": "02",
    "username": "03",
    "value": "04",
# ---------------------
    # tag: field
    "001": "type",
    "002": "datetime",
    "003": "username",
    "004": "value",
}

def encode_tlv(items, tags=tags, tlv_config={ "tag": 3, "length": 3 }):
    tlv = ""
    for item in items:
        value = items[item]
        length = f'{len(value)}'.zfill(tlv_config["tag"])
        tag = f'{tags[item]}'.zfill(tlv_config["length"])

        tlv += f"{tag}{length}{value}"

    return tlv

def decode_tlv(tlv, tags=tags, tlv_config={ "tag": 3, "length": 3 }):
    items = {}

    start = 0
    while start < len(tlv):
        end = start + tlv_config["tag"]
        tag = tlv[start:end]

        start = end
        end = start + tlv_config["length"]
        length = tlv[start:end]

        start = end
        end = start + int(length)
        value = tlv[start:end]

        start = end

        # print(tag, length, value)

        tagName = tags[tag] or tag
        items[tagName] = value

    return items
