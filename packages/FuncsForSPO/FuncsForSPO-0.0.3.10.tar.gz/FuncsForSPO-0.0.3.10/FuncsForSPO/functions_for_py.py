"""
Várias funções para ajudar no desenvolvimento de qualquer aplicação em Python

Nesse módulo você achará desde funções simples, até funções complexas que levariam um bom tempo para desenvolve-las.

Para usar esse módulo, será necessário instalar o psutil, pois existe uma função que coleta informações do sistema
-> pip install psutil
"""

from datetime import datetime
from time import sleep
import os, sys, psutil, shutil, platform, re, socket, uuid, logging

def remove_extensao_de_str(arquivo :str, extensao_do_arquivo :str) -> str:
    """Remove a extensão de um nome de arquivo.
    

    Args:
        arquivo (str): arquivo com a extensão em seu nome -> file.xlsx
        extensao_do_arquivo (str): extensão que deseja remover

    Returns:
        str: Nome do arquivo sem a extensão.
    """
    replacement =  arquivo.replace(f'.{extensao_do_arquivo}', '')
    replacement =  replacement.replace(f'{extensao_do_arquivo}', '')
    return replacement


def reverse_iter(iteravel :str | tuple | list) -> str | tuple | list:
    """Retorna qualquer iterável ao reverso
    
    Use:
        Antes da utilização: '1234567890'
        Antes da utilização: (1,2,3,4,5,6,7,8,9,0)
        Antes da utilização: [1,2,3,4,5,6,7,8,9,0]
    
    
        Após a utilização: '0987654321'
        Após a utilização: (0,9,8,7,6,5,4,3,2,1)
        Após a utilização: [0,9,8,7,6,5,4,3,2,1]

    * By https://www.geeksforgeeks.org/python-reversing-tuple/#:~:text=Since%20tuples%20are%20immutable%2C%20there,all%20of%20the%20existing%20elements.

    Args:
        iteravel (str | tuple | list): Qualquer iterável para ter seu valor reverso

    Returns:
        str | tuple | list: iterável com seus valores reversos
    """
    return iteravel[::-1]


def pega_caminho_atual(print_value: bool=False) -> str: 
    """Retorna o caminho absoluto do diretório de execução atual do script Python 
    
    Args: 
        print_value (bool, optional): Printa e retorna o path. Defaults to False. 
    
    Returns: 
        str: retorna o caminho absoluto da execução atual do script Python 
    """ 
    if print_value: 
        print(os.getcwd()) 
        return os.getcwd() 
    else: 
        return os.getcwd()


def cria_dir_no_dir_de_trabalho_atual(dir: str, print_value: bool=False, criar_diretorio: bool=False) -> str:
    """Faz essas funções 
    
    1 - Pega o caminho atual de execução do script 
    
    2 - Concatena o "dir" com o caminho atual de execução do script 
    
    3 - Cria o diretório novo no caminho atual (optional) 
    
    
    Args: dir (str): Diretório que poderá ser criado print_value (bool, optional): Printa na tela a saida do caminho com o diretório criado. Defaults to False. 
          cria_diretorio (bool, optional): Cria o diretório enviado no caminho em que o script está sendo utilizado. Defaults to False. 
          
    Returns: 
        str: Retorna o caminho do dir com o caminho absoluto 
    """
    current_path = pega_caminho_atual()
    path_new_dir = os.path.join(current_path, dir) 
    if print_value: 
        print(path_new_dir) 
        if criar_diretorio: 
            os.makedirs(path_new_dir, exist_ok=True)  # Se existir, não cria
            return (path_new_dir)
    else: 
        if criar_diretorio: 
            os.makedirs(path_new_dir, exist_ok=True) 
        return (path_new_dir)


