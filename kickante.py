import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup


my_url = 'https://www.kickante.com.br/campanhas-crowdfunding'


uclient = ureq(my_url)
page_html = uclient.read()
uclient.close()

page_soup = soup(page_html, 'html.parser')

containers = page_soup.find_all("div", {"class":"campaign-card-wrapper views-row"})


filename = "doacoes.csv"
f = open(filename, "w")

headers = "titulo, valorCampanha, numDoadores, targetCampanha, descricaoCampanha, linkCampanha\n"

f.write(headers)

for i in range(0,38):
    my_url = 'https://www.kickante.com.br/campanhas-crowdfunding?page='+str(i)
    uclient = ureq(my_url)
    page_html = uclient.read()
    uclient.close()

    page_soup = soup(page_html, 'html.parser')

    containers = page_soup.find_all("div", {"class":"campaign-card-wrapper views-row"})
    for container in containers:
        #Achando os títulos das campanhas
        titleCampaignBruto = container.div.div.a.img["title"].replace('Crowdfunding para: ', '')
        titleCampaignParsed = titleCampaignBruto.strip().replace(",", ";")
        #Achando o valor da campanha
        arrecadadoFind = container.div.find_all("div",{"class":"funding-raised"})
        arrecadado = arrecadadoFind[0].text.strip().replace(",", ".")

        #Número de doadores
        doadoresBruto = container.div.find_all('span', {"class":"contributors-value"})
        doadoresParsed = doadoresBruto[0].text.strip().replace(",",";")

        #target da campanha
        fundingGoal = container.div.find_all('div', {"class":"funding-progress"})
        quantoArrecadado = fundingGoal[0].text.strip().replace(",",";")

        #Descricao da campanha
        descricaoBruta = container.div.find_all('div', {"class":"field field-name-field-short-description field-type-text-long field-label-hidden"})
        descricaoParsed = descricaoBruta[0].text.strip().replace(",",";")

        #Achando os links das campanhas
        linkOrigem = "https://www.kickante.com.br"
        linkBruto = container.div.div.a["href"]
        linkParsed = linkOrigem+linkBruto


        print("Título da campanha: " + titleCampaignParsed)
        print("Valor da campanha: " +arrecadado)
        print("Doadores: "+ doadoresParsed)
        print("target: " + quantoArrecadado)
        print("descricao: " + descricaoParsed)
        print("Link: "+linkParsed)


        csvLineEntries = [titleCampaignParsed, arrecadado, doadoresParsed, quantoArrecadado, descricaoParsed.replace(",", ";"), linkParsed]
        csvLine = ','.join([entry.replace('\n', ' ') for entry in csvLineEntries])

        f.write(csvLine + '\n')
    i = i+1
f.close()


# In[ ]:
