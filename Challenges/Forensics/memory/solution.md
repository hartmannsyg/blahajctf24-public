commands to run to solve:
- .\vol2.exe -f .\dmp.raw imageinfo to get the profile
- .\vol2.exe -f .\dmp.raw --profile Win7SP1x86_23418 pslist to get the process
- .\vol2.exe -f .\dmp.raw --profile Win7SP1x86_23418 consoles to get the command
- .\vol2.exe -f .\dmp.raw --profile Win7SP1x86_23418 printkey -K "ControlSet001\Control\ComputerName\ComputerName" to get the computer name

Flag: `blahaj{M3M0R1ESDUMP3DM3M0R1ESR34D}`