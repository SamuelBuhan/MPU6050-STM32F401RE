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

#define ACCEL_CONFIG 0x1C

#define FIFO_ENABLE  0x23
#define PWR_MGMT_1 	 0x6B

#define ACCEL_XOUT_H 0x3B
#define ACCEL_XOUT_L 0x3C
#define ACCEL_YOUT_H 0x3D
#define ACCEL_YOUT_L 0x3E
#define ACCEL_ZOUT_H 0x3F
#define ACCEL_ZOUT_L 0x40

#define WHO_AM_I 0x75


/* Data structures */
typedef enum
{
	MPU6050_INIT,
	MPU6050_RUNNING,
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