def verifica_se_baixou_um_arquivo(path_pasta:str, qtd_arquivos_esperados : int=1) -> bool:
    """Retorna True quando achar ao menos um arquivo na pasta com a extensão proposta
    
    ## ATENÇÃO: ESTA FUNÇÃO AINDA ESTÁ EM DESENVOLVIMENTO
    
    Args:
        path_pasta (str): caminho da pasta para pesquisar se exite arquivos
        extensao (str): extenção do arquivo
        
    Returns:
        bool: True caso exista o arquivo; False caso não exista o arquivo
    """
    
    # pega todos os arquivos e pastas do diretório
    arquivos = os.listdir(os.path.abspath(path_pasta))
    # pega a qtd de arquivos
    qtd_arquivos = len(arquivos)
    tentativas = 5
    tentativas_count = 1
    # enquanto a qtd de arquivos for != da quantidade de arquivos esperados
    while qtd_arquivos != qtd_arquivos_esperados:
        if tentativas == 0:
            return False
        faz_log('O arquivo ainda não foi baixado.')
        faz_log(f'Existem {qtd_arquivos} atualmente na pasta.')
        faz_log(f'Tentativa {tentativas_count}')


        for arquivo in arquivos:
            if '.crdownload' in arquivo:
                os.system('cls')
                faz_log('Existe um arquivo que está sendo baixado...')
                sleep(5)
                arquivos = os.listdir(os.path.abspath(path_pasta))
                qtd_arquivos = len(arquivos)
                tentativas -= 1
                tentativas_count += 1
                return False
        else:
            sleep(3)
            arquivos = os.listdir(os.path.abspath(path_pasta))
            qtd_arquivos = len(arquivos)
            tentativas -= 1
            tentativas_count += 1
            return False
    else:
        faz_log('O arquivo foi baixado...')
        return True


def deleta_arquivos_duplicados(path_dir :str, qtd_copyes :int) -> None:
    """Deleta arquivos que contenham (1), (2) até a quantidade desejada
    
    Use:
        deleta_arquivos_duplicados('dir', 2)
            dir--|

                    |---File.txt
                    
                    |---File (1).txt -> This is deleted!
                    
                    |---File (2).txt -> This is deleted!
                    
                    |---File (3).txt -> This is not deleted!
                
    

    Args:
        path_dir (str): _description_
        qtd_copyes (int): quantidade de possíveis arquivos repetidos
    """
    path_downloads = os.path.abspath(path_dir)
    arquivos = os.listdir(path_downloads)
    if len(arquivos) > 1 or len(arquivos) > 2:
        copyes = [f'({i})' for i in range(qtd_copyes)]
        print(copyes)
        for copye in copyes:
            for arquivo in arquivos:
                if copye in arquivo:
                    print(f'deletando {path_downloads}\\{arquivo}')
                    os.remove(path_downloads+'\\'+arquivo)  


def arquivos_com_caminho_absoluto_do_arquivo(path_dir: str) -> tuple[str] | str:
    """Retorna uma tupla com vários caminhos dos arquivos e diretórios ou o caminho do arquivo / diretório apenas

    ### O script pegará esse caminho relativo, pegará o caminho absoluto dele e concatenará com os arquivo(s) e/ou diretório(s) encontrado(s)
    
    Args:
        path_dir (str): caminho relativo do diretório

    Returns:
        tuple[str] | str: Retorna uma tupla com os arquivos ou o caminho do arquivo (str)
    """
    ARQUIVOS = tuple(f'{os.path.abspath(path_dir)}\\{arquivo}' for arquivo in os.listdir(path_dir))
    if len(ARQUIVOS) > 1:
        return ARQUIVOS
    else:
        return ARQUIVOS[0]


def pega_id(assunto: str) -> str:
    """
    Essa função simplesmente pega uma string, separa ela por espaços e verifica se a palavra existe ou é igual a "ID",
        se existe, pega a string, caso seja igual, pega a string e um acima para pegar o id em si

    Args:
        assunto (str): Assunto do E-mail

    Returns:
        str | bool: Retorna o id com o número ou False se não tiver um assunto com ID
    """
    assunto = assunto.upper()
    assunto = assunto.strip()
    list_string_official = []
    if 'ID' in assunto:
        # Separa todos as strings por espaço
        assunto_list = assunto.split(' ')

        for i in range(len(assunto_list)):
            # se a palavra do assunto for id e a próxima palavra for 'elaw' pega id e o número
            if assunto_list[i] == 'ID' and assunto_list[i+1] == 'ELAW':
                list_string_official.append(assunto_list[i])
                list_string_official.append(assunto_list[i+2])
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
            if assunto_list[i] == 'ID' and 'ELAW' in assunto_list[i+1]:
                list_string_official.append(assunto_list[i])
                try:
                    list_string_official.append(assunto_list[i+2])
                except Exception:
                    list_string_official.append(assunto_list[i+1])
                    id_ = ' '.join(list_string_official)
                    num_id = re.findall(r'\d+', id_)  # pega somente números da string
                    id_ = f'ID {num_id[0]}'#EX (ID 111111)#
                    faz_log(id_)
                    return id_
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
            if assunto_list[i] == 'ID' or assunto_list[i] == 'ID:' or assunto_list[i] == 'ID.' or assunto_list[i] == '-ID':
                list_string_official.append(assunto_list[i])
                list_string_official.append(assunto_list[i+1])
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
        else:
            faz_log(f'Não existe ID para o ASSUNTO: {assunto}', 'w')
            return False
    else:
        faz_log(f'Não existe ID para o ASSUNTO: {assunto}', 'w')
        return False


