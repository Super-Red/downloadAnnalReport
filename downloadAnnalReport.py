#-*-encoding:utf-8-*-

'''
Author:     Super_Red
Date:       19/3/2017
Describe:   Download annal reports from the stock id 
'''

import requests
import csv
from bs4 import BeautifulSoup
import re

class downloader(object):

    def __init__(self):
        self.stockList = self.loadStockList()

    def loadStockList(self):
        with open("stockids.csv", "r", encoding="utf-8") as file:
            stockList = list(csv.reader(file))
        return stockList

    def searchID(self):
        companyNameList = [company[1] for company in self.stockList]
        idList = []
        while (len(idList) <= 0):
            inputName = input("Company Name :\t")
            idList = [companyNameList.index(name) for name in companyNameList if inputName in name]
        for index in idList:
            print(self.stockList[index])

    def downloadFromID(self, stockID):
        reportList = self.findAnnalReports(stockID)
        for index, value in enumerate(reportList):
            print("{index:3}:\t{date:2}\t{name}".format(index=index+1, date=value[0], name=value[1]))
        reportIndex = int(input("report index you wanna download:\t")) - 1
        print("{name} downloading...................".format(name=reportList[reportIndex][1]))
        pdfUrl = self.findPDFUrl(reportList[reportIndex][2])
        self.downloadPDF(reportList[reportIndex][1], pdfUrl)

    def findAnnalReports(self, stockid):
        r = requests.get("http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{stockid}/page_type/ndbg.phtml".format(stockid=stockid))
        r.encoding = "gbk"
        bsObj = BeautifulSoup(r.text, "html.parser")
        result = bsObj.findAll("div", {"class":"datelist"})[0]
        dateList = re.findall('\d{4}-\d{2}-\d{2}', result.text)
        returnList = []
        for index, value in enumerate(result.findAll("a")):
            returnList.append([dateList[index], value.text, "http://vip.stock.finance.sina.com.cn"+value["href"]])
        return returnList

    def findPDFUrl(self, originUrl):
        '''
            the links returned from the method <findAnnalReports> are not the PDF links
            those origin links should be further excavated to find the true links
        '''
        r = requests.get(originUrl)
        r.encoding = "gbk"
        bsObj = BeautifulSoup(r.text, "html.parser")
        result = bsObj.findAll("a")
        pdf = [link["href"] for link in result if "PDF" in link["href"]][0]
        return pdf

    def downloadPDF(self, name, url, isDesktop=True):
        if isDesktop:
            fileName = "/Users/red/Desktop/{name}.pdf".format(name=name)
        else:
            fileName = "{name}.pdf".format(name=name)
        pdf = requests.get(url, stream=True)
        with open(fileName, "wb") as file:
            for chunk in pdf:
                file.write(chunk)
        print("Done!")

a = downloader()
# a.searchID()
a.downloadFromID("000002")


