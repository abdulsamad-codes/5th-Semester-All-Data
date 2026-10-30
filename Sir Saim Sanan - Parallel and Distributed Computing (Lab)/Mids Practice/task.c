#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ARRAY_SIZE 20

static void bubbleSort(int values[], int size)
{
    for (int pass = 0; pass < size - 1; pass++)
    {
        int swapped = 0;

        for (int index = 0; index < size - pass - 1; index++)
        {
            if (values[index] > values[index + 1])
            {
                int temporary = values[index];
                values[index] = values[index + 1];
                values[index + 1] = temporary;
                swapped = 1;
            }
        }

        if (!swapped)
        {
            break;
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <roll_number>\n", argv[0]);
        return 1;
    }

    int rollNumber = atoi(argv[1]);
    int values[ARRAY_SIZE];
    srand((unsigned int)rollNumber);

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        values[index] = rand();
    }

    double start = omp_get_wtime();
    bubbleSort(values, ARRAY_SIZE);
    double end = omp_get_wtime();

    FILE *output = fopen("serial.txt", "w");
    if (output == NULL)
    {
        printf("Could not create serial.txt\n");
        return 1;
    }

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        fprintf(output, "%d\n", values[index]);
    }
    fclose(output);

    printf("roll number = %d\n", rollNumber);
    printf("input size = %d\n", ARRAY_SIZE);
    printf("serial\n");
    printf("execution time = %.12f seconds\n", end - start);
    printf("first value = %d\n", values[0]);
    printf("last value = %d\n", values[ARRAY_SIZE - 1]);
    return 0;
}
