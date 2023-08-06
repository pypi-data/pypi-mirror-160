def deletar_tabela_sqlite(cur, table_name) -> None:
    """Deleta uma tabela específica pelo nome dela

    Args:
        cur (_type_): Cursor SQLite3
        table_name (str): Nome da tabela a ser deletada
    """
    cur.execute(f'''DROP TABLE {table_name}''')
    
def select_all_from_table(cur, table):
    """SELECT * FROM table

    Args:
        cur (Cursor): Cursor do SQLite
        table (Tabela): Tabela do banco de dados
    """
    
    cur.execute('SELECT * FROM ?', (table))
    
def cria_tabela_3_cols(cursor, table_name, cols: dict, primary_key=True, if_not_exists=True) -> None:
    """Cria uma tabela de 3 colnas

    Args:
        cursor (_type_): Cursor SQLite3
        table_name (str): Nome da tabela a ser criada
        cols (dict): colunas a ser criadas
        primary_key (bool, optional): Deseja que a tabela seja uma Primary Key. Defaults to True.
        if_not_exists (bool, optional): Cria a tabela somente se não existir. Defaults to True.

    Raises:
        KeyError: _description_
    """
    # Cria uma tabela de 3 colunas (passar somente 3 keys)
    # nao precisa mandar a coluna id por padrao ela é id INTEGER PRIMARY KEY
    #  { "COLUNA" : "TIPO DECLARATION AND NOT EXIST..." }
    
    keys = [key for key in cols]  # desempacota dodos as keys do dict
    values = [*cols.values()]  # Desempacota todos os valores do dict
    
    if len(values) == 3 and len(keys) == 3:        
        if primary_key and if_not_exists:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {keys[0]} {values[0]}, {keys[1]} {values[1]}, {keys[2]} {values[2]})''')
            print('Tabela com coluna id do tipo primary key criada')
        elif if_not_exists:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} ({keys[0]} {values[0]}, {keys[1]} {values[1]}, {keys[2]} {values[2]})''')
            print('Tabela criada')
        elif not if_not_exists:
            cursor.execute(f'''CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, {keys[0]} {values[0]}, {keys[1]} {values[1]}, {keys[2]} {values[2]})''')
            print('Tabela criada')
        elif not primary_key and not if_not_exists:
            cursor.execute(f'''CREATE TABLE {table_name} ({keys[0]} {values[0]}, {keys[1]} {values[1]}, {keys[2]} {values[2]})''')
            print('Tabela criada')
    else:
        raise KeyError(f'Verifique se as chavers estão iguais, pois só há {len(keys)} chaves')