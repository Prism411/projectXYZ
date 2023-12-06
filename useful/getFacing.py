import time
import keyboard
import pyautogui
from PIL import Image
import numpy as np

# Coordenadas da região a ser capturada
# 1920x1080
# xi1, yi1, xf2, yf2 = 138, 249, 154, 265
# 1366x768 (-6 nos y)
# xi1, yi1, xf2, yf2 = 138, 243, 154, 259

import numpy as np
from PIL import Image

def identificarCord(imagem, tolerancia):
    # Define as regiões de interesse
    regioes_interesse = [
        {'coord': (0, 0, 16, 16), 'referencia': "../database/n.png"},
        {'coord': (18, 0, 34, 16), 'referencia': "../database/s.png"}
    ]

    for regiao_info in regioes_interesse:
        regiao_coord = regiao_info['coord']
        regiao_referencia_path = regiao_info['referencia']

        # Recorta a região de interesse da imagem
        try:
            regiao_cortada = imagem[regiao_coord[1]:regiao_coord[3], regiao_coord[0]:regiao_coord[2]]
        except IndexError:
            print(f"Error: Unable to slice region at coordinates {regiao_coord}")
            return

        # Carrega a imagem de referência
        try:
            imagem_referencia = np.array(Image.open(regiao_referencia_path).convert('RGB'))
        except FileNotFoundError:
            print(f"Error: Reference image not found at path {regiao_referencia_path}")
            return

        # Slice da imagem de referência
        referencia = imagem_referencia[regiao_coord[1]:regiao_coord[3], regiao_coord[0]:regiao_coord[2]]

        # Debugging information
        print("Shape of regiao_cortada:", regiao_cortada.shape)
        print("Shape of referencia:", referencia.shape)

        # Verificar se os shapes são consistentes
        if regiao_cortada.shape != referencia.shape:
            print("Error: Shapes of region and reference images do not match.")
            return

        # Compara a região de interesse com a imagem de referência
        if comparar_imagens(regiao_cortada, referencia, tolerancia):
            print("beleza")
        else:
            print("cancela")


def obter_coordenadas_crop(letra):
    # Coordenadas padrão
    xi_base, xf_base = 138, 254
    yi_base, yf_base = 243, 259

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
    referencias = {
        'W': "../database/w.png",
        'E': "../database/e.png",
        'N': "../database/n.png",
        'S': "../database/s.png"
    }

    for letra, referencia_path in referencias.items():
        # Carrega a imagem de referência
        imagem_referencia = np.array(Image.open(referencia_path).convert('RGB'))

        # Compara a imagem com a referência
        if comparar_imagens(imagem, imagem_referencia, tolerancia):
            return letra

    return None

def capturar_tela(xi1, yi1, xf2, yf2):
    # Captura a região da tela
    tela = pyautogui.screenshot()

    # Converte a imagem para um array NumPy
    imagem_array = np.array(tela)

    # Recorta a região desejada
    regiao_recortada = imagem_array[yi1:yf2, xi1:xf2]

    return regiao_recortada

def comparar_imagens(imagem1, imagem2, tolerancia):
    print("Shape of imagem1:", imagem1.shape)
    print("Shape of imagem2:", imagem2.shape)

    # Calcular a diferença entre os arrays
    diferenca = np.sum(np.abs(imagem1 - imagem2))

    # Verificar se as imagens são iguais com uma tolerância
    return diferenca <= tolerancia


def main():
    xi1, yi1, xf2, yf2 = 138, 243, 154, 259

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
