#include <stdio.h>
#include <stdint.h>

uint16_t crc16(uint8_t *data, uint32_t len) { 
    uint16_t crc = 0x0000; 
    for (uint32_t i = 0; i < len - 2; i++) { 
        uint8_t newByte = data[i]; 
        for (unsigned char i = 0; i < 8; i++) { 
            if (((crc & 0x8000) >> 8) ^ (newByte & 0x80)) { 
                crc = (crc << 1) ^ 0x1021; 
            } else { 
                crc = (crc << 1); 
            } 
            newByte <<= 1; 
        } 
    }
    uint16_t result = crc ^ data[len - 1] ^ (data[len - 2] << 8);
    return result; 
}

int main() {
    uint8_t data[] = {0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x77, 0x6F, 0x72, 0x6C, 0x64, 0x3A, 0x20, 0x36, 0x32};
    // uint8_t data[] = {0x32, 0x36, 0x20, 0x3A, 0x64, 0x6C, 0x72, 0x6F, 0x77, 0x20, 0x6F, 0x6C, 0x6C, 0x65, 0x48};
    uint32_t len = sizeof(data) / sizeof(data[0]);
    uint16_t result = crc16(data, len);
    printf("0x%04X\n", result);
    return 0;
}
