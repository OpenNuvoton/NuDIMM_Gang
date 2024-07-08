#include <stdio.h>
#include <string.h>
#include "ISPLib.h"

unsigned short Checksum(unsigned char* buf, unsigned int len)
{
	unsigned int i;
	unsigned short c;

	for (c = 0, i = 0; i < len; i++)
	{
		c += buf[i];
	}

	return (c);
}

unsigned int ISP_Open(io_handle_t* handle) {
	if (handle->dev_open) {
		return TRUE;
	}
	// do third party open()
	if (handle->m_dev_io.open()) {
		handle->dev_open = TRUE;
	}
	return handle->dev_open;
}

void ISP_Close(io_handle_t* handle) {
	if (handle->dev_open == FALSE) {
		return;
	}
	handle->m_dev_io.close();
	handle->dev_open = FALSE;
}

void ISP_ReOpen(io_handle_t* handle) {
	ISP_Close(handle);
	ISP_Open(handle);
}

unsigned int ISP_Read(io_handle_t* handle, unsigned char* pcBuffer, unsigned int szMaxLen, unsigned int dwMilliseconds, unsigned char* bNum, unsigned char* ext) {
	unsigned char usCheckSum = 0;
	unsigned char usNum = 0;
	unsigned int dwLength = 0;
	handle->bResendFlag = FALSE;
	if (handle->dev_open == FALSE) {
		return FALSE;
	}
	dwLength = handle->m_dev_io.read(dwMilliseconds, handle->ac_buffer);
	if (!dwLength) {
		return FALSE;
	}

	usCheckSum = *((unsigned short*)&(handle->ac_buffer[1]));
	if (bNum != NULL) {
		memcpy(bNum, (unsigned char*)&(handle->ac_buffer[4]), 1);
	}
	if (ext != NULL) {
		memcpy(ext, (unsigned char*)&(handle->ac_buffer[3]), 1);
	}

	if (dwLength >= 4 && usCheckSum == handle->m_usCheckSum) {
		if (szMaxLen > dwLength - 4) {
			szMaxLen = dwLength - 4;
		}
		if (pcBuffer != NULL && szMaxLen > 0) {
			memcpy(pcBuffer, (unsigned char*)&(handle->ac_buffer[5]), szMaxLen);
			//printf("szMaxLen = %d", szMaxLen);
		}
		return TRUE;
	}
	else {
		handle->bResendFlag = TRUE;
	}
	return TRUE;
}

unsigned int ISP_Write(io_handle_t* handle, unsigned char uCmd, unsigned char ext, unsigned char* pcBuffer, unsigned int dwLen, unsigned int dwMilliseconds) {
	unsigned int dwLength = 0;
	unsigned int dwCmdLength = dwLen;
	unsigned int bRet = FALSE;
	if (handle->dev_open == FALSE) {
		return FALSE;
	}

	if (dwCmdLength > sizeof(handle->ac_buffer) - 3) {
		dwCmdLength = sizeof(handle->ac_buffer) - 3;
	}
	memset(handle->ac_buffer, 0, sizeof(handle->ac_buffer));
	*(&(handle->ac_buffer[1])) = uCmd;
	*(&(handle->ac_buffer[2])) = ext;

	if (pcBuffer != NULL && dwCmdLength > 0) {
		memcpy((unsigned char*)(&(handle->ac_buffer[3])), pcBuffer, dwCmdLength);
	}
	handle->m_usCheckSum = Checksum(&(handle->ac_buffer[1]), sizeof(handle->ac_buffer) - 1);
	bRet = handle->m_dev_io.write(dwMilliseconds, handle->ac_buffer);
	if (bRet == FALSE) {
		handle->m_dev_io.close();
	}
	return bRet;
}

unsigned int ISP_Read_Config(io_handle_t* handle, unsigned int config[]) {
	ISP_Write(handle, CMD_READ_CONFIG, NULL, NULL, 0, USBCMD_TIMEOUT);
	unsigned int ret = ISP_Read(handle, (unsigned char*)config, 8, USBCMD_TIMEOUT, NULL, NULL);
	return ret;
}

unsigned int ISP_Erase_DataFlash(io_handle_t* handle) {
	ISP_Write(handle, CMD_ERASE_APROM, NULL, NULL, 0, USBCMD_TIMEOUT);
	unsigned int ret = ISP_Read(handle, NULL, 0, USBCMD_TIMEOUT, NULL, NULL);
	return ret;
}

unsigned int ISP_Update_DataFlash(io_handle_t* handle, unsigned short dcount, unsigned int staddr, unsigned char data[]) {
	unsigned char acBuffer[PACK_SIZE + 1];
	int ex_of = 0;
	if (dcount <= 250) {
		acBuffer[0] = dcount + 5;
		acBuffer[1] = dcount;
	}
	else {
		ex_of = 1;
		acBuffer[0] = 0;
		memcpy(&acBuffer[1], &dcount, 2);
	}
	memcpy(&acBuffer[2 + ex_of], &staddr, 4);
	memcpy(&acBuffer[6 + ex_of], data, dcount);
	unsigned int ret = ISP_Write(handle, CMD_UPDATE_APROM, NULL, acBuffer, dcount + 6 + ex_of, USBCMD_TIMEOUT_LONG);
	ISP_Read(handle, NULL, 0, USBCMD_TIMEOUT_LONG, NULL, NULL);
	return ret;
}

