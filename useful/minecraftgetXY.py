import os
import tempfile
import pyautogui
from PIL import Image
import easyocr
import keyboard
import numpy as np

# Função para interpretar o número na imagem usando easyocr
def interpretar_numero(imagem):
    # Salva a imagem temporariamente
    temp_file_path = tempfile.mktemp(suffix=".png")
    Image.fromarray(imagem).convert('L').save(temp_file_path)

    # Usa o easyocr para fazer o OCR
    reader = easyocr.Reader(['en'])

    try:
        resultado = reader.readtext(temp_file_path)

        # Verifica se algum texto foi reconhecido
        if resultado:
            # Extrai o texto reconhecido
            numero = resultado[0][-2]
            return numero
        else:
            return "Nenhum texto reconhecido"

    except Exception as e:
        return f"Erro durante o OCR: {str(e)}"

    finally:
        # Remove o arquivo temporário
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Função para capturar uma região específica da tela e salvar como imagem
def capturar_regiao_tela_e_salvar(x_inicio, y_inicio, largura, altura, nome_arquivo):
    # Captura a região especificada da tela e converte para NumPy array
    imagem_capturada = np.array(pyautogui.screenshot(region=(x_inicio, y_inicio, largura, altura)))

    # Salva a imagem capturada
    Image.fromarray(imagem_capturada).save(nome_arquivo)

    return imagem_capturada

# Main
if __name__ == "__main__":
    print("Pressione 'L' para interpretar o número em uma região específica da tela. Pressione 'Esc' para sair.")

    while True:
        # Aguarde até que a tecla 'L' seja pressionada
        keyboard.wait('l')

        # Define as coordenadas da região a ser capturada (ajuste conforme necessário)
        # x = 0 y = 240
        # x= 780 y = 260
        x_inicio, y_inicio = 0, 240
        largura, altura = 780 - x_inicio, 260 - y_inicio

        # Nome do arquivo para salvar a imagem capturada
        nome_arquivo = "captura_tela.png"

        # Captura a região da tela e salva a imagem
        imagem_capturada = capturar_regiao_tela_e_salvar(x_inicio, y_inicio, largura, altura, nome_arquivo)

        # Interpreta o número na imagem
        numero_interpretado = interpretar_numero(imagem_capturada)

        print(f"Número interpretado: {numero_interpretado}")

        # Verifica se a tecla 'Esc' foi pressionada para sair do loop
        if keyboard.is_pressed('esc'):
            break