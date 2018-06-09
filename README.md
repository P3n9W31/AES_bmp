# encbmp
A light, easy using tool to parse, encrypt and decrypt Bitmap file in AES.

## Install 

```bash
pip install encbmp
```

## Usage

```python
from encbmp import AES

bmp = AES.AES_bmp(img_path='bmp_target.bmp') # Load Bitmap file

bmp.show_header() # Show the Bitmap file Header information
bmp.show_div_header() # # Show the DIV Header information


bmp.encrypt(mode='CTR') # Choose a mode to encrypy,Support EBC,CBC,CFB,OFB,CTR.
bmp.show_enc()

bmp.decrypt()
bmp.show_dec()
```

## Output
![](https://ws3.sinaimg.cn/large/006tNc79gy1fpa521aqmwj31kw30ox6r.jpg)
