#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include "io.h"


void print_buf(uint8_t* buf, size_t sz)
{
	printf("\n");
	for(int i = 0; i < sz; i++)
		printf("%02hhX ", buf[i]);
	printf("\n");
}
