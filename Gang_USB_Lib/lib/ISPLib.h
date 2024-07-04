#pragma once

#define CMD_GET_VERSION     	(unsigned char)0xA6
#define CMD_UPDATE_APROM		(unsigned char)0xA0
#define CMD_READ_APROM			(unsigned char)0xA1
#define CMD_READ_CONFIG     	(unsigned char)0xA2
#define CMD_ERASE_APROM 	    (unsigned char)0xA3
#define CMD_GET_DEVICEID    	(unsigned char)0xB1
#define CMD_CONNECT				(unsigned char)0xAE
#define CMD_RESEND_PACKET   	(unsigned char)0xFF

#define CMD_ERASE_HUB           (unsigned char)0x10
#define CMD_WRITE_HUB           (unsigned char)0x20
#define CMD_READ_HUB            (unsigned char)0x30
#define CMD_GET_HUBVER          (unsigned char)0x40
#define CMD_GET_HUBBOOT         (unsigned char)0x50
#define CMD_JUMP_HUB            (unsigned char)0x60
#define CMD_READ_REG            (unsigned char)0x70
#define CMD_READ_INFO32         (unsigned char)0x80
#define CMD_WRITE_INFO32        (unsigned char)0x90

#define CMD_VERIFY_HUB          (unsigned char)0xC0
#define CMD_VERIFY_CHECKSUM     (unsigned char)0xD0
#define CMD_WRITE_REG			(unsigned char)0xE0

#define USBCMD_TIMEOUT				300000
#define USBCMD_TIMEOUT_LONG			3000000
#define I2CCMD_TIMEOUT				45000000

#define FALSE	0
#define TRUE	1

#define PACK_SIZE  1024

typedef struct
{
	void (*init)(void);
	unsigned int (*open)(void);
	void (*close)(void);
	unsigned int (*write)(unsigned int dwMilliseconds, unsigned char* pcBuffer);
	unsigned int (*read)(unsigned int dwMilliseconds, unsigned char* pcBuffer);
} DEV_IO;

typedef struct
{
	unsigned int dev_open;
	unsigned int bResendFlag;
	unsigned char m_usCheckSum;
	unsigned char ac_buffer[PACK_SIZE + 1];
	void* dev_io;
	DEV_IO m_dev_io;
} io_handle_t;

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

// use the open/close/read/write third party provided
DLL_EXPORT  unsigned short Checksum(unsigned char* buf, unsigned int len);

DLL_EXPORT  unsigned int ISP_Open(io_handle_t* handle);
DLL_EXPORT  void ISP_Close(io_handle_t* handle);
DLL_EXPORT  void ISP_ReOpen(io_handle_t* handle);

DLL_EXPORT  unsigned int ISP_Read(io_handle_t* handle, unsigned char* pcBuffer, unsigned int szMaxLen, unsigned int dwMilliseconds, unsigned char* bNum, unsigned char* ext);
DLL_EXPORT  unsigned int ISP_Write(io_handle_t* handle, unsigned char uCmd, unsigned char bext, unsigned char* pcBuffer, unsigned int dwLen, unsigned int dwMilliseconds);

DLL_EXPORT  unsigned int ISP_Connect(io_handle_t* handle, unsigned int dwMilliseconds);
DLL_EXPORT  unsigned int ISP_Resend(io_handle_t* handle, unsigned char* bNum, unsigned char* ext);

DLL_EXPORT  unsigned char ISP_GetVersion(io_handle_t* handle);
DLL_EXPORT  unsigned int ISP_GetDeviceID(io_handle_t* handle);

DLL_EXPORT  unsigned int Erase_APROM(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned short pcount, unsigned int staddr);
DLL_EXPORT  unsigned int Write_APROM(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned short dcount, unsigned int staddr, unsigned char data[]);
DLL_EXPORT  unsigned int Read_APROM(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned short dcount, unsigned int staddr, unsigned char data[]);
DLL_EXPORT  unsigned long long int Get_Version(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char* Num, unsigned char* ext);
DLL_EXPORT  unsigned long long int Get_Boot(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char* Num, unsigned char* ext);
DLL_EXPORT  unsigned int Jump_Code(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char boot_select);
DLL_EXPORT  unsigned long long int Read_Reg(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char reg, unsigned char* Num, unsigned char* ext);
DLL_EXPORT	unsigned int Read_Info32(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char pagecnt, unsigned char offset, unsigned char data[], unsigned char* Num, unsigned char* ext);
DLL_EXPORT	unsigned int Write_Info32(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char pagecnt, unsigned char offset, unsigned char data[], unsigned char* Num, unsigned char* ext);
DLL_EXPORT	unsigned int Write_Reg(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned char reg, unsigned char write_value, unsigned char* Num, unsigned char* ext);

DLL_EXPORT  unsigned int ISP_Read_Config(io_handle_t* handle, unsigned int config[]);
DLL_EXPORT	unsigned int ISP_Erase_DataFlash(io_handle_t* handle);
DLL_EXPORT	unsigned int ISP_Read_DataFlash(io_handle_t* handle, unsigned short dcount, unsigned int staddr, unsigned char data[]);
DLL_EXPORT	unsigned int ISP_Update_DataFlash(io_handle_t* handle, unsigned short dcount, unsigned int staddr, unsigned char data[]);

DLL_EXPORT  unsigned long long int Verify_APROM_Checksum(io_handle_t* handle, unsigned char bsel, unsigned char bext, unsigned long int crc32_checksum);

#ifdef __cplusplus
}
#endif