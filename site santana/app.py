from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import codecs

app = Flask(__name__)

SITE_ANTIGO = "https://cidadejanews.com.br"

PAGINA_NOTICIAS = (
    "https://cidadejanews.com.br/noticias"
)

IMAGEM_PADRAO = (
    "https://images.unsplash.com/"
    "photo-1504711434969-e33886168f5c"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto):

    if not texto:
        return ""

    if isinstance(texto, bytes):
        texto = texto.decode("utf-8", errors="ignore")

    texto = texto.replace("\u00a0", " ")
    texto = texto.replace("\u2019", "'")
    texto = texto.replace("\u201c", '"')
    texto = texto.replace("\u201d", '"')

    return " ".join(
        texto.split()
    )


def descobrir_categoria(titulo):

    texto = titulo.lower()

    palavras_policia = [
        "polícia",
        "policia",
        "preso",
        "presa",
        "prisão",
        "prisao",
        "crime",
        "tráfico",
        "trafico",
        "drogas",
        "homicídio",
        "homicidio",
        "assalto",
        "roubo",
        "operação",
        "operacao"
    ]

    palavras_esportes = [
        "futebol",
        "esporte",
        "jogo",
        "campeonato",
        "gol",
        "vitória",
        "vitoria",
        "esquadrão",
        "esquadrão",
        "bahia",
        "tricolor",
        "leão",
        "leao"
    ]

    palavras_politica = [
        "politica",
        "política",
        "governo",
        "prefeito",
        "vereador",
        "eleição",
        "eleicao",
        "camara",
        "câmara",
        "presidência",
        "presidencia",
        "brasil",
        "mundo",
        "congresso",
        "senado",
        "ministro",
        "parlamentar"
    ]

    if "lauro de freitas" in texto:
        return "LAURO DE FREITAS"

    for palavra in palavras_politica:
        if palavra in texto:
            return "POLITICA"

    for palavra in palavras_policia:
        if palavra in texto:
            return "POLICIA"

    for palavra in palavras_esportes:
        if palavra in texto:
            return "ESPORTES"

    return "BAHIA"


def buscar_clima():
    try:
        cidade = "Lauro de Freitas"
        resposta_geocode = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": cidade,
                "country": "BR",
                "language": "pt",
                "count": 5
            },
            timeout=15
        )

        resposta_geocode.raise_for_status()
        dados_geocode = resposta_geocode.json()

        if not dados_geocode.get("results"):
            return None

        resultados = dados_geocode["results"]
        local = None

        for item in resultados:
            if item.get("name", "").lower() == cidade.lower():
                local = item
                break

        if local is None:
            local = resultados[0]

        resposta_clima = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": local["latitude"],
                "longitude": local["longitude"],
                "current": "temperature_2m,weather_code",
                "timezone": "America/Salvador"
            },
            timeout=15
        )

        resposta_clima.raise_for_status()
        dados_clima = resposta_clima.json()

        atual = dados_clima.get("current", {})
        codigo = atual.get("weather_code")
        temperatura = atual.get("temperature_2m")

        mapa = {
            0: ("Céu limpo", "☀️"),
            1: ("Parcialmente nublado", "⛅"),
            2: ("Parcialmente nublado", "⛅"),
            3: ("Encoberto", "☁️"),
            45: ("Nevoeiro", "🌫️"),
            48: ("Geada", "🌫️"),
            51: ("Chuvisco leve", "🌦️"),
            53: ("Chuvisco", "🌦️"),
            55: ("Chuvisco forte", "🌧️"),
            61: ("Chuva leve", "🌧️"),
            63: ("Chuva", "🌧️"),
            65: ("Chuva forte", "⛈️"),
            80: ("Pancadas de chuva", "🌦️"),
            95: ("Trovoada", "⛈️"),
            96: ("Trovoada com granizo", "⛈️"),
            99: ("Trovoada severa", "⛈️")
        }

        descricao, icone = mapa.get(codigo, ("Clima variável", "🌤️"))

        return {
            "cidade": "Lauro de Freitas, BA",
            "descricao": descricao,
            "icone": icone,
            "temperatura": round(temperatura) if temperatura is not None else None
        }

    except Exception as erro:
        print("Erro ao buscar clima:", erro)
        return None


def _corrigir_texto(texto):
    if not texto:
        return ""

    try:
        return texto.encode("latin-1").decode("utf-8")
    except Exception:
        return texto


