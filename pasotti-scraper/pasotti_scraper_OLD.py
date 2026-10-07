import bs4, requests
import wget
import sys
import os


def foo(table, link):
    pdf = table.find_all("a")
    pdf_list = []
    for i in pdf:
        net = str(i.get("href"))
        if "pdf" in net:
            pdf_list.append(net)
    link = link.replace("teaching.html","")
    
    try:
        os.mkdir("pdf-download")
        os.chdir("pdf-download")
    except FileExistsError:
        print("Cartella già esistente")
        os.chdir("pdf-download")
    except:
        print("Altri errori sono avventuti, non so come gestirli")
        print("Salto questo passaggio")
        return 1

    for i in pdf_list:
        strn = f"{link}/{i}"
        print(f"{strn}")
        try:
            wget.download(strn)
            print()
        except:
            print("Qualcosa è andato storto, passo oltre")
    os.chdir("..")
    return 0


if __name__ == "__main__":
    link = "https://anita-pasotti.unibs.it/teaching.html"
    response = requests.get(link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find("dd")
    foo(table, link)