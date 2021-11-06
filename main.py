from bs4 import BeautifulSoup
import requests
import time

# for csv module
import csv


G_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
G_baseURL = "https://coinmarketcap.com/"
G_rowData = {}
#Input None for All match
#OR Input > 0 and < 100
G_limit = 10

def getSoupObj():
    mainPageResp = requests.get(G_baseURL, headers=G_header)
    mainPageSoup = BeautifulSoup(mainPageResp.text, 'html.parser')


    allMainPageTblRws = [iTblRws for iDiv in mainPageSoup.find_all("div", class_="h7vnx2-1 bFzXgL")
                     for iTbl in iDiv.find_all("table", class_="h7vnx2-2")
                     for iTBody in iTbl.find_all("tbody")
                     for iTblRws in iTBody.find_all("tr", limit=G_limit)]

    return allMainPageTblRws

def outputData():
    #header = ['Name','Price','Daily Change','Market Cap','Fully Diluted Market Cap','24 hour volume','Rank','Watchlists']
    print(f"Rank: {G_rowData['Rank']}")
    print(f"Name: {G_rowData['Name']}")
    print(f"Price: {G_rowData['Price']}")
    print(f"Daily Change: {G_rowData['Daily Change']}")
    print(f"Market Cap: {G_rowData['Market Cap']}")
    print(f"Fully Diluted Market Cap: {G_rowData['Fully Diluted Market Cap']}")
    print(f"24 hour volume: {G_rowData['24 hour volume']}")
    print(f"Watchlists: {G_rowData['Watchlists']}")
    print("==========================")

def writeToCsv():
    with open(f"output/{G_rowData['Name'].strip()}.csv", mode="w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(G_rowData.keys())
        writer.writerow(G_rowData.values())


def getData(tblRows):
    for tblRow in tblRows:
        coinResponse = requests.get(G_baseURL + tblRow.find_all("td")[2].find_all("a")[0].get("href"), headers=G_header)
        coinSoup = BeautifulSoup(coinResponse.text, 'html.parser')

        time.sleep(1)
        G_rowData['Rank'] = coinSoup.find("div", class_=["namePill namePillPrimary"]).get_text().split("#")[1]
        G_rowData['Name'] = coinSoup.find("h2", class_="h1").get_text(separator="**", strip=True).split("**")[0]
        G_rowData['Price'] = coinSoup.find("div", class_="priceValue").get_text()
        G_rowData['Daily Change'] = coinSoup.find("div", class_="priceTitle").find("span").get_text()

        G_rowData['Market Cap'] = [i.find("div", class_="statsValue").text
                     for i in coinSoup.find_all("div", class_="statsBlockInner")
                        if (i.text.strip().split('$')[0] == "Market Cap")][0]

        G_rowData['Fully Diluted Market Cap'] = [i.find("div", class_="statsValue").text
                                for i in coinSoup.find_all("div", class_="statsBlockInner")
                                    if(i.text.strip().split('$')[0]=="Fully Diluted Market Cap")][0]

        G_rowData['24 hour volume'] = [i.find("div", class_="statsValue").text
                                for i in coinSoup.find_all("div", class_="statsBlockInner")
                                    if(i.text.strip().split('$')[0]=="Volume 24h")][0]

        G_rowData['Watchlists'] = [i.text.split(" ")[1]
                                for i in coinSoup.find_all("div", class_="namePill")
                                    if "watchlists" in i.text][0]

        #to display the data for each row
        outputData()

        #to write the data to the csv file
        writeToCsv()


#main function call
getData(getSoupObj())