def data_atual() -> str:
    """Retorna a data atual
    A data a ser retornada tem essa formatação -> DD/MM/YYYY

    Returns:
        str: Data nessa formatação -> DD/MM/YYYY
    """
    e = datetime.now()
    return f'{e.day}/{e.month}/{e.year}'


def download_file(link: str, dest_path: str):
    import requests
    """Faz o Download de arquivos
    É necessário que o arquivo venha com a sua extensão no http; exemplo de uso abaixo:
    
    Use:
        donwload('https://filesamples.com/samples/document/xlsx/sample3.xlsx', file_xlsx.xlsx)

    Args:
        link (str): link do arquivo que será baixado
        dest_path (str): destino do arquivo que será baixado (com a sua extensão)
    """
    r = requests.get(link, allow_redirects=True)
    try:
        with open(dest_path, 'wb') as file:
            file.write(r.content)
            print(f'Download completo! -> {os.path.abspath(dest_path)}')
    except Exception as e:
        print(f'Ocorreu um erro:\n{str(e)}')
    finally:
        del r


def hora_atual(segundos: bool=False) -> str:
    """Função retorna a hora atual no formato hh:mm ou hh:mm:ss com segundos ativado"""
    from datetime import datetime
    e = datetime.now()
    if segundos:
        return f'{e.hour}:{e.minute}:{e.second}'
    else:
        return f'{e.hour}:{e.minute}'


def times() -> str:
    """Função retorna o tempo do dia, por exemplo, Bom dia, Boa tarde e Boa noite

    Returns:
        str: Periodo do dia, por exemplo, Bom dia, Boa tarde e Boa noite
    """
    import datetime
    hora_atual = datetime.datetime.now()
    if hora_atual.hour < 12:
        return 'Bom dia!'
    elif 12 <= hora_atual.hour < 18:
        return 'Boa tarde!'
    else:
        return 'Boa noite!'


def psutil_verifica(nome_do_exe : str) -> bool:
    # pip install psutil
    """Função verifica se executavel está ativo ou não

    Args:
        nome_do_exe (str): Nome do executável -> notepad.exe, chrome.exe
    """
    exe_ativo = nome_do_exe in (i.name() for i in psutil.process_iter())

    while exe_ativo:
        exe_ativo = nome_do_exe in (i.name() for i in psutil.process_iter())
        return exe_ativo
    else:
        return exe_ativo


def lista_todos_os_processos_atuais() -> object:
    """Esse é um gerador que mostra todos os processos e executáveis atívos no momento.
    
    para utilizar (ver os processos em execução):
        for i in lista_todos_os_processos_atuais():
            print(i)

    Returns:
        object: generator
    """
    return (i.name() for i in psutil.process_iter())


def verifica_se_caminho_existe(path_file_or_dir: str) -> bool:
    if os.path.exists(path_file_or_dir):
        return True
    else:
        return False


def deixa_arquivos_ocultos_ou_n(path_file_or_dir : str, oculto : bool) -> None:
    import ctypes
    from stat import FILE_ATTRIBUTE_ARCHIVE
    FILE_ATTRIBUTE_HIDDEN = 0x02

    if oculto:
        ctypes.windll.kernel32.SetFileAttributesW(path_file_or_dir, FILE_ATTRIBUTE_HIDDEN)
        print(f'O arquivo / diretório {path_file_or_dir} ESTÁ OCULTO!')
    else:
        ctypes.windll.kernel32.SetFileAttributesW(path_file_or_dir, FILE_ATTRIBUTE_ARCHIVE)
        print(f'O arquivo / diretório {path_file_or_dir} NÃO ESTÁ MAIS OCULTO!')
        
    # HIDDEN = OCULTO
    # ARCHIVE = Ñ OCULTO


