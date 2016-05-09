# nRF52832 Production Programming White Paper
Version 1.1

## Introduction
This white paper provides information regarding downloadloading software to nRF52 Series devices, and is intended for developers of flash download tools.  

The [nRF52 Series](https://www.nordicsemi.com/Products/nRF52-Series-SoC) is a family of highly flexible, multi-protocol, system-on-chip (SoC) devices for ultra-low power wireless applications. It is built around an ARM Cortex M4F CPU. It implements the CoreSight architecture and follows the standard SWD protocol as defined by ARM, with a standard Debug Port (DP) and Debug Access Port (DAP).  

The following information offers a high level programming flow stressing important details specific to nRF52 series devices. A robust way to program devices is described, and in many cases steps can be skipped if assumptions can be made (i.e. the chip has never been programmed before and it's flash is completely erased, the chip is unprotected, etc…). This guide is meant to serve as a starting point for nRF52 device support in production tools and is intended to accelerate the engineering process of supporting nRF52 devices.

## This paper does not...
*  Explain standards such as ARM, CoreSight, SWD, etc...

## nRF52 high-level programming flow
![Programming Process](https://github.com/NordicSemiconductor/nrf52-production-programming/blob/master/resources/programming_process.png)

## Programming
nRF52 series devices incorporate a 32-bit microcontroller. Therefore, each of the following operations should be considered a 32-bit operation. nRF52 series devices use flash based non-volatile memory (NVM) in the Code Flash and UICR [memory regions](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/memory.html?cp=1_3_0_6#memory).  

The [Debug and trace](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/dif.html?cp=1_3_0_14#debugandtrace) module provides access to the on-chip debug functionality. This is a standard two-pin serial wire debug (SWD) interface as defined by ARM™. Important: The SWDIO line has an internal pull-up resistor and the SWDCLK line has an internal pull-down resistor.  

See [NVMC Electrical Specification](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/nvmc.html?cp=1_3_0_9_7#unique_1869347048) for detailed specs regarding timing for write/erase operations etc… An example of the information here is that it takes the [NVMC](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/nvmc.html?cp=1_3_0_9#concept_pcl_wbz_vr) 67.5 (typical) to 338 microseconds (max) to write one word in flash, and it takes between 6.72 and 295.3 milliseconds to erase all flash. Based on this information ideal run times of flash programming algorithms can be calculated, and benchmarks to aim for can be determined, (i.e. the best possible time to write the entire flash of an nRF52832 device is approximately 8.85 seconds. [(512 * 1024) / 4 * (67.5 * 10^-6)]).  

There are 128 pages in the Code flash region of the nRF52832, and each page is 0x1000 (4096) bytes. So there is a total of 512 kB of Code flash.

#### 1.1 Connect
Use the standard SWD ARM™ CoreSight DAP protocol to enter [Debug Interface (DIF) mode](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/dif.html?cp=1_3_0_14_2#debuginterfacemode). A standard Debug Access Port (DAP) as provided by ARM™ is used and the Debug Port (DP) is in an always on domain to secure that the CxxxPWRUPREQ can be issued even if the device is in System OFF mode. Before the external debugger can access the CPU it must first request and make sure that the appropriate power domains are powered up – this is handled using the built in CxxxPwrUPREQ and CxxxPWRUPACK feature found in the ARM CoreSight DAP. As long as the debugger is requesting the debug domain or the complete system to be powered up, the device will be in debug interface mode.

#### 1.2 Check if access port protection is enabled (if APPROTECT)
The [CTRL-AP - Control Access Port](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.0/dif.html?cp=1_3_0_14_1#concept_udr_mns_1s) is a custom access port that enables control of the device even if the other access ports in the DAP are being disabled by access port protection. If access port protection has been enabled in the APPROTECT register (0x10001208) of the UICR, then the debugger's read/write access to all CPU registers and memory mapped addresses is blocked.  

Using the standard SWD ARM™ CoreSight DAP protocol:
*  Select/connect to the control access port. This access port is at index 0x01.
*  Read the APPROTECTSTATUS register (0x00C) of the CTRL-AP. If the least significant bit of this register is ‘0’, then access port protection is enabled. If it is ‘1’, then access port protection is not enabled. Proceed to steps 4.2.1 or 4.2.2 accordingly.

#### Access port protection is enabled (protected)
If access port protection is enabled on the device, access port 0 is unavailable. The only way to 'reopen/unlock' the device is to issue an ERASEALL command via the CTRL-AP access port, and then issue a reset via the CTRL-AP. This will erase the entire Code Flash and UICR area of the device, in addition to the entire RAM. Note: This method of erasing is slower than performing an erase all with the NVMC since it also must erase all RAM, but if access port protection is enabled, it is the **only** way to unlock the device.

###### 1.2.1 Erase all via CTRL-AP
Using the standard SWD ARM™ CoreSight DAP protocol, and while the CTRL-AP is still selected by the DP:
*  Write the value 0x00000001 to the ERASEALL register (0x004) of the CTRL-AP. This will start the ERASEALL operation which erases all FLASH and RAM on the device.
*  Read the ERASEALLSTATUS register (0x008) of the CTRL-AP until the value is 0x00000000. When this value is read the ERASEALL operation has completed.
*  Write the value 0x00000000 to the ERASEALL register (0x004) of the CTRL-AP. This is necessary after erase all has finished.
*  Write the value 0x00000001 to the RESET register (0x000) to issue a “soft reset” to the device and complete the erase & unlocking of the chip.
*  Write the value 0x00000000 to the RESET register (0x000).
*  Now access port 0x0 is available for use.
	
###### 1.2.2 Halt CPU
Use the standard SWD ARM™ CoreSight DAP protocol to issue a Halt command to the microcontroller.

###### 1.2.3 Read FICR
Factory information configuration registers (FICR) are pre-programmed in the factory and cannot be erased by the user. These registers contain chip-specific information and configuration.  

Using the standard SWD ARM™ CoreSight DAP protocol: 
*  Read the CODEPAGESIZE register (0x10000010) of the FICR. The value of this register will contain the code memory page size (in hexadecimal format, so 0x00001000 stored in this register corresponds to a page size of 4096 bytes).
*  Read the CODESIZE register (0x10000014) of the FICR. The value of this register will contain the number of pages in code memory (in hexadecimal format, so 0x0000080 stored in this register corresponds to 128 total pages in flash memory). Note: Total flash memory (in bytes) = CODEPAGESIZE * CODESIZE.
This information will be used later to determine the valid range of addresses to program.

#### Access port protection is not enabled (not protected)
This means that the UICR has not been previously configured to enable access port protection. In some cases you may assume that the entire flash has already been erased. If you are confident that the flash is already erased (the device has never been programmed before) skip to section 4.4. Important: The NVMC is only able to write bits in the NVM that are erased (set to ‘1’).
The Non-volatile memory controller (NVMC) is used for writing and erasing all flash memory. Before a write can be performed the NVM must be enabled for writing in CONFIG.WEN. Similarly, before an erase can be performed the NVM must be configured for erasing in CONFIG.EEN. The CPU is halted when the NVMC is performing a write/erase operation. User must check the Ready flag to make sure the NVMC is not busy (on-going write or erase operation) before performing an operation with the NVMC.

###### 1.2.1 Read FICR
Same as in section 4.2.3 Read FICR above in section “Access port protection is enabled (protected).” See above.

###### 1.2.2 Halt CPU
Same as in section 4.2.2 Halt CPU above in section “Access port protection is enabled (protected).” See above. Note: An application running on the device that was previously programmed may use the watch dog timer (WDT). If this is the case the WDT will be paused when the CPU is halted by default.

###### 1.2.3 Disable block protection (BPROT)
See section 11 Block protection (BPROT). The mechanism used to protect NVM from erroneous application code erasing/writing to protected pages in Code FLASH will cause the CPU to hard fault if an erase or write to a protected page is attempted. This can be turned off when in debug mode by configuring the DISABLEINDEBUG register.  

Using the standard SWD ARM™ CoreSight DAP protocol:
*  Write the value 0x00000001 to the DISABLEINDEBUG register (0x40000608) of the BPROT. This will disable the block protection mechanism in debug mode.

#### 1.3 Erase all or erase pages (optional)
An erase all operation takes the same amount of time as erasing three pages one by one. As there are 128 total pages of flash, erasing all will be more efficient than erasing page by page. In the case that a region of the chip has been pre-programmed you can erase the flash you intend to program page by page and then write those addresses with data – leaving pre-programmed flash untouched. Note: If you are sure that the entire flash of the device is erased (0xFFFFFFFF) then the erase step may be skipped completely to save time.  

###### Erase-all
Using the standard SWD ARM™ CoreSight DAP protocol:
*  Write the value 0x00000002 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM for erasing.
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001. When this value is read the NVMC is ready and not currently performing any operations.
*  Write the value 0x00000001 to the ERASEALL register (0x4001E50C) of the NVMC. This will erase all NVM including UICR registers but will not erase the FICR (FICR should never be erased). 
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001 before continuing to ensure the erase all operation has completed.
*  Write the value 0x00000000 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM back to read only.

###### Erasing page by page
Using the standard SWD ARM™ CoreSight DAP protocol:
*  Write the value 0x00000002 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM for erasing.
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001. When this value is read the NVMC is ready and not currently performing any operations.
*  Write the value of the address of the first word in desired page to be erased to the ERASEPAGE register (0x4001E508). This will start the erase of a page in Code Flash. Use the data read from the FICR for information about the total code size of the device you are programming, number of pages and page size. Attempts to erase pages that are outside the Code Flash area may result in undesirable behavior. If the page to be erased is the UICR page, write 0x00000001 to ERASEUICR register (0x4001E514) instead of erasing as you would for a normal page in flash.
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001 before continuing to ensure the erase page operation has completed.
*  Continue erasing page by page until done. Note that if you are erasing more than 3 pages an erase all will be much faster.
*  Write the value 0x00000000 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM back to read only.

#### 1.4 Write data
When writing is enabled, the NVM is written by writing a word to a word-aligned address in the CODE or UICR. Only word-aligned writes are allowed. Byte or half-word-aligned writes will result in a hard fault.  

To write the data into flash, using the standard SWD ARM™ CoreSight DAP protocol: 
*  Write the value 0x00000001 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM for writing.
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001. When this value is read the NVMC is ready and not currently performing any operations.
*  Write the data to the desired address. 
*  Read the READY register (0x4001E400) of the NVMC until the value is 0x00000001 before continuing to ensure the write operation has completed.
*  Continue writing and then reading the READY register (0x4001E400) as necessary.
*  Write the value 0x00000000 to the CONFIG register (0x4001E504) of the NVMC. This will configure the NVM back to read only.
The ranges of writeable addresses are:
*  UICR addresses (located in addresses 0x10001000 through 0x10002000). Important: These addresses must be writeable by the production programming tools. Users expect these to be written when the hex file is programmed by the programmer – it is bad practice for application to write these values at run time.
*  All program flash (located in addresses 0x00000000 through ((CODESIZE * CODEPAGESIZE) – 0x00000004)
Different methods can be used to write flash. For the nRF52 a good flash algorithm should take around 10 seconds to write the entire flash. If you are not able to reach this time please contact us for assistance.

#### 1.5 Verify (optional)
To verify the contents of flash use the standard SWD ARM™ CoreSight DAP protocol:
*  Read every address written and compare with the expected value.
Important: It is possible that the hex file being programmed will enable access port (read-back) protection that will make it impossible to verify the contents of flash. This protection will only take effect after a reset is applied. Make sure not to reset between steps 4.7 Write data and 4.8 Verify.

#### 1.6 Disconnect
Use the standard SWD ARM™ CoreSight DAP interface to disable debugger interface mode.
Note that here we assume you are programming a bare IC. There needs to be a hard reset after programming which can only be guaranteed by a power cycle. This is needed to take the device out of debug interface mode as well as other things. When programming a bare IC there is a guaranteed power cycle so there is no need to worry about this.

#### Conclusion
Some things to think about:
*  The bottleneck in optimizing the flash algorithms is writing words in flash. The absolute minimum time to write the entire flash is around 8.85 seconds, so optimizing out steps like erasing entire flash (6.72 ms), checking for different types of protection and reading registers in FICR (constant time) will not provide any real benefit.
*  The steps above should cover most corner cases – things we took into consideration when coming up with this programming flow are:
  *  Access port protection was enabled by a previously programmed application on the device that needs to be overwritten for any reason.
  *  Block protection was enabled by a previously programmed application on the device that may need to be overwritten or a different region of flash may need to be programmed while keeping the existing program unchanged.
  *  A watchdog timer has been enabled by a previously programmed application on the device and may reset the device (note that not all edge cases are covered here).  
