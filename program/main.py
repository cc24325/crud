import pyodbc

def apresenteSe ():
    print('+-------------------------------------------------------------+')
    print('|                                                             |')
    print('| AGENDA PESSOAL DE ANIVERSÁRIOS E FORMAS DE CONTATAR PESSOAS |')
    print('|                                                             |')
    print('| Prof André Luís dos Reis Gomes de Carvalho                  |')
    print('|                                                             |')
    print('| Versão 1.0 de 12/abril/2024                                 |')
    print('|                                                             |')
    print('+-------------------------------------------------------------+')

def umTexto (solicitacao, mensagem, valido):
    digitouDireito=False
    while not digitouDireito:
        txt=input(solicitacao)

        if txt not in valido:
            print(mensagem,'- Favor redigitar...')
        else:
            digitouDireito=True

    return txt

def opcaoEscolhida (mnu):
    print ()

    opcoesValidas=[]
    posicao=0
    while posicao<len(mnu):
        print (posicao+1,') ',mnu[posicao],sep='')
        opcoesValidas.append(str(posicao+1))
        posicao+=1

    print()
    return umTexto('Qual é a sua opção? ', 'Opção inválida', opcoesValidas)

def connect() -> bool:
    
    try:
        global connection
        connection = pyodbc.connect(
            driver = "{SQL Server}", #fabricante
            server = "143.106.250.84", #maquina onde esta o banco de dados
            database = "BD24325", #banco de dados
            uid = "BD24325", #LOGIN
            pwd = "BD24325" #SENHA
        ) # xxxxx é seu RA
        return True
    except:
        return False

def esta_cadastrado (nom):
    # cursor e um objeto que permite que 
    #nosso programa executre comandos SQL
    #la no sevidor
    cursor = connection.cursor()
    
    command = f"SELECT * FROM crud.contatos WHERE nome='{nom}'"
        
    try:
        #tentar executar o comando no banco de dados
        cursor.execute(command)
        #como select não altera nada no BD, não faz sentido pensar
        #em aplicar as alterações; por isso não tem cursor.commit()
        dados_selecionados=cursor.fetchall() #fetchall da uma listona
                                             #contendo 0 ou mais listinhas;
                                             #cada listinha seria uma linha
                                             #trazida pelo select;
                                             #neste caso, dará uma listona
                                             #contendo 0 ou 1 listinha(s);
                                             #isso pq ou nao tem o nome
                                             #procurado, ou tem 1 só vez
        return [True,dados_selecionados]
    except:
        #em caso de erro ele vai retornar falso 
        return [False,[]]

def incluir ():
    digitouDireito=False
    while not digitouDireito:
        nome=input('\nNome.......: ')

        resposta=esta_cadastrado(nome)
        sucessoNoAcessoAoBD = resposta[0]
        dados_selecionados  = resposta[1]

        if not sucessoNoAcessoAoBD or dados_selecionados!=[]:
            print ('Pessoa já existente - Favor redigitar...')
        else:
            digitouDireito=True
            
    aniversario=input('Aniversário: ')
    endereco   =input('Endereço...: ')
    telefone   =input('Telefone...: ')
    celular    =input('Celular....: ')
    email      =input('e-mail.....: ')
    
    try:
        # cursor e um objeto que permite que 
        #nosso programa executre comandos SQL
        #la no sevidor
        cursor = connection.cursor()

        command= "INSERT INTO crud.contatos "+\
                 "(Nome,Aniversario,endereco,telefone,celular,email) "+\
                 "VALUES"+\
                f"('{nome}','{aniversario}','{endereco}','{telefone}','{celular}','{email}')"

        cursor.execute(command)
        cursor.commit()
        print("Cadastro realizado com sucesso!")
    except:
        print("Cadastro mal sucedido!")


def procurar ():
    digitouDireito = False
    while not digitouDireito:
        nome = input('\nNome.......: ')
        resposta = esta_cadastrado(nome)
        sucessoNoAcessoAoBD = resposta[0]
        dados_selecionados = resposta[1]
        
        if sucessoNoAcessoAoBD:
            print('Encontrado/a')
            print('Esses são os dados disponiveis:\n')
            print("Nome...",dados_selecionados[0][1])
            print("Aniversario...",dados_selecionados[0][2])
            print("Endereço...",dados_selecionados[0][3])
            print("Telefone...",dados_selecionados[0][4])
            print("Celular...",dados_selecionados[0][5])
            print("Email...",dados_selecionados[0][6])
                
            return
            
    else:
        try:
            while True:
                print('Pessoa Não cadastrada')
                print(''' 
                    1 - Incluir cadastro
                    2 - Reescrever nome
                    3 - Voltar ao menu ''')
                opcao = int(input("\nO Que Deseja Realizar: "))
                if opcao == 1:
                    incluir()
                    break
                elif opcao == 3:
                    break         
        except ValueError:
            print("Digite apenas opções de 1 a 3! ")

