#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

int main(int argc, char *argv[]) { int rank, size; int incidents, units; int total_incidents = 0; int max_units = 0; int highest_zone = 0; int available_units = 0;

int report[2];

MPI_Init(&argc, &argv);

MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);

srand(time(NULL) + rank * 100);

incidents = (rand() % 5) + 1;
units = (rand() % 10) + 1;

printf("Zone %d: Incidents = %d, Required Units = %d\n",
       rank, incidents, units);

if (rank == 0)
{
    total_incidents = incidents;
    max_units = units;
    highest_zone = 0;

    for (int i = 1; i < size; i++)
    {
        MPI_Recv(report, 2, MPI_INT, i, 0,
                 MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        total_incidents += report[0];

        if (report[1] > max_units)
        {
            max_units = report[1];
            highest_zone = i;
        }
    }

    printf("\n----- Central Emergency Control -----\n");
    printf("Total Incidents: %d\n", total_incidents);

    printf("Zone Requiring Maximum Units: %d\n",
           highest_zone);

    printf("Maximum Required Units: %d\n", max_units);

    available_units = 20;

    printf("Available Emergency Units: %d\n",
           available_units);
}
else
{
    report[0] = incidents;
    report[1] = units;

    MPI_Send(report, 2, MPI_INT, 0, 0,
             MPI_COMM_WORLD);
}

MPI_Bcast(&available_units, 1, MPI_INT, 0,
          MPI_COMM_WORLD);

printf("Zone %d: ", rank);

if (units <= available_units)
{
    printf("Zone can be adequately served.\n");
}
else
{
    printf("Zone cannot be adequately served.\n");
}

MPI_Finalize();

return 0;


}