unsigned int ISP_Read_DataFlash(io_handle_t* handle, unsigned short dcount, unsigned int staddr, unsigned char data[]) {
	unsigned int ret = FALSE;
	unsigned char acBuffer[PACK_SIZE + 1];
	int ex_of = 0;
	if (dcount <= 254) {
		acBuffer[0] = dcount + 1;
		acBuffer[1] = dcount;
	}
	else {
		ex_of = 1;
		acBuffer[0] = 0;
		memcpy(&acBuffer[1], &dcount, 2);
	}
	memcpy(&acBuffer[2 + ex_of], &staddr, 4);
	if (ISP_Write(handle, CMD_READ_APROM, NULL, acBuffer, 6 + ex_of, USBCMD_TIMEOUT_LONG)) {
		ret = ISP_Read(handle, (unsigned char*)data, dcount, USBCMD_TIMEOUT_LONG, NULL, NULL);
	}
	return ret;
}

unsigned int ISP_Connect(io_handle_t* handle, unsigned int dwMilliseconds) {
	unsigned int ret = FALSE;
	unsigned int uID;

	if (ISP_Write(handle, CMD_CONNECT, NULL, NULL, 0, USBCMD_TIMEOUT_LONG)) {
		ret = ISP_Read(handle, (unsigned char*)&uID, 4, dwMilliseconds, NULL, NULL);
	}
	return ret;
}

unsigned char ISP_GetVersion(io_handle_t* handle) {
	unsigned char ucVersion = 0;
	ISP_Write(handle, CMD_GET_VERSION, NULL, NULL, 0, USBCMD_TIMEOUT);
	ISP_Read(handle, (unsigned char*)&ucVersion, 1, USBCMD_TIMEOUT, NULL, NULL);
	return ucVersion;
}

unsigned int ISP_GetDeviceID(io_handle_t* handle) {
	unsigned int uID = 0;
	ISP_Write(handle, CMD_GET_DEVICEID, NULL, NULL, 0, USBCMD_TIMEOUT);
	ISP_Read(handle, (unsigned char*)&uID, 4, USBCMD_TIMEOUT, NULL, NULL);
	return uID;
}

unsigned int ISP_Resend(io_handle_t* handle, unsigned char* Num, unsigned char* ext) {
	unsigned int ret = FALSE;
	if (ISP_Write(handle, CMD_RESEND_PACKET, NULL, NULL, 0, USBCMD_TIMEOUT_LONG)) {
		ret = ISP_Read(handle, NULL, 0, USBCMD_TIMEOUT_LONG, Num, ext);
	}
	return ret;
}

unsigned int Erase_APROM(io_handle_t* handle, unsigned char bsel, unsigned char ext, unsigned short pcount, unsigned int staddr) {
	unsigned char acBuffer[7];
	acBuffer[0] = 0x6;
	memcpy(&acBuffer[1], &pcount, 2);
	memcpy(&acBuffer[3], &staddr, 4);
	unsigned int ret = ISP_Write(handle, CMD_ERASE_HUB + bsel, ext, acBuffer, 7, I2CCMD_TIMEOUT);
	ISP_Read(handle, NULL, 0, I2CCMD_TIMEOUT, NULL, NULL);
	return ret;
}

unsigned int Write_APROM(io_handle_t* handle, unsigned char bsel, unsigned char ext, unsigned short dcount, unsigned int staddr, unsigned char data[]) {
	unsigned char acBuffer[PACK_SIZE + 1];
	int ex_of = 0;
	if (dcount <= 250){
		acBuffer[0] = dcount + 5;
		acBuffer[1] = dcount;
	}
	else {
		ex_of = 1;
		acBuffer[0] = 0;
		memcpy(&acBuffer[1], &dcount, 2);
	}
	memcpy(&acBuffer[2 + ex_of], &staddr, 4);
	memcpy(&acBuffer[6 + ex_of], data, dcount);
	//printf("dcount = %d\n", dcount);
	//printf("last data: %x\n", acBuffer[5 + ex_of + dcount]);
	unsigned int ret = ISP_Write(handle, CMD_WRITE_HUB + bsel, ext, acBuffer, dcount + 6 + ex_of, I2CCMD_TIMEOUT);
	ISP_Read(handle, NULL, 0, I2CCMD_TIMEOUT, NULL, NULL);
	return ret;
}

