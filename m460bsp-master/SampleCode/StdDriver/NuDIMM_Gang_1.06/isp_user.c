/***************************************************************************//**
 * @file     isp_user.c
 * @brief    ISP command source file
 * @version  0x32
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2021 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#include <stdio.h>
#include <string.h>
#include "NuMicro.h"
#include "isp_user.h"
#include "i2c_transfer.h"
#include "ssd1306.h"
#include "HAL_TICK_CONTROL.h"
#include "targetdev.h"

// -----------DEBUG-------------

// -----------DEBUG-------------
#define DEBUG
#define i2c_delay 3000

uint8_t g_au8ResponseBuff[PACK_SIZE];

static uint8_t g_au8ApromBuf[FMC_FLASH_PAGE_SIZE];

uint32_t g_u32UpdateApromCmd;
uint32_t g_u32ApromSize, g_u32DataFlashAddr, g_u32DataFlashSize;

I2C_T * I2C_PORT[5] = {I2C0, I2C1, I2C2, I2C4, I2C3};
uint8_t port_boot_state[MAX_PORT];
uint8_t port_boot_addr[MAX_PORT];

static  uint8_t  I2C_TxData[65];
static  uint8_t  I2C_RxData_0[65];
static  uint8_t  I2C_RxData_1[65];
static  uint8_t  I2C_RxData_2[65];
static  uint8_t  I2C_RxData_3[65];
static  uint8_t  I2C_RxData_4[65];
static  uint8_t* I2C_RxData[5] = {I2C_RxData_0, I2C_RxData_1, I2C_RxData_2, I2C_RxData_4, I2C_RxData_3};

extern int view_mode;
extern unsigned char st[1024];

static  uint8_t  Verify_Data[65];
static  uint8_t  isNuvoton = 0;

uint32_t u32Data[PACK_SIZE / 4];
void check_boot(void);

static uint16_t Checksum(unsigned char *buf, int len)
{
    int i;
    uint16_t c;

    for(c = 0, i = 0 ; i < len; i++)
    {
        c += buf[i];
    }
		
    return (c);
}

int ParseCmd(uint8_t *pu8Buffer, uint32_t u8len)
{
    uint8_t *pu8Response;
    uint16_t u16Lcksum;
		uint8_t u8Lcmd, u8Lext;
    uint32_t u32srclen, u32i, u32StartAddress;
    uint8_t *pu8Src;
    pu8Response = g_au8ResponseBuff;
    pu8Src = pu8Buffer;
	
		uint32_t light_ctrl = 0xFFFF;
	
    u32srclen = u8len;
    u8Lcmd = inps(pu8Src);
    pu8Src += 1;
    u32srclen -= 1;
		u8Lext = inps(pu8Src);
    pu8Src += 1;
    u32srclen -= 1;
	
		memset(I2C_TxData, 0xFF, sizeof(I2C_TxData));
		memset(I2C_RxData_0, 0xFF, sizeof(I2C_RxData_0));
		memset(I2C_RxData_1, 0xFF, sizeof(I2C_RxData_1));
		memset(I2C_RxData_2, 0xFF, sizeof(I2C_RxData_2));
		memset(I2C_RxData_4, 0xFF, sizeof(I2C_RxData_4));
		memset(I2C_RxData_3, 0xFF, sizeof(I2C_RxData_3));
		
		memset(pu8Response, 0xFF, 64);

    if(u8Lcmd == CMD_GET_FWVER)
    {
        pu8Response[4] = FW_VERSION; /* version 2.3 */
			  pu8Response[3] = 0;
				pu8Response[2] = 0;
				goto out;
    }
    else if(u8Lcmd == CMD_GET_DEVICEID)
    {			
				pu8Response[3] = 0;
				pu8Response[2] = 0;
			
        pu8Response[7] = (uint8_t)((SYS->PDID >> 24) & 0xFF); 
				pu8Response[6] = (uint8_t)((SYS->PDID >> 16) & 0xFF);
				pu8Response[5] = (uint8_t)((SYS->PDID >> 8) & 0xFF);  
				pu8Response[4] = (uint8_t)(SYS->PDID & 0xFF);

        goto out;
    }
		else if(u8Lcmd == CMD_READ_CONFIG)
    {
				uint32_t u32Data, u32Data2;
			
        SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
				FMC_ENABLE_CFG_UPDATE();
			
				FMC_Read_User(Config0, &u32Data);
				FMC_Read_User(Config1, &u32Data2);
			
				pu8Response[11] = (uint8_t)((u32Data2 >> 24) & 0xFF); 
				pu8Response[10] = (uint8_t)((u32Data2 >> 16) & 0xFF);
				pu8Response[9] = (uint8_t)((u32Data2 >> 8) & 0xFF);  
				pu8Response[8] = (uint8_t)(u32Data2 & 0xFF);
			
				pu8Response[7] = (uint8_t)((u32Data >> 24) & 0xFF); 
				pu8Response[6] = (uint8_t)((u32Data >> 16) & 0xFF);
				pu8Response[5] = (uint8_t)((u32Data >> 8) & 0xFF);  
				pu8Response[4] = (uint8_t)(u32Data & 0xFF);
			
				pu8Response[3] = 0;
				pu8Response[2] = 0;
			
				FMC_DISABLE_CFG_UPDATE();
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
			
        goto out;
    }
    else if(u8Lcmd == CMD_CONNECT)
    { 
				pu8Response[2] = 0;
				pu8Response[3] = 0;
			
				pu8Response[7] = (uint8_t)((SYS->PDID >> 24) & 0xFF); 
				pu8Response[6] = (uint8_t)((SYS->PDID >> 16) & 0xFF);
				pu8Response[5] = (uint8_t)((SYS->PDID >> 8) & 0xFF);  
				pu8Response[4] = (uint8_t)(SYS->PDID & 0xFF);

        goto out;
    }
		else if(u8Lcmd == CMD_ERASE_APROM)
    { 
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
			
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				
				u32StartAddress = g_u32DataFlashAddr;
			
				if(g_u32DataFlashSize != 0)
				{
						int retc = EraseAP(g_u32DataFlashAddr + 4, g_u32DataFlashSize);
				}
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
        goto out;
    }
		else if(u8Lcmd == CMD_UPDATE_APROM)
    { 
				// write data into dataflash 
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
				if (inpb(pu8Src) != 0){
						u32srclen = inpb(pu8Src) - 5;
						pu8Src += 2;
				}
				else {
						u32srclen = inps(pu8Src + 1);
						pu8Src += 3;
				}
				u32StartAddress = inpw(pu8Src);
				pu8Src += 4;
				WriteData(u32StartAddress, u32StartAddress + u32srclen, (uint32_t *)(uint32_t)pu8Src);
			
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
        goto out;
    }
		else if(u8Lcmd == CMD_READ_APROM)
    { 				
				// read dataflash 
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
				if (inpb(pu8Src) != 0){
						u32srclen = inpb(pu8Src) - 1;
						pu8Src += 2;
				}
				else {
						u32srclen = inps(pu8Src + 1);
						pu8Src += 3;
				}
				u32StartAddress = inpw(pu8Src);
				ReadData(u32StartAddress, u32StartAddress + u32srclen, (uint32_t *)u32Data);
			
				pu8Response[3] = 0;
				pu8Response[2] = 0;
			
				for (int i = 0; i * 4 < u32srclen; i++){
						pu8Response[7 + i * 4] = (uint8_t)((u32Data[i] >> 24) & 0xFF); 
						pu8Response[6 + i * 4] = (uint8_t)((u32Data[i] >> 16) & 0xFF);
						pu8Response[5 + i * 4] = (uint8_t)((u32Data[i] >> 8) & 0xFF);  
						pu8Response[4 + i * 4] = (uint8_t)(u32Data[i] & 0xFF);
				}
			
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
        goto out;
    }
		else if((u8Lcmd & 0xF0) == CMD_ERASE_HUB){
				// ERASE 
				pu8Response[3] = 0;
				int ret = 0;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
								I2C_ext = 1;
						}
				}

				for (int j = 0; j < 7; j++)
				{
						I2C_TxData[j] = inpb(pu8Src + j);
				}
				ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x80, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 7, 0, 1);
				light_ctrl = 0x7FFF;
				pu8Response[3] = I2C_num;
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_WRITE_HUB){
				//WRITE
				pu8Response[2] = 0;
				pu8Response[3] = 0;
				int ret = 0; 
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				light_ctrl = 0x7FFF;						
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
								I2C_num |= (0x01 << i);
								light_ctrl -= (0x2 << (i * 3));
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
								I2C_ext = 1;
								light_ctrl -= (0x2 << (i * 3));
						}
				}

				unsigned int total_length = 0;
				unsigned int write_addr = 0;
				unsigned int dcount = 0;
				if (inpb(pu8Src) != 0){
						total_length = inpb(pu8Src + 1);
						pu8Src += 2;
				}
				else {
						total_length = inps(pu8Src + 1);
						pu8Src += 3;
				}
				write_addr = inpw(pu8Src);
				pu8Src += 4;

				while(total_length > 0){
						//printf("total_length = %d, head = %d\n", total_length, inpb(pu8Src));
						CLK_SysTickDelay(i2c_delay);
						dcount = (total_length > 56) ? 56 : total_length;
						I2C_TxData[0] = dcount + 5;
						I2C_TxData[1] = dcount;
						memcpy(&I2C_TxData[2], &write_addr, 4);
						for (int j = 0; j < dcount; j++){
								I2C_TxData[j + 6] = inpb(pu8Src + j);
						}
						//printf("write_addr = %d, dcount = %d\n", write_addr, dcount);
						ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x81, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, dcount + 6, 0, 1);
						total_length -= dcount;
						write_addr += dcount;
						pu8Src += dcount;
				}
				
				pu8Response[3] = I2C_num;
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_READ_HUB){
				//READ
				pu8Response[3] = 0;
				int ret = 0; 
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
								I2C_ext = 1;
						}
				}
				unsigned int total_length = 0;
				unsigned int read_addr = 0;
				unsigned int read_length = 0;
				unsigned int dcount = 0;
				if (inpb(pu8Src) != 0){
						total_length = inpb(pu8Src + 1);
						pu8Src += 2;
				}
				else {
						total_length = inps(pu8Src + 1);
						pu8Src += 3;
				}
				read_addr = inpw(pu8Src);
				pu8Src += 4;
				while(total_length > 0){
						dcount = (total_length > 60)? 60 : total_length;
						I2C_TxData[0] = 5;
						I2C_TxData[1] = dcount;
						memcpy(&I2C_TxData[2], &read_addr, 4);
						ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0xA1, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 6, 64, 1);
						for (int i = 0 ; i < MAX_PORT ; i++){
								if((i < 4 && (((0x1 << i) & I2C_num) != 0)) || ((i == 4) && ((0x1 & I2C_ext) != 0))){
										for (int j = 0; j < 60; j++){
												pu8Response[j + 4 + read_length] = I2C_RxData[i][4 + j];
										}
										break;
								}
						}
						total_length -= dcount;
						read_addr += dcount;
						read_length += dcount;
						pu8Src += dcount;
				}				
				pu8Response[3] = I2C_num;	
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_VERIFY_CHECKSUM){
				//WRITE
				pu8Response[2] = 0;
				pu8Response[3] = 0;
				int ret = 0; 
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				uint32_t crc32 = inpw(pu8Src);
				light_ctrl = 0x7FFF;
				for(int i = 0 ; i < MAX_PORT ; i++){
						pu8Response[4 + i] = 0;
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
								I2C_ext = 1;
						}
						for(int j = 0; j < 4; j++){
								I2C_RxData[i][j] = 0;
						}
				}
				I2C_WriteMultiBytesOneReg_2(I2C_num, I2C_ext, I2C_PORT, port_boot_addr, 0xA4, I2C_TxData, 0);
				for(int i = 0 ; i < 40; i++){
						CLK_SysTickDelay(50000);
				}
				I2C_ReadMultiBytesOneReg_STOP(I2C_num, I2C_ext, I2C_PORT, port_boot_addr, 0xA4, I2C_RxData, 4);
				for (int i = 0; i < MAX_PORT; i++){
						if((i < 4 && (((0x1 << i) & I2C_num) != 0)) || ((i == 4) && ((0x1 & I2C_ext) != 0))){
								uint32_t result_crc32 = 0;
								result_crc32 += (I2C_RxData[i][3]) << 24; 
								result_crc32 += (I2C_RxData[i][2]) << 16;
								result_crc32 += (I2C_RxData[i][1]) << 8;  
								result_crc32 += (I2C_RxData[i][0]);
								if (result_crc32 != crc32){
										pu8Response[4 + i] = 0x1;
										light_ctrl -= (0x1 << (i * 3));
								}
								else{
										light_ctrl -= (0x4 << (i * 3));
								}
						}
				}
				
				pu8Response[3] = I2C_num;	
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_GET_HUBVER){
				// Get Version
				pu8Response[3] = 0;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){
						pu8Response[4 + i] = 0;
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
								I2C_ext = 1;
						}
				}
				int ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0xE0, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
				pu8Response[3] = I2C_num;
				for (int i = 0 ; i < MAX_PORT ; i++){
						pu8Response[4 + i] = I2C_RxData[i][0];
				}
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_GET_HUBBOOT){
				// Get Boot
				pu8Response[2] = 0;
				pu8Response[3] = 0;
				check_boot();
				for (int i = 0 ; i < 4 ; i++){
						if ((((0x1 << i) & u8Lcmd) != 0) && (port_boot_state[i] != 0xFF)){
								pu8Response[3] |= (0x01 << i);
								pu8Response[4 + i] = port_boot_state[i];
						}
				}	
				if (((0x1 & u8Lext) != 0) && (port_boot_state[4] != 0xFF)){
						pu8Response[2] = 1;
						pu8Response[8] = port_boot_state[4];
				}
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_JUMP_HUB){
				pu8Response[3] = 0;
				int ret = 0;
				check_boot();
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				if (inpb(pu8Src) == 0x0){
						for(int i = 0 ; i < MAX_PORT ; i++){
								if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x1){
										I2C_num |= (0x01 << i);
								}
								else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x1){
										I2C_ext = 1;
								}
						}
						I2C_TxData[0] = inpb(pu8Src);
						ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0xE2, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
				}
				else if (inpb(pu8Src) == 0x1){
						for(int i = 0 ; i < MAX_PORT ; i++){
								if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x0){
										I2C_num |= (0x01 << i);
								}
								else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x0){
										I2C_ext = 1;
								}
						}
						ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x3, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
						uint8_t I2C_num_2 = 0;
						uint8_t I2C_ext_2 = 0;
						for (int i = 0 ; i < 4 ; i++){
								if (I2C_RxData[i][0] == 0xDA){
										I2C_num_2 += (0x01 << i);
								}		
						}
						if (I2C_RxData[4][0] == 0xDA){
								I2C_ext_2 = 1;
						}
						I2C_TxData[0] = 0x4c;
						ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x8, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 0);
						I2C_TxData[0] = 0x4a;
						ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x8, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 0);
						
				}
				pu8Response[2] = 0;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_READ_REG){
				pu8Response[3] = 0 ;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0){
								I2C_ext = 1;
						}
				}				
				uint8_t reg = inpb(pu8Src);
				int ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, isNuvoton);
				pu8Response[3] = I2C_num;
				for (int i = 0 ; i < MAX_PORT ; i++){		
						pu8Response[4 + i] = I2C_RxData[i][0];
				}				
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_READ_INFO32){
				pu8Response[2] = 0;
				pu8Response[3] = 0;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				uint8_t offset = 0xFF;
				uint8_t i2c_t = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x0){
								I2C_num += (0x01 << i);
								i2c_t = i;
								break;
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x0){
								I2C_ext = 1;
								i2c_t = i;
								break;
						}
				}					
				uint8_t pagecnt = inpb(pu8Src);
				offset = inpb(pu8Src + 1);
				if (offset == 0x0){
						I2C_TxData[0] = pagecnt;
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0B, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
						CLK_SysTickDelay(6000);
				}
				uint8_t reg = offset * 32 + 0x80;
        I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 32, isNuvoton);
        for (int j = 0; j < 32; j++){
            pu8Response[4 + j] = I2C_RxData[i2c_t][j];
        }	

				pu8Response[3] = I2C_num;
				pu8Response[2] = I2C_ext;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_WRITE_INFO32){
				pu8Response[2] = 0;
				pu8Response[3] = 0;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				uint8_t offset = 0xFF;
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0 && port_boot_state[i] == 0x0){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0 && port_boot_state[i] == 0x0){
								I2C_ext = 1;
						}
				}	
				uint8_t pagecnt = inpb(pu8Src);
				offset = inpb(pu8Src + 1);
				
				if ((pagecnt == 0x0) && (offset == 0x0)){
						I2C_TxData[0] = 0x0;
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0C, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
						I2C_TxData[0] = 0x0;
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0D, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
				}
				
				if (offset == 0x0){
						I2C_TxData[0] = pagecnt;
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0B, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
						CLK_SysTickDelay(6000);
				}
				
				uint8_t I2C_num_2 = 0;
				uint8_t I2C_ext_2 = 0;

				I2C_num_2 = I2C_num;
				I2C_ext_2 = I2C_ext;
				
				uint8_t reg = offset * 32 + 0x80;
				for (int j = 0; j < 16; j++){
						I2C_TxData[j] = inpb(pu8Src + 2 + j);
				}
				int ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, isNuvoton);

				CLK_SysTickDelay(20000);
				
				for (int j = 0; j < 16; j++){
						I2C_TxData[j] = inpb(pu8Src + 18 + j);
				}
				int ret2 = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg + 16, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, isNuvoton);
				
				pu8Response[3] = I2C_num_2;
				pu8Response[2] = I2C_ext_2;
				goto out;
		}
		else if((u8Lcmd & 0xF0) == CMD_WRITE_REG){
				pu8Response[2] = 0;	
				pu8Response[3] = 0 ;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){
						if (i != 4 && (u8Lcmd & (0x01 << i)) != 0x0){
								I2C_num |= (0x01 << i);
						}
						else if (i == 4 && u8Lext != 0x0){
								I2C_ext = 1;
						}
				}				
				uint8_t reg = inpb(pu8Src);
				I2C_TxData[0] = inpb(pu8Src + 1);
				uint8_t two_b = inpb(pu8Src + 2);
				I2C_TxData[1] = inpb(pu8Src + 3);
				if(two_b != 0){
						int ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 2, 0, isNuvoton);
				}
				else{
				    int ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
				}
				pu8Response[3] = I2C_num;			
				pu8Response[2] = I2C_ext;
				goto out;
		}

