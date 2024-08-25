#from adafruit_datetime import datetime
import time

def release_displays():
    import displayio
    # release any currently configured displays
    displayio.release_displays()

def get_matrix():
    import board
    import rgbmatrix
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
    return matrix

def get_display(matrix):
    import framebufferio
    display = framebufferio.FramebufferDisplay(matrix)
    return display

def get_font():
    import terminalio
    return terminalio.FONT

def get_label(font):
    from adafruit_display_text.label import Label
    label = Label(
        font, 
        text="Test",
        color=0xFF0000,
        scale=1,
    )
    label.x = 0
    label.y = 10
    return label

def get_gps():
    import board
    import adafruit_gps
    try:
        gps = adafruit_gps.GPS_GtopI2C(board.STEMMA_I2C(), debug=False)
    except:
        return None

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    
    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")
    return gps

def print_gps_data(gps):
    print(f"GPS fixed:{gps.has_fix}")
    if gps.timestamp_utc != None:
        print(f"GPS TS:{gps.timestamp_utc}")
    if gps.latitude != None:
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
    if gps.longitude != None:
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
    if gps.fix_quality != None:
        print("Fix quality: {}".format(gps.fix_quality))
    if gps.satellites is not None:
        print("# satellites: {}".format(gps.satellites))
    if gps.altitude_m is not None:
        print("Altitude: {} meters".format(gps.altitude_m))
    if gps.speed_knots is not None:
        print("Speed: {} knots".format(gps.speed_knots))
    if gps.track_angle_deg is not None:
        print("Track angle: {} degrees".format(gps.track_angle_deg))
    if gps.horizontal_dilution is not None:
        print("Horizontal dilution: {}".format(gps.horizontal_dilution))
    if gps.height_geoid is not None:
        print("Height geo ID: {} meters".format(gps.height_geoid))

def gps_set_time(gps):
    if gps.has_fix:
        import rtc
        rtc.RTC().datetime = gps.timestamp_utc

print("Start...")

print("Get GPS...")
gps = get_gps()
if gps == None:
    print("No GPS found...")
else:
    print("GPS found...")

print("Release displays...")

release_displays()

matrix = get_matrix()

print("Got matrix...")

display = get_display(matrix)

print("Got display...")

font = get_font()

print("Got font...")

label = get_label(font)

print("Got label...")

print("Show:")

display.root_group = label

if gps != None:
    print_gps_data(gps)

#print(f"Current time:{time.localtime()}")

while(True):
    if gps != None:
        if gps.update():
            print(f"GPS update registered...")
            print_gps_data(gps)
            gps_set_time(gps)
    year_now, month_now, day_now, hour_now, minute_now, second_now, tm_wday, tm_yday, tm_isdst = time.localtime()
    label.text = f"{hour_now}:{minute_now}:{second_now}"
    time.sleep(1)
