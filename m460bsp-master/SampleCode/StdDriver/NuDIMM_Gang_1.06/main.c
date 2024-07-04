/**************************************************************************//**
 * @file     main.c
 * @version  V3.00
 * @brief    Demonstrate how to transfer data between USB device and PC through USB HID interface.
 *           A windows tool is also included in this sample code to connect with a USB device.
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2021 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#include <stdio.h>
#include <string.h>
#include "NuMicro.h"
#include "hid_transfer.h"
#include "i2c_transfer.h"
#include "isp_user.h"
#include "ssd1306.h"
#include "HAL_TICK_CONTROL.h"

volatile unsigned int button_start = 0;
volatile unsigned int joy_place = 0;
unsigned int target_i2c = 1;
unsigned int target_cmd = 1;
int input_flag = 1;
int left_right = 0;
int view_mode = 0;
int offline_mode = 1;
unsigned char st[1024];

int i2c_clock_time = 100000;

//extern __attribute__((aligned(4))) uint8_t g_au8ResponseBuff[64];
extern uint8_t g_au8ResponseBuff[PACK_SIZE];

/*--------------------------------------------------------------------------*/
void SYS_Init(void)
{
    uint32_t volatile i;

    /* Unlock protected registers */
    SYS_UnlockReg();

    /*---------------------------------------------------------------------------------------------------------*/
    /* Init System Clock                                                                                       */
    /*---------------------------------------------------------------------------------------------------------*/

    /* Enable HIRC and HXT clock */
    CLK_EnableXtalRC(CLK_PWRCTL_HIRCEN_Msk | CLK_PWRCTL_HXTEN_Msk);

    /* Wait for HIRC and HXT clock ready */
    CLK_WaitClockReady(CLK_STATUS_HIRCSTB_Msk | CLK_STATUS_HXTSTB_Msk);

    /* Set PCLK0 and PCLK1 to HCLK/2 */
    CLK->PCLKDIV = (CLK_PCLKDIV_APB0DIV_DIV2 | CLK_PCLKDIV_APB1DIV_DIV2);

    /* Set core clock to 200MHz */
    CLK_SetCoreClock(FREQ_200MHZ);

    /* Enable all GPIO clock */
    CLK->AHBCLK0 |= CLK_AHBCLK0_GPACKEN_Msk | CLK_AHBCLK0_GPBCKEN_Msk | CLK_AHBCLK0_GPCCKEN_Msk | CLK_AHBCLK0_GPDCKEN_Msk |
                    CLK_AHBCLK0_GPECKEN_Msk | CLK_AHBCLK0_GPFCKEN_Msk | CLK_AHBCLK0_GPGCKEN_Msk | CLK_AHBCLK0_GPHCKEN_Msk;
    CLK->AHBCLK1 |= CLK_AHBCLK1_GPICKEN_Msk | CLK_AHBCLK1_GPJCKEN_Msk;
		
		/* Enable HSUSBD module clock */
    CLK_EnableModuleClock(HSUSBD_MODULE);
		
		CLK_EnableModuleClock(UART0_MODULE);
		CLK_SetModuleClock(UART0_MODULE, CLK_CLKSEL1_UART0SEL_HIRC, CLK_CLKDIV0_UART0(1));
		
		/* Enable I2C0 and I2C1 clock */
    CLK_EnableModuleClock(I2C0_MODULE);
    CLK_EnableModuleClock(I2C1_MODULE);
		CLK_EnableModuleClock(I2C2_MODULE);
    CLK_EnableModuleClock(I2C4_MODULE);
		CLK_EnableModuleClock(I2C3_MODULE);
		
		CLK_EnableModuleClock(USCI0_MODULE);
		
		CLK_EnableModuleClock(TMR0_MODULE);
    CLK_SetModuleClock(TMR0_MODULE, CLK_CLKSEL1_TMR0SEL_HIRC, 0);
		
		SystemCoreClockUpdate();
						
		GPIO_SetMode(PB, BIT7 | BIT8 | BIT9, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PA, BIT8 | BIT9, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PA, BIT3 | BIT4 | BIT5, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PA, BIT0 | BIT1 | BIT2, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PE, BIT5 | BIT6 | BIT7, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PF, BIT6, GPIO_MODE_OUTPUT);
		
		GPIO_SetMode(PB, BIT15, GPIO_MODE_OUTPUT);
		GPIO_SetMode(PC, BIT14, GPIO_MODE_OUTPUT);
		
		GPIO_SetMode(PC, BIT5, GPIO_MODE_INPUT);
		GPIO_EnableInt(PC, 5, GPIO_INT_FALLING);
		
		GPIO_SetMode(PA, BIT12 | BIT13 | BIT14 | BIT15, GPIO_MODE_INPUT);
		GPIO_SetMode(PC, BIT4, GPIO_MODE_INPUT);
		
		GPIO_EnableInt(PA, 12, GPIO_INT_FALLING);
		GPIO_EnableInt(PA, 13, GPIO_INT_FALLING);
		GPIO_EnableInt(PA, 14, GPIO_INT_FALLING);
		GPIO_EnableInt(PA, 15, GPIO_INT_FALLING);
		GPIO_EnableInt(PC, 4, GPIO_INT_FALLING);
		
		GPIO_SET_DEBOUNCE_TIME(PA, GPIO_DBCTL_DBCLKSRC_LIRC, GPIO_DBCTL_DBCLKSEL_512);
		GPIO_SET_DEBOUNCE_TIME(PC, GPIO_DBCTL_DBCLKSRC_LIRC, GPIO_DBCTL_DBCLKSEL_512);
		
		GPIO_ENABLE_DEBOUNCE(PA, BIT12 | BIT13 | BIT14 | BIT15);
		GPIO_ENABLE_DEBOUNCE(PC, BIT4 | BIT5);

    /* Select HSUSBD */
    SYS->USBPHY &= ~SYS_USBPHY_HSUSBROLE_Msk;

    /* Enable USB PHY */
    SYS->USBPHY = (SYS->USBPHY & ~(SYS_USBPHY_HSUSBROLE_Msk | SYS_USBPHY_HSUSBACT_Msk)) | SYS_USBPHY_HSUSBEN_Msk;
    for(i = 0; i < 0x1000; i++);   // delay > 10 us
    SYS->USBPHY |= SYS_USBPHY_HSUSBACT_Msk;

		SET_UART0_RXD_PA6();
    SET_UART0_TXD_PA7();
		
		UART_Open(UART0, 115200);
    /*---------------------------------------------------------------------------------------------------------*/
    /* Init I/O Multi-function                                                                                 */
    /*---------------------------------------------------------------------------------------------------------*/
		
		SET_I2C0_SDA_PB4();
    SET_I2C0_SCL_PB5();
		
    SET_I2C1_SDA_PB2();
    SET_I2C1_SCL_PB3();
		
		SET_I2C2_SDA_PA10();
    SET_I2C2_SCL_PA11();
		
		SET_I2C4_SDA_PF4();
    SET_I2C4_SCL_PF5();
		
		SET_I2C3_SDA_PC2();
		SET_I2C3_SCL_PC3();
		
		SET_USCI0_CLK_PB12();
    SET_USCI0_DAT0_PB13();

    PB->SMTEN |= GPIO_SMTEN_SMTEN12_Msk | GPIO_SMTEN_SMTEN13_Msk;
		
		/* I2C pin enable schmitt trigger */
    PB->SMTEN |= GPIO_SMTEN_SMTEN4_Msk | GPIO_SMTEN_SMTEN5_Msk;
    PB->SMTEN |= GPIO_SMTEN_SMTEN2_Msk | GPIO_SMTEN_SMTEN3_Msk;
		PA->SMTEN |= GPIO_SMTEN_SMTEN10_Msk | GPIO_SMTEN_SMTEN11_Msk;
		PF->SMTEN |= GPIO_SMTEN_SMTEN4_Msk | GPIO_SMTEN_SMTEN5_Msk;
		PC->SMTEN |= GPIO_SMTEN_SMTEN2_Msk | GPIO_SMTEN_SMTEN3_Msk;

    /* Lock protected registers */
		
    SYS_LockReg();
}

