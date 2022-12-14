#include <stdio.h>
#include <stdlib.h>

#define flat2d(i, j, N) ((i) * (N) + (j))

// Code to remove data from the processor caches.
#define KB (1024)
#define MB (1024 * KB)
#define GB (1024 * MB)
#define LARGEST_CACHE_SZ (16 * MB)

#define flat2d(i, j, N) ((i) * (N) + (j))

void clearCache() {

    long *dummyBuffer = (long *)malloc(LARGEST_CACHE_SZ * sizeof(long));
    long i;
    for (i = 0; i < LARGEST_CACHE_SZ; i++) {
        dummyBuffer[i] += 1;
    }

    free(dummyBuffer);
}

void printMatrix(double *X, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%lf ", X[flat2d(i, j, N)]);
        }
        printf("\n");
    }
    printf("\n");
}

double randDouble(double min, double max) {
    double range = (max - min);
    double div = RAND_MAX / range;
    return min + (rand() / div);
}

double *matrixMultiplication(double *A, double *B, int N) {
    int i, j, k;
    double sum;

    double *C = (double *)calloc(N * N, sizeof(double));

    for (i = 0; i < N; i++) {
        for (k = 0; k < N; k++) {
            for (j = 0; j < N; j++) {
                C[flat2d(i, j, N)] += A[flat2d(i, k, N)] * B[flat2d(k, j, N)];
            }
        }
    }

    return C;
}

int main(int argc, char *argv[]) {

    clearCache();

    int i, n;
    double det;

    n = argc > 1 ? atoi(argv[1]) : 3;

    double *A = (double *)malloc(n * n * sizeof(double));
    double *B = (double *)malloc(n * n * sizeof(double));

    srand(42);

    for (i = 0; i < n * n; i++) {
        A[i] = randDouble(-0.5, 0.5);
    }

    for (i = 0; i < n * n; i++) {
        B[i] = randDouble(-0.5, 0.5);
    }

    double *C = matrixMultiplication(A, B, n);

#ifdef OUTPUT
    printMatrix(A, n);
    printMatrix(B, n);
    printMatrix(C, n);
#endif

    free(A);
    free(B);
    free(C);

    return 0;
}
