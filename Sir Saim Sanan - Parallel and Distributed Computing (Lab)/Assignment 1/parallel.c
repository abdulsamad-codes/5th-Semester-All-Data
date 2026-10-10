#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ARRAY_SIZE 20000
#define SECTION_COUNT 4

static void bubbleSortRange(int values[], int left, int right)
{
    for (int pass = left; pass < right - 1; pass++)
    {
        int swapped = 0;

        for (int index = left; index < right - (pass - left) - 1; index++)
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

static void mergeRanges(int values[], int temporary[], int left, int middle, int right)
{
    int leftIndex = left;
    int rightIndex = middle;
    int outputIndex = left;

    while (leftIndex < middle && rightIndex < right)
    {
        if (values[leftIndex] <= values[rightIndex])
        {
            temporary[outputIndex++] = values[leftIndex++];
        }
        else
        {
            temporary[outputIndex++] = values[rightIndex++];
        }
    }

    while (leftIndex < middle)
    {
          temporary[outputIndex++] = values[leftIndex++];
    }

    while (rightIndex < right)
    {
        temporary[outputIndex++] = values[rightIndex++];
    }

    for (int index = left; index < right; index++)
    {
        values[index] = temporary[index];
    }
}

static void parallelBubbleSort(int values[], int size, int *threadCount)
{
    int temporary[ARRAY_SIZE];
    int firstEnd = size / SECTION_COUNT;
    int secondEnd = firstEnd * 2;
    int thirdEnd = firstEnd * 3;

#pragma omp parallel shared(values, threadCount)
    {
#pragma omp single
        *threadCount = omp_get_num_threads();

#pragma omp sections
        {
#pragma omp section
            bubbleSortRange(values, 0, firstEnd);

#pragma omp section
            bubbleSortRange(values, firstEnd, secondEnd);

#pragma omp section
            bubbleSortRange(values, secondEnd, thirdEnd);

#pragma omp section
            bubbleSortRange(values, thirdEnd, size);
        }
    }

    mergeRanges(values, temporary, 0, firstEnd, secondEnd);
    mergeRanges(values, temporary, secondEnd, thirdEnd, size);
    mergeRanges(values, temporary, 0, secondEnd, size);
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
    int threadCount = 0;
    srand((unsigned int)rollNumber);

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        values[index] = rand();
    }

    double start = omp_get_wtime();
    parallelBubbleSort(values, ARRAY_SIZE, &threadCount);
    double end = omp_get_wtime();

    FILE *output = fopen("parallel out.txt", "w");
    if (output == NULL)
    {
        printf("Could not create parallel out.txt\n");
        return 1;
    }

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        fprintf(output, "%d\n", values[index]);
    }
    fclose(output);

    printf("roll number = %d\n", rollNumber);
    printf("input size = %d\n", ARRAY_SIZE);
    printf("parallel\n");
    printf("execution time = %.12f seconds\n", end - start);
    printf("first value = %d\n", values[0]);
    printf("last value = %d\n", values[ARRAY_SIZE - 1]);
    printf("threads = %d\n", threadCount);
    return 0;
}
