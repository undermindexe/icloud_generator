import os

def get_cokies():
    cookies = []
    if os.path.exists('cookies.txt'):
        with open('cookies.txt', 'r', encoding='utf-8') as file:
            strings = file.readlines()
            if strings:
                for i in strings:
                    cookies.append(i.strip())
                return cookies
    else:
        print('Error, cookies path not exists')

def get_proxy():
    proxy = []
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'r', encoding='utf-8') as file:
            strings = file.readlines()
            if strings:
                for i in strings:
                    proxy.append(i.strip())
                return proxy
    else:
        print('Error, cookies path not exists')

def get_forward():
    mail = {}
    if os.path.exists('forward.txt'):
        with open('forward.txt', 'r', encoding='utf-8') as file:
            for i in file.readlines():
                string = i.split(':')
                mail[string[0]] = string[1]
    return mail