import pyautogui
from datetime import datetime
import os


def close_tab():
    pyautogui.keyDown('ctrl')
    pyautogui.press('w')
    pyautogui.keyUp('ctrl')


def loading_screen(screen: object, image_error: object = "") -> object:
    loading = pyautogui.locateOnScreen(f'images/{screen}.png', confidence=0.8)
    while loading is None:
        pyautogui.sleep(0.5)
        loading = pyautogui.locateOnScreen(f'images/{screen}.png', confidence=0.8)
        error = False
        if image_error:
            error = pyautogui.locateOnScreen(f'images/{image_error}.png', confidence=0.8)
        if error:
            close_tab()
            exit()


def getCnpj():
    with open("config", "r") as configFile:
        content = configFile.readlines()
        cnpjInFile = [i for i in content if "CNPJ=" in i]
        return cnpjInFile[0][5:-1]


def getAuto():
    with open("config", "r") as configFile:
        content = configFile.readlines()
        autoInFile = [i for i in content if "AUTO=" in i]
        if autoInFile[0][5:-1].lower() == "true":
            return True
        else:
            return False


def getMonth():
    with open("config", "r") as configFile:
        content = configFile.readlines()
        monthInFile = [i for i in content if "MONTH=" in i]
        if int(monthInFile[0][6:-1]) > 0:
            return int(monthInFile[0][6:-1])
        else:
            return 0


def getYear():
    with open("config", "r") as configFile:
        content = configFile.readlines()
        yearInFile = [i for i in content if "YEAR=" in i]
        if int(yearInFile[0][5:-1]) > 0:
            return int(yearInFile[0][5:-1])
        else:
            return 0


cnpj = getCnpj()
auto = getAuto()
month = auto if getMonth() else 0
year = auto if getYear() else 0
actual_month = datetime.now().month
actual_year = datetime.now().year

# ACESSAR NAVEGADOR
os.system('start chrome {}'.format('http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao'))
# os.system ('google-chrome http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao' )
loading_screen('login')
pyautogui.typewrite(cnpj)

# LOGIN
continue_btn = pyautogui.locateCenterOnScreen('images/btn_continue.png')
pyautogui.moveTo(continue_btn.x, continue_btn.y, duration=0.2)
pyautogui.click(continue_btn.x, continue_btn.y)

# CLICK EMITIR GUIA
loading_screen('home')
link_emit_guia = pyautogui.locateCenterOnScreen('images/link_emit_guia.png', confidence=0.8)
pyautogui.click(link_emit_guia.x, link_emit_guia.y)

# CLICK SELECT ANO
loading_screen('screen_year')
pyautogui.press('tab', presses=6)
pyautogui.press('enter')

# CLICK YEAR VALUE
if not auto & year:
    actual_year = year
else:
    if actual_month == 1:
        actual_year = actual_year - 1

pyautogui.sleep(0.3)
positionYear = {
    2022: pyautogui.locateCenterOnScreen('images/2022.png', confidence=0.95),
    2023: pyautogui.locateCenterOnScreen('images/2023.png', confidence=0.95),
    2024: pyautogui.locateCenterOnScreen('images/2024.png', confidence=0.95),
    2025: pyautogui.locateCenterOnScreen('images/2025.png', confidence=0.95),
    2026: pyautogui.locateCenterOnScreen('images/2026.png', confidence=0.95),
}

pyautogui.click(positionYear[actual_year].x, positionYear[actual_year].y)
pyautogui.sleep(1)

# CLICK SUBMIT
pyautogui.press('tab')
pyautogui.press('enter')

# CLICK CHECKBOX MONTH
loading_screen('component_header_month')
tab_presses = {
    1: 9,
    2: 11,
    3: 13,
    4: 15,
    5: 17,
    6: 19,
    7: 21,
    8: 23,
    9: 25,
    10: 27,
    11: 29,
    12: 31
}

# Obtendo o mês atual
current_month = datetime.now().month

# Calculando o número de pressionamentos de tecla TAB necessários
month_pay = 12 if current_month == 1 else current_month - 1
num_tab_presses = tab_presses[month_pay]

# Pressionando a tecla TAB o número de vezes necessário
pyautogui.press('tab', num_tab_presses)

# Clicando no checkbox do mês anterior
pyautogui.press('space')

# CLICK GENERATE DAS
pyautogui.press('pgdn')
pyautogui.sleep(1)
generate_das = pyautogui.locateCenterOnScreen('images/btn_generate_das.png', confidence=0.95)
pyautogui.click(generate_das.x, generate_das.y)

# BAIXAR PDF
loading_screen('component_modal_success', "component_modal_warning")
download_pdf = pyautogui.locateCenterOnScreen('images/btn_download_pdf.png')
pyautogui.click(download_pdf.x, download_pdf.y)
close_tab()
