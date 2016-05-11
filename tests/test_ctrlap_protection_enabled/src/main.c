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
/** @test tests/test_ctrlap_protection_enabled/src/main.c
 *
 * @brief Locks the device (after this hex file is loaded and the device is reset).
 *
 * This file contains the source code for the test_ctrlap_protection_enabled hex file provided in ../hex/
 * See the corresponding README for expected behavior.
 */

#include <stdint.h>

#include "nrf.h"

// Enable Access Port protection on the device (effective after a reset).
const uint32_t UICR_APPROTECT  __attribute__((at(0x10001208))) __attribute__((used)) = 0xFFFFFF00;

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
