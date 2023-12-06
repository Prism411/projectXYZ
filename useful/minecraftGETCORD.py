import pyautogui
import keyboard


# x = 0 y = 240
# x= 780 y = 260

def mostrar_coordenadas_mouse():
    while True:
        # Obtenha as coordenadas dlo mouse
        coordenadas_mouse = pyautogui.position()

        # Exiba as coordenadas
        print(f"Coordenadas do mouse: {coordenadas_mouse}")

        # Saia do loop se a tecla 'L' for pressionada
        if keyboard.is_pressed('l'):
            break

if __name__ == "__main__":
    print("Pressione 'L' para sair.")

    # Inicie o loop para mostrar as coordenadas
    mostrar_coordenadas_mouse()
