/*
 * MPU6050.h
 *
 *  Created on: Feb 20, 2022
 *      Author: Utilisateur
 */

#ifndef INC_MPU6050_H_
#define INC_MPU6050_H_

/* Includes */
#include <stdint.h> // uint8_t

/* define */
#define SIZE_RX 256
#define SIZE_TX 256
#define MPU6050_ADDR (0x0068<<1)

/* Register map*/
//self test
#define SELF_TEST_X   		0x0D
#define SELF_TEST_Y   		0x0E
#define SELF_TEST_Z   		0x0F
#define SMPLRT_DIV    		0x19

//config
#define CONFIG		  		0x1A
#define GYRO_CONFIG   		0x1B
#define ACCEL_CONFIG  		0x1C

//fifo
#define FIFO_ENABLE   		0x23

//i2c
#define I2C_MST_CTRL  		0x24
#define I2C_SLV0_ADDR 		0x25
#define I2C_SLV0_REG  		0x26
#define I2C_SLV0_CTRL 		0x27
#define I2C_SLV1_ADDR 		0x28
#define I2C_SLV1_REG  		0x29
#define I2C_SLV1_CTRL 		0x2A
#define I2C_SLV2_ADDR 		0x2B
#define I2C_SLV2_REG  		0x2C
#define I2C_SLV2_CTRL 		0x2D
#define I2C_SLV3_ADDR 		0x2E
#define I2C_SLV3_REG  		0x2F
#define I2C_SLV3_CTRL 		0x30
#define I2C_SLV4_ADDR 		0x31
#define I2C_SLV4_REG  		0x32
#define I2C_SLV4_DO 		0x33
#define I2C_SLV4_CTRL 		0x34
#define I2C_SLV4_DI 		0x35
#define I2C_MST_STATUS 		0x36

//interruptions
#define INT_PIN_CFG 		0x37
#define INT_ENABLE 			0x38
#define INT_STATUS 			0x3A

// data out
#define ACCEL_XOUT_H 		0x3B
#define ACCEL_XOUT_L 		0x3C
#define ACCEL_YOUT_H 		0x3D
#define ACCEL_YOUT_L 		0x3E
#define ACCEL_ZOUT_H 		0x3F
#define ACCEL_ZOUT_L 		0x40
#define TEMP_OUT_H 			0x41
#define TEMP_OUT_L 			0x42
#define GYRO_XOUT_H 		0x43
#define GYRO_XOUT_L 		0x44
#define GYRO_YOUT_H 		0x45
#define GYRO_YOUT_L 		0x46
#define GYRO_ZOUT_H 		0x47
#define GYRO_ZOUT_L 		0x48

//EXT
#define EXT_SENS_DATA_00 	0x49
#define EXT_SENS_DATA_01 	0x4A
#define EXT_SENS_DATA_02 	0x4B
#define EXT_SENS_DATA_03 	0x4C
#define EXT_SENS_DATA_04 	0x4D
#define EXT_SENS_DATA_05 	0x4E
#define EXT_SENS_DATA_06 	0x4F
#define EXT_SENS_DATA_07 	0x50
#define EXT_SENS_DATA_08 	0x51
#define EXT_SENS_DATA_09 	0x52
#define EXT_SENS_DATA_10 	0x53
#define EXT_SENS_DATA_11 	0x54
#define EXT_SENS_DATA_12 	0x55
#define EXT_SENS_DATA_13 	0x56
#define EXT_SENS_DATA_14 	0x57
#define EXT_SENS_DATA_15 	0x58
#define EXT_SENS_DATA_16 	0x59
#define EXT_SENS_DATA_17 	0x5A
#define EXT_SENS_DATA_18 	0x5B
#define EXT_SENS_DATA_19 	0x5C
#define EXT_SENS_DATA_20 	0x5D
#define EXT_SENS_DATA_21 	0x5E
#define EXT_SENS_DATA_22 	0x5F
#define EXT_SENS_DATA_23 	0x60

//i2c DO
#define I2C_SLV0_DO 		0x63
#define I2C_SLV1_DO 		0x64
#define I2C_SLV2_DO 		0x65
#define I2C_SLV3_DO 		0x66
#define I2C_MST_DELAY_CTRL	0x67

//
#define SIGNAL_PATH_RESET 	0x68
#define USER_CTRL	 		0x6A

// POWER
#define PWR_MGMT_1 	 		0x6B
#define PWR_MGMT_2 	 		0x6C

//FIFO
#define FIFO_COUNTH 	 	0x72
#define FIFO_COUNTL 	 	0x73
#define FIFO_R_W	 	 	0x74

#define WHO_AM_I 			0x75


/* Data structures */
typedef enum
{
	MPU6050_INIT,
	MPU6050_RUNNING,
	MPU6050_WAIT_TX_DATA,
}MPU6050State_enum;


typedef struct
{
	uint8_t RxBuffer[SIZE_RX];
	uint8_t TxBuffer[SIZE_TX];
	uint8_t FlagRxEnd : 1;
	uint8_t FlagTxEnd : 1;
	uint8_t FlagError : 1;
	uint8_t RFU : 5;
	MPU6050State_enum sState;
} MPU6050_st;

/* Prototypes */
void MPU6050_init(void);
void MPU6050_main(void);

void MPU6050_sendFrame(uint8_t* pData, uint8_t size);
uint8_t CRC8(uint8_t* pData, uint8_t size);

#endif /* INC_MPU6050_H_ */
