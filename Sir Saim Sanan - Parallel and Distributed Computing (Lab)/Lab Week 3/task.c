#include <stdio.h>
#include <omp.h>

#define N 100000

int main(void)
{

    long i;
    long sum = 0;
// #pragma omp parallel for reduction(+:sum)
#pragma omp parallel
    for (i = 0; i < N; i++)
    {
        sum += i;
    }
    printf("sum = %ld\n", sum);
}

// we got the race condition and we have shared storage and multiple processes are accessing
// it at the same it to avoid this race cnoidtion we use reduction
