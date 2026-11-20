#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    printf("Hello from process %d out of %d\n", rank, size);
if (rank == 0){
int message = 40;
MPI_Send(&message, 1, MPI_INT, 3, 0, MPI_COMM_WORLD);
printf("Process 0 sent message (%d) to prcoess 3 \n", message);
}
else if (rank==3){
int recv;
MPI_Recv(&recv, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
printf("Process 3 received message (%d) from process 0 \n", recv);
}   
 MPI_Finalize();
}
