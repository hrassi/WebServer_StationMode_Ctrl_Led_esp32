# ************************
# Configure the ESP32 wifi
# as STAtion mode with a predifined static ip address for the esp32

import network
import time
import socket
import machine

# LED setup
led = machine.Pin(2, machine.Pin.OUT)
led.off()

# Wi-Fi credentials
ssid = "Rassi Net-2.4G"
password = "Holyshit"

# Step 1: Connect dynamically to retrieve network settings
sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('Connecting dynamically to the network...')
    sta.active(True)
    time.sleep(1)
    sta.connect(ssid, password)
    while not sta.isconnected():
        time.sleep(1)
print("Dynamic Config:", sta.ifconfig())

# Step 2: Retrieve and store the dynamically assigned network settings
ip, subnet, gateway, dns = sta.ifconfig()

# Step 3: Disconnect and reconnect using a static IP
sta.disconnect()
print("Reconnecting with a static IP...")
static_ip = "192.168.18.200"
sta.ifconfig((static_ip, subnet, gateway, dns))
time.sleep(1)
sta.connect(ssid, password)
while not sta.isconnected():
    time.sleep(1)
print("Static Config:", sta.ifconfig())

# Global variables for state and timer
led_timer = None
led_state = "OFF"

def stop_blinking():
    """
    Stops any active LED blinking by deactivating the timer.
    """
    global led_timer
    if led_timer:
        led_timer.deinit()
        led_timer = None
        print("Blinking stopped.")

def start_blinking(period):
    """
    Starts blinking the LED with the given period in milliseconds.
    """
    global led_timer
    stop_blinking()  # Ensure no existing blink is active
    led_timer = machine.Timer(-1)
    print(f"Starting blinking with period: {period}ms")
    led_timer.init(period=period, mode=machine.Timer.PERIODIC, callback=lambda t: led.value(1 - led.value()))

def web_page():
    """
    Returns the HTML page with the current LED state.
    """
    html_page = f"""   
      <html>   
      <head>   
       <meta content="width=device-width, initial-scale=1" name="viewport"></meta>   
      </head>   
      <body>   
        <center><h2>ESP32 Web Server in MicroPython</h2></center>   
        <center>   
         <form>   
          <button name="LED" type="submit" value="1"> LED ON </button>   
          <button name="LED" type="submit" value="0"> LED OFF </button>   
          <button name="LED" type="submit" value="2"> Slow Blink </button>   
          <button name="LED" type="submit" value="3"> Fast Blink </button>   
         </form>   
        </center>   
        <center><p>LED is now <strong>{led_state}</strong>.</p></center>   
      </body>   
      </html>"""
    return html_page

# Setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got connection from", addr)
    
    # Read request
    request = conn.recv(1024)
    request = str(request)
    print("Request:", request)
    
    # Parse request
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    slow_blinking = request.find('/?LED=2')
    fast_blinking = request.find('/?LED=3')
    
    # Handle LED commands
    if led_on == 6:
        stop_blinking()
        led.value(1)
        led_state = "ON"
        print("LED ON")
    elif led_off == 6:
        stop_blinking()
        led.value(0)
        led_state = "OFF"
        print("LED OFF")
    elif slow_blinking == 6:
        start_blinking(1000)  # Slow blink: 1 second
        led_state = "Slow Blink"
        print("Slow blinking started")
    elif fast_blinking == 6:
        start_blinking(100)  # Fast blink: 200 ms
        led_state = "Fast Blink"
        print("Fast blinking started")
    
    # Send response
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

