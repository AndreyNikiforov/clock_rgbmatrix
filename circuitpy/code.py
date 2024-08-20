import time
import board
import displayio
import rgbmatrix
import framebufferio
import wifi
import os
import socketpool
import struct
import rtc
from collections import OrderedDict

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

def _parse_iso_utc(iso: str) -> int:
    """ parse ISO w/o TZ as UTC into unix epoch(sec) """
    year = int(iso[0:4])
    month = int(iso[5:7])
    day = int(iso[8:10])
    hour = int(iso[11:13])
    minute = int(iso[14:16])
    second = int(iso[17:19])
    return time.mktime((year, month, day, hour, minute, second,0,-1,-1))


# stealing from https://github.com/evindunn/circuitpython_tzdb/blob/main/tzdb/_timezone.py
def _load_tz(tz_name: str):
# relative imports do not work
#    pkg = __import__(
#            "_zones." + tz_name.replace("/", "."), globals(), locals(), ["tz_data"], 1
#        )
#    sorted_kv_pairs = sorted(
#        pkg.tz_data.items(),
#        key=lambda kv_pair: _parse_iso_utc(kv_pair[0]),
#    )
    from _zones.America.Los_Angeles import tz_data
    sorted_kv_pairs = sorted(
        tz_data.items(),
        key=lambda kv_pair: _parse_iso_utc(kv_pair[0]),
    )
    return OrderedDict(sorted_kv_pairs)

def _find_offset(tz_data, ts: int) -> int:
    offset = 0
    for iso_value, offset_value in tz_data.items():
        if _parse_iso_utc(iso_value) <= ts:
            offset = offset_value
        else:
            break
    return offset
    
tz_data = _load_tz("America/Los_Angeles")

# https://learn.adafruit.com/adafruit-esp32-s3-feather/circuitpython-internet-test
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#print("Available WiFi networks:")
#for network in wifi.radio.start_scanning_networks():
#    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#                                             network.rssi, network.channel))
#wifi.radio.stop_scanning_networks()
try:
    print(f"Connecting to {os.getenv('WIFI_SSID')}")
    # throws if cannot connect
    wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
    print(f"Connected to {os.getenv('WIFI_SSID')}")
    print(f"My IP address: {wifi.radio.ipv4_address}")
except:
    print("Cannot connect to Wifi")
    raise

# ntp https://github.com/adafruit/Adafruit_CircuitPython_NTP/blob/main/adafruit_ntp.py
# https://github.com/adafruit/circuitpython/blob/main/tests/circuitpython-manual/socketpool/datagram/ntp.py
NTP_TO_UNIX_EPOCH = 2208988800  # 1970-01-01 00:00:00
PACKET_SIZE = const(48)

pool = socketpool.SocketPool(wifi.radio)
socket_address = pool.getaddrinfo("0.adafruit.pool.ntp.org", 123)[0][4]
with pool.socket(
    socketpool.SocketPool.AF_INET,
    socketpool.SocketPool.SOCK_DGRAM) as socket:

    socket.settimeout(10)

    packet = bytearray(PACKET_SIZE)
    packet[0] = 0b00100011  # Not leap second, NTP version 4, Client mode
    for i in range(1, PACKET_SIZE):
        packet[i] = 0

    local_send_ns = time.monotonic_ns()  # expanded
    socket.sendto(packet, socket_address)
    socket.recv_into(packet)
    local_recv_ns = time.monotonic_ns()  # was destination

    # parse packet
    poll = struct.unpack_from("!B", packet, offset=2)[0]
    srv_recv_s, srv_recv_f = struct.unpack_from("!II", packet, offset=32)
    srv_send_s, srv_send_f = struct.unpack_from("!II", packet, offset=40)

    print(f"poll:{poll}")
    print(f"srv_recv_s, srv_recv_f:{srv_recv_s}, {srv_recv_f}")
    print(f"srv_send_s, srv_send_f:{srv_send_s}, {srv_send_f}")

    # Convert the server times from NTP to UTC for local use
    srv_recv_ns = (srv_recv_s - NTP_TO_UNIX_EPOCH) * 1_000_000_000 + (
        srv_recv_f * 1_000_000_000 // 2**32
    )
    srv_send_ns = (srv_send_s - NTP_TO_UNIX_EPOCH) * 1_000_000_000 + (
        srv_send_f * 1_000_000_000 // 2**32
    )
    # Calculate (best estimate) offset between server UTC and board monotonic_ns time
    clock_offset = (
        (srv_recv_ns - local_send_ns) + (srv_send_ns - local_recv_ns)
    ) // 2

    current_time = (time.monotonic_ns() + clock_offset) // 1_000_000_000
    # set rtc https://learn.adafruit.com/super-simple-sunrise-lamp/code
    rtc.RTC().datetime = time.localtime(current_time)
    print(f"Time set to: {time.localtime()}")

    # get tz https://github.com/evindunn/circuitpython_tzdb
    # calculate time with offset

# Loop forever so you can enjoy your image
while True:
    now: int = int(time.time())
    offset = _find_offset(tz_data, now)
    #int(f"Now: {now}, Offset: {offset}")
    now_local: int = now + int(offset * 60 * 60) # need conversion to int here! otherwise float is used and it has issues later
    year_now, month_now, day_now, hour_now, min_now, sec_now, wd_now, yd_now, isdst_now = time.localtime(now_local)
    hour_high = hour_now // 10
    hour_low = hour_now % 10
    min_high = min_now // 10
    min_low = min_now % 10
    sec_high = sec_now // 10
    sec_low = sec_now % 10
    #print(f"{now:d}: {hour_now}={hour_high}-{hour_low} {min_now}={min_high}-{min_low} {sec_now}={sec_high}-{sec_low}")

    #change indexes
    tile_grid[0]=hour_high
    tile_grid[1]=hour_low
    tile_grid[2]=min_high
    tile_grid[3]=min_low
#    print(tile_grid.width)

    time.sleep(60-sec_now)
