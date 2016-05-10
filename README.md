# nrf52-production-programming
A guide to programming nRF52 series devices in production, along with test cases to verify implementation. For detailed information on the programming process, see white-paper.md.

# Before reading this guide
Know your options, we are partnered with [Elnec](http://www.elnec.com/), [Hi-Lo](http://www.hilo.systems/), and [SEGGER](https://www.segger.com/production-programmers.html) and they fully support programming nRF52 series devices in production.

###### Elnec
*  [Production Programmers](http://www.elnec.com/en/products/production-programmers/). Gang programmers and in system programmers (ISP).

###### Hi-Lo Systems
*  [Production Programmers](http://www.hilo.systems/programmer.aspx). Gang programmers.
*  [Automated Programming Systems](http://www.hilo.systems/system/programming%20system.aspx).
*  [Programming Service](http://www.hilo.systems/service/introduction.aspx).
*  [Hi-Lo Nordic Dev Zone Blog Post](https://devzone.nordicsemi.com/blogs/767/programming-services-hi-lo-electronics-in-corporat/).

###### SEGGER
*  [Production Programmers](https://www.segger.com/production-programmers.html). ISP programmers that program one device at a time. Ease the implementation into a production site by allowing the flash programming to be triggered manually or remotely.

## [nRF52 Product Specification](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52/dita/nrf52/chips/nrf52832_ps.html?cp=1_3_0)
*  CPU, Memory, NVMC, BPROT, UICR, DIF are important sections to read.
*  Power & Clock are less important but should be skimmed.

## Test cases
*  Provided tests in this repository will help verify that your programming algorithms cover important edge cases (not complete test coverage by any means).

## [Reference Hardware Design Files](http://www.nordicsemi.com/eng/nordic/download_resource/50980/3/35868157)
*  May provide some guidance for pin connections etc...

## Programming process high-level flow
![Programming Process](https://github.com/NordicSemiconductor/nrf52-production-programming/blob/master/resources/programming_process.png)
