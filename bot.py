import requests
import json
import time
import datetime
import pytz

from discord_hooks import Webhook

webHookUrls = ['url']

webHookUrls2 = ['url']

jsonMainUrl = "http://www.supremenewyork.com/shop.json"
jsonItemUrl = "http://www.supremenewyork.com/shop/{}.json"

header = {'User-Agent' : "Mozilla/5.0"}

#proxyList = ['http://users77a7173:passwd928q9173@65.216.210.174:10000']

proxyList = []

proxyIndex = 0


def requestData(url):
    global proxyIndex
    data = ""
    proxies = {
        'http': 'http://' + proxyList[proxyIndex],
        'https': 'https://' + proxyList[proxyIndex]
    }

    if proxyIndex == len(proxyList)-1:
        proxyIndex = 0
    else:
        proxyIndex += 1

    try:
        data = requests.get(url, headers=header, proxies=proxies, timeout=2)
    except:
        data = requestData(url)

    try:
        json.loads(data.text)
    except:
        data = requestData(url)

    return data

def buildList():
    
    #data = requests.get(jsonMainUrl, headers=header, proxies=proxies, timeout=2)
    data = requestData(jsonMainUrl)

    #data = requests.get(jsonMainUrl, headers=header)
    json_data = json.loads(data.text)

    monitorList = {}

    categories = json_data['products_and_categories']
    for category in categories.items():
        for item in category[1]:
            monitorList[str(item['id'])] = item
    
    return monitorList

def getItemStock(itemID):
    jsonUrl = jsonItemUrl.format(itemID)
    data = requestData(jsonUrl)
    #data = requests.get(jsonUrl, headers=header)
    itemInfo = json.loads(data.text)

    time.sleep(.1) #cooldown
    return itemInfo

#FIRST CHANGE MESSAGE
def sendStockChangeMessage(itemName, itemDescription, imageUrl, itemPrice, styleColor, itemSize, itemUrl, webHookUrl):
    itemPrice = int(itemPrice / 100)
    embed = Webhook(webHookUrl, title=itemName, desc="", color=0xFF0F54, title_url=itemUrl)
    embed.set_thumbnail(url="http:" + imageUrl)
    embed.add_field(
        name="Color/Style", value=styleColor, inline=True)
    embed.add_field(
        name="Price", value="${}".format(itemPrice), inline=True)
    embed.add_field(name="Size",
                    value=itemSize, inline=False)
    embed.set_footer(text="{0:%I:%M:%S %p} EST".format(datetime.datetime.now(tz=pytz.timezone(
        'US/Eastern'))), icon="BrandIconUrl")
    
    embed.post()
    time.sleep(.5) #cooldown

#SECOND CHANGE MESSAGE
def sendStockChangeMessage2(itemName, itemDescription, imageUrl, itemPrice, styleColor, itemSize, itemUrl, webHookUrl):
    itemPrice = int(itemPrice / 100)
    embed = Webhook(webHookUrl, title=itemName, desc="", color=0x1132d8, title_url=itemUrl)
    embed.set_thumbnail(url="http:" + imageUrl)
    embed.add_field(
        name="Color/Style", value=styleColor, inline=True)
    embed.add_field(
        name="Price", value="${}".format(itemPrice), inline=True)
    embed.add_field(name="Size",
                    value=itemSize, inline=False)
    embed.set_footer(text="@GlobalAIO | Supreme US | {0:%I:%M:%S %p} EST".format(datetime.datetime.now(tz=pytz.timezone(
        'US/Eastern'))), icon="BrandIconUrl")
    
    embed.post()
    time.sleep(.5) #cooldown

#FIRST MESSAGE
def sendNewItemMessage(itemName, itemDescription, imageUrl, itemPrice, itemUrl, webHookUrl):
    itemPrice = int(itemPrice / 100)
    embed = Webhook(webHookUrl, title=itemName, desc="", color=0xFF0F54, title_url=itemUrl)
    embed.set_thumbnail(url="http:" + imageUrl)
    embed.add_field(
        name="New Item", value="True", inline=True)
    embed.add_field(
        name="Price", value="${}".format(itemPrice), inline=True)
    embed.set_footer(text="@ProjectImpactIO | Supreme US | {0:%I:%M:%S %p} EST".format(datetime.datetime.now(tz=pytz.timezone(
        'US/Eastern'))), icon="BrandIconUrl")
    
    embed.post()
    time.sleep(.5) #cooldown

