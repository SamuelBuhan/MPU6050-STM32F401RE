/*
 * MPU6050.c
 *
 *  Created on: Feb 20, 2022
 *      Author: Utilisateur
 */

/* Includes */
#include "MPU6050.h"
#include "i2c.h"
#include "usart.h"

/* Defines */
#define SIZE_DATA 10

/* variables */
MPU6050_st MPU6050;

typedef struct {
	uint8_t header;
	uint16_t accX[SIZE_DATA];
	uint16_t accY[SIZE_DATA];
	uint16_t accZ[SIZE_DATA];
	uint16_t gyroX[SIZE_DATA];
	uint16_t gyroY[SIZE_DATA];
	uint16_t gyroZ[SIZE_DATA];
	uint8_t crc;
} Frame;

/* static functions */
static void imu_TxEnd(void);
static void imu_RxEnd(void);
static void imu_Error(void);
static uint8_t MPU6050_configureRegisters(void);

/* Functions*/
static void imu_TxEnd(void)
{
	MPU6050.FlagTxEnd = 1;
}


static void imu_RxEnd(void)
{
	MPU6050.FlagRxEnd = 1;
}

static void imu_Error(void)
{
	MPU6050.FlagError = 1;
}

static uint8_t MPU6050_configureRegisters(void)
{
	// Power on MPU6050
	MPU6050.FlagTxEnd = 0;
	MPU6050.TxBuffer[0] = 0x00;
	MX_I2C1_Mem_Write(PWR_MGMT_1, 1, MPU6050.TxBuffer, 1);
	while (MPU6050.FlagTxEnd == 0);

	MPU6050.FlagRxEnd = 0;
	MPU6050.RxBuffer[0] = 0;
	MX_I2C1_Mem_Read(PWR_MGMT_1, 1, MPU6050.RxBuffer, 1);
	while (MPU6050.FlagRxEnd == 0);
	return (MPU6050.TxBuffer[0] == MPU6050.RxBuffer[0]);
}

void MPU6050_init(void)
{
	I2cConfig_st I2cConfig;
	I2cConfig.fEndRx = imu_RxEnd;
	I2cConfig.fEndTx = imu_TxEnd;
	I2cConfig.fError = imu_Error;
	I2cConfig.DevAddress = MPU6050_ADDR;

	MX_I2C1_Configuration(&I2cConfig);

	// Power off MPU6050
	HAL_GPIO_WritePin(Alim_MPU6050_GPIO_Port, Alim_MPU6050_Pin, GPIO_PIN_RESET);
	HAL_Delay(100);

	// Power on MPU6050
	HAL_GPIO_WritePin(Alim_MPU6050_GPIO_Port, Alim_MPU6050_Pin, GPIO_PIN_SET);
	HAL_Delay(100);

	// Flags init
	MPU6050.FlagRxEnd = 0;
	MX_I2C1_Mem_Read(WHO_AM_I, 1, MPU6050.RxBuffer, 1);
	while (MPU6050.FlagRxEnd == 0);


	if (MPU6050.RxBuffer[0] == 0x68)
	{
		//MPU6050 detected
		MX_USART2_Transmit((uint8_t * )"MPU6050 detected\n", sizeof("MPU6050 detected\n"));
		// Configure register
		if (MPU6050_configureRegisters())
		{
			// MPU6050 init
			MPU6050.sState = MPU6050_RUNNING;
			MX_USART2_Transmit((uint8_t * )"MPU6050 configured\n", sizeof("MPU6050 configured\n"));
		}
	}
	else
	{
		MX_USART2_Transmit((uint8_t * )"MPU6050 not detected\n", sizeof("MPU6050 not detected\n"));
	}
}

void MPU6050_sendFrame(uint8_t* pData, uint8_t size)
{
	pData[size] = CRC8(pData, size);
	MX_USART2_Transmit(pData, size+1);
}

uint8_t CRC8(uint8_t* pData, uint8_t size)
{
	uint8_t crc = 0x00;
	for(uint8_t i = 0; i < size; ++i)
	{
		crc = crc ^ pData[i];
	}
	return crc;
}

void MPU6050_main(void)
{
	Frame frame;
	switch (MPU6050.sState)
	{
		case MPU6050_INIT:
			break;
		case MPU6050_RUNNING:
			// Flags init
			frame.header = 0x55;
			for(uint8_t i = 0; i < SIZE_DATA; ++i)
			{
				MPU6050.FlagRxEnd = 0;
				MPU6050.RxBuffer[0] = 0;
				MPU6050.RxBuffer[1] = 0;
				MPU6050.RxBuffer[2] = 0;
				MPU6050.RxBuffer[3] = 0;
				MPU6050.RxBuffer[4] = 0;
				MPU6050.RxBuffer[5] = 0;
				MX_I2C1_Mem_Read(ACCEL_XOUT_H, 1, MPU6050.RxBuffer, 6);
				while (MPU6050.FlagRxEnd == 0);
				frame.accX[i] = (MPU6050.RxBuffer[0] << 8) + MPU6050.RxBuffer[1];
				frame.accY[i] = (MPU6050.RxBuffer[2] << 8) + MPU6050.RxBuffer[3];
				frame.accZ[i] = (MPU6050.RxBuffer[4] << 8) + MPU6050.RxBuffer[5];
				frame.gyroX[i] = 0x0000;
				frame.gyroY[i] = 0x0000;
				frame.gyroZ[i] = 0x0000;
			}
			MPU6050_sendFrame((uint8_t*)&frame, sizeof(frame));
			break;
	}

}
