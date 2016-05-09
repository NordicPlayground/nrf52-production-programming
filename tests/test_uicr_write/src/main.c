/* Copyright (c) 2016 Nordic Semiconductor. All Rights Reserved.
 *
 * The information contained herein is property of Nordic Semiconductor ASA.
 * Terms and conditions of usage are described in detail in NORDIC
 * SEMICONDUCTOR STANDARD SOFTWARE LICENSE AGREEMENT.
 *
 * Licensees are granted free, non-transferable use of the information. NO
 * WARRANTY of ANY KIND is provided. This heading must NOT be removed from
 * the file.
 *
 */
/** @test tests/test_uicr_write/src/main.c
 *
 * @brief Tests that programming tool can properly write to the UICR area of FLASH.
 *
 * This file contains the source code for the test_uicr_write hex file provided in ../hex/
 * See the corresponding README for expected behavior.
 */

#include <stdint.h>

#include "nrf.h"

// This address/data will be placed in the generated .hex file and should be written when the application is flashed.
const uint32_t UICR_CUSTOMER_0 __attribute__((at(0x10001080))) __attribute__((used)) = 0xDEADBEEF;

/**@brief Function for application main entry.
 */
int main(void)
{
    // Enter main loop.
    for (;;)
    {
        // Loop.
    }
}
