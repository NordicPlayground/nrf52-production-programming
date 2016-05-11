# Running this test
1. Flash hex/test_ctrlap_protection.hex to device using your programming tool.
2. Reset the device. Now [Access Port Protection](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/dif.html?cp=1_3_0_14_1#concept_udr_mns_1s) is enabled on the device and the Debug Access Port (DAP) is completly locked to the outside world.
3. Try to connect (or do any operation through the DAP of the device) and note that the chip is locked.
4. Unlock the chip using your programming tool.
5. Verify operations can now be done through the DAP of the device.

# Troubleshooting
*  Access port protection is not enabled until the correct word in the UICR is written AND the chip is reset.
*  Many mistakes happen when devices are being programmed in production. If an incorrect firmware image is flashed to a device, and it locks the device, the programming tool must be able to unlock the device to flash the correct firmware image. Other cases may be protection was enabled too early, etc...
