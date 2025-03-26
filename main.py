import asyncio

from rich.prompt import Prompt
from rich.console import Console
from rich.columns import Columns
from rich.table import Table, box, Column
from typing import Union, List

from data.browser import Browser
from data.service import *
from data.text import TEXT

FORWARD_PASSWORD = get_forward()

class Account(Browser):
    def __init__(self, label = ".", cookies = "", proxy = ""):
        super().__init__(label, cookies, proxy)
        self.count_hme = 0
        self.icloud = ''

        self.console = Console()
        self.table = Table(
            Column("Label", style="bold white"),
            Column("Email", style="bold cyan"),
            Column("Creation Time", style="bold white"),
            Column("Status", style="bold cyan"),
            style="bold green", 
            box=box.MINIMAL,
        )


    async def get_statistic(self):
        async with self:
            hme = await self.list_email()
            if hme.get('success', False):
                count_hme = hme['result']['hmeEmails']
                self.count_hme = len(count_hme)
            info = await self.base_info()
            if info.get('dsInfo', False):
                self.icloud = info['dsInfo']['appleId']
                subscripe_status = info['dsInfo']['isHideMyEmailSubscriptionActive']
                hide_email_status = info['dsInfo']['isHideMyEmailFeatureAvailable']
                another_email = info['dsInfo']['appleIdAliases']
                country = info['dsInfo']['countryCode']
                full_name = info['dsInfo']['fullName']
                self.console.log(
                    f'[bold green]Success connect to ICloud[/]\n{self.icloud}\n{full_name}\n{another_email}\n{country}\nSubscribe status: {subscripe_status}\nHide email available: {hide_email_status}\nNumber of hiden emails: {self.count_hme}\n'
                    )

def get_accounts():
    try:
        accounts = []
        proxies = get_proxy()
        cookies = get_cokies()
        for c,p in zip(cookies, proxies):
            accounts.append(Account(cookies=c, proxy=p))
        return accounts
    except(TypeError) as e:
        print('The cookies.txt or proxy.txt file is likely empty')
        raise SystemExit

async def worker_save(acc: Account):
    await acc.get_statistic()
    with acc.console.status(f"[bold green]{acc.icloud} working...", spinner='clock') as status:
        async with acc:
            list_email = await acc.list_email()

        hiden_emails = list_email['result']['hmeEmails']

        with open('export.txt', 'a', encoding='utf-8') as file:
            for i in hiden_emails:
                if i['isActive'] == True:
                    hme = i['hme']
                    forward = i['forwardToEmail']
                    file.write(f'{hme}:{forward}' + FORWARD_PASSWORD.get(i['forwardToEmail'], '') + '\n')

async def worker_generator(acc: Account):
    await acc.get_statistic()

    async with acc:
        with acc.console.status(f"[bold green]{acc.icloud} working...", spinner='clock') as status:
            while acc.count_hme < 750:
                gen = await acc.generate_email()
                if gen.get('success', False):
                    generate_mail = gen['result']['hme']
                    acc.console.log(f'[bold green]{acc.icloud}[/] | Success generate adress [bold magenta]{generate_mail}[/]')
                    reserve = await acc.reserve_email(email=generate_mail)
                    if reserve.get('success', False):
                        adress = reserve['result']['hme']['hme']
                        acc.count_hme += 1
                        acc.console.log(f'[bold green]{acc.icloud}[/] | Success reserve adress [bold magenta]{adress}[/] | Total: {acc.count_hme}')
                        await asyncio.sleep(1)
                        continue
                    else:
                        acc.console.log(f'[bold red]{acc.icloud}[/] | Error reserve adress retry via 30m')
                else:
                    acc.console.log(f'[bold red]{acc.icloud}[/] | Error generate adress retry via 30m')
                await asyncio.sleep(1800)
            acc.console.log(f'[bold red]{acc.icloud}[/] | The task is over. Total hide email: {acc.count_hme}')

async def get_task():
    try:
        s = Prompt.ask(
            f"{TEXT}")
        if s == "1":
            return worker_generator
        elif s == "2":
            return worker_save
        else:
            raise ValueError
    except (KeyboardInterrupt, ValueError):
        return


async def main():
    accounts = get_accounts()
    job = await get_task()
    tasks = [job(i) for i in accounts]
    await asyncio.gather(*tasks)
    pass

if __name__ == '__main__':
    asyncio.run(main())