out:
    u16Lcksum = Checksum(pu8Buffer, u8len);
		pu8Response[1] = (uint8_t)((u16Lcksum >> 8) & 0xFF);  
		pu8Response[0] = (uint8_t)(u16Lcksum & 0xFF);
    return light_ctrl;
}

void check_boot(void){
		uint8_t res = 0;
		uint8_t addr_g[5] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
		for (int i = 0; i < MAX_PORT; i++){
				port_boot_state[i] = 0xFF;
				uint8_t already_find = 0;
				for (uint8_t addr = 0x50; addr <= 0x77; addr++) {
						uint8_t ret = 0;
						int ii = (i < 4) ? (0x1 << i) : 0;
						int iix = (i < 4) ? 0 : 1;
						if (already_find == 0){
								if (addr > 0x57 && addr < 0x70){
										ret = 0;
								}
								else{
										ret = i2c_address_acknowledged(i, addr);
								}
						}
						if (ret){
								I2C_RxData[i][0] = 0xFF;
								addr_g[i] = addr;
								int ret3 = I2C_Read_Write(ii, iix, addr_g, 0x00, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 4, 1);
								if (I2C_RxData[i][0] == 0x51){										
										port_boot_addr[i] = addr;
										port_boot_state[i] = 0x0; // APROM
										if (I2C_RxData[i][3] == 0xDA){
												isNuvoton = 1;
										}
										else{
												isNuvoton = 0;
										}
										already_find = 1;
								}
								else if (I2C_RxData[i][0] == 0x52){ 
										I2C_RxData[i][0] = 0xFF;
										int ret2 = I2C_Read_Write(ii, iix, addr_g, 0xE0, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
										if (I2C_RxData[i][0] == 0xB1 || I2C_RxData[i][0] == 0xB2){
												port_boot_addr[i] = addr;
												port_boot_state[i] = 0x1; // LDROM
												isNuvoton = 1;
												already_find = 1;
										}							
								}													
						}	
				}
		}
}

int offline_operation(int port, int cmd){
		uint8_t TxData[64] = {0xFF};
		uint8_t RxData[64] = {0xFF};
		uint32_t data[64] = {0xFF};
		char str_buffer[72] = {0};
		uint32_t bin_len = 0;
		uint32_t bin_written = 0;
		uint32_t bin_crc32 = 0;
		uint32_t dcount = 0;
		uint16_t verify = 0;
		uint16_t u16Lcksum = 0;
		int ret = 0; 
		
		gpio_led_ctrl(0x7FFF); // ALL OFF
		
		int lcd_order = 0;
		check_boot();
		
		uint8_t I2C_num_base = 0;
		uint8_t I2C_ext_base = 0;
		if (port == 1){
				I2C_ext_base = 0x1;
		}
		else if (port - 1 < MAX_PORT){
				I2C_num_base = (0x1 << (port - 2));
		}
		else if (port >= MAX_PORT + 1){  // ALL
				I2C_num_base = 0xF;
				I2C_ext_base = 0x1;
		}
		
		if (cmd == 1){
				// check offline data exist
				ssd1306_Fill(Black);
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
			
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				g_u32DataFlashAddr += 0x400;
				FMC_Read_User(g_u32DataFlashAddr, &bin_len);
				g_u32DataFlashAddr += 4;
				FMC_Read_User(g_u32DataFlashAddr, &bin_crc32);
				g_u32DataFlashAddr += 4;
			
				bin_written = 0;
				if (bin_len == 0 || bin_len == 0xFFFFFFFF){
						sprintf(str_buffer,  "No Bin in Flash");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
					
						FMC_DISABLE_AP_UPDATE(); 
						FMC_Close(); 
						SYS_LockReg();
						return 0;
				}
				// check and jump to LDROM
				unsigned int not_nuvoton = 0;
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x0) && (i < 4)){
								I2C_num += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x0) && (i == 4)){
								I2C_ext = 0x1;
						}
				}
				I2C_num = I2C_num & I2C_num_base;
				I2C_ext = I2C_ext & I2C_ext_base;
				ret = I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x3, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
				uint8_t I2C_num_2 = 0;
				uint8_t I2C_ext_2 = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if (i < 4 && I2C_RxData[i][0] == 0xDA){
								I2C_num_2 += (0x01 << i);
						}
						else if (i == 4 && I2C_RxData[i][0] == 0xDA){
								I2C_ext_2 += (0x01);
						}
						else if (i < 4 && ((0x1 << i) & I2C_num)){
								not_nuvoton = 1;
						}	
						else if (i == 4 && ((0x1) & I2C_ext)){
								not_nuvoton = 1;
						}	
				}
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				I2C_TxData[0] = 0x4c;
				ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x8, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
				I2C_TxData[0] = 0x4a;
				ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x8, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
				
				//check_boot();
				I2C_num_2 = 0;
				I2C_ext_2 = 0;
	
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x1) && (i < 4)){
								I2C_num_2 |= (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x1) && (i == 4)){
								I2C_ext_2 = 0x1;
						}
				}
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				if (not_nuvoton == 1){
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "Only Nuvoton DIMM");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "can Jump to LDROM");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 4);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
						return 0;
				}
				else if (I2C_num_2 != 0 || I2C_ext_2 != 0){
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jumped");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
				}
				else {
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jump failed");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
						return 0;
				}
				ssd1306_UpdateScreen();
				// write APROM				
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				g_u32DataFlashAddr += 0x400;
				FMC_Read_User(g_u32DataFlashAddr, &bin_len);
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Start Erase ...");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				I2C_num = 0;
				I2C_ext = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x1) && (i < 4)){
								I2C_num += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x1) && (i == 4)){
								I2C_ext = 0x1;
						}
				}
				I2C_num = I2C_num & I2C_num_base;
				I2C_ext = I2C_ext & I2C_ext_base;
				uint8_t temp[7] = {6, 200, 0, 0, 0, 0, 0};
				temp[1] = (bin_len / 2048) & 0xFF;
				temp[2] = ((bin_len / 2048) >> 8 ) & 0xFF;
				memcpy(I2C_TxData, temp, 7);
				I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x80, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 7, 0, 1);

				g_u32DataFlashAddr += 8;
				
				for(int i = 0 ; i < 20; i++){
						CLK_SysTickDelay(50000);
				}	

				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Erase Done.");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Start Program ...");
				ssd1306_SetCursor(2, 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				bin_written = 0;
				
				int progress = 0;
				while (bin_written < bin_len){
						dcount = (56 < bin_len - bin_written)? 56: bin_len - bin_written;
						FMC_Proc(FMC_ISPCMD_READ, g_u32DataFlashAddr + bin_written, g_u32DataFlashAddr + bin_written + dcount, data);
						I2C_TxData[0] = dcount + 5;
						I2C_TxData[1] = dcount;
						I2C_num = 0;
						memcpy(&I2C_TxData[2], &bin_written, 4);
						memcpy(&I2C_TxData[6], data, dcount);
						for (int i = 0 ; i < MAX_PORT ; i++){
								if ((port_boot_state[i] == 0x1) && (i < 4)){
										I2C_num += (0x1 << i);
								}
								else if ((port_boot_state[i] == 0x1) && (i == 4)){
										I2C_ext = 0x1;
								}
						}
						I2C_num = I2C_num & I2C_num_base;
						I2C_ext = I2C_ext & I2C_ext_base;
						
						uint32_t light = 0x7FFF;
						for (int i = 0 ; i < MAX_PORT ; i++){
								if (((0x1 << i) & I2C_num) && (i < 4)){
										light -= (0x2 << (i * 3));
								}
								else if ((0x1 & I2C_ext) && (i == 4)){
										light -= (0x2 << (i * 3));
								}
						}
						gpio_led_ctrl(light);
						
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x81, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, dcount + 6, 0, 1);
						bin_written += dcount;
						if (bin_written >= bin_len * progress / 10){
								sprintf(str_buffer,  "Progress: %d %%", progress * 10);
								ssd1306_SetCursor(2, 8 * 4);
								ssd1306_WriteString(str_buffer, Font_6x8, White);
								ssd1306_UpdateScreen();
								progress ++;
						}
				}
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Program Done.");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Start Verify ...");
				ssd1306_SetCursor(2, 0 + 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				bin_written = 0;
				progress = 0;
				
				verify = 0;

				I2C_num = 0;
				I2C_ext = 0;
				for(int i = 0 ; i < MAX_PORT ; i++){											
						if ((port_boot_state[i] == 0x1) && (i < 4)){
								I2C_num += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x1) && (i == 4)){
								I2C_ext = 0x1;
						}
						for(int j = 0; j < 4; j++){
								I2C_RxData[i][j] = 0;
						}
				}
				
				I2C_num = I2C_num & I2C_num_base;
				I2C_ext = I2C_ext & I2C_ext_base;
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Verifying .");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				I2C_WriteMultiBytesOneReg_2(I2C_num, I2C_ext, I2C_PORT, port_boot_addr, 0xA4, I2C_TxData, 0);
				for(int i = 0 ; i < 40; i++){
						CLK_SysTickDelay(50000);
				}
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Verifying ..");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				I2C_ReadMultiBytesOneReg_STOP(I2C_num, I2C_ext, I2C_PORT, port_boot_addr, 0xA4, I2C_RxData, 4);
				for (int i = 0; i < MAX_PORT; i++){
						if((i < 4 && (((0x1 << i) & I2C_num) != 0)) || ((i == 4) && ((0x1 & I2C_ext) != 0))){
								uint32_t result_crc32 = 0;
								result_crc32 += (I2C_RxData[i][3]) << 24; 
								result_crc32 += (I2C_RxData[i][2]) << 16;
								result_crc32 += (I2C_RxData[i][1]) << 8;  
								result_crc32 += (I2C_RxData[i][0]);
								if (result_crc32 != bin_crc32){
										verify |= (0x1 << i);						
								}
						}
				}
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Verifying ...");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				uint32_t light = 0x7FFF;
				for(int i = 0; i < MAX_PORT ; i++){
						if (port_boot_state[i] == 0x1){
								if ((verify & (0x1 << i)) != 0){
										light -= (0x1 << (i * 3)); // FAIL ON
								} else { 
										light -= (0x4 << (i * 3)); // PASS ON
								}
						}
				}
				gpio_led_ctrl(light);
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "Verify Done: %d", verify);
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				if (verify == 0) {
						sprintf(str_buffer,  "continue...");
				} else {
						sprintf(str_buffer,  "Input to continue...");
				}
				ssd1306_SetCursor(2, 0 + 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				
				ssd1306_UpdateScreen();

				if (verify != 0) {
						FMC_DISABLE_AP_UPDATE(); 
						FMC_Close(); 
						SYS_LockReg();
						return 0;
				}	

				I2C_num_2 = 0;
				I2C_ext_2 = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x1) && (i < 4)){
								I2C_num_2 += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x1) && (i == 4)){
								I2C_ext_2 = 0x1;
						}
				}				
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				I2C_TxData[0] = 0x0;
				ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0xE2, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);

				// wait for some time
				for(int i = 0 ; i < 20; i++){
						CLK_SysTickDelay(50000);
				}				
				//check_boot();
				
				I2C_num_2 = 0;
				I2C_ext_2 = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x0) && (i < 4)){
								I2C_num_2 += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x0) && (i == 4)){
								I2C_ext_2 = 0x1;
						}
				}				
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				if (I2C_num_2 != 0 || I2C_ext_2 != 0){
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jumped");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
				}
				else {
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jump failed");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
						return 0;
				}
				ssd1306_UpdateScreen();
				// write SPD
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				bin_written = 0x0;
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "SPD Writing...");
				ssd1306_SetCursor(2, 0 + 8 * 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
	
				I2C_num = 0;
				I2C_ext = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x0) && (i < 4)){
								I2C_num += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x0) && (i == 4)){
								I2C_ext = 0x1;
						}
				}	
				I2C_num = I2C_num & I2C_num_base;
				I2C_ext = I2C_ext & I2C_ext_base;
				unsigned int offset = 0;
				while (bin_written < 1024){
						dcount = (32 < 1024 - bin_written)? 32: 1024 - bin_written;
						FMC_Proc(FMC_ISPCMD_READ, g_u32DataFlashAddr + bin_written, g_u32DataFlashAddr + bin_written + dcount, data);
						
						if (offset % 4 == 0x0){
								I2C_TxData[0] = offset / 4;
								I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0B, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
								CLK_SysTickDelay(6000);
						}
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x30, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
						
						uint8_t block_pass[5] = {0, 0, 0, 0, 0};
						I2C_num_2 = 0;
						I2C_RxData[0][0] = 0;
						I2C_RxData[1][0] = 0;
						I2C_RxData[2][0] = 0;
						I2C_RxData[3][0] = 0;
						I2C_RxData[4][0] = 0;
						for(int i = 0 ; i < MAX_PORT ; i++){
								if (i != 4 && (I2C_num & (0x01 << i)) != 0x0){
										block_pass[i] = I2C_RxData[i][0] & 0x4;
										if (block_pass[i]){
												I2C_num_2 |= (0x01 << i);
										}
								}
								else if (i == 4 && I2C_ext != 0){
										block_pass[i] = I2C_RxData[i][0] & 0x4;
										if (block_pass[i]){
												I2C_ext_2 |= 0x01;
										}
								}
						}
						if (offset == 0x0 && offset / 4 == 0x0){
								I2C_TxData[0] = 0x0;
								I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x0C, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
								I2C_TxData[0] = 0x0;
								I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x0D, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
						}

						uint8_t oo = (offset % 4);
						uint8_t reg = oo * 32 + 0x80;

						for (int j = 0; j < 4; j++){
						    I2C_TxData[4 * j] = (uint8_t)(data[j] & 0xFF);
						    I2C_TxData[4 * j + 1] = (uint8_t)((data[j] >> 8) & 0xFF);
						    I2C_TxData[4 * j + 2] = (uint8_t)((data[j] >> 16) & 0xFF);
						    I2C_TxData[4 * j + 3] = (uint8_t)((data[j] >> 24) & 0xFF);
						}
						int ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, 1);
						
						CLK_SysTickDelay(20000);
						
						for (int j = 0; j < 4; j++){
						    I2C_TxData[4 * j] = (uint8_t)(data[j + 4] & 0xFF);
						    I2C_TxData[4 * j + 1] = (uint8_t)((data[j + 4] >> 8) & 0xFF);
						    I2C_TxData[4 * j + 2] = (uint8_t)((data[j + 4] >> 16) & 0xFF);
						    I2C_TxData[4 * j + 3] = (uint8_t)((data[j + 4] >> 24) & 0xFF);
						}
						int ret2 = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg + 16, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, 1);
						bin_written += dcount;
						offset ++;
				}
				
				light = 0x7FFF;
				for(int i = 0; i < MAX_PORT ; i++){
						if (i < 4 && port_boot_state[i] == 0x1 && (I2C_num & (0x1 << i))){
								light -= (0x4 << (i * 3)); // PASS ON
						}
						else if (i == 4 && port_boot_state[i] == 0x1 && (I2C_ext & 0x1)){
								light -= (0x4 << (i * 3)); // PASS ON
						}
				}
				gpio_led_ctrl(light);
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "SPD Writing done");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Input to continue...");
				ssd1306_SetCursor(2, 0 + 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
		}
		else if (cmd == 2) {  // bin information
				ssd1306_Fill(Black);
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
			
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				g_u32DataFlashAddr += 0x400;
			
				FMC_Read_User(g_u32DataFlashAddr, &bin_len);
				g_u32DataFlashAddr += 4;
			
				FMC_Read_User(g_u32DataFlashAddr, &bin_crc32);
				g_u32DataFlashAddr += 4;
			
				bin_written = 0;
				if (bin_len == 0 || bin_len == 0xFFFFFFFF){
						sprintf(str_buffer,  "No Bin in Flash");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
					
						FMC_DISABLE_AP_UPDATE(); 
						FMC_Close(); 
						SYS_LockReg();
						return 0;
				}
				
				while (bin_written < bin_len){
						dcount = (32 < bin_len - bin_written)? 32: bin_len - bin_written;
						FMC_Proc(FMC_ISPCMD_READ, g_u32DataFlashAddr + bin_written, g_u32DataFlashAddr + bin_written + dcount, data);
						memcpy(&TxData[0], data, dcount);
						u16Lcksum += Checksum(TxData, dcount);
						bin_written += dcount;
				}
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
				
				if (bin_len > 1024 && bin_len % 1024 == 0){
						sprintf(str_buffer,  "File Size: %d KB", (bin_len / 1024));
				}
				else if (bin_len > 1024 ){
						sprintf(str_buffer,  "File Size: %d KB % d B", (bin_len / 1024), (bin_len % 1024));
				}
				else {
						sprintf(str_buffer,  "File Size: %d B", bin_len);
				}
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Checksum: 0x%04X", u16Lcksum & 0xFFFF);
				ssd1306_SetCursor(2, 0 + 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "CRC32: 0x%08X", bin_crc32);
				ssd1306_SetCursor(2, 0 + 8 * 4);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Input to continue...");
				ssd1306_SetCursor(2, 0 + 8 * 6);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
		} 
		else if (cmd == 3) {  // spd information
				if (view_mode == 0){ 
						view_mode = 1;
				}
				else {
						return 0; 
				}
				uint8_t ii = (port == 1) ? 4 : port - 2;
				if (port_boot_state[ii] == 0x0){	
						for (int pagecnt = 0; pagecnt < 8; pagecnt++){
								I2C_TxData[0] = pagecnt;
								I2C_Read_Write(I2C_num_base, I2C_ext_base, port_boot_addr, 0x0B, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, isNuvoton);
								CLK_SysTickDelay(6000);
								for (int offset = 0; offset < 4; offset++){
										uint8_t reg = offset * 32 + 0x80;
										for (int j = 0; j < 32; j++){
												I2C_Read_Write(I2C_num_base, I2C_ext_base, port_boot_addr, reg + j, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, isNuvoton);
												st[pagecnt * 128 + offset * 32 + j] = I2C_RxData[ii][0];
										}
								}
						}		
						ssd1306_Fill(Black);
						ssd1306_SetCursor(2, 0);
						char str_buffer[64] = {0};
						int ord = (view_mode - 1) * 32;
						sprintf(str_buffer,  "View Mode: block %2d", (view_mode - 1)/2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						for (int i = 0; i < 5; i ++){
								ssd1306_SetCursor(2, 16 + i * 8);
								if (i != 4) sprintf(str_buffer, "%02X %02X %02X %02X %02X %02X %02X",st[ord],st[ord+1],st[ord+2],st[ord+3],st[ord+4],st[ord+5],st[ord+6]);
								else sprintf(str_buffer, "%02X %02X %02X %02X <- %02X ->",st[ord],st[ord+1],st[ord+2],st[ord+3], view_mode - 1);
								ord += 7;
								ssd1306_WriteString(str_buffer, Font_6x8, White);
						}
						ssd1306_UpdateScreen();
				}
				else {
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "SLOT info not find!");
						ssd1306_SetCursor(2, 8);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 3);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
						return 0;
				}
				return 1;
		} 
		else if (cmd == 4) {  // spd information			
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "DIMM Info: SLOT %d", port);
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				uint8_t ii = (port == 1) ? 4 : port - 2;
				if (port_boot_state[ii] == 0x0){	
						const char *word;
						for (int i = 0; i < 5; i++){
								I2C_RxData[ii][0] = 0xFF;
								int ret = I2C_Read_Write(I2C_num_base, I2C_ext_base, port_boot_addr, i + 21, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, isNuvoton);
								if (ret != -1){
										switch (i) {
											case 0: word = "CUSTOMER ID:"; break;
											case 1: word = "CHIP ID:    "; break;
											case 2: word = "LED ID:     "; break;
											case 3: word = "PROJECT ID: "; break;
											case 4: word = "FT ID:      "; break;
										}
										sprintf(str_buffer,  "%s 0x%02X", word, I2C_RxData[ii][0]);
										ssd1306_SetCursor(2, 8 + i * 8);
										ssd1306_WriteString(str_buffer, Font_6x8, White);
								}			
						}
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 8 + 5 * 8);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
				}
				else {
						sprintf(str_buffer,  "SLOT info not find!");
						ssd1306_SetCursor(2, 8);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 3);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
				}				
		}
		else if (cmd == 5) {  // bin information (spd
				ssd1306_Fill(Black);
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
			
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				
				bin_written = 0;
				
				while (bin_written < 1024){
						dcount = 32;
						FMC_Proc(FMC_ISPCMD_READ, g_u32DataFlashAddr + bin_written, g_u32DataFlashAddr + bin_written + dcount, data);
						for (int i = 0; i * 4 < 32; i++) {
								st[bin_written + i * 4] = (uint8_t)(data[i] & 0xFF);
								st[bin_written + i * 4 + 1] = (uint8_t)((data[i] >> 8) & 0xFF);
								st[bin_written + i * 4 + 2] = (uint8_t)((data[i] >> 16) & 0xFF);
								st[bin_written + i * 4 + 3] = (uint8_t)((data[i] >> 24) & 0xFF);
						}
						bin_written += dcount;
				}
				
				if (view_mode == 0){ 
					view_mode = 1;
				}
				else {
					return 0; 
				}
				
				ssd1306_Fill(Black);
				ssd1306_SetCursor(2, 0);
				char str_buffer[64] = {0};
				int ord = (view_mode - 1) * 32;
				sprintf(str_buffer,  "View Mode: block %2d", (view_mode - 1)/2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				for (int i = 0; i < 5; i ++){
						ssd1306_SetCursor(2, 16 + i * 8);
						if (i != 4) sprintf(str_buffer, "%02X %02X %02X %02X %02X %02X %02X",st[ord],st[ord+1],st[ord+2],st[ord+3],st[ord+4],st[ord+5],st[ord+6]);
						else sprintf(str_buffer, "%02X %02X %02X %02X <- %02X ->",st[ord],st[ord+1],st[ord+2],st[ord+3], view_mode - 1);
						ord += 7;
						ssd1306_WriteString(str_buffer, Font_6x8, White);
				}
				ssd1306_UpdateScreen();

				return 1;
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
		}
		else if (cmd == 6){
				// check offline data exist
				ssd1306_Fill(Black);
				SYS_UnlockReg();
				FMC_Open(); 
				FMC_ENABLE_AP_UPDATE();
			
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				g_u32DataFlashAddr += 0x400;
				FMC_Read_User(g_u32DataFlashAddr, &bin_len);
				g_u32DataFlashAddr += 4;
				FMC_Read_User(g_u32DataFlashAddr, &bin_crc32);
				g_u32DataFlashAddr += 4;
			
				bin_written = 0;
				if (bin_len == 0 || bin_len == 0xFFFFFFFF){
						sprintf(str_buffer,  "No Bin in Flash");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
					
						FMC_DISABLE_AP_UPDATE(); 
						FMC_Close(); 
						SYS_LockReg();
						return 0;
				}
				
				//check_boot();
				
				uint8_t I2C_num_2 = 0;
				uint8_t I2C_ext_2 = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x1) && (i < 4)){
								I2C_num_2 += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x1) && (i == 4)){
								I2C_ext_2 = 0x1;
						}
				}				
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				I2C_TxData[0] = 0x0;
				ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0xE2, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);

				// wait for some time
				for(int i = 0 ; i < 20; i++){
						CLK_SysTickDelay(50000);
				}				
				//check_boot();
				
				I2C_num_2 = 0;
				I2C_ext_2 = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x0) && (i < 4)){
								I2C_num_2 += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x0) && (i == 4)){
								I2C_ext_2 = 0x1;
						}
				}				
				I2C_num_2 = I2C_num_2 & I2C_num_base;
				I2C_ext_2 = I2C_ext_2 & I2C_ext_base;
				if (I2C_num_2 != 0 || I2C_ext_2 != 0){
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jumped");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
				}
				else {
						ssd1306_Fill(Black);
						sprintf(str_buffer,  "PORT jump failed");
						ssd1306_SetCursor(2, 0);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						sprintf(str_buffer,  "Input to continue...");
						ssd1306_SetCursor(2, 0 + 8 * 2);
						ssd1306_WriteString(str_buffer, Font_6x8, White);
						ssd1306_UpdateScreen();
						return 0;
				}
				ssd1306_UpdateScreen();
				// write SPD
				g_u32ApromSize = GetApromSize();
				GetDataFlashInfo(&g_u32DataFlashAddr, &g_u32DataFlashSize);
				bin_written = 0x0;
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "SPD Writing...");
				ssd1306_SetCursor(2, 0 + 8 * 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
	
				uint8_t I2C_num = 0;
				uint8_t I2C_ext = 0;
				for (int i = 0 ; i < MAX_PORT ; i++){
						if ((port_boot_state[i] == 0x0) && (i < 4)){
								I2C_num += (0x1 << i);
						}
						else if ((port_boot_state[i] == 0x0) && (i == 4)){
								I2C_ext = 0x1;
						}
				}	
				I2C_num = I2C_num & I2C_num_base;
				I2C_ext = I2C_ext & I2C_ext_base;
				unsigned int offset = 0;
				while (bin_written < 1024){
						dcount = (32 < 1024 - bin_written)? 32: 1024 - bin_written;
						FMC_Proc(FMC_ISPCMD_READ, g_u32DataFlashAddr + bin_written, g_u32DataFlashAddr + bin_written + dcount, data);
						
						if (offset % 4 == 0x0){
								I2C_TxData[0] = offset / 4;
								I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x0B, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
								CLK_SysTickDelay(6000);
						}
						I2C_Read_Write(I2C_num, I2C_ext, port_boot_addr, 0x30, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 0, 1, 1);
						
						uint8_t block_pass[5] = {0, 0, 0, 0, 0};
						I2C_num_2 = 0;
						I2C_RxData[0][0] = 0;
						I2C_RxData[1][0] = 0;
						I2C_RxData[2][0] = 0;
						I2C_RxData[3][0] = 0;
						I2C_RxData[4][0] = 0;
						for(int i = 0 ; i < MAX_PORT ; i++){
								if (i != 4 && (I2C_num & (0x01 << i)) != 0x0){
										block_pass[i] = I2C_RxData[i][0] & 0x4;
										if (block_pass[i]){
												I2C_num_2 |= (0x01 << i);
										}
								}
								else if (i == 4 && I2C_ext != 0){
										block_pass[i] = I2C_RxData[i][0] & 0x4;
										if (block_pass[i]){
												I2C_ext_2 |= 0x01;
										}
								}
						}
						if (offset == 0x0 && offset / 4 == 0x0){
								I2C_TxData[0] = 0x0;
								I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x0C, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
								I2C_TxData[0] = 0x0;
								I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, 0x0D, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 1, 0, 1);
						}

						uint8_t oo = (offset % 4);
						uint8_t reg = oo * 32 + 0x80;

						for (int j = 0; j < 4; j++){
						    I2C_TxData[4 * j] = (uint8_t)(data[j] & 0xFF);
						    I2C_TxData[4 * j + 1] = (uint8_t)((data[j] >> 8) & 0xFF);
						    I2C_TxData[4 * j + 2] = (uint8_t)((data[j] >> 16) & 0xFF);
						    I2C_TxData[4 * j + 3] = (uint8_t)((data[j] >> 24) & 0xFF);
						}
						int ret = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, 1);
						
						CLK_SysTickDelay(20000);
						
						for (int j = 0; j < 4; j++){
						    I2C_TxData[4 * j] = (uint8_t)(data[j + 4] & 0xFF);
						    I2C_TxData[4 * j + 1] = (uint8_t)((data[j + 4] >> 8) & 0xFF);
						    I2C_TxData[4 * j + 2] = (uint8_t)((data[j + 4] >> 16) & 0xFF);
						    I2C_TxData[4 * j + 3] = (uint8_t)((data[j + 4] >> 24) & 0xFF);
						}
						int ret2 = I2C_Read_Write(I2C_num_2, I2C_ext_2, port_boot_addr, reg + 16, (uint8_t *)I2C_TxData, (uint8_t **)I2C_RxData, 16, 0, 1);

						bin_written += dcount;
						offset ++;
				}
				
				uint32_t light = 0x7FFF;
				for(int i = 0; i < MAX_PORT ; i++){
						if (i < 4 && port_boot_state[i] == 0x1 && (I2C_num & (0x1 << i))){
								light -= (0x4 << (i * 3)); // PASS ON
						}
						else if (i == 4 && port_boot_state[i] == 0x1 && (I2C_ext & 0x1)){
								light -= (0x4 << (i * 3)); // PASS ON
						}
				}
				gpio_led_ctrl(light);
				
				ssd1306_Fill(Black);
				sprintf(str_buffer,  "SPD Writing done");
				ssd1306_SetCursor(2, 0);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				sprintf(str_buffer,  "Input to continue...");
				ssd1306_SetCursor(2, 0 + 8 * 2);
				ssd1306_WriteString(str_buffer, Font_6x8, White);
				ssd1306_UpdateScreen();
				
				FMC_DISABLE_AP_UPDATE(); 
				FMC_Close(); 
				SYS_LockReg();
		}
		return 0;
}

