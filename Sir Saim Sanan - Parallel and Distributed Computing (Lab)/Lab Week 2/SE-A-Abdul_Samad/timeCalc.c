#include <stdio.h>
#include <time.h>
#define N 10000000000

int main(void)
{
    long i;
    long sum = 0;
    clock_t start, end;
    start = clock();
    for (i = 0; i < N; i++)
    {
        sum += i;
    }
    end = clock();

    printf("Sum = %d\n", sum);
    printf("Serial time = %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
}
