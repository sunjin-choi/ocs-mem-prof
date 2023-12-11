#include <cstdlib>
#include <cstdio>
#define BIG 10000000
int main() {
    int * t = (int *)malloc(BIG* sizeof(int));
    printf("%p\n",t);
    for (int i=0; i < BIG; i++) {
        *t++;
        t++;
    }
    return 0;
}
