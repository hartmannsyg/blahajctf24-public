//compile: g++ -m32 -no-pie -fstack-protector chal.cpp -o chal
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#define MAX_SIZE 80

void win(){
    printf("Congrats, you win!!! Here is flag: [FLAG CENSORED]\n");
}
class formatter{
public:
    virtual void displayName(){};
    virtual void format(const char * ptr){};
};
 
class Skibidi: public formatter{
public:
    virtual void displayName(){
        printf("Skibidi converter!\n");
    }
    virtual void format( const char * ptr ){
        printf("THE REALEST SKIBIDI... %s\n", ptr);
    }
};

class StringFormatter{
public:
    StringFormatter(formatter* pFormatter):myFormatter(pFormatter) {};
    void GetInput(int padding){
        printf("I will be nice, here is an address for you: %p\nPlease enter your string: ", str);
        memset(str, ' ', MAX_SIZE);
        fgets(str+padding, MAX_SIZE, stdin);
    }
    void display(){
        myFormatter->format(str);
    }
    void displayName(){
        myFormatter->displayName();
    }
private:
    char str[MAX_SIZE];
    formatter* myFormatter;
};

int main(int argc, char* argv[]){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    printf("Please choose a padding (0-5): ");
    fflush(stdout);
    char size[4];
    int padding = atoi(fgets(size, 4, stdin));
    if (padding < 0 || padding > 5){
        printf("Go away hacker!!!!!\n");
        exit(0);
    }

    StringFormatter formatter(new Skibidi);
    formatter.displayName();
    formatter.GetInput(padding);
    formatter.display();
    return 0;
}