
# Compiler and compiler flags
CC = g++
CFLAGS = -O0 -Wall -Werror

# Find all .c files in the current directory
SOURCES = $(wildcard *.cpp)

# Replace the file extension .c from SOURCES with nothing to get executable names
EXECUTABLES = $(SOURCES:.cpp=)

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
