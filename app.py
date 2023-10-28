import re
import tkinter
from tkinter import ttk
from tkinter import *
from datetime import *
import sqlite3

'''################## CLASSE Window/ JANELA INICIAL ###################################################'''
class Window:
    db_auto = 'database/ManagerLuxury.db'# variavel para acessar o banco de dados de usuarios
    def __init__(self, root): #construtor recebe a rota
        self.janela = root #janela inicial vai receber root
        self.janela.title("Sistema de Gerenciamento de Frota Luxury Wheels")  # Adicionando um titulo a janela principal do programa
        self.janela.geometry(f"900x600+200+50")  # redimensionando o tamanho e posição da janela do programa de acordo com o tamanho da tela
        self.janela.wm_iconbitmap('recursos/icone1.ico')  # alterando o icone da janela
        self.janela['bg'] = '#B0E0E6' #alterando a cor de fundo da janela inicial
        #criando frame inicial com botão de login e exit
        self.janela.resizable(0,0) # impedir que a janela seja aumentada

        self.frame_inicial = Frame(self.janela) #Criando o frame inicial que vai receber a tela para login ou sair
        self.frame = LabelFrame(self.frame_inicial, text="Sistema de Gerenciamento de Frota Luxury Wheels", bd=8, relief="groove", font="sylfaen 15 bold", bg="#E6E6FA") #frame com login ou sair
        self.login = Button(self.frame, text="Login", font="sylfaen 15 bold", bd=5, relief="raised", bg='#B0E0E6', command=self.login) #criando botão de login que vai abrir a janela para inserir os dados de autenticação
        self.login.grid(row=0, column=0, pady=20, padx=200) #posicionando botão login
        self.cadastrar = Button(self.frame, text="Cadastrar usuário", font="sylfaen 15 bold", bd=5, relief="raised", bg='#B0E0E6', command=self.cadastrar)
        self.cadastrar.grid(row=1, column=0)
        self.exit = Button(self.frame, text="Sair", font="sylfaen 15 bold", bd=5, relief="raised", bg='#B0E0E6', command=self.exit) #criando botão de sair
        self.exit.grid(row=2, column=0, pady= 20) #posicionando botão de sair
        self.frame.grid(pady=200, padx=200) #posicionando frame
        self.frame_inicial.grid() #posicionado frame inicial

    '''###########################--JANELA CADASTRO--#################################'''
    def cadastrar(self):
        self.janela_cadastro = Toplevel()
        self.janela_cadastro.title("CADASTRAR USUARIO")  # titulo
        self.janela_cadastro.wm_iconbitmap("recursos/icone2.ico")  # mudando o icone
        self.janela_cadastro.resizable(FALSE, FALSE)
        self.janela_cadastro.geometry("450x300+400+200")  # tamanho e posição da janela
        frame_cadastro = Frame(self.janela_cadastro)
        id_usuario = Label(frame_cadastro, text="Insira seu ID:", font="sylfaen 15 bold")
        insert_id = Entry(frame_cadastro, width=45)
        nome = Label(frame_cadastro, text="Insira nome: ", font="sylfaen 15 bold")
        insert_nome = Entry(frame_cadastro, width=45)
        usuario_lb = Label(frame_cadastro, text="Insira usuário: ", font="sylfaen 15 bold") #etiqueta que mostra onde inserir o usuario
        insert_usuario = Entry(frame_cadastro, width=45)
        label_senha = Label(frame_cadastro, text="Senha: ", font="sylfaen 15 bold")  #etiqueta que mostra onde inserir a senha
        insert_senha = Entry(frame_cadastro, width=45)
        info_senha = Label(frame_cadastro, text="A senha deve conter no minimo\n8 digitos com letras e numeros.", font="sylfaen 12 italic")
        self.mensagem_cadastro=Label(frame_cadastro, text='', font="sylfaen 13 bold", fg="red")
        button_insert = Button(frame_cadastro, text="Confirmar dados", font="sylfaen 13 bold", command=lambda: self.verificar_cadastro(insert_id.get(), insert_usuario.get(), insert_senha.get(), insert_nome.get()))

        id_usuario.grid(row=0)
        insert_id.grid(row=0, column=1)
        nome.grid(row=1)
        insert_nome.grid(row=1, column=1)
        usuario_lb.grid(row=2, column=0)
        insert_usuario.grid(row=2, column=1)
        label_senha.grid(row=3, column=0)
        insert_senha.grid(row=3, column=1)
        info_senha.grid(row=4, columnspan=3)
        button_insert.grid(row=5, rowspan=3, columnspan=3)
        self.mensagem_cadastro.grid(row=8, columnspan=3)
        frame_cadastro.pack()

    def verificar_cadastro(self, id, usuario, senha, nome):
        self.mensagem_cadastro['text'] = ''
        senha_pequena = len(senha) < 8
        senha_letras = senha.isalpha()
        senha_numeros = senha.isnumeric()
        if senha_pequena:
            self.mensagem_cadastro['text'] = 'A senha deve conter no minimo 8 letras.'
            return
        elif senha_letras:
            self.mensagem_cadastro['text'] = 'A senha deve conter pelo menos um numero.'
            return
        elif senha_numeros:
            self.mensagem_cadastro['text'] = 'A senha deve conter pelo menos uma letra.'
            return
        else:
            return self.inserir_usuario(id, usuario, senha, nome)

    def inserir_usuario(self, id, usuario, senha, nome):
        query_id = "SELECT * FROM usuarios WHERE ID = ? OR usuario = ?"
        parametros1 = id, usuario
        consulta = self.db_consulta(query_id, parametros1)
        resposta = consulta.fetchall()
        print(resposta)
        try:
            if int(id) == resposta[0][0]:
                self.mensagem_cadastro['text'] = 'O colaborador com o ID informado\n já está cadastrado.'
                return
            elif usuario == resposta[0][1]:
                self.mensagem_cadastro['text'] = 'O nome de usuario informado\n já está sendo utulizado.'
            return
        except IndexError as i:
            query2 = "INSERT INTO usuarios VALUES(?,?,?,?)"
            paramentros2 = id, usuario, senha, nome
            self.db_consulta(query2, paramentros2)
            self.mensagem_cadastro['text'] = 'Usuário cadastrado com sucesso!'
            return



    '''###########################--JANELA LOGIN--#################################'''
    def login(self):
        self.janela_login = Toplevel()  # abrindo a tela de login em uma janela menor
        self.janela_login.title("LOGIN") #titulo
        self.janela_login.wm_iconbitmap("recursos/icone2.ico") #mudando o icone
        self.janela_login.resizable(FALSE, FALSE)
        self.janela_login.geometry("250x150+500+200") #tamanho e posição da janela
        frame_login = Frame(self.janela_login)
        usuario = Label(frame_login, text="Usuário: ", font="sylfaen 15 bold") #etiqueta que mostra onde inserir o usuario
        usuario.grid(row=0, sticky=W)
        senha = Label(frame_login, text="Senha: ", font="sylfaen 15 bold")  #etiqueta que mostra onde inserir a senha
        senha.grid(row=1, sticky=W)
        insert_usuario = Entry(frame_login)
        insert_usuario.grid(row=0, column=1)
        insert_senha = Entry(frame_login, show='*')
        insert_senha.grid(row=1, column=1)
        confirmar = Button(frame_login, text="acessar", bd=5, relief="raised", bg='#B0E0E6', font="sylfaen 15 bold",
                           command= lambda: self.Validacao(insert_usuario.get(), insert_senha.get()))
        self.mensagem = Label(frame_login, text='')
        self.mensagem.grid(row=2, columnspan=2)
        confirmar.grid(row=3, column=1, columnspan=2)
        insert_usuario.focus()  # para iniciar com entry usuario
        frame_login.grid(row=1)

    def exit(self): #metodo para encerrar o programa
        self.janela.destroy()

    def db_consulta(self, consulta, parametros=()): #função para acessar a base de dados e fazer consulta de usuario
        with sqlite3.connect(self.db_auto) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return resultado

    def Validacao(self, user, senha): #metodo para verificar se a senha e usuario estão corretos
        query = 'SELECT * FROM Usuarios WHERE usuario = ? and senha = ?'
        parametros = user, senha

        teste1 = self.db_consulta(query, parametros)
        resposta = teste1.fetchall()

        if len(resposta) != 0:
            self.janela_login.destroy()
            self.frame_inicial.destroy()
            menu = Menu(self.janela)
            menu.grid(sticky=E)
        else:
            self.mensagem['text'] = 'Usuario ou senhas incorreto'''


