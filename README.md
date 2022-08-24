# Python-bank-card-stealer
For my first malicious program, albeit it does not do much. This was a fun and very informative experience into learning about how malware operates. Some key techniques and tactics I employed in this malware are:

    1. Accessing the clipboard
    2. Data encryption and exfiltration
    3. Custom user agent to blend in with network traffic
    4. Kill switch based on domain presence
    5. Kill switch if analysis tools are present on the machine
    6. Persistence by altering the start up registry key

I will be writing more malware samples in the future and maybe in other popular languages used by current malware authors. For now I hope this was informative and you enjoyed reading this as much as I enjoyed writing this script. This definitely helped me better understand how a malware author thinks and hopefully will help me become a better analyst.

In order for the malware to fire and actually work, you need to have a sample bank card number in your clipboard in the format of XXXX-XXXX-XXXX-XXXX:

    1. 5123-4567-8912-3456
    2. 1234-5678-1245-3213
    3. 7648-4987-2553-0961
