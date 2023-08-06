from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from fake_useragent import UserAgent
from time import sleep

def url_atual(driver) -> str:
    """
    ### Função RETORNA a url atual

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera...)

    Returns:
        (str): URL atual da janela atual
    """
    return driver.current_url


def atualiza_page_atual(driver) -> None:
    """
    ### Função atualiza a página atual da janela atual

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera...)
        
    """
    driver.refresh()
        
        
def espera_e_clica_em_varios_elementos(driver, wdw, locator: tuple) -> None:
    
    wdw.until(EC.presence_of_all_elements_located(locator))
    elements = driver.find_elements(*locator)
    len_elements = len(elements)

    for i in range(len_elements):
        elements[i].click()
        
        
def espera_elemento_disponivel_e_clica(wdw, locator: tuple) -> None:
    """Espera o elemento ficar disponível para clicar e clica

    Args:
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): localização do elemento -> (By.CSS_SELECTOR, '.b')
    """
    wdw.until(EC.element_to_be_clickable(locator)).click()


def espera_elemento(wdw, locator: tuple) -> WebElement:
    """
    ### Função que espera pelo elemento enviado do locator

    Args:
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    return wdw.until(EC.element_to_be_clickable(locator))


def espera_2_elementos(wdw, locator1: tuple, locator2 : tuple) -> WebElement:
    """
    ### Função que espera pelo elemento enviado do locator

    Args:
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator1))
    except Exception:
        wdw.until(EC.element_to_be_clickable(locator2))
        

def espera_elemento_e_envia_send_keys(driver, wdw, string, locator: tuple) -> None:
    """
    ### Função que espera pelo elemento enviado do locator e envia o send_keys no input ou textarea assim que possível

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    wdw.until(EC.element_to_be_clickable(locator))
    try:
        driver.find_element(*locator).send_keys(string)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).send_keys(string)
    
    
def espera_e_retorna_lista_de_elementos(driver, wdw, locator: tuple) -> list:
    """
    ### Função espera e retorna uma lista de elementos indicados no locator

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Opera, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista com os elementos com o formato de Objetos (lista de Objetos)
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_elements(*locator)


def espera_e_retorna_lista_de_elementos_text_from_id(driver, wdw, locator: tuple) -> list:
    """
    ### Função espera e retorna uma lista de elementos com id
    

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista de textos dos elementos com id -> [adv 1, adv 2, adv 3, adv 4, adv 5]
    """
    wdw.until(EC.element_to_be_clickable(locator))
    webelements = driver.find_elements(*locator)
    id = 1
    elementos_com_id = []
    for element in webelements:
        if element.text == ' ':
            elementos_com_id.append(element.text)
        else:
            elementos_com_id.append(f'{element.text} {id}')
        id += 1
    else:
        return elementos_com_id

    
# utilizado para o STJ   
# def espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
#     """Função espera e retorna 

#     Args:
#         driver (_type_): _description_
#         wdw (_type_): _description_
#         locator (tuple, optional): _description_. Defaults to ("BY_SELECTOR", "WEBELEMENT").

#     Returns:
#         _type_: _description_
#     """
#     if locator == ("BY_SELECTOR", "WEBELEMENT"):
#         print('Adicione um locator!!!!')
#         return
#     wdw.until(EC.element_to_be_clickable(locator))
#     webelements = driver.find_elements(*locator)
#     id = 1
#     elementos_com_id = []
#     for element in webelements:
#         if element.text == ' ':
#             elementos_com_id.append(f'VOLUME(S) col{id}')
#         else:
#             elementos_com_id.append(f'{element.text} col{id}')
#         id += 1
#     else:
#         return elementos_com_id


def espera_e_retorna_lista_de_elementos_text(driver, wdw, locator: tuple) -> list:
    """
    ### Função espera e retorna uma lista com os textos dos elementos

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista dos textos dos elementos
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return [element.text for element in driver.find_elements(*locator)]


def espera_e_retorna_conteudo_do_atributo_do_elemento_text(driver, wdw, atributo, locator: tuple) -> str:
    """
    ### Função que espera pelo elemento e retorna o texto do atributo do elemento escolhido

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        atributo (str): O atributo que deseja recuperar, como um href, id, class, entre outros
        locator (tuple): A localização do elemento no DOM ("By.CSS_SELECTOR", "body > div > a").

    Returns:
        str: retorna uma string com o valor do atributo do elemento
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).get_attribute(atributo)


def espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(driver, wdw, atributo, locator: tuple) -> list:
    """
    ### Função espera e retorna o valor dos atributos de vários elementos

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        atributo (str): Atributo (esse deve existir em todos os elementos)
        locator (tuple): Posição dos elementos no DOM.("By.CSS_SELECTOR", "#list_works").

    Returns:
        list: Lista com os atributos de todos os elementos (é necessário que o atibuto enviado exista em todos os elementos como um href)
    """
    wdw.until(EC.element_to_be_clickable(locator))
    atributos = driver.find_elements(*locator)
    elementos_atributos = [atributo_selen.get_attribute(atributo) for atributo_selen in atributos]
    return elementos_atributos
        
        
def espera_e_retorna_elemento_text(driver,  wdw, locator: tuple) -> str:
    """Função espera o elemento e retorna o seu texto

    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): Localização do elemento no DOM. ("By.CSS_SELECTOR", "#name")

    Returns:
        str: Retorna a string de um elemento
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).text
    
    
def vai_para_a_primeira_janela(driver) -> None:
    """Vai para a primeira janela, geralmente a primeira que é iniciada

    Args:
        driver (_type_): WebDriver
    """
    window_ids = driver.window_handles # ids de todas as janelas
    driver.switch_to.window(window_ids[0])
    
    
def espera_abrir_n_de_janelas_e_muda_para_a_ultima_janela(driver, wdw, num_de_janelas: int=2) -> None:
    """Função espera abrir o numero de janelas enviada por ti, e quando percebe que abriu, muda para a última janela aberta

    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriver
        num_de_janelas (int): Quantidade de janelas esperadas para abrie. O padrão é 2.
    """
    print(f'Você está na janela -> {driver.current_window_handle}')
    wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    print(f'Agora, você tem {len(driver.window_handles)} janelas abertas')
    todas_as_windows = driver.window_handles
    driver.switch_to.window(todas_as_windows[-1])
    print(f'Agora, você está na janela -> {driver.current_window_handle}')
    
    
def procura_pela_janela_que_contenha_no_titulo(driver, title_contain_switch : str) -> None: # quero que pelo menos um pedaco do titulo que seja str
    """
    ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
    #### Ex -> Minha janela = janela
    
    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        title_contain_switch (str) : Pelo menos um pedaco do titulo exista para mudar para a página 
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)  
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Janela não encontrada!\n'
            f'Verifique o valor enviado {title_contain_switch}')
    
    
def fecha_janela_atual(driver) -> None:
    """
    ### Função que fecha a janela atual

    Args:
        driver (WebDriver): Seu WebDriver (Chrome, Firefox)
    """
    driver.close()


def fecha_ultima_janela(driver) -> None:
    qtd_de_windows = driver.window_handles
    while len(qtd_de_windows) !=2:
        qtd_de_windows = driver.window_handles
    else:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def espera_enquanto_nao_tem_resposta_do_site(driver, wdw, locator : tuple) -> None:
    """
    ### Função que espera enquanto o site não tem resposta
    
    #### ESSA FUNÇÃO SÓ DEVE SER USADA CASO VOCÊ TENHA CERTEZA QUE O SITE POSSA VIR A CAIR

    Args:
        driver (WebDriver): Seu WebDriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): Localização do elemento no DOM. ("By.CSS_SELECTOR", "#ElementQueSempreEstaPresente")
    """
    try:
        element = wdw.until(EC.element_to_be_clickable(locator))
        if element:
            return element
    except TimeoutException:
        print('Talvez a página tenha dado algum erro, vou atualiza-lá')
        sleep(2)
        try:
            driver.refresh()
            element = wdw.until(EC.element_to_be_clickable(locator))
            if element:
                print('Voltou!')
                return element
        except TimeoutException:
            print('A página ainda não voltou, vou atualiza-lá')
            sleep(2)
            try:
                driver.refresh()
                element = wdw.until(EC.element_to_be_clickable(locator))
                if element:
                    print('Voltou!')
                    return element
            except TimeoutException:
                print('Poxa, essa será a última vez que vou atualizar a página...')
                sleep(2)
                try:
                    driver.refresh()
                    element = wdw.until(EC.element_to_be_clickable(locator))
                    if element:
                        print('Voltou!')
                        return element
                except TimeoutException:
                    print("Olha, não foi possível. A página provavelmente caiu feio :(")
                    print("Infelizmente o programa vai ser finalizado...")
                    driver.quit()
                   
                   
