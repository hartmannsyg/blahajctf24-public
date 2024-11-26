// gcc chal.c -no-pie -o chal
#include <stdio.h>
void dump(unsigned char* addr){
    for(int i=0;i<48;i++){
        if(i%16 == 0)
            printf("\nhackme + 0x%02x - ", i);
        printf("%02x ", addr[i]);
    }
    printf("\n%39s%s\n", "", "|_______________________| - return address");
}
void win(){
    printf("Congratulations! Here is your flag: blahaj{[REDACTED]}\n");
}
int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    char hackme[16] = {0};
    printf("Welcome to pwn 101! In this challenge, you will need to override the return address on the stack.\n");
    printf("STACK DUMP");
    dump(hackme);
    printf("In order to beat this challenge, you will need to replace the value of the return address, with that of the win() function, which is at %p.\nGood luck!\n\n", &win);
    while(1){
        printf("Options:\n0 - read data into hackme\n1 - exit\nPlease select an option: ");
        int option = -1;
        scanf("%d", &option);
        int c;
        while ((c = getchar()) != '\n' && c != EOF); //flush stdin
        if(option == 0){
            printf("STACK DUMP");
            dump(hackme);
            printf("Please enter data you wish to insert into hackme: ");
            gets(hackme);
            printf("\nNEW DATA");
            dump(hackme);
        }else if(option == 1){
            break;
        }else{
            printf("Unrecognized option!\n");
        }
    }
}