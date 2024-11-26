#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>
#include <seccomp.h>

void setup_seccomp()
{
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (ctx == NULL)
    {
        const char *err = "seccomp_init failed\n";
        write(STDOUT_FILENO, err, strlen(err));
        exit(EXIT_FAILURE);
    }
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(rt_sigreturn), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(read), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pread64), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwrite64), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv), 0) < 0)
    {
        const char *err = "seccomp_rule_add failed\n";
        write(STDOUT_FILENO, err, strlen(err));
        seccomp_release(ctx);
        exit(EXIT_FAILURE);
    }
    if (seccomp_load(ctx) < 0)
    {
        const char *err = "seccomp_load failed\n";
        write(STDOUT_FILENO, err, strlen(err));
        seccomp_release(ctx);
        exit(EXIT_FAILURE);
    }
    seccomp_release(ctx);
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    int fd = -1;
    char *addr;
    addr = mmap((void *)0x100000, 0x200000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, fd, 0);
    if (addr == MAP_FAILED)
    {
        const char *err = "MMAP failed\n";
        write(STDOUT_FILENO, err, strlen(err));
        exit(1);
    }
    ssize_t max_len = 0x100;
    const char *msg = "I'm sick of people using shellcraft.sh()/open()/read()/write() to get a shell or try to leak out sensitive data. So, I blocked every syscall (i think) that lets you do that. Try breaking this secure implementation.\n";
    write(STDOUT_FILENO, msg, strlen(msg));
    ssize_t bytes_read = read(STDIN_FILENO, addr, max_len);
    if (bytes_read < 0)
    {
        const char *err = "What the sigma? Ok.\n";
        write(STDOUT_FILENO, err, strlen(err));
        munmap(addr, 0x4000);
        exit(1);
    }
    setup_seccomp();
    ((void (*)())addr)();
}
