
def get_files(path):
    """
    Obtém todos os arquivos no diretório pesquisado
    :param path: um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
    """
    return [ item for item in path.iterdir() if item.is_file()]

def find_by_name(path, value):
    """
        Verifica se o arquivo com o nome escolhido existe
        :param path: um objeto Path() que representa o diretório
        :param value: uma string com o nome do arquivo pesquisado
        :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
        """
    return [file for file in get_files(path) if file.stem == value]

def find_by_ext(path, value):
    """
            Verifica se os arquivso com a extensão escolhida existe
            :param path: um objeto Path() que representa o diretório
            :param value: uma string com a extensão pesquisada
            :return: uma lista de objetos Path() em que cada elemento será um arquivo que existe em `path`
            """
    return [file for file in get_files(path) if file.suffix == value]

def find_by_modified(path, value):
    pass

