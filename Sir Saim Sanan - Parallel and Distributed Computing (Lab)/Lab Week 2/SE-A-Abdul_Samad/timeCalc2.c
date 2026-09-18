#include <stdio.h>
#include <omp.h>

#define N 1000000000LL

int main(void)
{
    long long i;
    long long sum = 0;
    double start, end;

    start = omp_get_wtime();
#pragma omp parallel for reduction(+ : sum)
    for (i = 0; i < N; i++)
    {
        sum += i;
    }
    end = omp_get_wtime();

    printf("Threads used = %d\n", omp_get_max_threads());
    printf("Sum = %lld\n", sum);
    printf("Parallel time = %.6f seconds\n", end - start);

    return 0;
}