void UI2C_Init(void)
{
    UI2C_Open(UI2C0, i2c_clock_time);
    printf("UI2C clock %d Hz\n", UI2C_GetBusClockFreq(UI2C0));
}

void I2C_Init(void)
{
    /* Open I2C0 and set clock to 100k */
    I2C_Open(I2C0, i2c_clock_time);
		I2C_Open(I2C1, i2c_clock_time);
		I2C_Open(I2C2, i2c_clock_time);
		I2C_Open(I2C4, i2c_clock_time);
		I2C_Open(I2C3, i2c_clock_time);

    I2C_EnableInt(I2C0);
		I2C_EnableInt(I2C1);
		I2C_EnableInt(I2C2);
		I2C_EnableInt(I2C4);
		I2C_EnableInt(I2C3);
}

void GPA_IRQHandler(void)
{
		if (GPIO_GET_INT_FLAG(PA, BIT12)) // substitude button since START button not work
    {
        GPIO_CLR_INT_FLAG(PA, BIT12);
        button_start = 1;
        //joy_place = 1;
    }
		else if (GPIO_GET_INT_FLAG(PA, BIT13))
    {
        GPIO_CLR_INT_FLAG(PA, BIT13);
				if (view_mode == 0){
					target_i2c ++;
					if (target_i2c > MAX_PORT + 1){
						target_i2c = 1;
					}
					if (target_i2c == MAX_PORT + 1 && target_cmd != 1){
						target_i2c = 1;
					}
				}
        joy_place = 2;
    }
		else if (GPIO_GET_INT_FLAG(PA, BIT14))
    {
        GPIO_CLR_INT_FLAG(PA, BIT14);
				if (view_mode == 0){
					target_cmd --;
					if (target_cmd == 0){
						target_cmd = MAX_CMD;
					}
					if (target_cmd == 2 || target_cmd == 5){
						target_i2c = 1;
					}
					if (target_cmd != 1 && target_i2c == MAX_PORT + 1){
						target_i2c = 1;
					}
				}
				left_right = -1;
        joy_place = 3;
    }
		else if (GPIO_GET_INT_FLAG(PA, BIT15))
    {
        GPIO_CLR_INT_FLAG(PA, BIT15);
				if (view_mode == 0){
					target_i2c --;
					if (target_i2c == 0 && target_cmd != 1){
						target_i2c = MAX_PORT;
					}
					if (target_i2c == 0){
						target_i2c = MAX_PORT + 1;
					}
				}
        joy_place = 4;
    }
}

