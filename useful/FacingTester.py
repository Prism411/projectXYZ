import os
import time
import keyboard
import pyautogui
from PIL import Image, ImageChops
import numpy as np

# Coordenadas da região a ser capturada
# 1920x1080 (+6 nos y)
# xi1, yi1, xf2, yf2 = 138, 249, 154, 265
# 1366x768 (-6 nos y)
#xi1, yi1, xf2, yf2 = 138, 243, 154, 259

# regiao_interesse = (160, 0, 176, 16)  (6 quadradinhos) pior caso possivel.
# regiao_interesse = (142, 0, 158, 16)  (5 quadradinhos) caso menos ruim
# regiao_interesse = (124, 0, 140, 16)  (4 quadradinhos) caso nao tao ruim assim.
# regiao_interesse = (106, 0, 122, 16)  (3 quadradinhos) melhor caso possivel.
#18 pixels de diferença por aqui, tomar cuidado com o vlaor a ser plotado
#fazer alguma função que distribua esses valores.

## coordenada do quadrado é (xi=0, yi=0, xf=16, yf=16)
# a cada quadradinho lido o proximo vai estar na coordenadas (xi=0+18, yi=0, xf=16+18, yf=16) entao ela le ele e ve se encontra
# a imagem para comparar, o nome dela (nome_temp) pode ser entre "0 e 9", se nao encotrar nenhum dos numeros ela tenta encontrar um (nome_temp) "ponto"
#caso seja um ponto ela ira ler apenas mais um quadradinho e ira printar os numeros que leu a partir das comparaçoes
# e assim sucessivamente
#      regiao_interesse = (xi, yi, xf, yf=)
#     regiao_cortada = imagem.crop(regiao_interesse)
#     salvar_path = "cortetemp.png"
#     regiao_cortada.save(salvar_path)
#     referencia_path = "../database/ponto.png"
#     if comparar_imagens(salvar_path, referencia_path, tolerancia):
#         print("ponto ENCONTRADO!")
#           ((aqui ele só ira ler mais um quadrado))
#           e terminara
#         os.remove(salvar_path)
#     else:
#         print("cancela")
def detectar_sinal(imagem, regiao_interesse, referencia_path, nome_temp, tolerancia):
    regiao_cortada = imagem.crop(regiao_interesse)
    salvar_path = f"quadradotemp{nome_temp}.png"
    regiao_cortada.save(salvar_path)

    if comparar_imagens(salvar_path, referencia_path, tolerancia):
        os.remove(salvar_path)
        return str(nome_temp)
    else:
        os.remove(salvar_path)
        return ""

def getCord(imagem, tolerancia):
    #quadrado1 = (18, 0, 34, 16) faça uma função que começando desta coordenada
    #ela vai procurar aqui referencia_paths = [f"../database/{i}.png" for i in range(10)]
    #na função: detectar_sinal(imagem, regiao_interesse, referencia_path, nome_temp, tolerancia):
    #regiao_cortada = imagem.crop(regiao_interesse)
    #salvar_path = f"quadradotemp{nome_temp}.png"
    #regiao_cortada.save(salvar_path)

    #if comparar_imagens(salvar_path, referencia_path, tolerancia):
    #    os.remove(salvar_path)
    #    return str(nome_temp)
   # else:
    #    os.remove(salvar_path)
    #    return ""
    #ela vai fazer a verificação


    #regiao_cortada = imagem.crop(quadrado1)
    #salvar_path = "quadradotemp.png"
    #regiao_cortada.save(salvar_path)

    referencia_paths = [f"../database/{i}.png" for i in range(10)]

    #for referencia_path in referencia_paths:
       # if detectar_sinal(imagem, quadrado1, referencia_path,"temp", tolerancia):
           # return str(referencia_paths.index(referencia_path))

    # Se não encontrou nenhum número, tenta encontrar um ponto
    ponto_referencia_path = "../database/ponto.png"
    if detectar_sinal(imagem, quadrado1, ponto_referencia_path,"temp", tolerancia):
        # Leitura de mais um número após encontrar o ponto
        xi, xf = 18, 34
        cord_detectada = ""
        while xi < imagem.width:
            regiao_interesse = (xi, 0, xf, 16)
            for referencia_path in referencia_paths:
                if detectar_sinal(imagem, regiao_interesse, referencia_path,"temp", tolerancia):
                    cord_detectada += str(referencia_paths.index(referencia_path))
                    xi += 18
                    xf += 18
                    break
            else:
                break  # Sai do loop se não encontrar um número

        return cord_detectada

    return "Nenhum número ou ponto detectado"


