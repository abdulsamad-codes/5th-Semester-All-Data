#include <stdio.h>
#include <omp.h>

#define N 500

int main(void)
{
    omp_set_num_threads(4);
    static double A[N][N];
    static double B[N][N];
    static double C[N][N];
    int i, j, k;
    double start, end;

    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            A[i][j] = 1.0;
            B[i][j] = 1.0;
            C[i][j] = 0.0;
        }
    }

    start = omp_get_wtime();
#pragma omp parallel for private(j,k)
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            double sum = 0.0;
// #pragma omp parallel for reduction(+ : sum)
            for (k = 0; k < N; k++)
            {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    end = omp_get_wtime();
    printf ( " parallel time = % f seconds \n " , end - start ) ;
    printf("C[0][0] = %f (expected %d)\n", C[0][0], N);
    // printf("serial time = %f seconds\n", end - start);
    return 0;
}