def _extrair_valor_js(objeto, chave):
    padrao = re.compile(
        rf'{re.escape(chave)}:("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)',
        re.S
    )
    procura = padrao.search(objeto)

    if not procura:
        return ""

    valor = procura.group(1)

    delimitador = valor[0]
    conteudo = valor[1:-1]

    if delimitador == '"':
        conteudo = bytes(conteudo, "latin-1").decode("utf-8", errors="ignore")
        return conteudo.replace("\\n", " ").replace("\\t", " ")

    if delimitador == "'":
        return _corrigir_texto(conteudo.replace("\\'", "'"))

    return _corrigir_texto(conteudo)


def _extrair_objetos_de_array(texto):
    objetos = []
    inicio = texto.find("[")

    if inicio == -1:
        return objetos

    conteudo = texto[inicio + 1:]
    profundidade = 0
    em_string = None
    escapado = False
    objeto_inicio = None

    for indice, caractere in enumerate(conteudo):
        if em_string:
            if escapado:
                escapado = False
            elif caractere == "\\":
                escapado = True
            elif caractere == em_string:
                em_string = None
            continue

        if caractere in {"\"", "'", "`"}:
            em_string = caractere
            continue

        if caractere == "{":
            if profundidade == 0:
                objeto_inicio = indice
            profundidade += 1
            continue

        if caractere == "}" and profundidade > 0:
            profundidade -= 1

            if profundidade == 0 and objeto_inicio is not None:
                objetos.append(conteudo[objeto_inicio:indice + 1])
                objeto_inicio = None

    return objetos


def buscar_noticias_site_antigo():

    noticias = []

    try:
        print(
            "Buscando notícias do site..."
        )

        resposta = requests.get(
            PAGINA_NOTICIAS,
            headers=HEADERS,
            timeout=30
        )

        resposta.raise_for_status()
        resposta.encoding = "utf-8"

        html = resposta.text

        print(
            "STATUS DO SITE:",
            resposta.status_code
        )

        print(
            "TAMANHO DO HTML:",
            len(html)
        )

        padrao_script = re.search(
            r'<script[^>]+src=["\']([^"\']+)["\']',
            html
        )

        if not padrao_script:
            raise ValueError("Nenhum script com conteúdo de notícias encontrado")

        url_script = urljoin(
            PAGINA_NOTICIAS,
            padrao_script.group(1)
        )

        print(
            "BUSCANDO BUNDLE:",
            url_script
        )

        resposta_bundle = requests.get(
            url_script,
            headers=HEADERS,
            timeout=30
        )

        resposta_bundle.raise_for_status()
        resposta_bundle.encoding = "latin-1"

        bundle = resposta_bundle.text

        inicio_pr = bundle.find("pr=[")

        if inicio_pr == -1:
            raise ValueError("Estrutura de notícias não encontrada no bundle")

        array_pr = bundle[inicio_pr + 4:]

        objetos = _extrair_objetos_de_array(array_pr)

        print(
            "ARTIGOS ENCONTRADOS NO BUNDLE:",
            len(objetos)
        )

        for objeto in objetos:
            titulo = limpar_texto(
                _extrair_valor_js(objeto, "title")
            )

            if not titulo:
                continue

            titulo_minusculo = titulo.lower()

            if titulo_minusculo == "whatsapp":
                continue

            if "${a.title}" in titulo:
                continue

            if titulo.strip() == "${a.title} | CidadeJá NEWS":
                continue

            imagem = _extrair_valor_js(objeto, "image")

            if not imagem:
                imagem = IMAGEM_PADRAO

            resumo = limpar_texto(
                _extrair_valor_js(objeto, "description")
            )

            noticias.append({
                "titulo": titulo,
                "link": f"{SITE_ANTIGO}/noticias",
                "imagem": imagem,
                "resumo": resumo,
                "categoria": descobrir_categoria(titulo)
            })

        print(
            "TOTAL ENCONTRADO:",
            len(noticias)
        )

    except Exception as erro:
        print(
            "ERRO AO ACESSAR SITE:",
            erro
        )

    return noticias


@app.route("/")
def inicio():

    noticias = (
        buscar_noticias_site_antigo()
    )

    clima = buscar_clima()

    destaque = None

    if noticias:
        destaque = noticias[0]

    noticias_bahia = [
        noticia for noticia in noticias
        if noticia.get("categoria") in {"BAHIA", "LAURO DE FREITAS"}
    ]

    noticias_esportes = [
        noticia for noticia in noticias
        if noticia.get("categoria") == "ESPORTES"
    ]

    noticias_politica = [
        noticia for noticia in noticias
        if noticia.get("categoria") == "POLITICA"
    ]

    return render_template(
        "index.html",
        noticias=noticias,
        noticias_bahia=noticias_bahia,
        noticias_esportes=noticias_esportes,
        noticias_politica=noticias_politica,
        destaque=destaque,
        clima=clima
    )


if __name__ == "__main__":

    print(
        "INICIANDO CIDADE JÁ NEWS..."
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
