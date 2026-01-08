#include <stdio.h>
#include "NuMicro.h"
#include "i2c_transfer.h"
#include "isp_user.h"

//#define verC

I2C_T* i2c_f[5] = {I2C0, I2C1, I2C2, I2C4, I2C3};
int32_t I2C_Read_Write(int I2c_num, int I2c_ext, uint8_t u8SlvAddr[5], uint8_t u8DataAddr, uint8_t *I2C_TxData, uint8_t **I2C_RxData, int tx_length, int rx_length, int need_stop)
{
		if (I2c_num == 0 && I2c_ext == 0){
		    return 0;
		}
    uint32_t u32TimeOutCnt = I2C_TIMEOUT;
		if (tx_length != 0){
				I2C_WriteMultiBytesOneReg_2(I2c_num, I2c_ext, i2c_f, u8SlvAddr, u8DataAddr, I2C_TxData, tx_length);
				//CLK_SysTickDelay(40); 
		}	
		if (rx_length == 0){
		    return 0;
		}
#ifdef verC
		if (need_stop == 1){
				I2C_ReadMultiBytesOneReg_STOP(I2c_num, I2c_ext, i2c_f, u8SlvAddr, u8DataAddr, I2C_RxData, rx_length);
		}
		else{
				I2C_ReadMultiBytesOneReg_2(I2c_num, I2c_ext, i2c_f, u8SlvAddr, u8DataAddr, I2C_RxData, rx_length);	
		}
#else
		I2C_ReadMultiBytesOneReg_2(I2c_num, I2c_ext, i2c_f, u8SlvAddr, u8DataAddr, I2C_RxData, rx_length);	
#endif
		return 0;
}

uint8_t i2c_address_acknowledged(int I2c_num, uint8_t u8SlaveAddr) {
    uint8_t u8Err = 0u;
    uint32_t u32TimeOutCount = 0u;

    g_I2C_i32ErrCode = 0;
		I2C_T * I2C_PORT[5] = {I2C0, I2C1, I2C2, I2C4, I2C3};
    I2C_START(I2C_PORT[I2c_num]); // Send START
    while (1) {
        u32TimeOutCount = I2C_TIMEOUT / 10000;
        I2C_WAIT_READY(I2C_PORT[I2c_num]) {
            if(--u32TimeOutCount == 0) {
                g_I2C_i32ErrCode = I2C_ERR_TIMEOUT;
                u8Err = 1u;
                break;
            }
        }
        switch(I2C_GET_STATUS(I2C_PORT[I2c_num])) {
            case 0x08u:
                I2C_SET_DATA(I2C_PORT[I2c_num], (uint8_t)(u8SlaveAddr << 1u)); // Send slave address
                I2C_SET_CONTROL_REG(I2C_PORT[I2c_num], I2C_CTL_SI); // Clear SI
                break;
            case 0x18u: // Slave Address ACK
                I2C_SET_CONTROL_REG(I2C_PORT[I2c_num], I2C_CTL_STO_SI); // Send STOP
                if (g_I2C_i32ErrCode == 0) {
                    return 1; // Address acknowledged and no error
                }
								break;
            case 0x20u: // Slave Address NACK
                I2C_SET_CONTROL_REG(I2C_PORT[I2c_num], I2C_CTL_STO_SI); // Send STOP
                return 0; // Address not acknowledged
            default:
                I2C_SET_CONTROL_REG(I2C_PORT[I2c_num], I2C_CTL_STO_SI); // Send STOP in other cases
                return 0;
        }
				if (u8Err || g_I2C_i32ErrCode != 0) {
						break; // If any error occurred, exit loop
				}
    }
    return 0; // Default return
}