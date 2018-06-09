from Crypto.Cipher import AES
from binascii import b2a_hex, hexlify, unhexlify
from PIL import Image, ImageFile
from Crypto.Util import Counter

ImageFile.LOAD_TRUNCATED_IMAGES = True


class AES_bmp():
    def __init__(self, img_path='bmp_target.bmp'):
        # self.key = key
        self.img_path = img_path
        self.img_enc_path = 'bmp_encrypted.bmp'
        self.__gethead__()
        self.__get_headerdata__()
        self.__get_div_headerdata__()

    def __gethead__(self):
        """Get Bitmap Header, DIV Header and imageData"""
        with open(self.img_path, 'rb') as f_read:
            self.header = f_read.read(14)
            self.div_header = f_read.read(40)
            self.imagedata = f_read.read()

    def __get_div_headerdata__(self):
        """Parse DIV Header information"""
        header = []
        for i in range(0, 28, 2):
            header.append(int(hexlify(self.header)[i:i + 2], 16))
        self.type = ''.join([chr(int(bytes(map(ord, str(header[i]))).decode('ASCII'))) for i in range(0, 2)])
        self.size_tal = sum([header[i + 2] * 256 ** i for i in range(0, 4)])
        self.reserved = sum([header[i + 6] * 256 ** i for i in range(0, 2)])
        self.offbit = [hex(header[i + 10]) for i in range(0, 4)][0]

    def __get_headerdata__(self):
        """Parse Bitmap Header"""
        DIBheader = []
        for i in range(0, 80, 2):
            DIBheader.append(int(hexlify(self.div_header)[i:i + 2], 16))
        self.size_of_header = sum([DIBheader[i] * 256 ** i for i in range(0, 4)])
        self.width = sum([DIBheader[i + 4] * 256 ** i for i in range(0, 4)])
        self.height = sum([DIBheader[i + 8] * 256 ** i for i in range(0, 4)])
        self.num_of_planes = sum([DIBheader[i + 12] * 256 ** i for i in range(0, 2)])
        self.color_depth = sum([DIBheader[i + 14] * 256 ** i for i in range(0, 2)])
        self.compression_method = sum([DIBheader[i + 16] * 256 ** i for i in range(0, 4)])
        self.size = sum([DIBheader[i + 20] * 256 ** i for i in range(0, 4)])
        self.hol_res = sum([DIBheader[i + 24] * 256 ** i for i in range(0, 4)])
        self.ver_res = sum([DIBheader[i + 28] * 256 ** i for i in range(0, 4)])
        self.num_of_color = sum([DIBheader[i + 32] * 256 ** i for i in range(0, 4)])
        self.num_of_impcol = sum([DIBheader[i + 36] * 256 ** i for i in range(0, 4)])

    def show_header(self):
        """Show Bitmap information"""
        print('Header')
        print('-------------------------------------------------------')
        print('Type of BMP: \t\t\t\t\t\t\t' + str(self.type))
        print('Size of BMP: \t\t\t\t\t\t\t' + str(self.size_tal) + ' bytes')
        print('Reserved of BMP: \t\t\t\t\t\t' + str(self.reserved))
        print('OffBit of BMP: \t\t\t\t\t\t\t' + str(self.offbit))
        print('-------------------------------------------------------')

    def show_div_header(self):
        """Show DIV Header information"""
        compression_method_name = ''
        print('DIV Header')
        print('-------------------------------------------------------')
        print('|Size of header: \t\t\t\t\t\t\t' + str(self.size_of_header) + ' bytes')
        print('|Width of BMP: \t\t\t\t\t\t\t\t' + str(self.width) + ' px')
        print('|Height of BMP: \t\t\t\t\t\t\t' + str(self.height) + ' px')
        print('|Number of color planes: \t\t\t\t\t' + str(self.num_of_planes) + '')
        print('|Color Depth: \t\t\t\t\t\t\t\t' + str(self.color_depth) + ' B')
        value_com = [0, 1, 2, 3, 4, 5, 6, 11, 12, 13]
        com_name = ['None', 'RLE 8-bit/pixel', 'RLE 4-bit/pixel', 'Huffman 1D', 'RLE-24', 'RGBA bit field masks',
                    'None', 'RLE-8', 'RLE-4']
        for item in value_com:
            if int(self.compression_method) == int(item):
                compression_method_name = com_name[value_com.index(item)]
        print('|Compression method: \t\t\t\t\t\t' + compression_method_name + '')
        print('|Size of raw BMP: \t\t\t\t\t\t\t' + str(self.size) + 'B')
        print('|Horizontal resolution of the BMP: \t\t\t' + str(self.hol_res) + ' px/m')
        print('|Vertical resolution of the BMP: \t\t\t' + str(self.ver_res) + ' px/m')
        print('|Number of colors in the color palette: \t' + str(self.num_of_color) + '')
        print('|Number of important colors: \t\t\t\t' + str(self.num_of_impcol) + '')
        print('-------------------------------------------------------')

    def encrypt(self, key='keykeykeykeykeyk', mode='ECB'):
        """Use AES to encrypt target Bitmap file with given
        key and encrypt mode.
        mode Support:EBC: Electronic Code Book,
                     CBC: Cipher-Block Chaining,
                     CFB: Cipher FeedBack,
                     OFB: Output FeedBack,
                     CTR: CounTer Mode,
        Output as 'bmp_encrypted.bmp'.
        """
        self.key = key
        f_out = open(self.img_enc_path, 'wb')
        f_out.write(self.header)
        f_out.write(self.div_header)
        image_data = self.imagedata
        cleartext = unhexlify(hexlify(image_data))

        length = 16
        count = len(cleartext)
        add = length - (count % length)
        cleartext = cleartext + (b'\0' * add)

        self.IV = self.key

        if mode in ['ECB', 'CBC', 'CFB', 'OFB']:
            self.mode_str = 'AES.MODE_{0}'.format(mode)
            mode = eval(self.mode_str)
            encryptor = AES.new(key, mode, IV=self.IV)

        elif mode in ['CTR']:
            self.mode_str = 'AES.MODE_{0}'.format(mode)
            mode = eval(self.mode_str)
            ctr = Counter.new(128)
            encryptor = AES.new(key, mode, IV=self.IV, counter=ctr)


        else:
            print("AES does't has this mode! Use ECB as default!")
            mode = 'ECB'
            self.mode_str = 'AES.MODE_{0}'.format(mode)
            mode = eval(self.mode_str)
            encryptor = AES.new(key, mode, IV=self.IV)

        self.mode = mode
        encrypted_text = unhexlify(b2a_hex(encryptor.encrypt(cleartext)).decode("ASCII"))
        self.encrypted_text = encrypted_text
        f_out.write(encrypted_text)
        f_out.close()

    def decrypt(self):
        """Decrypt encrypted Bitmap file.
        Output as 'bmp_decrypted.bmp'.
        """
        f_out = open('bmp_decrypted.bmp', 'wb')
        f_out.write(self.header)
        f_out.write(self.div_header)

        if self.mode_str == 'AES.MODE_CTR':
            ctr = Counter.new(128)
            cryptor = AES.new(self.key, self.mode, IV=self.IV, counter=ctr)
        else:
            cryptor = AES.new(self.key, self.mode, IV=self.IV)
        plain_text = unhexlify(b2a_hex(cryptor.decrypt(self.encrypted_text)))

        f_out.write(plain_text)
        f_out.close()

    def show_ori(self):
        """Show the original Bitmap file"""
        im = Image.open(self.img_path)
        im.show()

    def show_enc(self):
        """Show the encrypted Bitmap file"""
        im = Image.open('bmp_encrypted.bmp')
        im.show()

    def show_dec(self):
        """Show the decrypted Bitmap file
        Input file as 'bmp_decrypted.bmp'.
        """
        im = Image.open('bmp_decrypted.bmp')
        im.show()


if __name__ == '__main__':
    bmp = AES_bmp(img_path='../pic/bmp_target.bmp')
    bmp.show_header()
    bmp.show_div_header()
    bmp.encrypt(mode='ECB')
    bmp.show_enc()
    bmp.decrypt()
    bmp.show_dec()
