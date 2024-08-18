# download libs

https://circuitpython.org/libraries

# clock link

https://learn.adafruit.com/network-connected-metro-rgb-matrix-clock/code-the-matrix-clock

# problems

adafruit-io lib is not available, seems simpleio solves the issue

# font 

- woff to png with AA: https://stmn.itch.io/font2bitmap
    - src https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap
    - width: 16
    - Height: 32
    - font size: 30
    - charcters: 0123456789:
    - font selection: Roboto [normal] [300]
- png to bmp: https://convertio.co/ OR GIMP

These bmp are not showing AA in CPY

Converting in GIMP suggests that 
- png used Alpha for AA
- dithering or not converting to Indexed bmp is ugly (Alpha channel is discarded on Export)

Converting with GIMP to Grayscale produced indexed BMP, which was loaded as Palette in CPY (no AA)

We need indexed bmp, but https://online-converting.com/image/convert2bmp/# produces bmp as wite line (something not working)

# tzdata

python tzdata: https://github.com/python/tzdata/tree/master/src/tzdata/zoneinfo
tzfile format: https://man7.org/linux/man-pages/man5/tzfile.5.html and compiler: https://man7.org/linux/man-pages/man8/zic.8.html
cpy impl: https://github.com/evindunn/circuitpython_tzdb/tree/main
