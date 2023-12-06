import os
import time
import keyboard
import pyautogui
from PIL import Image, ImageChops
import numpy as np

# Coordenadas da região a ser capturada
# 1920x1080
# xi1, yi1, xf2, yf2 = 138, 249, 154, 265
# 1366x768 (-6 nos y)
#xi1, yi1, xf2, yf2 = 138, 243, 154, 259

def identificarCord(imagem, tolerancia):
    # Define a região de interesse
    regiao_interesse = (0, 0, 16, 16)
    regiao_cortada = imagem.crop(regiao_interesse)
    salvar_path = "quadradotemp.png"
    regiao_cortada.save(salvar_path)
    # Caminho completo para a imagem de referência
    referencia_path = "../database/(.png"
    # Compara a região de interesse com a imagem de referência
    if comparar_imagens(salvar_path, referencia_path, tolerancia):
        print("beleza")
        os.remove(salvar_path)
    else:
        print("cancela")

    regiao_interesse = (18, 0, 34, 16)
    regiao_cortada = imagem.crop(regiao_interesse)
    salvar_path = "quadradotemp2.png"
    regiao_cortada.save(salvar_path)
    referencia_path = "../database/traco.png"
    if comparar_imagens(salvar_path, referencia_path, tolerancia):
        print("beleza")
        os.remove(salvar_path)
    else:
        print("cancela")





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
    yi_base, yf_base = 243, 265


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
    #xi1, yi1, xf2, yf2 = 138, 243, 154, 259
    xi1, yi1, xf2, yf2 = 138, 249, 154, 265
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