def volta_paginas(driver, qtd_pages_para_voltar : int=1, espera_ao_mudar=0) -> None:
    """
    ### Essa função volta (back) quantas páginas você desejar

    Args:
        driver (_type_): Seu webdriver
        qtd_pages_para_voltar (int): Quantidade de páginas que serão voltadas. O padrão é uma página (1).
        espera_ao_mudar (int or float, optional): Se você quer esperar um tempo para voltar uma página. O padrão é 0.
        
    Uso:
        volta_paginas(driver=self.chrome, qtd_pages_para_voltar=3, espera_ao_mudar=1)
    """
    if espera_ao_mudar == 0:
        for back in range(qtd_pages_para_voltar):
            driver.back()
            driver.refresh()
    else:
        for back in range(qtd_pages_para_voltar):
            sleep(espera_ao_mudar)
            driver.back()
            driver.refresh()
    
    
# Em desenvolvimento
    
# def muda_p_alerta_e_clica_em_accept(driver, wdw, sleeping):
    # sleep(sleeping)
    # alerta = driver.switch_to.alert
    # alerta.accept()


# def muda_p_alerta_e_clica_em_dismiss(self):
    # alerta = self.chrome.switch_to.alert
    # alerta.dismiss()

    
# Em desenvolvimento

def cria_user_agent() -> str:
    """Cria um user-agent automaticamente com a biblio fake_useragent

    Use:
        https://stackoverflow.com/questions/48454949/how-do-i-create-a-random-user-agent-in-python-selenium

    Returns:
        str: user_agent
    """
    _ua = UserAgent()
    user_agent = _ua.random
    return user_agent


def espera_input_limpa_e_envia_send_keys_preessiona_esc(driver, wdw, keys : str, locator : tuple) -> None:
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.keys import Keys

    """
    ### Função espera pelo input ou textarea indicado pelo locator, limpa ele e envia os dados

    Args:
        driver (_type_): Seu webdriver
        wdw (_type_): WebDriverWait criado em seu código
        keys (str): Sua string para enviar no input ou textarea
        locator (tuple): Tupla que contém a forma e o caminho do elemento (By.CSS_SELECTOR, '#myelementid')
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)

    
def espera_input_limpa_e_envia_send_keys(driver, wdw, keys : str, locator : tuple) -> None:
    from selenium.common.exceptions import StaleElementReferenceException
    """
    ### Função espera pelo input ou textarea indicado pelo locator, limpa ele e envia os dados

    Args:
        driver (_type_): Seu webdriver
        wdw (_type_): WebDriverWait criado em seu código
        keys (str): Sua string para enviar no input ou textarea
        locator (tuple): Tupla que contém a forma e o caminho do elemento (By.CSS_SELECTOR, '#myelementid')
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    
        
def espera_elemento_sair_do_dom(wdw, locator) -> WebElement:
    return wdw.until_not(EC.presence_of_element_located(locator))
    

def pega_somente_numeros_de_uma_str(string) -> list:
    """
    ### Função que retorna uma LISTA somente com os números de uma string
    #### Removida do site: https://www.delftstack.com/pt/howto/python/python-extract-number-from-string/#:~:text=Utilizar%20a%20Compreens%C3%A3o%20da%20Lista,%C3%A9%20encontrado%20atrav%C3%A9s%20da%20itera%C3%A7%C3%A3o.
       
    Args:
        string (str): String que tem números com letras
    """
    numbers = [int(temp) for temp in string.split() if temp.isdigit()]
    print(f'A string tem {len(numbers)}, {numbers}')
    return numbers
    
    