def fazer_requirements_txt() -> None:
    os.system("pip freeze > requirements.txt")


def limpa_terminal_e_cmd() -> None:
    """Essa função limpa o Terminal / CMD no Linux e no Windows"""
    
    os.system('cls' if os.name == 'nt' else 'clear')


def print_bonito(string : str, efeito='=', quebra_ultima_linha : bool=True) -> str:
    """Faz um print com separadores
    

    Args:
        string (str): o que será mostrado
        
    
    Exemplo:
        print_bonito('Bem vindo')
    
            =============
            = Bem vindo =
            =============
    
    
    """
    try:
        if len(efeito) != 1:
            print('O EFEITO DEVE SER SOMENTE UMA STRING efeito="="\n'
                '=========\n'
                '== Bem ==\n'
                '=========\n')
            return
        else:
            ...
        
        if quebra_ultima_linha:
            print(efeito*2 + efeito*len(string) + efeito*4)
            print(efeito*2 + ' '+string+' ' + efeito*2)
            print(efeito*2 + efeito*len(string) + efeito*4)
            print('')
        else:
            print(efeito*2 + efeito*len(string) + efeito*4)
            print(efeito*2 + ' '+string+' ' + efeito*2)
            print(efeito*2 + efeito*len(string) + efeito*4)
    except TypeError:
        print('O tipo de string, tem que ser obviamente, string | texto')


def instalar_bibliotecas_globalmente() -> None:
    """
        Instalar bibliotecas
            * pandas
            * unidecode
            * openpyxl
            * pyinstaller==4.6
            * selenium
            * auto-py-to-exe.exe
            * webdriver-manager
            * xlsxwriter
    """
    print('Instalando essas bibliotecas:\n'
          ' *pandas\n'
          ' *unidecode\n'
          ' *openpyxl\n'
          ' *pyinstaller==4.6\n'
          ' *selenium\n'
          ' *auto-py-to-exe.exe\n'
          ' *webdriver-manager\n'
          ' *xlsxwriter\n')
    aceita = input('você quer essas bibliotecas mesmo?s/n\n >>> ')
    if aceita == 's':
        os.system("pip install pandas unidecode openpyxl pyinstaller==4.6 selenium auto-py-to-exe webdriver-manager xlsxwriter")
        print('\nPronto')
    if aceita == '':
        os.system("pip install pandas unidecode openpyxl pyinstaller==4.6 selenium auto-py-to-exe webdriver-manager xlsxwriter")
        print('\nPronto')
    if aceita == 'n':
        dependencias = input('Escreva as dependencias separadas por espaço\nEX: pandas selenium pyautogui\n>>> ')
        os.system(f'pip install {dependencias}')
        print('\nPronto')
        sleep(3)


def criar_ambiente_virtual(nome_da_venv: str) -> None:
    nome_da_venv = nome_da_venv.strip()
    nome_da_venv = nome_da_venv.replace('.', '')
    nome_da_venv = nome_da_venv.replace('/', '')
    nome_da_venv = nome_da_venv.replace(',', '')
    os.system(f'python -m venv {nome_da_venv}')
    print(f'Ambiente Virtual com o nome {nome_da_venv} foi criado com sucesso!')
    sleep(2)
    
def restart_program() -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)


