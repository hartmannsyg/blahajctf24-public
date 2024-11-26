//gcc chal.c -m32 -no-pie -o chal

#include <stdio.h>
#include <stdlib.h>

void win(){
    system("cat flag.txt");
}

void isEven(){
    int num;
    printf("Enter your number: ");
    scanf("%d", num);
    
    if(num % 2 == 0){
        puts("The number is even!");
    }else{
        puts("The number is odd!");
    }
}
void getFeedback(){
    char feedback[100];
    printf("We know our service is amazing, so you can give feedback before using it!\nFeedback: ");
    scanf("%100s", feedback);
}

int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("IsEven Service\n");
    getFeedback();
    isEven();
    return 0;
}