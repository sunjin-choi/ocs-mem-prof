#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdlib.h>

int main() {
    // Using the write syscall to display a message
    write(STDOUT_FILENO, "Starting syscall demo...\n", 25);

    // Allocating memory using mmap
    void *memory = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (memory == MAP_FAILED) {
        perror("mmap failed");
        exit(1);
    }

    // Allocating memory using mmap
    void *memory_2 = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (memory_2 == MAP_FAILED) {
        perror("mmap failed");
        exit(1);
    }

    // Allocating memory using mmap
    void *memory_3 = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (memory_3 == MAP_FAILED) {
        perror("mmap failed");
        exit(1);
    }

    return 0;
}