def print_colorido(string : str, color='default', bolder : bool=False) -> str:
    """Dê um print com saida do terminal colorida

    Args:
        string (str): string que você quer colorir na saida do terminal / cmd
        color (str, optional): cor que você deseja colorir a string. Defaults to 'default'.
        bolder (bool, optional): se você deseja deixar a string com negrito / bolder. Defaults to False.
        
    Color List:
        white;
        red;
        green;
        blue;
        cyan;
        magenta;
        yellow;
        black.
    """
    color.lower()
    
    win_version = platform.system()+' '+platform.release()
    
    if 'Windows 10' in win_version:
        if bolder == False:
            if color == 'default':  # white
                print(string)
            elif color == 'red':  # red
                print(f'\033[31m{string}\033[m')
            elif color == 'green':  # green
                print(f'\033[32m{string}\033[m')
            elif color == 'blue':  # blue
                print(f'\033[34m{string}\033[m')
            elif color == 'cyan':  # cyan
                print(f'\033[36m{string}\033[m')
            elif color == 'magenta':  # magenta
                print(f'\033[35m{string}\033[m')
            elif color == 'yellow':  # yellow
                print(f'\033[33m{string}\033[m')
            elif color == 'black':  # black
                print(f'\033[30m{string}\033[m')
            
        elif bolder == True:
            if color == 'default':  # white
                print(f'\033[1m{string}\033[m')
            elif color == 'red':  # red
                print(f'\033[1;31m{string}\033[m')
            elif color == 'green':  # green
                print(f'\033[1;32m{string}\033[m')
            elif color == 'blue':  # blue
                print(f'\033[1;34m{string}\033[m')
            elif color == 'cyan':  # cyan
                print(f'\033[1;36m{string}\033[m')
            elif color == 'magenta':  # magenta
                print(f'\033[1;35m{string}\033[m')
            elif color == 'yellow':  # yellow
                print(f'\033[1;33m{string}\033[m')
            elif color == 'black':  # black
                print(f'\033[1;30m{string}\033[m')
    else:
        print(string)


def input_color(color : str='default', bolder : bool=False, input_ini: str='>>>') -> None:
    """A cor do input que você pode desejar

    Args:
        color (str, optional): cor do texto do input (não o que o user digitar). Defaults to 'default'.
        bolder (bool, optional): adiciona um negrito / bolder na fonte. Defaults to False.
        input_ini (str, optional): o que você deseja que seja a string de saida do input. Defaults to '>>>'.

    Returns:
        input: retorna o input para ser adicionada em uma var ou qualquer outra coisa
        
    Color List:
        white;
        red;
        green;
        blue;
        cyan;
        magenta;
        yellow;
        black.
    """

    if bolder == False:
        if color == 'default':  # white
            return input(f'{input_ini} ')
        elif color == 'red':  # red
            return input(f'\033[31m{input_ini}\033[m ')
        elif color == 'green':  # green
            return input(f'\033[32m{input_ini}\033[m ')
        elif color == 'blue':  # blue
            return input(f'\033[34m{input_ini}\033[m ')
        elif color == 'cyan':  # cyan
            return input(f'\033[36m{input_ini}\033[m ')
        elif color == 'magenta':  # magenta
            return input(f'\033[35m{input_ini}\033[m ')
        elif color == 'yellow':  # yellow
            return input(f'\033[33m{input_ini}\033[m ')
        elif color == 'black':  # black
            return input(f'\033[30m{input_ini}\033[m ')
        else:
            print('Isso não foi compreensivel. Veja a doc da função, as cores válidas')
    elif bolder == True:
        if color == 'default':  # white
            return input(f'\033[1m{input_ini}\033[m ')
        elif color == 'red':  # red
            return input(f'\033[1;31m{input_ini}\033[m ')
        elif color == 'green':  # green
            return input(f'\033[1;32m{input_ini}\033[m ')
        elif color == 'blue':  # blue
            return input(f'\033[1;34m{input_ini}\033[m ')
        elif color == 'cyan':  # cyan
            return input(f'\033[1;36m{input_ini}\033[m ')
        elif color == 'magenta':  # magenta
            return input(f'\033[1;35m{input_ini}\033[m ')
        elif color == 'yellow':  # yellow
            return input(f'\033[1;33m{input_ini}\033[m ')
        elif color == 'black':  # black
            return input(f'\033[1;30m{input_ini}\033[m ')
        else:
            print('Isso não foi compreensivel.\nVeja na doc da função (input_color), as cores válidas')
    else:
        print('Não entendi, veja a doc da função (input_color), para utiliza-lá corretamente')


def move_arquivos(path_origem: str, path_destino: str, extension: str) -> None:
    """Move arquivos para outra pasta

    Args:
        path_origem (str): caminho de origem
        path_destino (str): caminho de destino
        extension (str): Estensão do arquivo.
    """

    arquivos_da_pasta_origem = os.listdir(path_origem)
    arquivos = [path_origem + "\\" + f for f in arquivos_da_pasta_origem if extension in f]
    
    for arquivo in arquivos:
        try:
            shutil.move(arquivo, path_destino)
        except shutil.Error:
            shutil.move(arquivo, path_destino)
            os.remove(arquivo)