#SECOND MESSAGE
def sendNewItemMessage2(itemName, itemDescription, imageUrl, itemPrice, itemUrl, webHookUrl):
    itemPrice = int(itemPrice / 100)
    embed = Webhook(webHookUrl, title=itemName, desc="", color=0x1132d8, title_url=itemUrl)
    embed.set_thumbnail(url="http:" + imageUrl)
    embed.add_field(
        name="New Item", value="True", inline=True)
    embed.add_field(
        name="Price", value="${}".format(itemPrice), inline=True)
    embed.set_footer(text="@GlobalAIO | Supreme US | {0:%I:%M:%S %p} EST".format(datetime.datetime.now(tz=pytz.timezone(
        'US/Eastern'))), icon="BrandIconUrl")
    
    embed.post()
    time.sleep(.5) #cooldown



#Proxy set up
with open ('proxies.txt') as f:
    for line in f:
        info = line.rstrip('\n').split(':')
        ipAddr = info[0]
        port = info[1]
        user = info[2]
        password = info[3]
        proxy = '{}:{}@{}:{}'.format(user, password, ipAddr, port)
        proxyList.append(proxy)
#Proxy set up




masterID = []

monitorList = buildList()
for item in monitorList:
    masterID.append(item)
for item in monitorList.items():
    item[1]['stock'] = getItemStock(item[0])

time.sleep(1)

while True:

    newMonitorList = buildList()
    for item in newMonitorList.items():
        item[1]['stock'] = getItemStock(item[0])
    
    #masterID.remove('171190')

    for itemID in newMonitorList:
        if itemID not in masterID:
            newItem = newMonitorList[itemID]
            print()
            itemName = newItem['name']
            itemDescription = newItem['stock']['description']
            imageUrl = newItem['image_url']
            itemPrice = newItem['price']
            itemUrl = 'http://www.supremenewyork.com/shop/{}'.format(item[1]['id'])

            for webHookUrl in webHookUrls:
                sendNewItemMessage(itemName=itemName, itemDescription=itemDescription, imageUrl=imageUrl, itemPrice=itemPrice, itemUrl=itemUrl, webHookUrl=webHookUrl)

            for webHookUrl in webHookUrls2:
                sendNewItemMessage2(itemName=itemName, itemDescription=itemDescription, imageUrl=imageUrl, itemPrice=itemPrice, itemUrl=itemUrl, webHookUrl=webHookUrl)

    for item in monitorList.items():
        newItem = newMonitorList[item[0]]
        for idx, style in enumerate(item[1]['stock']['styles']):
            newStyle = newItem['stock']['styles'][idx]
            for index, sizes in enumerate(style['sizes']):
                newSizes = newStyle['sizes'][index]
                if sizes['stock_level'] == 0 and newSizes['stock_level'] > 0:
                    itemName = item[1]['name']
                    itemDescription = item[1]['stock']['description']
                    imageUrl = style['image_url']
                    styleColor = style['name']
                    itemPrice = item[1]['price']
                    itemSize = sizes['name']
                    itemUrl = 'http://www.supremenewyork.com/shop/{}'.format(item[1]['id'])

                    for webHookUrl in webHookUrls:
                        sendStockChangeMessage(itemName=itemName, itemDescription=itemDescription, imageUrl=imageUrl, itemPrice=itemPrice, styleColor=styleColor, itemSize=itemSize, itemUrl=itemUrl, webHookUrl=webHookUrl)
                
                    for webHookUrl in webHookUrls2:
                        sendStockChangeMessage2(itemName=itemName, itemDescription=itemDescription, imageUrl=imageUrl, itemPrice=itemPrice, styleColor=styleColor, itemSize=itemSize, itemUrl=itemUrl, webHookUrl=webHookUrl)

    monitorList = newMonitorList
    time.sleep(10) #cooldown

