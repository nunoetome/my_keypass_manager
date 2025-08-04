from pykeepass import PyKeePass
import os

def renomear_campos():
    # Acede ao ficheiro .kdbx
    # Caminho absoluto para o ficheiro Main.kdbx na mesma pasta do script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kdbx_path = os.path.join(base_dir, 'Main.kdbx')

    senha = 'asdasdsad'  # ou keyfile, se usares
    string_to_change_before = '_template'  # string a ser substituída
    string_to_change_after= '_t'  # string nova

    # lista de custom_propertys a serem ignoradas
    ignore_list = [
        '_etm_template'
        ]
    #lista de substrings a serem ignoradas
    ignore_substrings = [
        'etm_template',
        'etm_t'
        ]
    
    # Verifica se o ficheiro existe
    if not os.path.exists(kdbx_path):
        print(f'Ficheiro {kdbx_path} não encontrado.')
        return
    kp = PyKeePass(kdbx_path, password=senha)

    # Verifica se o ficheiro foi carregado corretamente
    if kp is None:
        print('Erro ao carregar o ficheiro .kdbx. Verifique a senha ou o caminho.')
        return
    print(f'Ficheiro {kdbx_path} carregado com sucesso.')


    modificados = 0

    # Itera sobre todas as entradas do KeePass
    # Se quiseres filtrar por grupo, podes usar kp.find_groups(name='nome_do_grupo')
    # ou kp.find_entries(title='nome_da_entrada') para entradas específicas
    # Aqui, iteramos por todas as entradas
    for entry in kp.entries:
        # Copia da dict original para iterar com segurança
        for custom_property in list(entry.custom_properties.keys()):
            if string_to_change_before in custom_property:
                new_key = custom_property.replace(string_to_change_before, string_to_change_after)
                value = entry.get_custom_property(custom_property)

                value = value if value is not None else ''  # Garante que o valor não é None

                # Verifica se a nova key já existe
                if entry.get_custom_property(new_key) is not None:
                    print(f'\n ⚠️ Atenção: A chave {new_key} já existe. Ignorando renomeação de {custom_property}.')
                    continue

                # Cria nova key com o mesmo valor
                entry.set_custom_property(new_key, value)

                # Apaga a antiga
                entry.delete_custom_property(custom_property)

                print(f'\nRenomeado: {custom_property} → {new_key}')
                modificados += 1

    # Salvar no mesmo ficheiro ou outro, se quiser backup
    kp.save()  # sobrescreve
    #kp.save('novo_arquivo.kdbx')  # para salvar como novo

    print(f'\n✅ Campos renomeados: {modificados}')



if __name__ == '__main__':
    renomear_campos()
