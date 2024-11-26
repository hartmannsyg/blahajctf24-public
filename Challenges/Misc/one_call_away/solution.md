# Solution

- When you import threading an exit handler is registered.

```python
def _shutdown():
    """
    Wait until the Python thread state of all non-daemon threads get deleted.
    """
    # Obscure: other threads may be waiting to join _main_thread.  That's
    # dubious, but some code does it. We can't wait for it to be marked as done
    # normally - that won't happen until the interpreter is nearly dead. So
    # mark it done here.
    if _main_thread._handle.is_done() and _is_main_interpreter():
        # _shutdown() was already called
        return

    global _SHUTTING_DOWN
    _SHUTTING_DOWN = True

    # Call registered threading atexit functions before threads are joined.
    # Order is reversed, similar to atexit.
    for atexit_call in reversed(_threading_atexits):
        atexit_call()

    if _is_main_interpreter():
        _main_thread._handle._set_done()

    # Wait for all non-daemon threads to exit.
    _thread_shutdown()
```
Source: [https://github.com/python/cpython/blob/main/Lib%2Fthreading.py#L1533](https://github.com/python/cpython/blob/main/Lib%2Fthreading.py#L1533)

- The above function is called when the main thread exits.
- It calls the `reversed` builtin method.
- Thus, by overriding the method you can effectively run code at exit.
- Use one `setattr` call to override the `reversed` method. You can access the `flag` variable which is global.
- No calls left so you can't print the flag, but you can use an error-based oracle to do binary exfiltration.
- `setattr(__builtins__, 'reversed', lambda _: flag[0] == 'b' or 1/0)`
- Write a script to leak the flag (see solve/s.py).

## Previous unintended solutions

- `threading._os.system('cat flag.txt')` (discovered by @fern), so I added `del threading`
- `__import__('jail').flag` -> added `if __name__ == '__main__'` check
- `[line for line in open('flag.txt')]` -> added `open` to the blacklist
- `[setattr(license, '_Printer__filenames', ['/app/flag.txt']), f'{license}']` (you can do the same
thing with `copyright` and `credits`) -> added `license`, `copyright` and `credits` to the blacklist

## Extra comments

- I have no idea why the `threading._shutdown` function is called when `threading` is imported, but _not_ when it's not imported.
- When I print the backtrace / previous frames `_shutdown` is already the outermost frame.
- I'm guessing `_shutdown` is called from c code somewhere.
