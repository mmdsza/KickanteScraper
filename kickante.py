import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
from tqdm import tqdm

#Opening our file and placing the headers

filename = "doacoes.csv"
f = open(filename, "w")

headers = "titulo, valorCampanha, numDoadores, targetCampanha, descricaoCampanha, linkCampanha\n"

f.write(headers)

#This is where the magic happens. This loop goes over the n pages chosen and
#returns our desired items.

for i in tqdm(range(0,38)):

    #Declaring our URL, establishing a connection and closing the client.
    my_url = 'https://www.kickante.com.br/campanhas-crowdfunding?page='+str(i)
    uclient = ureq(my_url)
    page_html = uclient.read()
    uclient.close()
    #Our "soup"
    page_soup = soup(page_html, 'html.parser')

    #Making our lives easier by using this containers declaration.
    containers = page_soup.find_all("div", {"class":"campaign-card-wrapper views-row"})
    for container in containers:
        #Getting the campaign names
        titleCampaignBruto = container.div.div.a.img["title"].replace('Crowdfunding para: ', '')
        titleCampaignParsed = titleCampaignBruto.strip().replace(",", ";")
        #Getting the campaign values
        arrecadadoFind = container.div.find_all("div",{"class":"funding-raised"})
        arrecadado = arrecadadoFind[0].text.strip().replace(",", ".")

        #Getting the number of donors
        doadoresBruto = container.div.find_all('span', {"class":"contributors-value"})
        doadoresParsed = doadoresBruto[0].text.strip().replace(",",";")

        #Campaign targets
        fundingGoal = container.div.find_all('div', {"class":"funding-progress"})
        quantoArrecadado = fundingGoal[0].text.strip().replace(",",";")

        #Campaign description
        descricaoBruta = container.div.find_all('div', {"class":"field field-name-field-short-description field-type-text-long field-label-hidden"})
        descricaoParsed = descricaoBruta[0].text.strip().replace(",",";")

        #Getting the links
        linkOrigem = "https://www.kickante.com.br"
        linkBruto = container.div.div.a["href"]
        linkParsed = linkOrigem+linkBruto


        print("Título da campanha: " + titleCampaignParsed)
        print("Valor da campanha: " +arrecadado)
        print("Doadores: "+ doadoresParsed)
        print("target: " + quantoArrecadado)
        print("descricao: " + descricaoParsed)
        print("Link: "+linkParsed)

        #Removing potential linebreakers in text, writing our CSV.
        csvLineEntries = [titleCampaignParsed, arrecadado, doadoresParsed, quantoArrecadado, descricaoParsed.replace(",", ";"), linkParsed]
        csvLine = ','.join([entry.replace('\n', ' ') for entry in csvLineEntries])

        f.write(csvLine + '\n')
    i = i+1
f.close()
