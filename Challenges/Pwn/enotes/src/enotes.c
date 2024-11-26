//gcc enotes.c -o enotes -no-pie
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_MESSAGES 256
#define MESSAGE_SIZE 1024

void *notes[MAX_MESSAGES];
int isadmin = 0;

void *run_thread(void *arg) {
    int fd = (long long)arg;
    FILE *fin = fdopen(fd, "r");
    FILE *fout = fdopen(fd, "w");

    if (!fin || !fout) {
        close(fd);
        free(arg);
        return NULL;
    }

    setvbuf(fin, NULL, _IONBF, 0);
    setvbuf(fout, NULL, _IONBF, 0);

    char buffer[1032];
    int index;

    fprintf(fout, "Welcome to Enotes, private edition!\nCollaborate with your friends to take notes!\n");
    fprintf(fout, "Commands: new/read/write/delete/quit/shutdown.\n");

    while (1) {
        if (fscanf(fin, "%1024s", buffer) == EOF) break;
        if (strcmp(buffer, "read") == 0) {
            if (fscanf(fin, "%d", &index) == EOF) break;
            if (index >= MAX_MESSAGES || index < 0)
                fprintf(fout, "ERROR!!!\n");
            else{
                if (notes[index]) {
                    fprintf(fout, "NOTE: ");
                    fwrite((char*)notes[index], 1, MESSAGE_SIZE, fout);
                } else {
                    fprintf(fout, "NOTE: (empty)\n");
                }
            }
        } else if (strcmp(buffer, "new") == 0) {
            if (fscanf(fin, "%d", &index) == EOF) break;
            if (index >= MAX_MESSAGES || index < 0)
                fprintf(fout, "ERROR!!!\n");
            else{
                notes[index] = malloc(MESSAGE_SIZE);
            }
        } else if (strcmp(buffer, "write") == 0) {
            if (fscanf(fin, "%d", &index) == EOF) break;
            if (index >= MAX_MESSAGES || index < 0)
                fprintf(fout, "ERROR!!!\n");
            else{
                char *target = notes[index] ? notes[index] : buffer;
                fscanf(fin, "%1024s", target);
            }
        } else if (strcmp(buffer, "delete") == 0) {
            if (fscanf(fin, "%d", &index) == EOF) break;
            if (index >= MAX_MESSAGES || index < 0)
                fprintf(fout, "ERROR!!!\n");
            else{
                if (notes[index]) {
                    free(notes[index]);
                    notes[index] = 0;
                }
            }
        } else if (strcmp(buffer, "shutdown") == 0) {
            if(isadmin)
                exit(0);
            else
                fprintf(fout, "Admin not here, we cannot shut down!\n");
        } else if (strcmp(buffer, "quit") == 0) {
            break;
        } else {
            fprintf(fout, "Unrecognized choice!\n");
        }
    }
    
    fclose(fin);
    fclose(fout);
    close(fd);
    return 0;
}

int main(int argc, char **argv) {
    int server_fd, client_fd;
    struct sockaddr_in address;
    int opt = 1;
    int port = atoi(argv[1]);
    pthread_t thread_id;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("Hello user! I am listening for connections on port %d.\n", port);
    
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 1);
    
    while (1) {
        client_fd = accept(server_fd, NULL, NULL);
        pthread_create(&thread_id, NULL, run_thread, (void*)client_fd);
    }
}