# Solution

Realize that the encrypted result can be any character EXCEPT for the flag. From there you can just make requests (typically takes ~1024 - 2048 tries to obtain, a reasonable amount) for encrypted flag, until each character of the flag has been narrowed down to only a single char. See `solve/` for solvescript.