void GPC_IRQHandler(void)
{
    /* To check if PC.5 interrupt occurred */
    if (GPIO_GET_INT_FLAG(PC, BIT5))
    {
        GPIO_CLR_INT_FLAG(PC, BIT5);
        button_start = 1;
    }
		
		if (GPIO_GET_INT_FLAG(PC, BIT4))
    {
        GPIO_CLR_INT_FLAG(PC, BIT4);
				if (view_mode == 0){
					target_cmd ++;
					if (target_cmd > MAX_CMD){
						target_cmd = 1;
					}
					if (target_cmd == 2 || target_cmd == 5){
						target_i2c = 1;
					}
					if (target_cmd != 1 && target_i2c == MAX_PORT + 1){
						target_i2c = 1;
					}
				}
				left_right = 1;
        joy_place = 5;
    }
}

void LCD_Init(void){
		HAL_InitTick(3);
		ssd1306_Init();
		ssd1306_Fill(Black);
		ssd1306_SetCursor(2, 0);
		ssd1306_WriteString("NUDIMM_GANG", Font_6x8, White);
		ssd1306_SetCursor(2, 8 * 2);
		ssd1306_WriteString("Please Wait ...", Font_6x8, White);
		ssd1306_UpdateScreen();		
		//HAL_Delay(3000);
}

//int count = 0;
void update_lcd(void){
		input_flag = 1;
		
		if (view_mode == 0){			
			ssd1306_Fill(Black);
			ssd1306_SetCursor(2, 0);
			ssd1306_WriteString("NUDIMM_GANG V1.08", Font_6x8, White);
			char str_buffer[64] = {0};
			const char *word;
			switch (target_cmd) {
				//case 1: word = "UPDATE APROM"; break;
				case 1: word = "PROGRAM"; break;
				case 2: word = "BIN INFO"; break;
				case 3: word = "SPD READ"; break;
				case 4: word = "DIMM INFO"; break;
				case 5: word = "SPD INFO"; break;
        default: word = "INVALID"; break;
			}
			sprintf(str_buffer, "I2C CMD: %s", word);
			ssd1306_SetCursor(2, 16);
			ssd1306_WriteString(str_buffer, Font_6x8, White);
			char str_buffer2[64] = {0};
			if (target_cmd != 2 && target_cmd != 5){
					switch (target_i2c) {
						case 1: word = "PORT 0"; break;
						case 2: word = "PORT 1"; break;
						case 3: word = "PORT 2"; break;
						case 4: word = "PORT 3"; break;
						case 5: word = "PORT 4"; break;
						case 6: word = "ALL PORT"; break;
						default: word = "INVALID"; break;
					}
					sprintf(str_buffer2,  "I2C PORT: %s", word);
					ssd1306_SetCursor(2, 8 * 4);
					ssd1306_WriteString(str_buffer2, Font_6x8, White);
			}
			ssd1306_UpdateScreen();
		}
		else{
			view_mode = view_mode + left_right;
			if (view_mode == 0) view_mode = 32;
			if (view_mode > 32) view_mode = 1;
			ssd1306_Fill(Black);
			ssd1306_SetCursor(2, 0);
			char str_buffer[64] = {0};
			int ord = (view_mode - 1) * 32;
			sprintf(str_buffer,  "View Mode: block %2d", (view_mode - 1)/2);
			ssd1306_WriteString(str_buffer, Font_6x8, White);
			for (int i = 0; i < 5; i ++){
					ssd1306_SetCursor(2, 16 + i * 8);
					if (i != 4) sprintf(str_buffer, "%02X %02X %02X %02X %02X %02X %02X",st[ord],st[ord+1],st[ord+2],st[ord+3],st[ord+4],st[ord+5],st[ord+6]);
					else sprintf(str_buffer, "%02X %02X %02X %02X <- %02d ->",st[ord],st[ord+1],st[ord+2],st[ord+3], view_mode - 1);
					ord += 7;
					ssd1306_WriteString(str_buffer, Font_6x8, White);
			}
			ssd1306_UpdateScreen();
		}
}

