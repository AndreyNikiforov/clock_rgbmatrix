
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

print("Start...")

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

while(True):
    pass
