/***************************************************************************//**
 * @file     targetdev.c
 * @brief    ISP support function source file
 * @version  0x32
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2021 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#include "NuMicro.h"
#include "targetdev.h"
#include "isp_user.h"

int FMC_Read_User(unsigned int u32Addr, unsigned int *data)
{
    return FMC_Proc(FMC_ISPCMD_READ, u32Addr, u32Addr + 4, data);
}

void WriteData(unsigned int addr_start, unsigned int addr_end, unsigned int *data)  // Write data into flash
{
    FMC_Proc(FMC_ISPCMD_PROGRAM, addr_start, addr_end, data);
    return;
}

void ReadData(unsigned int addr_start, unsigned int addr_end, unsigned int *data)  // Write data into flash
{
    FMC_Proc(FMC_ISPCMD_READ, addr_start, addr_end, data);
    return;
}

int FMC_Proc(unsigned int u32Cmd, unsigned int addr_start, unsigned int addr_end, unsigned int *data)
{
    unsigned int u32Addr, Reg;
    uint32_t u32TimeOutCount = SystemCoreClock;

    for(u32Addr = addr_start; u32Addr < addr_end; data++)
    {
        FMC->ISPCMD = u32Cmd;
        FMC->ISPADDR = u32Addr;

        if(u32Cmd == FMC_ISPCMD_PROGRAM)
        {
            FMC->ISPDAT = *data;
        }

        FMC->ISPTRG = 0x1;
        __ISB();

        /* Wait ISP cmd complete */
        while(FMC->ISPTRG & FMC_ISPTRG_ISPGO_Msk)
        {
            if(--u32TimeOutCount == 0) /* 1 second time-out */
                return -1;
        }

        Reg = FMC->ISPCTL;

        if(Reg & FMC_ISPCTL_ISPFF_Msk)
        {
            FMC->ISPCTL = Reg;
            return -1;
        }

        if(u32Cmd == FMC_ISPCMD_READ)
        {
            *data = FMC->ISPDAT;
        }

        if(u32Cmd == FMC_ISPCMD_PAGE_ERASE)
        {
            u32Addr += FMC_FLASH_PAGE_SIZE;
        }
        else
        {
            u32Addr += 4;
        }
    }

    return 0;
}

/* Supports maximum 1M (APROM) */
uint32_t GetApromSize()
{
    /* The smallest of APROM size is 2K. */
    uint32_t size = 0x800, data;
    int result;

    do
    {
        result = FMC_Read_User(size, &data);

        if(result < 0)
        {
            return size;
        }
        else
        {
            size *= 2;
        }
    }
    while(1);
}

/* Data Flash is shared with APROM.
   The size and start address are defined in CONFIG1. */
void GetDataFlashInfo(uint32_t *pu32Addr, uint32_t *pu32Size)
{
    uint32_t u32Data, u32Data2;
    *pu32Size = 0;
    FMC_Read_User(Config0, &u32Data);
		
    if((u32Data & 0x01) == 0)  
    {
        FMC_Read_User(Config1, &u32Data2);

        u32Data2 &= 0x000FFFFF;

        if(u32Data2 > g_u32ApromSize || u32Data2 & (FMC_FLASH_PAGE_SIZE - 1)) 
        {
            u32Data2 = g_u32ApromSize;
        }

        *pu32Addr = u32Data2;
        *pu32Size = g_u32ApromSize - u32Data2;
    }
    else
    {
        *pu32Addr = g_u32ApromSize;
        *pu32Size = 0;
    }
}

int EraseAP(unsigned int addr_start, unsigned int size)
{
    unsigned int u32Addr, u32Cmd, u32Size;
    int32_t i32Size;
    uint32_t u32TimeOutCount = FMC_TIMEOUT_ERASE;

    u32Addr = addr_start;
    i32Size = (int32_t)size;

    while(i32Size > 0)
    {
        if((size >= FMC_BANK_SIZE) && !(u32Addr & (FMC_BANK_SIZE - 1)))
        {
            u32Cmd = FMC_ISPCMD_BANK_ERASE;
            u32Size = FMC_BANK_SIZE;
        }
        else if((size >= FMC_BLOCK_SIZE) && !(u32Addr & (FMC_BLOCK_SIZE - 1)))
        {
            u32Cmd = FMC_ISPCMD_BLOCK_ERASE;
            u32Size = FMC_BLOCK_SIZE;
        }
        else
        {
            u32Cmd = FMC_ISPCMD_PAGE_ERASE;
            u32Size = FMC_FLASH_PAGE_SIZE;
        }

        FMC->ISPCMD = u32Cmd;
        FMC->ISPADDR = u32Addr;
        FMC->ISPTRG = FMC_ISPTRG_ISPGO_Msk;
        __ISB();

        while(FMC->ISPTRG & FMC_ISPTRG_ISPGO_Msk)    /* Wait for ISP command done. */
        {
            if(--u32TimeOutCount == 0)
                return -2;
        }

        if(FMC->ISPCTL & FMC_ISPCTL_ISPFF_Msk)
        {
            FMC->ISPCTL |= FMC_ISPCTL_ISPFF_Msk;
            return -1;
        }

        u32Addr += u32Size;
        size -= u32Size;
        i32Size = (int32_t)size;
    }

    return 0;
}