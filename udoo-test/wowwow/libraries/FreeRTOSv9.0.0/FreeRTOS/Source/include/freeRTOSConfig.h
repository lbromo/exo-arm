/*
  FreeRTOS.org V5.0.3 - Copyright (C) 2003-2008 Richard Barry.

  This file is part of the FreeRTOS.org distribution.

  FreeRTOS.org is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  FreeRTOS.org is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with FreeRTOS.org; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  A special exception to the GPL can be applied should you wish to distribute
  a combined work that includes FreeRTOS.org, without being obliged to provide
  the source code for any proprietary components.  See the licensing section
  of http://www.FreeRTOS.org for full details of how and when the exception
  can be applied.

  ***************************************************************************
  ***************************************************************************
  *                                                                         *
  * SAVE TIME AND MONEY!  We can port FreeRTOS.org to your own hardware,    *
  * and even write all or part of your application on your behalf.          *
  * See http://www.OpenRTOS.com for details of the services we provide to   *
  * expedite your project.                                                  *
  *                                                                         *
  ***************************************************************************
  ***************************************************************************

  Please ensure to read the configuration and relevant port sections of the
  online documentation.

  http://www.FreeRTOS.org - Documentation, latest information, license and
  contact details.

  http://www.SafeRTOS.com - A version that is certified for use in safety
  critical systems.

  http://www.OpenRTOS.com - Commercial support, development, porting,
  licensing and training services.
*/

#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/*-----------------------------------------------------------
 * Application specific definitions.
 *
 * These definitions should be adjusted for your particular hardware and
 * application requirements.
 *
 * THESE PARAMETERS ARE DESCRIBED WITHIN THE 'CONFIGURATION' SECTION OF THE
 * FreeRTOS API DOCUMENTATION AVAILABLE ON THE FreeRTOS.org WEB SITE.
 *----------------------------------------------------------*/

#define LITTLE_ENDIAN				1

/* IMPORTANT:
 * This re-define of printf moves all stored string into program-space
 * This REUQIRES that FreeRTOS.h is ALWAYS includede AFTER <stdio.h>
 */
#define printf(s, ...) printf_P(PSTR(s), ## __VA_ARGS__)

#define configUSE_PREEMPTION		1
#define configUSE_IDLE_HOOK			1
#define configUSE_TICK_HOOK			0

extern unsigned long fcpu;
//#define configCPU_CLOCK_HZ			( ( unsigned portLONG ) 8000000 )
//#define configCPU_CLOCK_HZ			( ( unsigned portLONG ) 16000000 )
#define configTICK_RATE_HZ			( ( portTickType ) 100 )
#define configMAX_PRIORITIES		( ( unsigned portBASE_TYPE ) 20 ) //possible task priorities (high number uses more RAM)
#define configMINIMAL_STACK_SIZE	( ( unsigned portSHORT ) 200 ) //The size of the stack used by the idle task.
#define stack_size		            ( ( unsigned portSHORT ) 200 ) //The size of the stack used by tasks.
//#define configTOTAL_HEAP_SIZE		( (size_t ) ( 2000 ) ) //The total amount of RAM available to the kernel. (define it when using heap_2.c)
#define configMAX_TASK_NAME_LEN		( 8 ) //Max 7 chars as name
#define configUSE_TRACE_FACILITY	1 //debug facility
#define configUSE_16_BIT_TICKS		1 //Max 650 seconds delay on tasks. If set to 0 a 32 bit value is used, but decreases performance.
#define configIDLE_SHOULD_YIELD		0 //0 = If we have tasks that share IDLE priority, they will share timeslices with idle_task.
#define configQUEUE_REGISTRY_SIZE	0 //Allows a textual name to be associated with a queue for easy queue identification within a debugging GUI.
#define configUSE_MUTEXES			1

/* Co-routine definitions. */
#define configUSE_CO_ROUTINES 		0
#define configMAX_CO_ROUTINE_PRIORITIES ( 0 )

/* Set the following definitions to 1 to include the API function, or zero
   to exclude the API function. */

#define INCLUDE_vTaskPrioritySet		0
#define INCLUDE_uxTaskPriorityGet		0
#define INCLUDE_vTaskDelete				1
#define INCLUDE_vTaskCleanUpResources	0
#define INCLUDE_vTaskSuspend			1
#define INCLUDE_vTaskDelayUntil			1
#define INCLUDE_vTaskDelay				1
#define INCLUDE_uxTaskGetStackHighWaterMark 0
#define INCLUDE_xTaskGetCurrentTaskHandle 1

#endif /* FREERTOS_CONFIG_H */
