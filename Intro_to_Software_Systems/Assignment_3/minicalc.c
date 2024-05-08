// Author: Eloi Dallaire
// McGill Student ID: 260794674

//Imports
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

// Helper functions
// GCD calculator
int gcd(int a, int b) {
        int temp;
                while(b > 0) {
                        temp = b;
                        b = a % b;
                        a = temp;
                }
                return a;
}

// Explanation of GCD algorithm used
// Source: https://www.rookieslab.com/posts/cpp-python-code-to-find-gcd-of-a-list-of-numbers
// Euclid's Algorithm: finds the GCD of two integers
// 1. Finding Remainder: Inside the loop, we calculate the remainder when dividing the larger number by the smaller one.
// 2. Swapping: We update the numbers to continue the iteration.
// 3. Base Case: When the remainder becomes zero, we have found the GCD and return the non-zero number.

// For minicalc, the gcd function will also work in the situation where it is called with more than 2 integers.
// It will recurisvely update the list of GCD with the reaining integers provided.
// It will do so by finding the GCD of the current number and the result list.


// Check if argument is a string
int is_string(const char *str) {
        // Check if the string is not empty
        if (str == NULL || *str == '\0') {
                return 0;
        }
        // Check if all characters in the string are alphabetic
        while (*str) {
                if (!isalpha(*str)) {
                        return 0;
                }
                str++;
        }
        return 1;
}


// Check if string is all lower-case letters
int is_lower_case(const char *str) {
        // Check if the string is not empty
        if (str == NULL || *str == '\0') {
                return 0;
        }
        // Check if all characters in the string are lowercase
        while (*str) {
                if (!islower(*str)) {
                        return 0;
                }
                str++;
        }
        return 1;
}


int main(int argc, char *argv[]) {
        // Check at least one command-line argument
        if (argc < 3) {
                fprintf(stderr, "Error: Minicalc requires at least one command-line argument.\n");
                return 1;
        }

  
	// 1: Addition
	if (strcmp(argv[1], "+") == 0) {
		// Check appropriate number of subsequent arguments (2)
    		if (argc != 4) {
        		fprintf(stderr, "Error: Addition operation requires exactly two operands.\n");
        		return 3;
    		}
    		// Check appropriate type of operands (integers)
        	for (int i = 2; i < argc; i++) {
            		char *endptr;
            		long num = strtol(argv[i], &endptr, 10);
            		if (*endptr != '\0') {
                		fprintf(stderr, "Error: Operand %d is not a valid integer.\n", i - 1);
                		return 4;
            		}
        	}
        	// Perform addition
        	long result = 0;
        	for (int i = 2; i < argc; i++) {
            		result += strtol(argv[i], NULL, 10);
        	}
        	printf("%ld\n", result);
	}


        // 2: GCD
        else if (strcmp(argv[1], "gcd") == 0) {

                // Check appropriate number of subsequent arguments (>= 2)
                if (argc < 4) {
                        fprintf(stderr, "Error: GCD operation requires at least two operands.\n");
                        return 3;
                }

                // Check appropriate type of operands (integers)
                for (int i = 2; i < argc; i++) {
                        char *endptr;
			long num = strtol(argv[i], &endptr, 10);
                        if (*endptr != '\0') {
                                fprintf(stderr, "Error: Operand %d is not a valid integer.\n", i - 1);
                                return 4;
                        }
                        // Check integers are greater than 0
                        if (num <= 0) {
                                fprintf(stderr, "Error: Operand %d must be greater than 0.\n", i - 1);
                                return 7;
                        }
                }
		// Perform GCD operation
        	long result = strtol(argv[2], NULL, 10);
        	for (int i = 3; i < argc; i++) {
            		long num = strtol(argv[i], NULL, 10);
            		result = gcd(result, num);
        	}
        	printf("%ld\n", result);
        }
	

	// 3: Square root
        else if (strcmp(argv[1], "sqrt") == 0) {
                // Check appropriate number of subsequent argument (1)
                if (argc != 3) {
                        fprintf(stderr, "Error: Square root operation requires exactly one operand.\n");
                        return 3;
                }
		// Check appropriate type of operand (double)
        	char *endptr;
        	double num = strtod(argv[2], &endptr);
        	if (*endptr != '\0') {
            		fprintf(stderr, "Error: Operand is not a valid double.\n");
            		return 4;
        	}
                // Check operand is nonnegative
                if (num < 0) {
                        fprintf(stderr, "Error: Operand must be nonnegative.\n");
                        return 5;
                }

                // Perform square root
                printf("%lf\n", sqrt(num));
        }



        // 4: Anagram
        else if (strcmp(argv[1], "anagram") == 0) {

                // Check appropriate number of subsequent arguments (2)
                if (argc != 4) {
                        fprintf(stderr, "Error: Anagram operation requires exactly two strings.\n");
                        return 3;
                }

                // Check appropriate type of subsequent arguments (strings)
                if (!is_string(argv[2]) || !is_string(argv[3])) {
                        fprintf(stderr, "Error: Operand is not a valid string.\n");
                        return 4;
                }

                // Check arguments are lowercase letters
                if (!is_lower_case(argv[2]) || !is_lower_case(argv[3])) {
                        fprintf(stderr, "Error: Operand contains non-lowercase characters.\n");
                        return 6;
                }

                char *str1 = argv[2];
                char *str2 = argv[3];

                // Check identical lengths
                int len1 = strlen(str1);
                int len2 = strlen(str2);
                if (len1 != len2) {
                        printf("false\n");
                        return 0;
                }

                int count[256] = {0};
                for (int i = 0; i < len1; i++) {
                        count[str1[i]]++;
                        count[str2[i]]--;
                }

                for (int i = 0; i < 256; i++) {
                        if (count[i] != 0) {
                                printf("false\n");
                                return 0;
                        }
                }
                printf("true\n");
        }



        // Incorrect operation type
        else {
                fprintf(stderr, "Error: Unsupported operation.\n");
                return 2;
        }

    return 0;
}