def espera_elemento_ficar_ativo_e_clica(driver, wdw, locator : tuple) -> None:

    wdw.until_not(EC.element_to_be_selected(driver.find_element(*locator)))
            # qualquer h1 que aparecer vai falar (apareceu)

    print('O Botão está ativo')

    driver.find_element(*locator).click()
        
        
def espera_elemento_nao_estar_mais_visivel(wdw, locator) -> WebElement:
    return wdw.until_not(EC.visibility_of(*locator))
    

def find_window_to_title_contain(driver, title_contain_switch: str) -> None: # quero que pelo menos um pedaco do titulo que seja str
    """
    ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
    #### Ex -> Minha janela = janela
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for ao menos de um pedaço do titulo que passei
        em title_contain_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)  
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Janela não encontrada!\n'
              f'Verifique o valor enviado {title_contain_switch}')
    
    
def find_window_to_url(driver, url_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url for igual ao parametro enviado
    #### Ex -> https://google.com.br  = https://google.com.br
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)
        if driver.current_url == url_switch:
            break
        else:
            print(f'Janela não encontrada!\n'
                f'Verifique o valor enviado "{url_switch}"')
    
          
def find_window_to_url_contain(driver, contain_url_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url conter no parametro enviado
    #### Ex -> https://google.com.br  = google
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_switch in driver.current_url:
            break
        else:
            print(f'Janela não encontrada!\n'
                f'Verifique o valor enviado "{contain_url_switch}"')
        
        
# def avisa_quando_fecha_janela(wdw, num_de_janelas: int=2):
#     qtd_janelas = wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    
#     if qtd_janelas == num_de_janelas:
#         if wdw.until(EC.new_window_is_opened(2))
    
#     tentativas = 10
    
#     while tentativas != 0:
#         sleep(1)
#         if qtd_janelas == num_de_janelas:
#             while qtd_janelas == num_de_janelas:
#                 qtd_janelas = wdw.until(EC.number_of_windows_to_be(num_de_janelas))
#             else:
#                 return True
#         else:
#             tentativas -= 1
#             continue
#     else:
#         print('NAO ACHOU JANELAS')
        
def pega_codigo_fonte_de_elemento(driver, wdw, locator: tuple) -> str:
    """Retorna todo o código fonte do locator

    Args:
        driver (WebDriver): Webdriver
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): localização do elemento no modo locator -> (By.ID, '.b')

    Returns:
        str: Código fonte do WebElement
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    element = driver.find_element(*locator)
    return element.get_attribute("outerHTML")


def verifica_se_diminuiu_qtd_de_janelas(driver, qtd_de_w) -> None:
    if len(driver.window_handles) == qtd_de_w:
        while len(driver.window_handles) >= qtd_de_w:
            ...
        else:
            window_ids = driver.window_handles # ids de todas as janelas
            driver.switch_to.window(window_ids[1])  # vai para a ultima window
            driver.close()
    else:
        verifica_se_diminuiu_qtd_de_janelas(driver, qtd_de_w)
        
            
