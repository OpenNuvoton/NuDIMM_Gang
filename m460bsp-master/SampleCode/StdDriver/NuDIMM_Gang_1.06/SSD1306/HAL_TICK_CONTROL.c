#include <stdio.h>
#include "NuMicro.h"
volatile uint32_t uwTick = 0;

uint32_t HAL_GetTick(void)
{
  return uwTick;
}

void HAL_Delay(__IO uint32_t Delay)
{
		uint32_t tickstart = 0U;
		tickstart = HAL_GetTick();
		while((HAL_GetTick() - tickstart) < Delay)
		{
			
		}
}

void HAL_InitTick(uint32_t TickPriority)
{
		if (TIMER_Open(TIMER0, TIMER_PERIODIC_MODE, 1000) != 1000)
    {
        printf("Set the frequency different from the user\n");
    }

    TIMER_EnableInt(TIMER0);
		/* Enable Timer0 ~ Timer3 NVIC */
    NVIC_EnableIRQ(TMR0_IRQn);
		NVIC_SetPriority (TMR0_IRQn,TickPriority);
		TIMER_Start(TIMER0);
}

volatile uint32_t dis_count=0;
void TMR0_IRQHandler(void)
{
    if (TIMER_GetIntFlag(TIMER0))
    {
        /* Clear Timer0 time-out interrupt flag */
        TIMER_ClearIntFlag(TIMER0);
        uwTick++;
			  dis_count++;
    }
}
