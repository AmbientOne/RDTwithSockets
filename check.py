def ip_checksum(data):
    # The checksum is just a sum of all the bytes. I swear.
    if isinstance(data, bytearray):
        total = sum(data)
    elif isinstance(data, bytes):
        if data and isinstance(data[0], bytes):
            # Python 2 bytes (str) index as single-character strings.
            total = sum(map(ord, data))
        else:
            # Python 3 bytes index as numbers (and PY2 empty strings sum() to 0)
            total = sum(data)
    else:
        # Unicode strings (should never see?)
        total = sum(map(ord, data))
    return total & 0xFFFFFFFF