
#!/bin/bash

# Start writing the C++ program
echo '#include <iostream>' > program_with_long_array.cpp
echo '' >> program_with_long_array.cpp
echo 'int calculateSum(int arr[], int size) {' >> program_with_long_array.cpp
echo '    int sum = 0;' >> program_with_long_array.cpp
echo '    for (int i = 0; i < size; ++i) {' >> program_with_long_array.cpp
echo '        sum += arr[i];' >> program_with_long_array.cpp
echo '    }' >> program_with_long_array.cpp
echo '    return sum;' >> program_with_long_array.cpp
echo '}' >> program_with_long_array.cpp
echo '' >> program_with_long_array.cpp
echo 'int main() {' >> program_with_long_array.cpp
echo '    int array[1000] = {' >> program_with_long_array.cpp

# Generate the array elements
for i in $(seq 1 1000); do
    if [ $i -ne 1000 ]; then
        echo "$i, " >> program_with_long_array.cpp
    else
        echo "$i" >> program_with_long_array.cpp
    fi
done

# Finish writing the program
echo '};' >> program_with_long_array.cpp
echo '' >> program_with_long_array.cpp
echo '    int sum = calculateSum(array, 1000); // pass array to function' >> program_with_long_array.cpp
echo '    std::cout << "Sum (stack): " << sum << std::endl;' >> program_with_long_array.cpp
echo '' >> program_with_long_array.cpp
echo '    return 0;' >> program_with_long_array.cpp
echo '}' >> program_with_long_array.cpp

echo "C++ program with long array generated as program_with_long_array.cpp"