def pega_somente_numeros(string :str) -> str or int:
    """Função pega somente os números de qualquer string
    
    * remove inclusive . e ,
    
    Args:
        string (str): sua string com números e outros caracteres

    Returns:
        str: somente os números
    """
    if isinstance(string, (str)):
        r = re.compile(r'\D')
        return r.sub('', string)
    else:
        print('Por favor, envie uma string como essa -> "2122 asfs 245"')
        return


def remove_arquivo(file_path : str) -> None:
    os.remove(os.path.abspath(file_path))


def remove_diretorio(dir_path : str):
    """Remove diretórios recursivamente

    Args:
        dir_path (str): caminho do diretório a ser removido
    """
    shutil.rmtree(os.path.abspath(dir_path))


def ver_tamanho_de_objeto(objeto : object) -> int:
    """Veja o tamanho em bytes de um objeto

    Args:
        objeto (object): objeto a verificar o tamanho

    Returns:
        int: tamanho do objeto
    """
    print(sys.getsizeof(objeto))


def remove_espacos_pontos_virgulas_de_um_int(numero: int, remove_2_ultimos_chars: bool=False) -> int:
    """Remove espaços, pontos, virgulas e se quiser os 2 últimos caracteres

    Args:
        numero (int): número com todos os elementos que serão removidos
        remove_2_ultimos_chars (bool, optional): remove os 2 últimos caracteres, por exemplo, 0,00 fica 0. Defaults to False.

    Returns:
        int: _description_
    """
    numero = str(numero)
    numero = numero.replace(',', '')
    numero = numero.replace('.', '')
    numero = numero.strip()
    if remove_2_ultimos_chars:
        numero = numero[:-2]
    return int(numero)


def fecha() -> None:
    """Fecha o programa
    """
    try:
        quit()
    except NameError:
        pass

    
def fecha_em_x_segundos(qtd_de_segundos_p_fechar : int) -> None:
    """Espera os segundos enviados para fechar o programa

    Args:
        qtd_de_segundos_p_fechar (int): segundos para fazer regresivamente para fechar o programa
    """
    faz_log(f'Saindo do robô em: {qtd_de_segundos_p_fechar} segundos...')
    for i in range(qtd_de_segundos_p_fechar):
        faz_log(str(qtd_de_segundos_p_fechar))
        qtd_de_segundos_p_fechar -= 1
        sleep(1)
    fecha()
    
    