def identificarCord(imagem, tolerancia):
    quadrado1 = (0, 0, 16, 16)
    regiao_cortada = imagem.crop(quadrado1)
    salvar_path = "quadradotemp.png"
    regiao_cortada.save(salvar_path)

    referencia_path1 = "../database/(.png"
    if comparar_imagens(salvar_path, referencia_path1, tolerancia):
        print("( foi detectado")
        os.remove(salvar_path)
    else:
        print("Cancela")

    # Defina as regiões de interesse e caminhos de referência para os sinais
    regioes_sinais = [
        ((18, 0, 34, 16), "../database/traco.png", "teste"),
        ((160, 0, 176, 16), "../database/traco.png", "teste"),
        ((142, 0, 158, 16), "../database/traco.png", "teste"),
        ((124, 0, 140, 16), "../database/traco.png", "teste"),
        ((106, 0, 122, 16), "../database/traco.png", "teste"),
    ]

    for i, (regiao_interesse, referencia_path, nome_temp) in enumerate(regioes_sinais, start=1):
        print(detectar_sinal(imagem, regiao_interesse, referencia_path, nome_temp, tolerancia))

    print("detectado = "+ getCord(imagem,tolerancia))

# faça aqui uma função que recebe uma letra e retorna os numeros para realizar crop
#se a letra for e ou w ele fará o corte xi = 138 + 428 xf = 254 + 621
#se nao for s ou n ele fará o corte xi = 138 + 446 xf = 254 + 524
#capturar_tela(xi1, yi1, xf2, yf2)
def obter_coordenadas_crop(letra):
    # Coordenadas padrão
    #xi_base, xf_base = 138, 254
    #yi_base, yf_base = 243, 259
    #xi1, yi1, xf2, yf2 = 138, 249, 154, 265
    xi_base, xf_base = 138, 249
    yi_base, yf_base = 243+6, 265+6


    if letra.lower() in ('e', 'w'):
        # Se a letra for 'e' ou 'w'
        return xi_base + 428, yi_base, xf_base + 621, yf_base
    elif letra.lower() in ('s', 'n'):
        # Se a letra for 's' ou 'n'
        return xi_base + 446, yi_base, xf_base + 524, yf_base
    else:
        # Letra desconhecida, retorna None ou lança uma exceção, dependendo da sua preferência
        return None
def identificar_letra_imagem(imagem, tolerancia):
    # Salvar a imagem temporariamente
    temp_path = "temp_letra.png"
    imagem.save(temp_path)

    # Comparar a letra com as referências
    if comparar_imagens(temp_path, "../database/w.png", tolerancia):
        return 'W'
    elif comparar_imagens(temp_path, "../database/e.png", tolerancia):
        return 'E'
    elif comparar_imagens(temp_path, "../database/n.png", tolerancia):
        return 'N'
    elif comparar_imagens(temp_path, "../database/s.png", tolerancia):
        return 'S'

    # Remover a imagem temporária após a comparação
    os.remove(temp_path)
    return None

def capturar_tela(xi1, yi1, xf2, yf2):
    # Capturar a região da tela
    tela = pyautogui.screenshot()

    # Recortar a região desejada
    regiao_recortada = tela.crop((xi1, yi1, xf2, yf2))
    salvar_path = "quadrado_recortado.png"
    regiao_recortada.save(salvar_path)

    return regiao_recortada

def comparar_imagens(imagem1_path, imagem2_path, tolerancia):
    # Carregar as imagens
    imagem1 = Image.open(imagem1_path).convert('RGBA')
    imagem2 = Image.open(imagem2_path).convert('RGBA')

    # Redimensionar a imagem maior para o tamanho da imagem menor
    if imagem1.size != imagem2.size:
        imagem1 = imagem1.resize(imagem2.size)

    #- Calcular a diferença entre os arrays
    diferenca = ImageChops.difference(imagem1, imagem2)
    # Converter a diferença para um array numpy para calcular a soma
    array_diferenca = np.array(diferenca)

    # Calcular a soma das diferenças absolutas
    soma_diferencas = np.sum(np.abs(array_diferenca))

    # Verificar se as imagens são iguais com uma tolerância
    return soma_diferencas <= tolerancia


def main():
    xi1, yi1, xf2, yf2 = 138, 243+6, 154, 259+6
    while True:
        if keyboard.is_pressed('n'):
            print("N pressionado")
            regiao_capturada = capturar_tela(xi1, yi1, xf2, yf2)
            letra_identificada = identificar_letra_imagem(regiao_capturada, tolerancia=100)

            if letra_identificada:
                print(letra_identificada)
                xiCoord1, xyCoord2, xfCoord1, yfCoord2 = obter_coordenadas_crop(letra_identificada)
                cut = capturar_tela(xiCoord1, xyCoord2, xfCoord1, yfCoord2)

                # Identificar a região específica na imagem capturada
                identificarCord(cut, tolerancia=100)

            time.sleep(0.5)


if __name__ == "__main__":
    main()