int32_t main(void)
{
    /* Init System, peripheral clock and multi-function I/O */
    SYS_Init();
	
		button_start = 0;
		joy_place = 0;

		PC14 = 1;
		PB15 = 1;
	
		char str_buffer[64] = {0};
		char str_buffer2[64] = {0};
		char str_buffer3[64] = {0};
		
		memset(st, 0xFF, sizeof(st));

    printf("NuMicro HSUSBD HID\n");

    /* Endpoint configuration */
		HSUSBD_Open(&gsHSInfo, HID_ClassRequest, NULL);
    HSUSBD_SetVendorRequest(HID_VendorRequest);
		
		I2C_Init();
    HID_Init();
		UI2C_Init();
		LCD_Init();
		
		gpio_led_ctrl(0x0000);
		
		for(int i = 0 ; i < 40; i++){
				CLK_SysTickDelay(50000);
		}	
		
		gpio_led_ctrl(0x7FFF);
		
    /* Enable HSUSBD interrupt */
    NVIC_EnableIRQ(USBD20_IRQn);
    NVIC_EnableIRQ(GPA_IRQn);
		NVIC_EnableIRQ(GPC_IRQn);

    /* Start transaction */
    HSUSBD_Start();
		update_lcd();

    while(1)
    {		
				if (!HSUSBD_IS_ATTACHED()){
						offline_mode = 1;
				}
			
				if (button_start != 0)
        {
						button_start = 0; //clear button
						if (view_mode != 0){
								view_mode = 0;
								update_lcd();
						}
						else if (offline_mode && input_flag){
								NVIC_DisableIRQ(USBD20_IRQn);
								NVIC_DisableIRQ(GPA_IRQn);
								NVIC_DisableIRQ(GPC_IRQn);
							
								view_mode = offline_operation(target_i2c, target_cmd);
								input_flag = 0;
							
								NVIC_EnableIRQ(USBD20_IRQn);
								NVIC_EnableIRQ(GPA_IRQn);
								NVIC_EnableIRQ(GPC_IRQn);
						}
						else if (offline_mode){
								update_lcd();
						}
						else{
								ssd1306_Fill(Black);
								sprintf(str_buffer,  "Offline Mode not work");
								ssd1306_SetCursor(2, 0);
								ssd1306_WriteString(str_buffer, Font_6x8, White);
								sprintf(str_buffer2,  "when USB connect");
								ssd1306_SetCursor(2, 8 * 2);
								ssd1306_WriteString(str_buffer2, Font_6x8, White);
								sprintf(str_buffer3,  "Input to continue...");
								ssd1306_SetCursor(2, 8 * 4);
								ssd1306_WriteString(str_buffer3, Font_6x8, White);
								ssd1306_UpdateScreen();
								view_mode = 0;
						}
        }
				
				if (joy_place > 0 && joy_place < 6)
        {		
						joy_place = 0;
						update_lcd();
						left_right = 0;
        }
				
				if(g_u8UsbDataReady == TRUE)
        {		
						offline_mode = 0;
						NVIC_DisableIRQ(USBD20_IRQn);
						NVIC_DisableIRQ(GPA_IRQn);
						NVIC_DisableIRQ(GPC_IRQn);
					
            int res = ParseCmd((uint8_t *)g_u8OutBuff, PACK_SIZE);
            EPA_Handler();								
            g_u8UsbDataReady = FALSE;
					
						NVIC_EnableIRQ(USBD20_IRQn);
						NVIC_EnableIRQ(GPA_IRQn);
						NVIC_EnableIRQ(GPC_IRQn);
					
						if (res != 0xFFFF){
								gpio_led_ctrl(res);
						}				
        }			
    }
}
