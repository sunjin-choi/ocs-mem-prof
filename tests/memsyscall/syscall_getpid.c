#include <stdio.h>
#include <unistd.h>

int main() {
    for (int i = 0; i < 10; i++) {
        printf("Call %d: Process ID is %d\n", i + 1, getpid());
    }
    return 0;
}

