from ..station import AbrirArquivo

def generate_tree(path_root,tree_dict,text_dict,target=''):
    """Gera Uma Árvore De Arquivos e Escrever Em Cada Arquivo.

    tree_dict = {
    'root':{
        "database":['__init__.py'],
        "blueprints":['__init__.py'],
        "templates":['base.html']}
    }
    text_dict = {
        "/root/database":'databse',
        "/root/blueprints":'blueprints',
        "/root/templates":'templates'
    }
    """
    for key,value in tree_dict.items():
        AbrirArquivo(path_root+'/'+key,True)
        if type(value) == dict:
            generate_tree(path_root+'/'+key,value,text_dict,target+'/'+key)
        elif type(value) == list:
            for file in value:
                print(path_root+'/'+key+'/'+file)
                if type(text_dict[target+'/'+key]) == str:
                    with AbrirArquivo(path_root+'/'+key+'/'+file,'w',True) as filer:
                        filer.write(text_dict[target+'/'+key])
                else:
                    with AbrirArquivo(path_root+'/'+key+'/'+file,'wb',True) as filer:
                        filer.write(text_dict[target+'/'+key])