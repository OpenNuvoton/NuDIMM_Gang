/***************************************************************************//**
 * @file     isp_user.h
 * @brief    ISP Command header file
 * @version  0x32
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2021 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#ifndef ISP_USER_H
#define ISP_USER_H

#define MAX_PORT  									5
#define MAX_CMD											6

#define FW_VERSION                  0x19
#define PACK_SIZE										1024

#define CMD_GET_FWVER               0xA6
#define CMD_UPDATE_APROM            0xA0
#define CMD_READ_APROM            	0xA1
#define CMD_READ_CONFIG             0xA2
#define CMD_ERASE_APROM            	0xA3
#define CMD_CONNECT                 0xAE
#define CMD_GET_DEVICEID            0xB1

#define CMD_ERASE_HUB               0x10
#define CMD_WRITE_HUB               0x20
#define CMD_READ_HUB                0x30
#define CMD_GET_HUBVER              0x40
#define CMD_GET_HUBBOOT             0x50
#define CMD_JUMP_HUB               	0x60
#define CMD_READ_REG               	0x70
#define CMD_READ_INFO32             0x80
#define CMD_WRITE_INFO32            0x90

#define CMD_VERIFY_CHECKSUM         0xD0
#define CMD_WRITE_REG         			0xE0

#define V6M_AIRCR_VECTKEY_DATA      0x05FA0000UL
#define V6M_AIRCR_SYSRESETREQ       0x00000004UL

extern void GetDataFlashInfo(uint32_t *pu32Addr, uint32_t *pu32Size);
extern uint32_t GetApromSize(void);
extern int ParseCmd(uint8_t *pu8Buffer, uint32_t u8len);
extern void debug(unsigned int a, unsigned int b, unsigned int c);
extern int offline_operation(int port, int cmd);
extern void cmd_message(int cmd, int cksm);
extern void gpio_led_ctrl(uint32_t light);
extern uint32_t g_u32ApromSize, g_u32DataFlashAddr, g_u32DataFlashSize;

//extern __attribute__((aligned(4))) uint8_t g_u8OutBuff[];
//extern __attribute__((aligned(4))) uint8_t g_au8ResponseBuff[64];

extern uint8_t g_u8OutBuff[];
extern uint8_t g_au8ResponseBuff[PACK_SIZE];

#endif  /* ISP_USER_H */
