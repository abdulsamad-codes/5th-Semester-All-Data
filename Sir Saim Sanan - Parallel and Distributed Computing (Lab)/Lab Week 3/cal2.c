#include <stdio.h>
#include <omp.h>

int main(void)
{
    omp_set_num_threads(4);

#pragma omp parallel
    {
#pragma omp sections
        {
#pragma omp section
            {
                printf("Task A thread %d\n", omp_get_thread_num());
            }
#pragma omp section
            {
                printf("Task B thread %d\n", omp_get_thread_num());
            }
#pragma omp section
            {
                printf("Task C thread %d\n", omp_get_thread_num());
            }
#pragma omp section
            {
                printf("Task D thread %d\n", omp_get_thread_num());
            }
        }
    }
}