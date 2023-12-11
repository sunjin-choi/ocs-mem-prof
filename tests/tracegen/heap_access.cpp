#include <iostream>

int calculateSum(int* arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; ++i) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int size = 1000;
    int* heapArray = new int[size]; // dynamically allocating an array on the heap

    // Initializing array elements
    for (int i = 0; i < size; ++i) {
        heapArray[i] = i + 1;
    }

    int sum = calculateSum(heapArray, size); // pass heap array to function
    std::cout << "Sum (stack + heap): " << sum << std::endl;

    delete[] heapArray; // important: freeing the heap memory
    return 0;
}
