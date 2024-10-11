#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int main(){
	int seed = (int)time(NULL);
	srand(seed);
	char flag[256];
	printf("Please enter yout flag to encode it: ");
	scanf("%s", flag);
	printf("%s\n", flag);
	printf("%d\n", seed);
	FILE* file;
	file = fopen("flag.encode", "w");
	for(int i = 0; i < strlen(flag); i++){
		fputc(flag[i] ^ (rand() % 256), file);
	}
}
