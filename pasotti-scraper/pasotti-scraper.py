from requests import Response, get
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path
import sys
from locale import getdefaultlocale


DOWNLOAD_PROGRESS_TRANSLATION_LIST: dict[str, str] = {
    "en_GB": "Download progress",
    "en_US": "Download progress",
    "it_IT": "Avanzamento di scaricamento",
    "es_ES": "Progreso de la descarga",
    "fr_FR": "Progression du téléchargement",
    "de_DE": "Download-Fortschritt",
    "pt_PT": "Progresso do download",
    "pt_BR": "Progresso do download",
    "nl_NL": "Downloadvoortgang",
    "pl_PL": "Postęp pobierania",
    "ru_RU": "Прогресс загрузки",
    "uk_UA": "Прогрес завантаження",
    "tr_TR": "İndirme ilerlemesi",
    "ja_JP": "ダウンロードの進行状況",
    "zh_CN": "下载进度",
    "ko_KR": "다운로드 진행 상황",
    "ar_SA": "تقدم التنزيل",
    "sv_SE": "Nedladdningsförlopp",
}

DOWNLOAD_STRING: str = (
    " ⬇️ {}: {} / {}"
)


DEFAULT_LINK : str = "https://anita-pasotti.unibs.it/Esami/"
DEFAULT_FOLDER : str = "TemiEsame"


def _get_pdf_uri(url: str) -> list[str]:
    r = get(url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].lower().endswith(".pdf")
    ]


def download_all_files(url : str, destination_folder : str) -> None:
    try:
        folder = Path(__file__).resolve().parent / destination_folder
        folder.mkdir(parents=True, exist_ok=True)
    except:
        pass


    uri_list : list[str] = _get_pdf_uri(url)
    
    total_files : int = len(uri_list)
    progress : int = 1

    for uri in uri_list:
        print(
            DOWNLOAD_STRING.format(
                DOWNLOAD_PROGRESS_TRANSLATION_LIST[getdefaultlocale()[0]],
                progress,
                total_files
            ),
            end='\r'
        )
        urlretrieve(
            f"{url}/{uri}", 
            folder / uri
        )
        progress += 1


if __name__ == "__main__":
    url : str = None
    folder : str = None
    
    try: 
        url = sys.argv[1]
        folder = sys.argv[2]
    except IndexError:
        url = DEFAULT_LINK
        folder = DEFAULT_FOLDER

    download_all_files(url, folder)