def atualizar (dados_selecionados):
    

    print("Contatos Cadastrados: \n")
    
    if not dados_selecionados:
        print("Nenhum contato cadastrado no sistema!")
        return
    
    for contato in dados_selecionados:
        print(contato[0])
    
    atualizacao = ['Aniversário', 'Endereço', 'Telefone', 'Celular', 'e-mail', 'Finalizar alterações']
    
    while True:
        digitouDireito = False
        while not digitouDireito:
            nome = input('\nDigite o nome de qual cadastro será atualizado: ')
            resposta = esta_cadastrado(nome, dados_selecionados)
            achou = resposta[0]
            posicao = resposta[1]
            
            if not achou:
                print("Pessoa inexistente! Por favor, digite novamente!")
            else:
                digitouDireito = True
            
        opcao = 7
        while opcao != 6:
            opcao = opcaoEscolhida(atualizacao)
            if opcao == '1':
                aniversario = input("Aniversário: ")
                dados_selecionados[posicao][1] = aniversario
            elif opcao == '2':
                endereco = input("Endereço: ")
                dados_selecionados[posicao][2] = endereco
            elif opcao == '3':
                telefone = input("Telefone: ")
                dados_selecionados[posicao][3] = telefone
            elif opcao == '4':
                celular = input("Celular: ")
                dados_selecionados[posicao][4] = celular
            elif opcao == '5':
                email = input("e-mail: ")
                dados_selecionados[posicao][5] = email
            elif opcao == '6':
                print("Atualizações realizadas com sucesso!")
                break
        
        # Verifica se houve alguma modificação nos dados
        if opcao != '6':
            try:
                cursor = connection.cursor()
                command = "UPDATE crud.contatos SET Aniversario=?, endereco=?, telefone=?, celular=?, email=? WHERE Nome=?"
                cursor.execute(command, (aniversario, endereco, telefone, celular, email, nome))

                connection.commit()
                print("Atualização realizada com sucesso!")
            except Exception as e:
                print("Erro durante a atualização:", e)
                connection.rollback()  # Rollback changes if an error occurs
            finally:
                cursor.close()
            return

                    
def listar (dados_selecionados):
    if dados_selecionados :
        print("Esses são todos os dados encontrados Disponiveis:")
        for i in range(len(dados_selecionados)):
            print(f"Nome...{dados_selecionados[i][0]}")
            print(f"Anivesario...{dados_selecionados[i][1]}")
            print(f"Endereço...{dados_selecionados[i][2]}")
            print(f"Telefone...{dados_selecionados[i][3]}")
            print(f"Celular...{dados_selecionados[i][4]}")
            print(f"e-mail...{dados_selecionados[i][5]}")
            print()

def excluir ():
    digitouDireito=False
    while not digitouDireito:
        nome=input('\nNome.......: ')

        resposta=esta_cadastrado(nome)
        sucessoNoAcessoAoBD = resposta[0]
        dados_selecionados  = resposta[1]

        if not sucessoNoAcessoAoBD:
            print("Sem conexão com o BD!")
        elif dados_selecionados==[]:
            print ('Pessoa inexistente - Favor redigitar...')
        else:
            digitouDireito=True
            
    print('Aniversario:',dados_selecionados[0][2])
    print('Endereco...:',dados_selecionados[0][3])
    print('Telefone...:',dados_selecionados[0][4])
    print('Celular....:',dados_selecionados[0][5])
    print('e-mail.....:',dados_selecionados[0][6])
    
    resposta=umTexto('Deseja realmente excluir? ','Você deve digitar S ou N',['s','S','n','N'])
    
    if resposta in ['s','S']:
        try:
            #cursor e um objeto que permite que 
            #nosso programa executre comandos SQL
            #la no sevidor
            cursor = connection.cursor()

            command= "DELETE FROM crud.contatos "+\
                    f"WHERE nome='{nome}'"

            cursor.execute(command)
            cursor.commit()
            print('Remoção realizada com sucesso!')
        except:
            print("Remoção mal sucedida!")
    else:
        print('Remoção não realizada!')


# daqui para cima, definimos subprogramas (ou módulos, é a mesma coisa)
# daqui para baixo, implementamos o programa (nosso CRUD, C=create(inserir), R=read(recuperar), U=update(atualizar), D=delete(remover,apagar)

apresenteSe()

sucessoNoAcessoAoBD = connect()
if not sucessoNoAcessoAoBD:
    print("Falha ao conectar-se ao SQL Severver")
    exit() # encerra o programa

menu=['Incluir Contato',\
      'Procurar Contato',\
      'Atualizar Contato',\
      'Listar Contatos',\
      'Excluir Contato',\
      'Sair do Programa']

opcao=666
while opcao!=6:
    opcao = int(opcaoEscolhida(menu))

    if opcao==1:
        incluir()
    elif opcao==2:
        procurar()
    elif opcao==3:
        atualizar()
    elif opcao==4:
        listar()
    elif opcao==5:
        excluir()
        
connection.close()        
print('OBRIGADO POR USAR ESTE PROGRAMA!')
