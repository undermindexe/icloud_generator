TEXT = "\n\
[bold magenta]+-------------------+\n\
|ICloud Generator by|       https://t.me/expanse_crypto\n\
|  Expanse Crypto   |       https://t.me/expanse_chat\n\
+-------------------+[/]\n \
\n \
[bold cyan]1.[/bold cyan] Generate emails\n \
[bold cyan]2.[/bold cyan] Export emails list\n \
\n\
[bold cyan]INFO:[/] The [bold purple]cookies.txt[/] file must contain, on each line, the cookies of your authorization on the iCloud website.\n\
The [bold purple]proxy.txt[/] file must contain, on each line, HTTPS proxies in the format [bold green]login:password@host:port[/].\n\
The number of lines (accounts) in cookies.txt must match the number of proxies in proxy.txt.\n\
\n\
During the export of your emails, you will receive a file named export.txt, formatted as [bold green]hidden_email:forward_email[/].\n\
If you want the password of the main email to also be included, create a file named [bold purple]forward.txt[/] with the format [bold green]forward_email:password[/].\n\
Then, if a forward_email is found in this file, its password will automatically be added to export.txt, changing the format to [bold green]hidden_email:forward_email:password[/]\n\n\
[bold green]Select your action [cyan](Ctrl+C to exit)[reset]"