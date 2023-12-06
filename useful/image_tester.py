import os
import time

import keyboard
import pyautogui
from PIL import Image, ImageChops
import numpy as np

def identificar_letra_imagem(imagem):
    # Salvar a imagem temporariamente
    temp_path = "temp_letra.png"
    imagem.save(temp_path)

    # Comparar a letra com as referências
    if comparar_imagens(temp_path, "../database/w.png", tolerancia=100) == True:
        os.remove(temp_path)
        return 'W'
    if comparar_imagens(temp_path, "../database/e.png", tolerancia=100) == True:
        os.remove(temp_path)
        return 'E'
    if comparar_imagens(temp_path, "../database/n.png", tolerancia=100) == True:
        os.remove(temp_path)
        return 'N'
    if comparar_imagens(temp_path, "../database/s.png", tolerancia=100) == True:
        os.remove(temp_path)
        return 'S'

    # Remover a imagem temporária após a comparação
    os.remove(temp_path)
def capturar_tela(xi1, yi1, xf2, yf2):
    # Capturar a região da tela
    tela = pyautogui.screenshot()

    # Recortar a região desejada
    regiao_recortada = tela.crop((xi1, yi1, xf2, yf2))
    salvar_path = "quadrado_recortado.png"
    regiao_recortada.save(salvar_path)

    return regiao_recortada
def identificar_letra(imagem_path, xi1, yi1, xf2, yf2):
    # Carregar a imagem
    imagem = Image.open(imagem_path)

    # Recortar o quadrado correspondente à letra
    letra_recortada = imagem.crop((xi1, yi1, xf2, yf2))

    # Salvar a letra recortada temporariamente
    temp_path = "letra_temporaria.png"
    letra_recortada.save(temp_path)

    # Comparar a letra com as referências
    comparar_imagens(temp_path, "../database/w.png", tolerancia=100)
    comparar_imagens(temp_path, "../database/e.png", tolerancia=100)
    comparar_imagens(temp_path, "../database/n.png", tolerancia=100)
    comparar_imagens(temp_path, "../database/s.png", tolerancia=100)


    # Remover a letra temporária após a comparação
    os.remove(temp_path)

def comparar_imagens(imagem1_path, imagem2_path, tolerancia):
    # Carregar as imagens
    imagem1 = Image.open(imagem1_path).convert('RGBA')
    imagem2 = Image.open(imagem2_path).convert('RGBA')

    # Redimensionar a imagem maior para o tamanho da imagem menor
    if imagem1.size != imagem2.size:
        print("tamanho diferente")
        imagem1 = imagem1.resize(imagem2.size)

    # Calcular a diferença entre os arrays
    diferenca = ImageChops.difference(imagem1, imagem2)
    # Converter a diferença para um array numpy para calcular a soma
    array_diferenca = np.array(diferenca)

    # Calcular a soma das diferenças absolutas
    soma_diferencas = np.sum(np.abs(array_diferenca))

    # Verificar se as imagens são iguais com uma tolerância
    if soma_diferencas <= tolerancia:
        print("As imagens são iguais.")
        return True
    else:
        print("As imagens são diferentes.")
        return False

#Crie uma função que leia a letra na posição
    # xi1, yi1 = 138, 3
    # xf2, yf2 = 153, 19
    #essa função vai verificar a imagem (se nao possivel não salvar
    #na memoria secundaria para evitar problema de desempenho)
    #e entao vai comparar se a letra é database/w.png , ou e.png ou n.png ou s.png
    #dependo do resultado será printado w = WEST e = EAST n = NORTH e S = South


def recortar_quadrado(imagem_path, salvar_prefix):
    # Carregar a imagem
    imagem = Image.open(imagem_path)

    # Coordenadas iniciais
    xi1, yi1 = 388, 3
    xf2, yf2 = 403, 19

    # Contador de quadrados lidos
    nQuadradosLidos = 0

    #while nQuadradosLidos < 7:
        # Recortar o quadrado
    quadrado_recortado = imagem.crop((xi1, yi1, xf2, yf2))

        # Atualizar coordenadas para o próximo quadrado
        #xi1 = xf2 + 3
        #xf2 = xi1 + 15

        # Incrementar o contador
        #nQuadradosLidos += 1

        # Salvar o quadrado recortado
    salvar_path = f"{salvar_prefix}{nQuadradosLidos}.png"
    quadrado_recortado.save(salvar_path)

    # Encerrar a função quando 7 quadrados foram lidos
    return "Processo concluído."

def main():
        # Coordenadas da região a ser capturada
    xi1, yi1, xf2, yf2 = 138, 249, 154, 265
    #print(comparar_imagens("quadrado_recortado.png","../database/n.png",100))

    while True:
            # Verificar se a tecla 'N' foi pressionada
        if keyboard.is_pressed('N'):
            # Capturar a tela na região desejada
            regiao_capturada = capturar_tela(xi1, yi1, xf2, yf2)

            # Identificar a letra na imagem capturada
            print(identificar_letra_imagem(regiao_capturada))

            # Aguardar um curto período para evitar detecção repetitiva
            time.sleep(0.5)

if __name__ == "__main__":
    main()



#if __name__ == "__main__":
    # Substitua "caminho_da_imagem.jpg" pelo caminho da sua imagem
    #imagem_path = "captura_tela.png"
    #xi1, yi1 = 138, 3
    #xf2, yf2 = 153, 19
    #identificar_letra(imagem_path, xi1, yi1, xf2, yf2)
    # Substitua "quadrado_recortado.jpg" pelo nome desejado para a imagem recortada
    #salvar_path = "quadrado_recortado.png"



