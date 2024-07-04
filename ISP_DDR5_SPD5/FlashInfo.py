import os

from PartNumID import *
from Flash import *

def GetStaticInfo(self, UID, config):
    chip_name = ""
    chip_type = 0x0
    aprom_size = 0
    nvm_size = 0
    nvm_addr = 0
    memory_size = 0
    flash_type = 0
    dataflash_size = 0
    page_size = 0
    table_len = len(PartNumIDs)
    for i in range(table_len):
        if (UID == PartNumIDs[i][1]):
            chip_name = PartNumIDs[i][0]
            chip_type = PartNumIDs[i][2]
            break 
        
    if chip_type != 0x0:
        # type Numicro
        flash_table_len = len(Flash_NuMicro)
        for i in range(flash_table_len):
            if (UID == Flash_NuMicro[i][5]):
                memory_size = Flash_NuMicro[i][0]
                dataflash_size = Flash_NuMicro[i][1]
                ldrom_size = Flash_NuMicro[i][4]
                break
        
        flash_type = 1 if (dataflash_size != 0) else 0
            
        if ((chip_type == PROJ_M460HD) or (chip_type == PROJ_M460LD)):
            flash_type |= 0x300
        
        aprom_size = memory_size
        nvm_size = 0
        nvm_addr = aprom_size
        aprom_size, nvm_size, nvm_addr = GetDynamicInfo_NuMicro(UID, config, memory_size, flash_type)
        page_size = 1 << (((flash_type & 0x0000FF00) >>  8) + 9)
            
    return chip_name, chip_type, aprom_size, nvm_size, nvm_addr, page_size 
    
def GetDynamicInfo_NuMicro(UID, config, memory_size, flash_type):
    utype = flash_type & 0xFF
    bShare = True if (utype == 0) else False
    
    if (utype == 2) and (config[0] & 0x4 == 0):
        memory_size += 0x1000
        bShare = True
    
    if (bShare):
        if (config[0] & 0x1 == 0):
            page_size = ((flash_type & 0x0000FF00) >>  8) + 9
            addr = config[1] & 0x00FFFFFF
            addr &= ~((1 << page_size) - 1)
            aprom_size = addr if (memory_size > addr) else memory_size
            nvm_size = memory_size - aprom_size
        else:
            aprom_size = memory_size
            nvm_size = 0
        nvm_addr = aprom_size
    else:
        aprom_size = memory_size
        nvm_size = 0x1000
        nvm_addr = 0x1F000
    
    return aprom_size, nvm_size, nvm_addr