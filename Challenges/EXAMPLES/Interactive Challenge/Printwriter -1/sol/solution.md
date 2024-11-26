Python 2 does this silly thing where it evaluates the user input from input(), leading to the user being able to execute arbitrary code.

Intended solution path:
1. Notice that Python 2 is being used
2. Input random stuff and notice that whatever entered for number of times is evaluated
3. `__import__("os").popen("cat flag.txt").read()` to get flag

Flag: `blahaj{0uT_w17h_th3_N3W_4Nd_1N_w1tH_the_Old}`
