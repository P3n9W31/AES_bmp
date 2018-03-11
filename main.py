from AES import AES_bmp


if __name__ == '__main__':
    bmp = AES_bmp()
    bmp.show_header()
    bmp.show_div_header()
    bmp.encrypt(mode='CTR')
    bmp.show_enc()
    bmp.decrypt()
    bmp.show_dec()