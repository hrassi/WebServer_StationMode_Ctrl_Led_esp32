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

