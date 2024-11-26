// gcc chal.c -no-pie -o chal
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NOTES 16
#define NOTE_SIZE 256

void win(){
    printf("You win! Here is your flag:\n");
    system("cat flag.txt");
    _exit(0);
}

char *notes[MAX_NOTES];

void create_note() {
    int index;
    printf("Enter the index where you want to create the note (0 to %d): ", MAX_NOTES - 1);
    scanf("%d", &index);
    getchar(); // Consume the newline character

    if (index < 0 || index >= MAX_NOTES) {
        printf("Invalid index.\n");
        return;
    }

    notes[index] = (char *)malloc(NOTE_SIZE * sizeof(char));

    printf("Enter the note (max %d characters): ", NOTE_SIZE - 1);
    fgets(notes[index], NOTE_SIZE, stdin);
    notes[index][strcspn(notes[index], "\n")] = 0; // Remove newline character

    printf("Note created/overridden successfully at index %d.\n", index);
}

void delete_note() {
    int index;
    printf("Enter the index of the note to delete (0 to %d): ", MAX_NOTES - 1);
    scanf("%d", &index);

    if (index < 0 || index >= MAX_NOTES || notes[index] == NULL) {
        printf("Invalid index or no note exists at this index.\n");
        return;
    }

    free(notes[index]);
    printf("Note deleted successfully at index %d.\n", index);
}

void edit_note() {
    int index;
    printf("Enter the index of the note to edit (0 to %d): ", MAX_NOTES - 1);
    scanf("%d", &index);
    getchar(); // Consume the newline character

    if (index < 0 || index >= MAX_NOTES || notes[index] == NULL) {
        printf("Invalid index or no note exists at this index.\n");
        return;
    }

    printf("Enter the new note (max %d characters): ", NOTE_SIZE - 1);
    fgets(notes[index], NOTE_SIZE, stdin);
    notes[index][strcspn(notes[index], "\n")] = 0; // Remove newline character

    printf("Note edited successfully at index %d.\n", index);
}

void display_notes() {
    int index;
    printf("Enter the index of the note to read (0 to %d): ", MAX_NOTES - 1);
    scanf("%d", &index);
    getchar(); // Consume the newline character

    if (index < 0 || index >= MAX_NOTES || notes[index] == NULL) {
        printf("Invalid index or no note exists at this index.\n");
        return;
    }

    printf("NOTE: %s\n", notes[index]);
}

int main() {
    int choice;
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    while (1) {
        printf("Menu:\n");
        printf("1. Create Note\n");
        printf("2. Delete Note\n");
        printf("3. Edit Note\n");
        printf("4. Read Note\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                create_note();
                break;
            case 2:
                delete_note();
                break;
            case 3:
                edit_note();
                break;
            case 4:
                display_notes();
                break;
            case 5:
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
