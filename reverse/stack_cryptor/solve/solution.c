#include <stdio.h>
#include <string.h>

#define XOR_KEY 0x5A  

void scramble(char *str) {
    int len = strlen(str);
    
    for (int i = 0; i < len; i++) {
        str[i] = str[i] ^ XOR_KEY;
    }

    for (int i = 0; i < len - 1; i += 2) {
        printf("%d ", i + 1);
        str[i] = str[i] ^ str[i + 1];
        str[i + 1] = str[i] ^ str[i + 1];
        str[i] = str[i] ^ str[i + 1];
    }
}

void unscramble(char *str) {
    int len = strlen(str);

    for (int i = 0; i < len - 1; i += 2) {
        str[i] = str[i] ^ str[i + 1];
        str[i + 1] = str[i] ^ str[i + 1];
        str[i] = str[i] ^ str[i + 1];
    }

    for (int i = 0; i < len; i++) {
        str[i] = str[i] ^ XOR_KEY;
    }
}

int main() {
    // char text[] = "ctf{vms_3re_qu1t3_funny_3a4gb9}";
    char text[] = "sussy_baka";
    
    printf("Original text: %s\n", text);
    
    scramble(text);
    printf("Scrambled text: %s\n", text);
    
    unscramble(text);
    printf("Unscrambled text: %s\n", text);
    
    return 0;
}
