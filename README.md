
# encbmp

[![PyPI version](https://badge.fury.io/py/encbmp.svg)](https://badge.fury.io/py/encbmp)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/ZhanPwBibiBibi/AES_bmp/blob/master/LICENSE.md)

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
![](https://github.com/P3n9W31/AES_bmp/blob/master/pic/usage.jpg)