def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller 
    
        SE QUISER ADICIONAR ALGO NO ROBÔ BASTA USAR ESSA FUNÇÃO PARA ADICIONAR O CAMINHO PARA O EXECUTÁVEL COLOCAR
        * PARA USAR DEVE COLOCAR ESSA FUNÇÃO NO MÓDULO POR CAUSA DO os.path.abspath(__file__) * 
    """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def pega_infos_da_maquina():
    """
    ### Pega os dados da máquina
    Necessário ter a função faz_log
    https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
    """
    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
         
            
    faz_log("==== INFORMAÇÃO DO SISTEMA ====", 'i*')
    uname = platform.uname()
    faz_log(f"SISTEMA: {uname.system}", 'i*')

    faz_log(f"NOME DO PC: {uname.node}", 'i*')

    faz_log(f"VERSÃO DO SISTEMA: {uname.release}", 'i*')

    faz_log(f"VERSÃO DO SISTEMA (COMPLETO): {uname.version}", 'i*')
    faz_log(f"ARQUITETURA: {uname.machine}", 'i*')
    faz_log(f"PROCESSADOR: {uname.processor}", 'i*')
    faz_log(f"ENDEREÇO IP: {socket.gethostbyname(socket.gethostname())}", 'i*')
    faz_log(f"ENDEREÇO MAC: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}", 'i*')

    # print CPU information
    faz_log("==== INFOS DA CPU ====", 'i*')
    # number of cores
    faz_log(f"NÚCLEOS FÍSICOS: {psutil.cpu_count(logical=False)}", 'i*')
    faz_log(f"TOTAL DE NÚCLEOS: {psutil.cpu_count(logical=True)}", 'i*')
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    faz_log(f"FREQUÊNCIA MÁXIMA: {cpufreq.max:.2f}Mhz", 'i*')
    faz_log(f"FREQUÊNCIA MÍNIMA: {cpufreq.min:.2f}Mhz", 'i*')
    faz_log(f"FREQUÊNCIA ATUAL: {cpufreq.current:.2f}Mhz", 'i*')
    # CPU usage
    faz_log("USO DA CPU POR NÚCLEO:", 'i*')
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        faz_log(f"NÚCLEO {i}: {percentage}%", 'i*')
    faz_log(f"USO TOTAL DA CPU: {psutil.cpu_percent()}%", 'i*')

    # Memory Information
    faz_log("==== INFOS DA MEMÓRIA RAM ====", 'i*')
    # get the memory details
    svmem = psutil.virtual_memory()
    faz_log(f"MEMÓRIA RAM TOTAL: {get_size(svmem.total)}", 'i*')
    faz_log(f"MEMÓRIA RAM DISPONÍVEL: {get_size(svmem.available)}", 'i*')
    faz_log(f"MEMÓRIA RAM EM USO: {get_size(svmem.used)}", 'i*')
    faz_log(f"PORCENTAGEM DE USO DA MEMÓRIA RAM: {svmem.percent}%", 'i*')

    ## Network information
    faz_log("==== INFORMAÇÕES DA INTERNET ====", 'i*')
    ## get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            faz_log(f"=== Interface: {interface_name} ===", 'i*')
            if str(address.family) == 'AddressFamily.AF_INET':
                faz_log(f"  ENDEREÇO IP: {address.address}", 'i*')
                faz_log(f"  MASCARÁ DE REDE: {address.netmask}", 'i*')
                faz_log(f"  IP DE TRANSMISSÃO: {address.broadcast}", 'i*')
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                faz_log(f"  ENDEREÇO MAC: {address.address}", 'i*')
                faz_log(f"  MASCARÁ DE REDE: {address.netmask}", 'i*')
                faz_log(f"  MAC DE TRANSMISSÃO: {address.broadcast}", 'i*')
    ##get IO statistics since boot
    net_io = psutil.net_io_counters()
    faz_log(f"TOTAL DE Bytes ENVIADOS: {get_size(net_io.bytes_sent)}", 'i*')
    faz_log(f"TOTAL DE Bytes RECEBIDOS: {get_size(net_io.bytes_recv)}", 'i*')
    
    
def limpa_logs():
    path_logs_dir = os.path.abspath(r'.\logs')
    path_logs_file = os.path.abspath(r'.\logs\botLog.log')
    
    if os.path.exists(path_logs_dir):
        try:
            os.remove(path_logs_file)
        except Exception:
            ...
    else:
        os.mkdir(path_logs_dir)


def faz_log(msg: str, level: str = 'i'):
    """Faz log na pasta padrão (./logs/botLog.log)

    Args:
        msg (str): "Mensagem de Log"
        level (str): "Niveis de Log"
        
        Levels:
            'i' or not passed = info and print

            'i*' = info log only

            'w' = warning
            
            'c*' = critical / Exception Error exc_info=True
            
            'c' = critical
            
            'e' = error
    """
    path_logs_dir = os.path.abspath(r'.\logs')
    path_logs_file = os.path.abspath(r'.\logs\botLog.log')

    if not os.path.exists(path_logs_dir):
        os.mkdir(path_logs_dir)
    else:
        ...

    if isinstance(msg, (str)):
        pass
    
    if isinstance(msg, (object)):
        msg = str(msg)    
    

    if isinstance(level, (str)):
        pass
    else:
        print('COLOQUE UMA STING NO PARAMETRO LEVEL!')

    if isinstance(msg, (str)) and isinstance(level, (str)):
        if level == 'i' or level == '' or level is None:
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO
                                )
            print(msg)
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logging.info(msg)

        if level == 'i*':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO
                                )
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logging.info(msg)

        elif level == 'w':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.WARNING
                                )
            logging.warning(msg)
            print('! ' + msg + ' !')

        elif level == 'e':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.ERROR
                                )
            logging.error(msg)
            print('!! ' + msg + ' !!')

        elif level == 'c':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.CRITICAL
                                )
            logging.critical(msg)
            print('!!! ' + msg + ' !!!')

        elif level == 'c*':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.CRITICAL
                                )
            logging.critical(msg, exc_info=True)
            print('!!! ' + msg + ' !!!')
