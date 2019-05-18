import codecs


def remove_bom(val):
    val_bytes = val.encode()
    BOM = codecs.BOM_UTF8
    while (BOM[0] == val_bytes[0] and BOM[1] == val_bytes[1] and BOM[2] == val_bytes[2]):
        val_bytes = val_bytes[3:]
    val = val_bytes.decode()
    return val