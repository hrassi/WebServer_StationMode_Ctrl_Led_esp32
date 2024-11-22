this script will first connect dynamically to the network as station mode and save
the network settings given by the router to the esp then disconect and reconect with
a predefine static  ip address 192.168.18.200 and keeping other router settings the same.
like this we are sure to have always the same ip address for the esp32 : 192.168.18.200

now if we open browser to 192.168.18.200 it will open the server page of the esp
we can control with the server page the different status of the led : 
    onboard led off :      http://192.168.18.200/control?LED=0
    onboard led on  :      http://192.168.18.200/control?LED=1
    onbrd ld BlinkSlow :   http://192.168.18.200/control?LED=2
    onbrd ld BlinkFast :   http://192.168.18.200/control?LED=3
    
the opensoket protocol (websocket) give us a real time control of the led

we used the timer build in library of esp32 (import machine) to blink the led
without interupting our script(it works like thread and interupt mode)

to activate the led with siri : go to shortcut then
Tap the + icon to create a new shortcut.
Add the "Get Contents of URL" action:
Tap Add Action.
Search for and select "Get Contents of URL".
In the URL field, enter the URL to turn the LED on, e.g., http://192.168.18.200/control?LED=1
Name the shortcut:
Tap the shortcut name at the top and name it "Turn LED On."
Save the shortcut.

do the same and create shortcut for led off

you can now call siri to turn the led on and off and blink fast and blink slow

