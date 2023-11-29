
# Compiler and compiler flags
CC = gcc
CFLAGS = -Wall -Werror

# Find all .c files in the current directory
SOURCES = $(wildcard *.c)

# Replace the file extension .c from SOURCES with nothing to get executable names
EXECUTABLES = $(SOURCES:.c=)

# Default target
all: $(EXECUTABLES)

# Rule to compile each .c file into its own executable
%: %.c
	$(CC) $(CFLAGS) $< -o $@

# Clean target
clean:
	rm -f $(EXECUTABLES)

# Phony targets
.PHONY: all clean
