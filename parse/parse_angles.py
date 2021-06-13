def parse_angles(txt_file):
    key_words = ['CORNER_UL_LAT_PRODUCT', 'CORNER_UL_LON_PRODUCT',
                 'CORNER_UR_LON_PRODUCT', 'CORNER_UR_LON_PRODUCT',
                 'CORNER_LL_LAT_PRODUCT', 'CORNER_LL_LON_PRODUCT',
                 'CORNER_LR_LAT_PRODUCT', 'CORNER_LR_LON_PRODUCT']
    angles_dict = dict()
    text = txt_file.read().decode()
    for line in text.split('\n'):
        string = line.replace(' ','').replace('\n', '').split('=')
        if string[0] in key_words:
            angles_dict[string[0]] = float(string[1])
    return angles_dict