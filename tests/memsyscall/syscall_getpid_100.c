#include <stdio.h>
#include <unistd.h>

int main() {
	// note that syscall for getpid is 39 -- check if it matches
    for (int i = 0; i < 100; i++) {
        printf("Call %d: Process ID is %d\n", i + 1, getpid());
    }
    return 0;
}

