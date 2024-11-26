// compiled with: gcc -g -o santa santa.c on Ubuntu 22.04
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup() {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void banner() {
  puts("\n\n\x1B[3m\x1B[5mall i want for christmas is you!\x1B[0m\n\n");
}

void bye() {
  puts("\n\n\x1B[3m\x1B[5mall i want for christmas is "
       "\x1B[9myou\x1B[0m \x1B[3m\x1B[5m/bin/sh!\x1B[0m\n\n");
}

void read_str(char *buf, int size) {
  int i;
  for (i = 0; i < size; i++) {
    buf[i] = getchar();
    if (buf[i] == '\n') {
      buf[i] = '\0';
      return;
    }
  }
  buf[size - 1] = '\0';
}

void print_menu() {
  puts("1. Add wish");
  puts("2. Remove wish");
  puts("3. View wish");
  puts("4. Exit");
  printf("> ");
}

int main() {
  void *wishlist[10] = {0};
  char buf[128];

  int64_t choice;
  int64_t idx;
  int64_t size;
  const int64_t limit = 10;

  setup();
  banner();

  while (1) {
    print_menu();
    fgets(buf, 128, stdin);
    choice = atoi(buf);
    switch (choice) {
    case 1:
      puts("There's just one thing I need");
      printf("> ");
      fgets(buf, 128, stdin);
      idx = atoi(buf);

      if (idx >= limit) {
        printf("Don't care about the presents underneath %ld and %ld\n", 0,
               limit - 1);
        break;
      }

      puts("I won't ask for much this Christmas");
      printf("> ");
      fgets(buf, 128, stdin);
      size = atoi(buf);
      if (size < 0) {
        puts("Invalid size");
        break;
      }

      wishlist[idx] = malloc(size);

      puts("All I want for Christmas is");
      printf("> ");
      fgets(wishlist[idx], size, stdin);
      break;
    case 2:
      puts("I won't make a list");
      printf("> ");
      fgets(buf, 128, stdin);
      idx = atoi(buf);

      if (idx < 0 || idx >= limit) {
        printf("Don't care about the presents underneath %ld and %ld\n", 0,
               limit - 1);
        break;
      }

      free(wishlist[idx]);
      wishlist[idx] = NULL;
      break;
    case 3:
      puts("Make my wish come true");
      printf("> ");
      fgets(buf, 128, stdin);
      idx = atoi(buf);

      if (idx < 0 || idx >= limit) {
        printf("Don't care about the presents underneath %ld and %ld\n", 0,
               limit - 1);
        break;
      }

      if (wishlist[idx] == NULL) {
        puts("Santa, won't you bring me the one I really need?");
        break;
      }

      puts("All I want for Christmas is");
      puts(wishlist[idx]);
      break;
    case 4:
      bye();
      exit(0);
    }
  }
}
