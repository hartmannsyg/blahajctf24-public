#include <stdlib.h>
#include <time.h>
#include <stdio.h>

int nah=0;

int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);;
    char buf[200];
    long some_val=113848163;
    printf("My friend told me 2 wrongs don't make a right.\nI don't really agree with that. In fact, prove me wrong.\n");
    printf("> ");
    fgets(buf,200,stdin);
    printf(buf);
    printf("Your case isn't that compelling. But I may give you a 2nd chance to prove your case.\n"); 
    printf("Fine here's another chance to prove me wrong.\n>");
    scanf("%d",&nah);
    while (getchar() != '\n'); 
    if (nah==some_val){second_chance_to_prove_your_case();}
    printf("On 2nd thought, nah. you're definitely wrong.\n");
    return 0;
}

int second_chance_to_prove_your_case(){
    char buf[100];
    printf("Hmm. I'm going to need to have a think about it. In the meantime, enter your name in so I can get back to you later about what you just said.\n");
    fgets(buf,0x100,stdin);
}
