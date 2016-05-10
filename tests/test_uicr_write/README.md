# Running this test
1. Flash hex/test_uicr_write.hex to device using your programming tool.
2. Read address 0x10001080. Verify the read value is 0xDEADBEEF.

# Troubleshooting
If a different value was read than expected the programming tool did not write the [UICR](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/nvmc.html?cp=1_3_0_9_2#concept_etv_shz_vr) region of memory properly.
