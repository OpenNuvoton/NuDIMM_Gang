/***************************************************************************//**
 * @file     targetdev.h
 * @brief    ISP support function header file
 * @version  0x32
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2021 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#ifndef __TARGET_H__
#define __TARGET_H__

#ifdef __cplusplus
extern "C"
{
#endif

// Nuvoton MCU Peripheral Access Layer Header File
#include "NuMicro.h"
#include "isp_user.h"

#define Config0         FMC_CONFIG_BASE
#define Config1         (FMC_CONFIG_BASE+4)

#define FMC_BLOCK_SIZE           (FMC_FLASH_PAGE_SIZE * 4UL)

int FMC_Proc(unsigned int u32Cmd, unsigned int addr_start, unsigned int addr_end, unsigned int *data);
int FMC_Read_User(unsigned int u32Addr, unsigned int *data);
void WriteData(unsigned int addr_start, unsigned int addr_end, unsigned int *data);
void ReadData(unsigned int addr_start, unsigned int addr_end, unsigned int *data);
int EraseAP(unsigned int addr_start, unsigned int size);
void GetDataFlashInfo(uint32_t *pu32Addr, uint32_t *pu32Size);

#endif  /* __TARGET_H__ */
