import time
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

bitmap = displayio.OnDiskBitmap("/Roboto_2g.bmp")

print("Bitmap Loaded...")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, tile_width=16, width=10)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

print("Bitmap Displayed...")

# Loop forever so you can enjoy your image
while True:
    year_now, month_now, day_now, hour_now, min_now, sec_now, wd_now, yd_now, isdst_now = time.localtime()
    hour_high = int(hour_now / 10)
    hour_low = hour_now % 10
    min_high = int(min_now / 10)
    min_low = min_now % 10
#    print(f"{hour_now}={hour_high}-{hour_low} {min_now}={min_high}-{min_low}")

    #change indexes
    tile_grid[0]=hour_high
    tile_grid[1]=hour_low
    tile_grid[2]=min_high
    tile_grid[3]=min_low
#    print(tile_grid.width)

    time.sleep(60-sec_now)
