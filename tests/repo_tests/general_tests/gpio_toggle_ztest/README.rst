Overview
********

This test verifies the correct GPIO functionality using the Ztest and GPIO commands.
The gpio0 controller switches gpio port with connectd LED and uses other port to verify
the output state after toggle-command.


Setup
********
The test configures two GPIO pins:
- GPIO_OUT_PIN (13) - output pin to toggle LED
- GPIO_IN_PIN (9) - auxiliary input pin to check GPIO_OUT_PIN state