void gpio_led_ctrl(uint32_t light){
		PB7 = light & 0x1 ? 1 : 0;    
		PB8 = light & 0x2 ? 1 : 0;     
		PB9 = light & 0x4 ? 1 : 0;  
		PF6 = light & 0x8 ? 1 : 0;     
		PA8 = light & 0x10 ? 1 : 0;   
		PA9 = light & 0x20 ? 1 : 0;
		PA3 = light & 0x40 ? 1 : 0;   
		PA4 = light & 0x80 ? 1 : 0;   
		PA5 = light & 0x100 ? 1 : 0; 
		PA0 = light & 0x200 ? 1 : 0;  
		PA1 = light & 0x400 ? 1 : 0;  
		PA2 = light & 0x800 ? 1 : 0; 
		PE5 = light & 0x1000 ? 1 : 0; 
		PE6 = light & 0x2000 ? 1 : 0; 
		PE7 = light & 0x4000 ? 1 : 0;
}

void debug(unsigned int a, unsigned int b, unsigned int c){
		char str_buffer[16] = {0};
		char str_buffer2[16] = {0};
		char str_buffer3[64] = {0};
		
		sprintf(str_buffer,  "A : %02u", a);
		sprintf(str_buffer2,  "B : %02u", b);
		sprintf(str_buffer3,  "C : %02u", c);
		ssd1306_Fill(Black);
		ssd1306_SetCursor(2, 0);
		ssd1306_WriteString(str_buffer, Font_6x8, White);
		ssd1306_SetCursor(2, 8);
		ssd1306_WriteString(str_buffer2, Font_6x8, White);
		ssd1306_SetCursor(2, 16);
		ssd1306_WriteString(str_buffer3, Font_6x8, White);
		
		ssd1306_UpdateScreen();
}