unsigned int Read_APROM(io_handle_t* handle, unsigned char bsel, unsigned char ext, unsigned short dcount, unsigned int staddr, unsigned char data[]) {
	unsigned int ret = FALSE;
	unsigned char acBuffer[6];
	int ex_of = 0;
	if (dcount <= 255) {
		acBuffer[0] = 0x5;
		acBuffer[1] = dcount;
	}
	else {
		ex_of = 1;
		acBuffer[0] = 0;
		memcpy(&acBuffer[1], &dcount, 2);
	}
	memcpy(&acBuffer[2 + ex_of], &staddr, 4);
	if (ISP_Write(handle, CMD_READ_HUB + bsel, ext, acBuffer, 6 + ex_of, I2CCMD_TIMEOUT)) {
		ret = ISP_Read(handle, (unsigned char*)data, dcount, I2CCMD_TIMEOUT, NULL, NULL);
	}
	return ret;
}

unsigned long long int Get_Version(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char* Num, unsigned char* ext) {
	unsigned int ret = FALSE;
	unsigned long long int version_result = 0;
	if (ISP_Write(handle, CMD_GET_HUBVER + bsel, bext, NULL, 0, I2CCMD_TIMEOUT)) {
		ret = ISP_Read(handle, (unsigned char*)&version_result, 5, I2CCMD_TIMEOUT, Num, ext);
	}
	return version_result;
}

unsigned long long int Get_Boot(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char* Num, unsigned char* ext) {
	unsigned int ret = FALSE;
	unsigned long long int boot_result = 0;
	if (ISP_Write(handle, CMD_GET_HUBBOOT + bsel, bext, NULL, 0, I2CCMD_TIMEOUT)) {
		ret = ISP_Read(handle, (unsigned char*)&boot_result, 5, I2CCMD_TIMEOUT, Num, ext);
	}
	//printf("boot_result = %lld", boot_result);
	return boot_result;
}

unsigned int Jump_Code(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char boot_select) {
	unsigned char acBuffer[1];
	acBuffer[0] = boot_select;
	unsigned int ret = ISP_Write(handle, CMD_JUMP_HUB + bsel, bext, acBuffer, 1, I2CCMD_TIMEOUT);
	ISP_Read(handle, NULL, 0, I2CCMD_TIMEOUT, NULL, NULL);
	return ret;
}

unsigned long long int Read_Reg(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char reg, unsigned char* Num, unsigned char* ext) {
	unsigned char acBuffer[1];
	acBuffer[0] = reg;
	unsigned int ret = FALSE;
	unsigned long long int reg_result = 0;
	ret = ISP_Write(handle, CMD_READ_REG + bsel, bext, acBuffer, 1, I2CCMD_TIMEOUT);
	ISP_Read(handle, (unsigned char*)&reg_result, 5, I2CCMD_TIMEOUT, Num, ext);
	return reg_result;
}

unsigned int Write_Reg(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char reg, unsigned char write_value, unsigned char* Num, unsigned char* ext) {
	unsigned char acBuffer[2];
	acBuffer[0] = reg;
	acBuffer[1] = write_value;
	unsigned int ret = FALSE;
	unsigned long long int reg_result = 0;
	ret = ISP_Write(handle, CMD_WRITE_REG + bsel, bext, acBuffer, 2, I2CCMD_TIMEOUT);
	ISP_Read(handle, NULL, 0, I2CCMD_TIMEOUT, Num, ext);
	return ret;
}

unsigned int Read_Info32(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char pagecnt, unsigned char offset, unsigned char data[], unsigned char* Num, unsigned char* ext) {
	unsigned char acBuffer[2];
	acBuffer[0] = pagecnt;
	acBuffer[1] = offset;
	unsigned int ret = FALSE;
	if (ISP_Write(handle, CMD_READ_INFO32 + bsel, bext, acBuffer, 2, I2CCMD_TIMEOUT)) {
		ret = ISP_Read(handle, (unsigned char*)data, 32, I2CCMD_TIMEOUT, Num, ext);
	}
	return ret;
}

unsigned int Write_Info32(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char pagecnt, unsigned char offset, unsigned char data[], unsigned char* Num, unsigned char* ext) {
	unsigned char acBuffer[34];
	acBuffer[0] = pagecnt;
	acBuffer[1] = offset;
	memcpy(&acBuffer[2], data, 32);
	unsigned int reg_result = 0;
	unsigned int ret = ISP_Write(handle, CMD_WRITE_INFO32 + bsel, bext, acBuffer, 34, I2CCMD_TIMEOUT);
	ISP_Read(handle, NULL, 0, I2CCMD_TIMEOUT, Num, ext);
	return ret;
}

unsigned long long int Verify_APROM_Checksum(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned long int crc32_checksum) {
	unsigned long long int verify;
	unsigned char acBuffer[4];
	memcpy(&acBuffer[0], &crc32_checksum, 4);
	//printf("Checksum = %d\n", crc32_checksum);
	ISP_Write(handle, CMD_VERIFY_CHECKSUM + bsel, bext, acBuffer, 4, 5 * I2CCMD_TIMEOUT);
	ISP_Read(handle, (unsigned char*)&verify, 5, USBCMD_TIMEOUT, NULL, NULL);
	return verify;
}
