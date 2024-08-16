#import time
import board
import displayio
import rgbmatrix
import framebufferio

#import terminalio
#from adafruit_display_text.label import Label
#from adafruit_bitmap_font import bitmap_font
#from adafruit_matrixportal.network import Network
#from adafruit_matrixportal.matrix import Matrix

print("RGBMatrix Clock Start...")

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
   width=64, bit_depth=4,
   rgb_pins=[
       board.MTX_R1,
       board.MTX_G1,
       board.MTX_B1,
       board.MTX_R2,
       board.MTX_G2,
       board.MTX_B2
   ],
   addr_pins=[
       board.MTX_ADDRA,
       board.MTX_ADDRB,
       board.MTX_ADDRC,
       board.MTX_ADDRD
   ],
   clock_pin=board.MTX_CLK,
   latch_pin=board.MTX_LAT,
   output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix)

print("Matrix Display Setup..")

bitmap = displayio.OnDiskBitmap("/Roboto.bmp")

print("Bitmap Loaded...")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

print("Bitmap Displayed...")

# Loop forever so you can enjoy your image
while True:
    pass
