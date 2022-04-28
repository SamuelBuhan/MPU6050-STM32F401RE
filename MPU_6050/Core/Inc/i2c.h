/**
  ******************************************************************************
  * @file    i2c.h
  * @brief   This file contains all the function prototypes for
  *          the i2c.c file
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __I2C_H__
#define __I2C_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

extern I2C_HandleTypeDef hi2c1;

/* USER CODE BEGIN Private defines */
typedef struct
{
	void (* fEndTx)(void);
	void (* fEndRx)(void);
	void (* fError)(void);
	uint16_t DevAddress;
}I2cConfig_st;
/* USER CODE END Private defines */

void MX_I2C1_Init(void);

/* USER CODE BEGIN Prototypes */
void MX_I2C1_Configuration(I2cConfig_st*);
void MX_I2C1_Transmit(uint8_t* pTxBuffer, uint8_t ucSize);
void MX_I2C1_Receive(uint8_t* pRxBuffer, uint8_t ucSize);
void MX_I2C1_Mem_Write(uint16_t memAdress, uint16_t memSize,uint8_t* pTxBuffer, uint8_t ucSize);
void MX_I2C1_Mem_Read(uint16_t memAdress, uint16_t memSize,uint8_t* pRxBuffer, uint8_t ucSize);
/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __I2C_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
