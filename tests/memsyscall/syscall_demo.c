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

    // Writing to the allocated memory
    sprintf(memory, "Memory allocated and written using mmap.\n");

    // Using the write syscall to display the content of allocated memory
    write(STDOUT_FILENO, memory, 40);

    // Opening a file using the open syscall
    int fd = open("demo.txt", O_CREAT | O_WRONLY, 0644);
    if (fd < 0) {
        perror("open failed");
        munmap(memory, 4096);
        exit(1);
    }

    // Writing to the file
    write(fd, "Writing to file using the write syscall.\n", 40);

    // Closing the file
    close(fd);

    // Unmapping the memory
    munmap(memory, 4096);

    // Using the getpid syscall
    printf("The process ID is: %d\n", getpid());

    return 0;
}