'''################################################# CLASSE MENU ###################################################'''
class Menu(Frame):
    db_auto = 'database/ManagerLuxury.db'  # variavel para acessar o banco de dados da frota
    def __init__(self, master):
        super().__init__()
        self['bd'] = 2
        self['relief'] = SOLID

        self.frame = Frame(self, bg='#ADD8E6', highlightbackground='black', highlightthickness=2, width=200, height=600)  # frame com os botões
        # criando e posicionando botões do menu
        b_veic_disp = Button(self.frame, text="VEICULOS", font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                             command=lambda: self.indicar(self.indicador_disponiveis, self.veiculos_page))
        b_veic_disp.place(x=50, y=100)
        self.indicador_disponiveis = Label(self.frame, text='', bg="#ADD8E6")
        self.indicador_disponiveis.place(x=10, y=90, width=10, height=60)
        b_legalizar = Button(self.frame, text="LEGALIZAR", font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                             command=lambda: self.indicar(self.indicador_legalizar, self.legalizar_page))
        b_legalizar.place(x=50, y=200)
        self.indicador_legalizar = Label(self.frame, text='', bg="#ADD8E6")
        self.indicador_legalizar.place(x=10, y=190, width=10, height=60)
        b_manutencao = Button(self.frame, text="MANUTENÇÃO", font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                              command=lambda: self.indicar(self.indicador_manutencao, self.manutencao_page))
        b_manutencao.place(x=50, y=300)
        self.indicador_manutencao = Label(self.frame, text='', bg="#ADD8E6")
        self.indicador_manutencao.place(x=10, y=290, width=10, height=60)
        b_sair = Button(self.frame, text="SAIR", font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                        command=lambda: self.indicar(self.indicador_sair, self.page_sair))
        b_sair.place(x=50, y=400)
        self.indicador_sair = Label(self.frame, text='', bg="#ADD8E6")
        self.indicador_sair.place(x=10, y=390, width=10, height=60)

        self.frame.pack(side=LEFT)  # posicionando

        self.frame2 = Frame(self, highlightbackground='black', highlightthickness=2, bg='#B0E0E6', width=697,
                            height=597)

        self.frame2.pack(side=RIGHT, fill=BOTH)

    '''################################################# ABA VEICULOS ###################################################'''
    def veiculos_page(self):
        veiculo = Frame(self.frame2,width=900)
        veiculos_frame = LabelFrame(veiculo, text="FROTA", font="sylfaen 16 bold", width=900)
        '''############################--- TABELA VEICULOS --- ############################3'''
        self.tabela = ttk.Treeview(veiculos_frame, columns=('ID', 'placa', 'tipo', 'categoria', 'disponivel', 'disponivel em'), height=13, show='headings')
        self.tabela.column('ID', minwidth=0, width=40)
        self.tabela.column('placa', minwidth=0,width=70)
        self.tabela.column('tipo', minwidth=0, width=60)
        self.tabela.column('categoria', minwidth=0, width=80)
        self.tabela.column('disponivel', minwidth=0, width=110)
        self.tabela.column('disponivel em', minwidth=0, width=120)
        self.tabela.heading('ID', text='ID')
        self.tabela.heading('placa', text='PLACA')
        self.tabela.heading('tipo', text='TIPO')
        self.tabela.heading('categoria', text='CATEGORIA')
        self.tabela.heading('disponivel', text='STATUS')
        self.tabela.heading('disponivel em', text='DISPONIVEL EM:', anchor='w')
        self.tabela.grid(row=0)
        self.tabela_pag_veiculos()
        veiculos_frame.pack(expand=TRUE, fill=BOTH, pady=0, padx=44)

        '''#######################---ALERTA DE FROTA---##############################'''
        frame_alerta = LabelFrame(veiculos_frame, text='Alerta de veiculos disponiveis', font="sylfaen 12 bold")
        contador_gold = 0
        contador_silver = 0
        contador_economico = 0
        self.alerta_frota1 = Label(frame_alerta, text='', font="sylfaen 12 italic")
        self.alerta_frota2 = Label(frame_alerta, text='', font="sylfaen 12 italic")
        self.alerta_frota3 = Label(frame_alerta, text='', font="sylfaen 12 italic")
        query_frota_gold = "SELECT placa FROM automoveis WHERE disponibilidade == 'disponivel' AND categoria = 'Gold'"
        consulta_frota_gold = self.db_consulta(query_frota_gold)
        for item in consulta_frota_gold:
            contador_gold += 1
        if contador_gold <= 5:
            self.alerta_frota1['text'] = f'Alerta, existem apenas {contador_gold} veiculos categoria: "Gold" disponiveis!'
            self.alerta_frota1.fg = 'red'
        else:
            self.alerta_frota1['text'] = f'há {contador_gold} veiculos categoria: "Gold" disponiveis!'
            self.alerta_frota1['fg'] = 'green'

        query_frota_silver = "SELECT placa FROM automoveis WHERE disponibilidade == 'disponivel' AND categoria = 'Silver'"
        consulta_frota_silver = self.db_consulta(query_frota_silver)
        for item in consulta_frota_silver:
            contador_silver += 1
        if contador_silver <= 5:
            self.alerta_frota2['text'] = f'Alerta, existem apenas {contador_silver} veiculos categoria: "Silver" disponiveis!'
            self.alerta_frota2['fg'] = 'red'
        else:
            self.alerta_frota2['text'] = f'há {contador_silver} veiculos categoria: "Silver" disponiveis!'
            self.alerta_frota2['fg'] = 'green'

        query_frota_econimico = "SELECT placa FROM automoveis WHERE disponibilidade == 'disponivel' AND categoria = 'Economico'"
        consulta_frota_economico = self.db_consulta(query_frota_econimico)
        for item in consulta_frota_economico:
            contador_economico += 1
        if contador_economico <= 5:
            self.alerta_frota3['text'] = f'Alerta, existem apenas {contador_economico} veiculos categoria: "Econômico" disponiveis!'
            self.alerta_frota3['fg'] = 'red'
        else:
            self.alerta_frota3['text'] = f'há {contador_economico} veiculos categoria: "Economico" disponiveis!'
            self.alerta_frota3['fg'] = 'green'

        '''#######################---BOTÃO DE PESQUISA---##############################'''
        frame_pesquisar = Frame(veiculos_frame)
        icone_pesquisa = tkinter.PhotoImage(file='recursos/magnifying_glass.png')
        self.buttom_pesquisar = Button(frame_pesquisar, text='Pesquisar\nveiculo', font="sylfaen 10 bold", image=icone_pesquisa,
                                       compound='left', background='#B0E0E6', command=self.pesquisar_veiculo)
        self.buttom_pesquisar.image = icone_pesquisa

        self.alerta_frota1.grid(row=0, column=0, sticky='w')
        self.alerta_frota2.grid(row=1, column=0, sticky='w')
        self.alerta_frota3.grid(row=2, column=0, sticky='w')
        self.buttom_pesquisar.grid(row=0, sticky='we')
        frame_alerta.grid(row=1, sticky='we')
        frame_pesquisar.grid(row=1, column=0, sticky='e', padx=10)


        '''#####################---ADICIONAR NOVO VEICULO--- #####################'''
        adicionar_veiculo = LabelFrame(veiculos_frame, text="Inserir novo veiculo", font="sylfaen 16 bold")
        self.label_placa = Label(adicionar_veiculo, text="Placa:", font="sylfaen 12 bold" )
        self.nova_placa = Entry(adicionar_veiculo)
        self.label_tipo = Label(adicionar_veiculo, text="Tipo:", font="sylfaen 12 bold" )
        self.tipo_veiculo = IntVar()
        self.opcao_carro = Radiobutton(adicionar_veiculo, text='Carro', variable=self.tipo_veiculo, value=0)
        self.opcao_moto = Radiobutton(adicionar_veiculo, text='Moto', variable=self.tipo_veiculo, value=1)
        self.label_aquisicao = Label(adicionar_veiculo, text="Data de aquisição:", font="sylfaen 12 bold" )
        self.nova_aquisicao = Entry(adicionar_veiculo)
        self.nova_aquisicao.insert(0, "DD/MM/AAAA")
        self.check_valor = IntVar()
        self.check_legalizado = Checkbutton(adicionar_veiculo, text="Veiculo legalizado", variable=self.check_valor, offvalue=0, onvalue=1, command=self.checkCheckButton)
        self.data_da_legalizacao = Label(adicionar_veiculo, text="Data da legalização:", font="sylfaen 12 bold")
        self.inserir_data_da_legalizacao = Entry(adicionar_veiculo)
        self.inserir_data_da_legalizacao.insert(0, "DD/MM/AAAA")
        self.label_categoria = Label (adicionar_veiculo, text="Categoria", font="sylfaen 12 bold")
        self.categoria = Spinbox(adicionar_veiculo, values=("Gold", "Silver", "Economico"), wrap=True)
        self.inserir_dados = Button(adicionar_veiculo, text="Confirmar", font="sylfaen 12 bold", bd=5, relief="raised", bg='#B0E0E6', command= lambda: self.mascara_inserir_veiculo(self.nova_placa.get(), self.tipo_veiculo.get(), self.nova_aquisicao.get(), self.check_valor.get(), self.inserir_data_da_legalizacao.get(), self.categoria.get()))
        self.mensagem_add = Label(adicionar_veiculo, text="", font="sylfaen 12 bold", fg="red")

        self.label_placa.grid(row=0, column=0, sticky='w')
        self.nova_placa.grid(row=0, column=1)
        self.label_tipo.grid(row=0, column=2)
        self.opcao_carro.grid(row=0, column=3)
        self.opcao_moto.grid(row=0,column=4)
        self.opcao_carro.select()
        self.label_aquisicao.grid(row=1, column=0, sticky='w')
        self.nova_aquisicao.grid(row=1, column=1, )
        self.check_legalizado.grid(row=1, column=2)
        self.data_da_legalizacao.grid(row=2, column=0, sticky='e')
        self.label_categoria.grid(row=2, column=2)
        self.categoria.grid(row=2, column=3)
        self.inserir_dados.grid(row=3, column=1, columnspan=4, sticky='e')
        self.mensagem_add.grid(row=3, column=0, columnspan=3)
        adicionar_veiculo.grid()
        veiculo.pack(expand=TRUE, fill=BOTH)

    def checkCheckButton(self):
        if self.check_valor.get() == 1:
            self.inserir_data_da_legalizacao.grid(row=2, column=1, sticky='e')
        else:
            self.inserir_data_da_legalizacao.grid_forget()
    def mascara_inserir_veiculo(self, placa, opcao, aquisicao, check, data_legalizacao, categoria):
        self.mensagem_add['text'] = ""
        placa_vazia = True if placa == '' else False
        padrao = r'\d{2}/\d{2}/\d{4}'
        padrao_data_aquisicao = re.match(padrao, aquisicao)
        if placa_vazia:
            self.mensagem_add['text'] = "Campo 'Placa' obrigatório!"
            return
        if not padrao_data_aquisicao:
            self.mensagem_add['text'] = "Data de aquisição incorreta!"
            return
        if check == 1:
            padrao_data_legalizacao = re.match(padrao, data_legalizacao)
            if not padrao_data_legalizacao:
                self.mensagem_add['text'] = "Data de legalização incorreta!"
                return
            else:
                data_legalizacao = datetime.strptime(data_legalizacao, '%d/%m/%Y')
        else:
            data_legalizacao = None
        aquisicao = datetime.strptime(aquisicao, '%d/%m/%Y')
        self.inserir_veiculo(placa, opcao, aquisicao, data_legalizacao, categoria)
        return
    def testar_placa(self, placa):
        query_placa = "SELECT placa FROM automoveis WHERE placa = ?"
        parametro_placa = [placa.upper()]
        retorno = self.db_consulta(query_placa,parametro_placa)
        if len(retorno) != 0:
            return True
        else:
            return False
    def inserir_veiculo(self, placa, opcao, aquisicao, data_legalizacao, categoria):
        disponibilidade = 'disponivel'
        utilizacoes = 0
        ultima_legalizacao = data_legalizacao
        proxima_legalizacao = None
        if data_legalizacao == None:
            dias = timedelta(days=30)
            proxima_legalizacao = aquisicao + dias
            proxima_legalizacao = proxima_legalizacao.strftime('%d/%m/%Y')
        else:
            anos = timedelta(days=1826)
            proxima_legalizacao = ultima_legalizacao + anos
            proxima_legalizacao = proxima_legalizacao.strftime('%d/%m/%Y')
            data_legalizacao = data_legalizacao.strftime('%d/%m/%Y')
            ultima_legalizacao = ultima_legalizacao.strftime('%d/%m/%Y')
        aquisicao = aquisicao.strftime('%d/%m/%Y')
        if self.testar_placa(placa) == True:
            self.mensagem_add['text'] = "Veiculo já cadastrado!"
            return
        else:
            query_inserir = 'INSERT INTO automoveis (placa, tipo, categoria, disponibilidade, utilizacoes, data_de_aquisicao, primeira_legalizacao, ultima_legalizacao, proxima_legalizacao) VALUES (?,?,?,?,?,?,?,?,?)'
            parametros_inserir = placa.upper(), opcao, categoria, disponibilidade, utilizacoes, aquisicao, data_legalizacao, ultima_legalizacao, proxima_legalizacao
            self.db_consulta(query_inserir, parametros_inserir)
            self.mensagem_add['text'] = "Veiculo inserido com sucesso!"
            self.tabela_pag_veiculos()
    def tabela_pag_veiculos(self):
        self.tabela.delete(*self.tabela.get_children())
        query = 'SELECT id_veiculo, placa, tipo, categoria, disponibilidade, disponivel_em FROM automoveis ORDER BY id_veiculo ASC'
        informacoes = self.db_consulta(query)

        for item in informacoes:
            id, placa, tipo, categoria, disponibilidade, disponivel_em = item
            nome_tipo = 'Carro' if int(tipo) == 0 else 'Moto'
            nome_disponivel_em = disponibilidade if disponivel_em == '' else disponivel_em
            self.tabela.insert('', 'end', values=(
            id, placa, nome_tipo, categoria, disponibilidade, nome_disponivel_em))

    def pesquisar_veiculo(self):
        self.janela_pesquisar = Toplevel()
        self.janela_pesquisar.title("Pesquisar Veiculo")
        self.janela_pesquisar.resizable(FALSE,FALSE)
        self.janela_pesquisar.geometry("600x150+500+200")
        self.frame_pesquisar = Frame(self.janela_pesquisar)
        self.lb_id = Label(self.frame_pesquisar, text="ID ou PLACA", font="sylfaen 10 bold" )
        self.ent_id = Entry(self.frame_pesquisar)
        self.bttm_id = Button(self.frame_pesquisar, text="OK", font="sylfaen 10 bold", command=lambda: self.povoar_tabela(self.ent_id.get()))
        self.mensagem_erro = Label(self.frame_pesquisar, text=" ", font="sylfaen 10 bold", fg='red')

        self.tabela_pesquisa = ttk.Treeview(self.frame_pesquisar, columns=('ID', 'placa', 'tipo', 'categoria', 'status',
                                                           'disponivel em', 'utilizacoes'), height=3, show='headings' )
        self.tabela_pesquisa.column('ID', minwidth=0, width=40)
        self.tabela_pesquisa.column('placa', minwidth=0,width=70)
        self.tabela_pesquisa.column('tipo', minwidth=0, width=50)
        self.tabela_pesquisa.column('categoria', minwidth=0, width=80)
        self.tabela_pesquisa.column('status', minwidth=0, width=90)
        self.tabela_pesquisa.column('disponivel em', minwidth=0, width=120)
        self.tabela_pesquisa.column('utilizacoes', minwidth=0, width=80)
        self.tabela_pesquisa.heading('ID', text='ID')
        self.tabela_pesquisa.heading('placa', text='PLACA')
        self.tabela_pesquisa.heading('tipo', text='TIPO')
        self.tabela_pesquisa.heading('categoria', text='CATEGORIA')
        self.tabela_pesquisa.heading('status', text='STATUS')
        self.tabela_pesquisa.heading('disponivel em', text='DISPONIVEL EM:')
        self.tabela_pesquisa.heading('utilizacoes', text='UTILIZACOES')
        self.lb_id.grid(row=0, column=0, padx=5, sticky='E')
        self.ent_id.grid(row=0, column=1, padx=5, sticky='WE')
        self.bttm_id.grid(row=0, column=2, padx=5, sticky='W')
        self.mensagem_erro.grid(row=2, column=0, columnspan=2)
        self.tabela_pesquisa.grid(row=3, columnspan=3)
        self.frame_pesquisar.pack()

    def povoar_tabela(self, ok):
        self.tabela_pesquisa.delete(*self.tabela_pesquisa.get_children())
        query_pesquisa = ('SELECT id_veiculo, placa, tipo, categoria, disponibilidade, disponivel_em, '
                          'utilizacoes FROM automoveis WHERE id_veiculo = ? OR placa = ?')
        if len(ok) == 0:
            self.mensagem_erro['text'] = 'Inserir informação!'
            return
        ok = ok.upper()
        id_parametro = ok, ok
        registros_db = self.db_consulta(query_pesquisa, id_parametro)
        print(registros_db)
        if registros_db == []:
            self.mensagem_erro['text'] = 'Veiculo não encontrado!'
            return
        else:
            self.mensagem_erro['text'] = ''
            for item in registros_db:
                id_veiculo, placa, tipo, categoria, disponibilidade, disponivel_em, utilizacoes = item
                nome_tipo = 'Carro' if tipo == '0' else 'Moto'
                self.tabela_pesquisa.insert('', END, values=(id_veiculo, placa, nome_tipo, categoria, disponibilidade, disponivel_em, utilizacoes))


    def legalizar_page(self):
        legalizar = Frame(self.frame2)
        frame_legalizar = LabelFrame(legalizar, text="LEGALIZAR", font="sylfaen 16 bold")
        self.tv_legalizar = ttk.Treeview(frame_legalizar, columns=('id', 'placa', 'data_de_aquisicao', 'ultima_legalizacao', 'proxima_legalizacao', 'dias_proxima_legalizacao'), height=17, show='headings')
        self.tv_legalizar.column('id', minwidth=0, width=50)
        self.tv_legalizar.column('placa', minwidth=0, width=70)
        self.tv_legalizar.column('data_de_aquisicao', minwidth=0, width=150)
        self.tv_legalizar.column('ultima_legalizacao', minwidth=0, width=150)
        self.tv_legalizar.column('proxima_legalizacao', minwidth=0, width=150)
        self.tv_legalizar.column('dias_proxima_legalizacao', minwidth=0, width=100)
        self.tv_legalizar.heading('id', text='ID')
        self.tv_legalizar.heading('placa', text='PLACA')
        self.tv_legalizar.heading('data_de_aquisicao', text='DATA DE AQUISIÇÃO')
        self.tv_legalizar.heading('ultima_legalizacao', text='ULTIMA LEGALIZAÇÃO')
        self.tv_legalizar.heading('proxima_legalizacao', text='PRÓXIMA LEGALIZAÇÃO')
        self.tv_legalizar.heading('dias_proxima_legalizacao', text='DIAS RESTANTES')
        frame_atualizar_status = LabelFrame(legalizar, text="Atualizar status", font="sylfaen 12 bold")
        self.label_id_legalizar = Label(frame_atualizar_status, text="ID do veiculo:", font="sylfaen 12")
        self.entry_id_legalizar = Entry(frame_atualizar_status)
        self.label_data_legalizar = Label(frame_atualizar_status, text="Data da legalização:", font="sylfaen 12")
        self.entry_data_legalizar = Entry(frame_atualizar_status)
        self.entry_data_legalizar.insert(0,"DD/MM/AAAA")
        self.button_confirm_legalizar = Button(frame_atualizar_status, text="confirmar")


        self.tv_legalizar.grid(row=2, column=1)
        self.tabela_legalizar()
        frame_atualizar_status.grid(row=3)
        self.label_id_legalizar.grid(row=1, column=0)
        self.entry_id_legalizar.grid(row=1, column=1)
        self.label_data_legalizar.grid(row=2, column=0)
        self.entry_data_legalizar.grid(row=2, column=1)
        self.button_confirm_legalizar.grid(row=3, column=0, columnspan=2)
        frame_legalizar.grid(row=1)
        legalizar.pack(expand=TRUE, fill=BOTH)
    def tabela_legalizar(self):
        self.tv_legalizar.delete(*self.tv_legalizar.get_children())
        data_atual = datetime.now()
        dias_proxima_legalizacao = []
        query_datas = 'SELECT proxima_legalizacao FROM automoveis'
        query_ids = 'SELECT id_veiculo FROM automoveis'
        datas_proxima_legalizacao = self.db_consulta(query_datas)
        ids_veiculos = self.db_consulta(query_ids)
        for i in datas_proxima_legalizacao:
            i = str(i)
            i = i[2:12]
            i = datetime.strptime(str(i), '%d/%m/%Y')
            dias_proxima_legalizacao.append(i - data_atual)
        for dias, id in zip(dias_proxima_legalizacao, ids_veiculos):
            dias = dias.days
            dias = 0 if int(dias) < 0 else int(dias)
            id = id[0]
            query_add_data = 'UPDATE automoveis SET dias_proxima_legalizacao = ? WHERE id_veiculo = ?'
            param = dias, id
            self.db_consulta(query_add_data, param)
        #for i in dias_proxima_legalizacao:


        query = 'SELECT id_veiculo, placa, data_de_aquisicao, ultima_legalizacao, proxima_legalizacao, dias_proxima_legalizacao FROM automoveis WHERE dias_proxima_legalizacao <= 10 ORDER BY dias_proxima_legalizacao ASC'
        informacoes = self.db_consulta(query)

        for item in informacoes:
            id, placa, data_de_aquisicao, ultima_legalizacao, proxima_legalizacao, dias_proxima_legalizacao = item
            nome_ultima_legalizacao = "Necessita legalizar" if ultima_legalizacao == None else ultima_legalizacao
            self.tv_legalizar.insert('', 'end', values=(id, placa, data_de_aquisicao, nome_ultima_legalizacao, proxima_legalizacao, dias_proxima_legalizacao))

    def db_consulta(self, consulta, parametros=()): #função para acessar a base de dados e fazer consulta
        with sqlite3.connect(self.db_auto) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            dados = resultado.fetchall()
            con.commit()
            return dados

    def manutencao_page(self):
        manutencao = Frame(self.frame2,width=900)
        frame_manutencao = LabelFrame(manutencao, text="VEICULOS EM ALERTA:", font="sylfaen 16 bold", width=800, height=10)
        self.tv_manutencao = ttk.Treeview(frame_manutencao, columns=('utilizacoes', 'placa', 'tipo', 'disponivel', 'disponivel em'), show='headings')
        self.tv_manutencao.column('utilizacoes', minwidth=0, width=100)
        self.tv_manutencao.column('placa', minwidth=0, width=70)
        self.tv_manutencao.column('tipo', minwidth=0, width=70)
        self.tv_manutencao.column('disponivel', minwidth=0, width=100)
        self.tv_manutencao.column('disponivel em', minwidth=0, width=100)
        self.tv_manutencao.heading('utilizacoes', text='nº de utilizações')
        self.tv_manutencao.heading('placa', text='Placa')
        self.tv_manutencao.heading('tipo', text='tipo')
        self.tv_manutencao.heading('disponivel', text='Disponibilidade')
        self.tv_manutencao.heading('disponivel em', text='Disponivel em:')

        self.tv_manutencao.grid()
        self.tabela_manutencao()
        ################--- ATUALIZAR MANUTENÇÃO ---#####################
        self.label_manutencao = Label(frame_manutencao, text='''Veiculos com 50 utilizações ou mais deverão ser enviados para manutenção, 
        após a regularização do veiculo o administrador deve atualizar o status na base de dados.''')
        self.mensagem_atualizar = Label(frame_manutencao, text='')
        self.manutencao_em_andamento = Button(frame_manutencao, text="Enviado para manutenção", font='sylfaen 12 bold',
                                              command=self.em_manutencao)
        self.concluir_manutencao = Button(frame_manutencao, text="Manutenção Concluida", font="sylfaen 12 bold",
                                          command= self.atualizar_manutencao)
        self.label_manutencao.grid()
        self.mensagem_atualizar.grid()
        self.manutencao_em_andamento.grid()
        self.concluir_manutencao.grid()
        frame_manutencao.pack(expand=TRUE, fill=BOTH, pady=20, padx=94)
        manutencao.pack(expand=TRUE, fill=BOTH)

    def tabela_manutencao(self):
        self.tv_manutencao.delete(*self.tv_manutencao.get_children())
        query = 'SELECT utilizacoes,placa, tipo, disponibilidade, disponivel_em FROM automoveis WHERE utilizacoes >= 10 ORDER BY utilizacoes DESC'
        informacoes = self.db_consulta(query)
        for item in informacoes:
            self.tv_manutencao.insert('', 'end', values=item)
    def atualizar_manutencao(self):
        self.mensagem_atualizar['text'] = ''
        try:
            item_selecionado = self.tv_manutencao.selection()[0]
            placa_item = self.tv_manutencao.item(item_selecionado, 'values')
            if placa_item[3] == 'em manutenção':
                query = 'UPDATE automoveis SET disponibilidade = "disponivel", utilizacoes = 0 WHERE placa = ?'
                self.db_consulta(query, (placa_item[1],))
                self.mensagem_atualizar['text'] = f'Manutenção do veiculo de placa {placa_item[1]} concluida com sucesso!'
                self.tabela_manutencao()
            elif placa_item[3] == 'disponivel':
                self.mensagem_atualizar['text'] = 'O status do veiculo precisa estar "em manutenção" antes de conclui-la.'
            else:
                self.mensagem_atualizar['text'] = 'O veiculo está em uso, não é possivel atualizar o status.'
        except IndexError as e:
            self.mensagem_atualizar['text'] = 'Por favor, selecione um produto.'
            return

    def em_manutencao(self):
        self.mensagem_atualizar['text'] = ''
        try:
            item_selecionado = self.tv_manutencao.selection()[0]
            placa_item = self.tv_manutencao.item(item_selecionado, 'values')
            if placa_item[3] == 'disponivel':
                query = 'UPDATE automoveis SET disponibilidade = "em manutenção"  WHERE placa = ?'
                self.db_consulta(query, (placa_item[1],))
                self.mensagem_atualizar['text'] = f'O satus do veiculo de placa {placa_item[1]} foi alterado para "Em andamento"!'
                self.tabela_manutencao()
            elif placa_item[3] == 'em manutenção':
                self.mensagem_atualizar['text'] = 'O veiculo ja encontra-se em manutenção.'
            else:
                self.mensagem_atualizar['text'] = 'O veiculo está em uso, não é possivel atualizar o status.'
        except IndexError as e:
            self.mensagem_atualizar['text'] = 'Por favor, selecione um produto.'
            return
    def page_sair(self):
        teste = Frame(self.frame2)
        lb = LabelFrame(teste, text="SAIR", font='sylfaen 12 bold')
        botao_sair2 = Button(lb, text="Voltar ao menu inicial", font='sylfaen 12 bold', command=self.sair)
        botao_sair2.grid()
        lb.grid(pady=265, padx=252)
        teste.pack()
    def sair(self):
        self.destroy()
        voltar = Window(root)

    def delet_pages(self):
        for item in self.frame2.winfo_children():
            item.destroy()

    def remover_indicador(self):
        self.indicador_disponiveis.config(bg='#ADD8E6')
        self.indicador_sair.config(bg='#ADD8E6')
        self.indicador_manutencao.config(bg='#ADD8E6')
        self.indicador_legalizar.config(bg='#ADD8E6')

    def indicar(self, indicador, page):
        self.remover_indicador()
        indicador.config(bg='red')
        self.delet_pages()
        page()

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.mainloop()
