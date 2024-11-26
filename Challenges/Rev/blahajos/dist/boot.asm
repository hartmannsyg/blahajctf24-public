[org 0x7C00]
[bits 16]

KERNEL_OFFSET:  equ 0x1000                       
DATA_OFFSET:    equ 0x2000                       

mov [boot_disk], dl                             
mov si, password_prompt_string                  
mov ah, 0x0E                                    
print_read_message
    lodsb                                       
    int 0x10                                    
    test al, al                                 
    jnz print_read_message                      

mov cx, 10
mov si, input_string
mov di, input_string

read_input:
    mov ah, 1
    int 0x16
    jz read_input

    mov ah, 0
    int 0x16

    cmp al, 0x0D
    je end_read_input
    cmp cx, 0
    je read_input
    stosb
    dec cx
    jmp read_input

end_read_input:
    mov al, 0xD
    mov ah, 0x0E
    int 0x10
    mov al, 0xA
    mov ah, 0x0E
    int 0x10
    
    mov si, password_string
    add si, 9
    mov di, input_string

    mov cx, 10

check_input:
    std
    lodsb
    mov ah, al

    xor di, si 
    xor si, di 
    xor di, si
    
    cld
    lodsb

    xor di, si 
    xor si, di 
    xor di, si

    cmp al, ah
    jne end_program

    dec cx
    cmp cx, 0
    jne check_input

mov ah, 0x0E                                   
mov si, wait_message_string
print_wait_message:
    lodsb                                      
    int 0x10                                   
    test al, al                                 
    jnz print_wait_message 


mov ah, 0x86
mov dx, 0x1400
mov cx, 0xf73
int 0x15


mov ah, 2                                       
mov al, 1                                       
mov bx, KERNEL_OFFSET                           
mov cl, 2                                       
mov ch, 0                                       
mov dh, 0                                       
mov dl, [boot_disk]                             
int 0x13                                        

jmp KERNEL_OFFSET                               

end_program:
    mov ah, 0xE
    mov si, password_wrong_string

print_wrong_message:
    lodsb                                       
    int 0x10                                    
    test al, al                                 
    jnz print_wrong_message   

cli                                             
hlt

boot_disk: db 0

password_prompt_string: db "Input password to continue: ", 0
password_string: db "4ha0B$2sLP"
wait_message_string: db "Your flag will load in 3 days...", 0
input_string: db 0,0,0,0,0,0,0,0,0,0
password_wrong_string: db "Incorrect password!", 0

times 510-($ - $$) db 0
db 0x55, 0xAA