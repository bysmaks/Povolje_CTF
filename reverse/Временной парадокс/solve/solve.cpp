#include <iostream>
#include <string.h>
#include <stdio.h>

using namespace std;
int main()
{
    int c = 0;
    int seed = time(NULL);
    while (true) {
        srand(seed);
        if (rand() % 256 == 215 && rand() % 256 == 92 && rand() % 256 == 64 && rand() % 256 == 168) {
            cout << seed << ' ';
            srand(seed);
            FILE* fd = fopen("flag.encode", "r");
            char ch;
            while ((ch = fgetc(fd)) != EOF) {
                cout << char((int)ch ^ (rand() % 256));
            }
            cout << endl;
            c += 1;
            break;
        }
        seed -= 1;
    }
}