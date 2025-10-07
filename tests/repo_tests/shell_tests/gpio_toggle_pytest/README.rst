Overview
********

This test verifies the correct GPIO functionality using the Pytes GPIO shell commands.
The gpio0 controller switches gpio port with connectd LED and uses other port to verify
the output state after toggle-command.


Setup
********
The test configures two GPIO pins:
- GPIO_OUT_PIN (13) - output pin to toggle LED
- GPIO_IN_PIN (9) - auxiliary input pin to check GPIO_OUT_PIN state


Shell console example
==========================
uart:~$ gpio devices
Device           Other names
gpio@60004000    gpio0
gpio@60004800    gpio1
uart:~$ gpio get gpio0 9
0
uart:~$ gpio toggle gpio0 13
uart:~$ gpio get gpio0 9
1
uart:~$ gpio toggle gpio0 13
uart:~$ gpio get gpio0 9
0