def find_window_to_url_contain_and_close_window(driver, contain_url_to_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url conter no parametro enviado
    #### Ex -> https://google.com.br  = google
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_to_switch in driver.current_url:
            driver.close()
            break
        

###########################################################
######### Padrão de classe __init__ para projetos #########
###########################################################

"""
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from FuncsForSPO.functions_for_py import *
from FuncsForSPO.functions_selenium import *
from FuncsForSPO.exceptions import *
import json
import os


class Bot:    
    def __init__(self, headless) -> None:
        # --- CHROME OPTIONS --- #
        self._options = webdriver.ChromeOptions()
        
        
        # --- PATH BASE DIR --- #
        self.__DOWNLOAD_DIR = pega_caminho_atual_e_concatena_novo_dir(dir='base', print_value=False, criar_diretorio=True)
        self._SETTINGS_SAVE_AS_PDF = {
                    "recentDestinations": [
                        {
                            "id": "Save as PDF",
                            "origin": "local",
                            "account": ""
                        }
                    ],
                    "selectedDestinationId": "Save as PDF",
                    "version": 2,
                }

    
        self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{self.__DOWNLOAD_DIR}",
                "download.default_directory":  f"{self.__DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
            
        self._options.add_experimental_option('prefs', self._PROFILE)
        
        self._options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless == 'True':
            self._options.add_argument('--headless')
        self._options.add_argument("--disable-print-preview")
        self._options.add_argument("--disable-web-security")
        self._options.add_argument("--allow-running-insecure-content")
        self._options.add_argument("--disable-extensions")
        self._options.add_argument("--start-maximized")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-setuid-sandbox")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument("--disable-webgl")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-software-rasterizer')
        self._options.add_argument('--no-proxy-server')
        self._options.add_argument("--proxy-server='direct://'")
        self._options.add_argument('--proxy-bypass-list=*')
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--block-new-web-contents')
        self._options.add_argument('--incognito')
        self._options.add_argument('–disable-notifications')
        self._options.add_argument('--suppress-message-center-popups')
        
        self.__service = Service(ChromeDriverManager().install())
        
    def instance_chrome(self):
        self.DRIVER = Chrome(service=self.__service, options=self._options)
        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.DRIVER.maximize_window()
        return self.DRIVER

    def quit_web(self):
        self.DRIVER.quit()
"""

###########################################################
######### Padrão de classe __init__ para projetos #########
##########################################################







#######################################################################################################
######### Padrão de classe __init__ para projetos QUE TENHAM IMPRESSÃO E DOWNLOAD DE ARQUIVOS #########
#######################################################################################################
"""
from datetime import datetime
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from src.tools.functions.functions_for_py import *
from src.tools.functions.functions_selenium import *
from src.tools.functions.openpyxl_funcs import *
from FuncsForSPO.functions.functions_for_py import faz_log
import json
import os
import pandas
import openpyxl
from src.tools.exceptions.exceptions import *


class Bot:    
    def __init__(self, configs):
        # --- PATH BASE DIR --- #
        # self.__PATH_BASE_DIR = os.path.abspath(r".\base")

        # --- CONFIG.INI SETTINGS --- #
        self.config = configs
        self._URL = self.config['SECTION']['site']
        self._TIMEOUT = self.config['SECTION']['tempo_para_achar_elementos']
        self._HEADLESS = self.config['SECTION']['headless']
        self._USUARIO = self.config['SECTION']['usuario']
        self._SENHA = self.config['SECTION']['senha']
        
        # --- CHROME OPTIONS --- #
        self._options = webdriver.ChromeOptions()
        self._SETTINGS_SAVE_AS_PDF = {
                        "recentDestinations": [
                            {
                                "id": "Save as PDF",
                                "origin": "local",
                                "account": ""
                            }
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2,
                    }

        self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{self.__DOWNLOAD_DIR}",
                "download.default_directory":  f"{self.__DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
                
        self._options.add_experimental_option('prefs', self._PROFILE)
        self._options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if self._HEADLESS == 'True':
            self._options.add_argument('--headless')
        self._options.add_argument("--disable-print-preview")
        self._options.add_argument("--disable-web-security")
        self._options.add_argument("--allow-running-insecure-content")
        self._options.add_argument("--disable-extensions")
        self._options.add_argument("--start-maximized")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-setuid-sandbox")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument("--disable-webgl")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-software-rasterizer')
        self._options.add_argument('--no-proxy-server')
        self._options.add_argument("--proxy-server='direct://'")
        self._options.add_argument('--proxy-bypass-list=*')
        self._options.add_argument('--disable-dev-shm-usage')
        
        self.__service = Service(ChromeDriverManager().install())
        self.CHROME = Chrome(service=self.__service, options=self._options)
        self.WDW = WebDriverWait(self.CHROME, timeout=int(self._TIMEOUT))
        self.WDW3 = WebDriverWait(self.CHROME, timeout=3)
        self.CHROME.maximize_window()
        
        # --- READ BASE --- #
        self._DADOS_BASE = self.le_base()
"""

#######################################################################################################
######### Padrão de classe __init__ para projetos QUE TENHAM IMPRESSÃO E DOWNLOAD DE ARQUIVOS #########
#######################################################################################################
