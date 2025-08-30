import datetime
import re
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import PhotoImage
from datetime import *
import sqlite3
import os

'''################## CLASSE Window/ JANELA INICIAL ###################################################'''
class Window:
    db_auto = 'database/ManagerLuxury.db'# variavel para acessar o banco de dados
    def __init__(self, root): #construtor recebe a rota
        self.janela = root #janela inicial vai receber root
        self.janela.title("Sistema de Gerenciamento de Frota Luxury Wheels")  # Adicionando um titulo a janela principal do programa
        self.janela.geometry(f"900x600+200+50")  # redimensionando o tamanho e posição da janela do programa de acordo com o tamanho da tela
        caminho_icone = os.path.join(os.path.dirname(__file__), "recursos", "icone1.png")
        icone = PhotoImage(file=caminho_icone)
        self.janela.iconphoto(False, icone)  # alterando o icone da janela
        self.janela['bg'] = '#B0E0E6' #alterando a cor de fundo da janela inicial
        #criando frame inicial com botão de login e exit
        self.janela.resizable(0,0) # impedir que a janela seja aumentada

        self.frame_inicial = Frame(self.janela) #Criando o frame inicial que vai receber a tela para login ou sair
        self.frame = LabelFrame(self.frame_inicial, text="Sistema de Gerenciamento de Frota Luxury Wheels", bd=8,
                                relief="groove", font="sylfaen 15 bold", bg="#E6E6FA") #frame com login ou sair
        self.login = Button(self.frame, text="Login", cursor='hand2', font="sylfaen 15 bold", bd=5, relief="raised",
                            bg='#B0E0E6', command=self.login) #criando botão de login que vai abrir a janela para inserir os dados de autenticação
        self.login.grid(row=0, column=0, pady=20, padx=200) #posicionando botão login
        self.cadastrar = Button(self.frame, text="Cadastrar usuário", cursor='hand2', font="sylfaen 15 bold",
                                bd=5, relief="raised", bg='#B0E0E6', command=self.cadastrar)
        self.cadastrar.grid(row=1, column=0)
        self.exit = Button(self.frame, text="Sair", cursor='hand2', font="sylfaen 15 bold", bd=5, relief="raised",
                           bg='#B0E0E6', command=self.exit) #criando botão de sair
        self.exit.grid(row=2, column=0, pady= 20) #posicionando botão de sair
        self.frame.grid(pady=200, padx=200) #posicionando frame
        self.frame_inicial.grid() #posicionado frame inicial

    '''###########################--JANELA CADASTRO--#################################'''
    def cadastrar(self):
        self.janela_cadastro = Toplevel()
        self.janela_cadastro.title("CADASTRAR USUARIO")  # titulo
        icon2 = PhotoImage(file="recursos/icone2.png")
        self.janela_cadastro.iconphoto(False, icon2)  # mudando o icone
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
        button_insert = Button(frame_cadastro, text="Confirmar dados", cursor='hand2', font="sylfaen 13 bold",
                               command=lambda: self.verificar_cadastro(insert_id.get(), insert_usuario.get(), insert_senha.get(), insert_nome.get()))

        id_usuario.grid(row=0)      ######### Posicionando os widgets na frame.
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
        self.mensagem_cadastro['text'] = ''     #Limpando a mensagem
        senha_pequena = len(senha) < 8  #testando se a senha é menor que oito digitos
        senha_letras = senha.isalpha() #testando se a senha não tem numeros
        senha_numeros = senha.isnumeric() #testando se a senha não tem letras
        if senha_pequena:       #fazendo os testes e retornando erro.
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
            # se tudo estiver de acordo é chamada a função de inserir_usuario

    def inserir_usuario(self, id, usuario, senha, nome):
        query_id = "SELECT * FROM usuarios WHERE ID = ? OR usuario = ?"
        parametros1 = id, usuario
        consulta = self.db_consulta(query_id, parametros1)
        resposta = consulta.fetchall()
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
        icon3 = PhotoImage(file="recursos/icone2.png")
        self.janela_login.iconphoto(False, icon3) #mudando o icone
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
        confirmar = Button(frame_login, text="acessar", bd=5, cursor='hand2', relief="raised", bg='#B0E0E6', font="sylfaen 15 bold",
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
        self['bd'] = 2 #defininado o tamanho da borda
        self['relief'] = SOLID #definindo o tipo

        # frame que vai estar os botões e os indicadores
        self.frame = Frame(self, bg='#ADD8E6', highlightbackground='black', highlightthickness=2, width=200, height=600)

        # criando os botões para as abas e seus respectivos indicadores!
        b_veic_disp = Button(self.frame, text="VEICULOS", cursor='hand2', font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                             command=lambda: self.indicar(self.indicador_disponiveis, self.veiculos_page))
        self.indicador_disponiveis = Label(self.frame, text='', bg="#ADD8E6")
        b_legalizar = Button(self.frame, text="LEGALIZAR", cursor='hand2', font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                             command=lambda: self.indicar(self.indicador_legalizar, self.legalizar_page))
        self.indicador_legalizar = Label(self.frame, text='', bg="#ADD8E6")
        b_manutencao = Button(self.frame, text="MANUTENÇÃO", cursor='hand2', font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                              command=lambda: self.indicar(self.indicador_manutencao, self.manutencao_page))
        self.indicador_manutencao = Label(self.frame, text='', bg="#ADD8E6")
        b_sair = Button(self.frame, text="SAIR", cursor='hand2', font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                        command=lambda: self.indicar(self.indicador_sair, self.page_sair))
        self.indicador_sair = Label(self.frame, text='', bg="#ADD8E6")

        self.frame2 = Frame(self, highlightbackground='black', highlightthickness=2, bg='#B0E0E6', width=697,
                            height=597)

        # Posicionando os botões, indicadores e as frames
        b_veic_disp.place(x=50, y=100)  #
        self.indicador_disponiveis.place(x=10, y=90, width=10, height=60)
        b_legalizar.place(x=50, y=200)
        self.indicador_legalizar.place(x=10, y=190, width=10, height=60)
        b_manutencao.place(x=50, y=300)
        self.indicador_manutencao.place(x=10, y=290, width=10, height=60)
        b_sair.place(x=50, y=400)
        self.indicador_sair.place(x=10, y=390, width=10, height=60)
        self.frame.pack(side=LEFT)
        self.frame2.pack(side=RIGHT, fill=BOTH)

    def delet_pages(self):
        #DELETAR A FRAME ATUAL PARA POSICIONAR A NOVA FRAME QUE FOR CLICADA
        for item in self.frame2.winfo_children():
            item.destroy()

    def remover_indicador(self):
        #TIRAR A MARCAÇÃO DOS INDICADORE (ALTERAR A COR)
        self.indicador_disponiveis.config(bg='#ADD8E6')
        self.indicador_sair.config(bg='#ADD8E6')
        self.indicador_manutencao.config(bg='#ADD8E6')
        self.indicador_legalizar.config(bg='#ADD8E6')

    def indicar(self, indicador, page):
        #MOTRAR O INDICADOR QUE FOI CLICADO, DELETAR A FRAME ATUAL E INSERIR OS DADOS DA FRAME INDICADA.
        self.remover_indicador()
        indicador.config(bg='red')
        self.delet_pages()
        page()

    # ABA PARA MOSTRAR OS DADOS DOS VEICULOS, ALERTAR A QUANTIDADE DE VEICULOS DISPONIVEIS, INSERIR E PESQUISAR.
    def veiculos_page(self):
        veiculo = Frame(self.frame2,width=900)
        veiculos_frame = LabelFrame(veiculo, text="FROTA", font="sylfaen 16 bold", width=900)

        #--- CRIANDO A TABELA DA ABA VEICULOS --- #
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

        #---FRAME QUE VAI HOSPEDAR O ALERTA DE FROTA DE ACORDO COM A CATEGORIA---#
        self.frame_alerta = LabelFrame(veiculos_frame, text='Alerta de veiculos disponiveis', font="sylfaen 12 bold")

        #CRIANDO AS FRAMES QUE VÃO RECEBER A QUANTIDADE DE VEICULOS DISPONIVEIS
        self.alerta_frota1 = Label(self.frame_alerta, text='', font="sylfaen 12 italic")
        self.alerta_frota2 = Label(self.frame_alerta, text='', font="sylfaen 12 italic")
        self.alerta_frota3 = Label(self.frame_alerta, text='', font="sylfaen 12 italic")
        #FUNÇÃO PARA VERIFICAR A QUANTIDADE DE VEICULOS DISPONIVEIS
        self.alerta()

       #---INSERINDO FUNÇÃO DE BOTÃO DE PESQUISA--#
        frame_pesquisar = Frame(veiculos_frame)
        icone_pesquisa = tkinter.PhotoImage(file='recursos/magnifying_glass.png')
        self.buttom_pesquisar = Button(frame_pesquisar, cursor='hand2', text='Pesquisar\nveiculo', font="sylfaen 10 bold", image=icone_pesquisa,
                                       compound='left', background='#B0E0E6', command=self.pesquisar_veiculo)
        self.buttom_pesquisar.image = icone_pesquisa

        #POSICIONANDO USANDO GRID
        self.alerta_frota1.grid(row=0, column=0, sticky='w')
        self.alerta_frota2.grid(row=1, column=0, sticky='w')
        self.alerta_frota3.grid(row=2, column=0, sticky='w')
        self.buttom_pesquisar.grid(row=0, sticky='we')
        self.frame_alerta.grid(row=1, sticky='we')
        frame_pesquisar.grid(row=1, column=0, sticky='e', padx=10)


        '''#####################---ADICIONAR NOVO VEICULO--- #####################'''

        #CRIANDO LAYOUT QUE VAI RECEBER AS INFORMAÇÕES PARA INSERIR VEICULO
        adicionar_veiculo = LabelFrame(veiculos_frame, text="Inserir novo veiculo", font="sylfaen 16 bold")
        self.label_placa = Label(adicionar_veiculo, text="Placa:", font="sylfaen 12 bold" )
        self.nova_placa = Entry(adicionar_veiculo)
        self.label_tipo = Label(adicionar_veiculo, text="Tipo:", font="sylfaen 12 bold" )
        self.tipo_veiculo = IntVar()
        self.opcao_carro = Radiobutton(adicionar_veiculo, text='Carro', variable=self.tipo_veiculo, value=0)
        self.opcao_moto = Radiobutton(adicionar_veiculo, text='Moto', variable=self.tipo_veiculo, value=1)
        self.label_aquisicao = Label(adicionar_veiculo, text="Data de aquisição:", font="sylfaen 12 bold" )
        self.nova_aquisicao = Entry(adicionar_veiculo)
        self.nova_aquisicao.insert(0, "DD/MM/AAAA") #FUNÇÃO INSERT PARA TER COMO DEFAULT A STRING 'DD/MM/AAAA' NA ENTRY DE DATA
        self.check_valor = IntVar()
        self.check_legalizado = Checkbutton(adicionar_veiculo, text="Veiculo legalizado", variable=self.check_valor, offvalue=0, onvalue=1, command=self.checkCheckButton)
        self.checkb_valor = IntVar()
        self.check_data_atual = Checkbutton(adicionar_veiculo, text="Data atual", variable=self.checkb_valor,
                                            offvalue=0, onvalue=1, command=lambda: self.data_atual_adicionar(self.checkb_valor.get()))
        self.data_da_legalizacao = Label(adicionar_veiculo, text="Data da legalização:", font="sylfaen 12 bold")
        self.inserir_data_da_legalizacao = Entry(adicionar_veiculo)
        self.inserir_data_da_legalizacao.insert(0, "DD/MM/AAAA")
        self.label_categoria = Label (adicionar_veiculo, text="Categoria", font="sylfaen 12 bold")
        self.categoria = Spinbox(adicionar_veiculo, values=("Gold", "Silver", "Economico"), wrap=True)
        self.inserir_dados = Button(adicionar_veiculo, text="Confirmar", cursor='hand2', font="sylfaen 12 bold", bd=5,
                                    relief="raised", bg='#B0E0E6', command= lambda: self.mascara_inserir_veiculo(self.nova_placa.get(), self.tipo_veiculo.get(), self.nova_aquisicao.get(), self.check_valor.get(), self.inserir_data_da_legalizacao.get(), self.categoria.get()))
        self.mensagem_add = Label(adicionar_veiculo, text="", font="sylfaen 12 bold", fg="red")

        #POSICIONANDO WIDGETS NA FRAME
        self.label_placa.grid(row=0, column=0, sticky='w')
        self.nova_placa.grid(row=0, column=1)
        self.label_tipo.grid(row=0, column=2)
        self.opcao_carro.grid(row=0, column=3)
        self.opcao_moto.grid(row=0,column=4)
        self.opcao_carro.select()
        self.label_aquisicao.grid(row=1, column=0, sticky='w')
        self.nova_aquisicao.grid(row=1, column=1, )
        self.check_legalizado.grid(row=1, column=2)
        self.check_data_atual.grid(row=1, column=3)
        self.data_da_legalizacao.grid(row=2, column=0, sticky='e')
        self.label_categoria.grid(row=2, column=2)
        self.categoria.grid(row=2, column=3)
        self.inserir_dados.grid(row=3, column=1, columnspan=4, sticky='e')
        self.mensagem_add.grid(row=3, column=0, columnspan=3)
        adicionar_veiculo.grid()
        veiculo.pack(expand=TRUE, fill=BOTH)


    def db_consulta(self, consulta, parametros=()):
        #PRINCIPAL FUNÇÃO PARA FAZER CONSULTA NA BASE DE DADOS
        with sqlite3.connect(self.db_auto) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            dados = resultado.fetchall()
            con.commit()
            return dados
    def data_atual_adicionar(self,valor):
        #Função para inserir a data de hoje caso seja marcado a opção em adicionar veiculo
        hoje = datetime.today()
        hoje = hoje.strftime("%d/%m/%Y")
        if valor == 1:
            self.nova_aquisicao.delete(0,11)
            self.nova_aquisicao.insert(0,hoje)
        if valor == 0:
            self.nova_aquisicao.delete(0,11)
            self.nova_aquisicao.insert(0,"DD/MM/AAAA")

    def alerta(self):
        #FUNÇÃO PARA LISTAR TODOS VEICULOS DISPONIVEIS POR CATEGORIA
        # CONTADORES DE CADA CATEGORIA DE VEICULO
        contador_gold = 0
        contador_silver = 0
        contador_economico = 0

        # QUERY PARA VERIFICAR TODOS OS VEICULOS DISPONIVEIS
        query_frota = "SELECT placa, categoria FROM automoveis WHERE disponibilidade == 'disponivel'"
        consulta_frota = self.db_consulta(query_frota)
        for item in consulta_frota:
            if item[1] == "Gold":
                contador_gold += 1
                if contador_gold <= 5:
                    self.alerta_frota1[
                        'text'] = f'Alerta, existem apenas {contador_gold} veiculos categoria: "Gold" disponiveis!'
                    self.alerta_frota1.fg = 'red'
                else:
                    self.alerta_frota1['text'] = f'há {contador_gold} veiculos categoria: "Gold" disponiveis!'
                    self.alerta_frota1['fg'] = 'green'
            if item[1] == "Silver":
                contador_silver += 1
                if contador_silver <= 5:
                    self.alerta_frota2[
                        'text'] = f'Alerta, existem apenas {contador_silver} veiculos categoria: "Silver" disponiveis!'
                    self.alerta_frota2['fg'] = 'red'
                else:
                    self.alerta_frota2['text'] = f'há {contador_silver} veiculos categoria: "Silver" disponiveis!'
                    self.alerta_frota2['fg'] = 'green'
            if item[1] == "Economico":
                contador_economico += 1
                if contador_economico <= 5:
                    self.alerta_frota3['text'] = f'Alerta, existem apenas {contador_economico} veiculos categoria: "Econômico" disponiveis!'
                    self.alerta_frota3['fg'] = 'red'
                else:
                    self.alerta_frota3['text'] = f'há {contador_economico} veiculos categoria: "Economico" disponiveis!'
                    self.alerta_frota3['fg'] = 'green'
    def checkCheckButton(self):
        #FUNÇÃO PARA MOSTRAR A ENTRY 'INSERIR DATA' CASO A OPÇÃO DE 'JÁ LEGALIZADO' ESTEJA MARCADO
        if self.check_valor.get() == 1:
            self.inserir_data_da_legalizacao.grid(row=2, column=1, sticky='e')
        else:
            self.inserir_data_da_legalizacao.grid_forget()
    def mascara_inserir_veiculo(self, placa, opcao, aquisicao, check, data_legalizacao, categoria):

        #FUNÇÃO PARA FILTRAR OS DADOS INSERIDOS PARA ADICIONAR UM VEICULO NA FROTA
        self.mensagem_add['text'] = "" #limpar a mensagem com erros
        placa_vazia = True if placa == '' else False #teste logico para saber se o campo placa esta vazio
        padrao = r'\d{2}/\d{2}/\d{4}' #usando a biblioteca regex 'regular expressions' para verificar o formato da data
        padrao_data_aquisicao = re.match(padrao, aquisicao)
        if placa_vazia: #teste para verificar o campo placa
            self.mensagem_add['text'] = "Campo 'Placa' obrigatório!"
            return
        if self.testar_placa(placa) == True: #teste para verificar se a placa ja esta cadastrada
            self.mensagem_add['text'] = "Veiculo já cadastrado!"
            return
        if not padrao_data_aquisicao: #teste para verificar o formato da data de aquisicao
            self.mensagem_add['text'] = "Data de aquisição incorreta!"
            return
        if check == 1: #teste para verificar o formato da data de legalização caso o checkbox esteja marcado
            padrao_data_legalizacao = re.match(padrao, data_legalizacao)
            if not padrao_data_legalizacao:
                self.mensagem_add['text'] = "Data de legalização inválida!"
                return
            else:
                try:
                    data_legalizacao = datetime.strptime(data_legalizacao, '%d/%m/%Y')
                except ValueError as e:
                    self.mensagem_add['text'] = "Data de legalização inválida!"
                    return
        else:
            data_legalizacao = None #se o checkbox estiver desmarcado a data de legalização não ira receber um valor
        try:
            aquisicao = datetime.strptime(aquisicao, '%d/%m/%Y')
        except ValueError as e:
            self.mensagem_add['text'] = "Data de legalização inválida!"
            return
        if categoria != 'Gold' and categoria != 'Silver' and categoria != 'Economico':
            #testando se a spinbox está com o valor correto, epenas 'Gold, Silver e Economico' são válidos.
            self.mensagem_add['text'] = "Categoria inválida!"
            return
        self.inserir_veiculo(placa, opcao, aquisicao, data_legalizacao, categoria)
        #se tudo estiver correto é chamada a função para inserir o veiculo
        return
    def testar_placa(self, placa):
        #FUNÇÃO PARA VERIFICAR SE A PLACA DO VEICULO A SER ADICIONADO JÁ EXISTE
        query_placa = "SELECT placa FROM automoveis WHERE placa = ?"
        parametro_placa = [placa.upper()]
        retorno = self.db_consulta(query_placa,parametro_placa)
        if len(retorno) != 0:
            return True
        else:
            return False
    def inserir_veiculo(self, placa, opcao, aquisicao, data_legalizacao, categoria):
        #FUNÇÃO PARA INSERIR O VEICULO NA BASE DE DADOS
        disponibilidade = 'disponivel' #O novo veiculo sempre estará disponivel assim que adicionado
        utilizacoes = 0 #O novo veiculo estará com zero utilizações por default
        ultima_legalizacao = data_legalizacao #a ultima legalizacao receberá o mesmo valor da data de legalização
        proxima_legalizacao = None #os proximos teste logicos vão dizer se a proxima legalização será dentro de 30
        # dias se for a primeira legalização ou 5 anos para as próximas.
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
        ultima_manutencao = None #Novos veiculos não terão valor na de ultima manutenção
        proxima_manutencao = aquisicao + timedelta(days=365) #A proxima manutenção deverá ser a partir de um ano após
                                                            # a aquisição do veiculo
        proxima_manutencao = proxima_manutencao.strftime('%d/%m/%Y') #alterando datas pro formato string antes de inserir na base de dados
        aquisicao = aquisicao.strftime('%d/%m/%Y') #alterando datas pro formato string antes de inserir na base de dados
        query_inserir = ('INSERT INTO automoveis (placa, tipo, categoria, disponibilidade, utilizacoes, data_de_aquisicao, '
                         'primeira_legalizacao, ultima_legalizacao, proxima_legalizacao, ultima_manutencao, '
                         'proxima_manutencao) VALUES (?,?,?,?,?,?,?,?,?,?,?)')
        parametros_inserir = (placa.upper(), opcao, categoria, disponibilidade, utilizacoes, aquisicao, data_legalizacao,
                              ultima_legalizacao, proxima_legalizacao,ultima_manutencao,proxima_manutencao)
        self.db_consulta(query_inserir, parametros_inserir)
        self.mensagem_add['text'] = "Veiculo inserido com sucesso!"
        self.tabela_pag_veiculos()
        self.alerta()

    def tabela_pag_veiculos(self):
        #FUNÇÃO PARA INSERIR AS INFORMAÇÕES DO BANCO DE DADOS NA TABELA.
        self.tabela.delete(*self.tabela.get_children())
        query = 'SELECT id_veiculo, placa, tipo, categoria, disponibilidade, disponivel_em FROM automoveis ORDER BY id_veiculo ASC'
        informacoes = self.db_consulta(query)
        hoje = datetime.today()
        for item in informacoes:
            #atualizando o status se a data de disponibilidade já estiver chegado ou de manutenção já estiver acabado
            if item[5] != None and item[5] != '':
                data = datetime.strptime(item[5], "%d/%m/%Y")
                if data < hoje:
                    none = None
                    query = "UPDATE automoveis SET disponivel_em = ?, disponibilidade = 'disponivel' WHERE id_veiculo = ?"
                    parametros = none, item[0]
                    self.db_consulta(query, parametros)
        for item in informacoes:
            #inserindo informações na tabela
            id, placa, tipo, categoria, disponibilidade, disponivel_em = item
            tipo = 'Carro' if int(tipo) == 0 else 'Moto' #alterando o nome dos tipos de veiculos de 0 ou 1 para carro ou moto
            disponivel_em = disponibilidade if disponivel_em == '' or disponivel_em == None else disponivel_em
            self.tabela.insert('', 'end', values=(id, placa, tipo, categoria, disponibilidade, disponivel_em))

    def pesquisar_veiculo(self):
        #JANELA PARA FAZER A PESQUISA DOS VEICULOS
        self.janela_pesquisar = Toplevel()
        self.janela_pesquisar.title("Pesquisar Veiculo") #titulo
        icon_lupa2 = PhotoImage(file="recursos/lupa-1.png")
        self.janela_pesquisar.iconphoto(False, icon_lupa2) #icone
        self.janela_pesquisar.resizable(FALSE,FALSE) #impedir que a janela seja maximizada
        self.janela_pesquisar.geometry("600x150+500+200") #tamanho e local onde a janela abrirá
        #INSERINDO FRAMES E WIDGETS NA JANELA
        self.frame_pesquisar = Frame(self.janela_pesquisar)
        self.lb_id = Label(self.frame_pesquisar, text="ID ou PLACA", font="sylfaen 10 bold" )
        self.ent_id = Entry(self.frame_pesquisar)
        self.bttm_id = Button(self.frame_pesquisar, cursor='hand2',text="OK", font="sylfaen 10 bold", bd=5,
                              relief="raised", bg='#B0E0E6', command=lambda: self.retorno_pesquisa(self.ent_id.get()))
        self.mensagem_erro = Label(self.frame_pesquisar, text=" ", font="sylfaen 10 bold", fg='red')

        #TABELA QUE MOSTRARÁ O RESULTADO DA PESQUISA
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

        #POSICIONANDO TABELA E WIDGETS
        self.lb_id.grid(row=0, column=0, padx=5, sticky='E')
        self.ent_id.grid(row=0, column=1, padx=5, sticky='WE')
        self.bttm_id.grid(row=0, column=2, padx=5, sticky='W')
        self.mensagem_erro.grid(row=2, column=0, columnspan=2)
        self.tabela_pesquisa.grid(row=3, columnspan=3)
        self.frame_pesquisar.pack()

    def retorno_pesquisa(self, informacao):
        #FUNÇÃO QUE PESQUISARÁ O VEICULO DE ACORDO COM OS DADOS INSERIDOS (ID OU PLACA)
        self.tabela_pesquisa.delete(*self.tabela_pesquisa.get_children())
        query_pesquisa = ('SELECT id_veiculo, placa, tipo, categoria, disponibilidade, disponivel_em, '
                          'utilizacoes FROM automoveis WHERE id_veiculo = ? OR placa = ?')
        if len(informacao) == 0:
            self.mensagem_erro['text'] = 'Inserir informação!'
            return
        informacao = informacao.upper()
        id_parametro = informacao, informacao
        registros_db = self.db_consulta(query_pesquisa, id_parametro)
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
        #ABA PARA MOSTRAR OS VEICULOS EM ALERTA DE LEGALIZAR
        legalizar = Frame(self.frame2)
        frame_legalizar = LabelFrame(legalizar, text="LEGALIZAR", font="sylfaen 16 bold")

        #TABELA COM OS VEICULOS QUE ESTÃO PRÓXIMOS A DATA DE LEGALIZAÇÃO
        self.tv_legalizar = ttk.Treeview(frame_legalizar, columns=('id', 'placa', 'data_de_aquisicao',
                'ultima_legalizacao', 'proxima_legalizacao', 'dias_proxima_legalizacao'), height=17, show='headings')
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

        #FRAME COM OS WIDGETS PARA ATUALIZAR O STATUS DA LEGALIZAÇÃO
        frame_atualizar_status = LabelFrame(legalizar, text="Atualizar status", font="sylfaen 12 bold")
        self.label_id_legalizar = Label(frame_atualizar_status, text="ID do veiculo:", font="sylfaen 12")
        self.entry_id_legalizar = Entry(frame_atualizar_status)
        self.label_data_legalizar = Label(frame_atualizar_status, text="Data da legalização:", font="sylfaen 12")
        self.entry_data_legalizar = Entry(frame_atualizar_status)
        self.entry_data_legalizar.insert(0,"DD/MM/AAAA")
        self.check_valor2 = IntVar()
        self.check_data_atual = Checkbutton(frame_atualizar_status, text="Data atual", variable=self.check_valor2,
                                            offvalue=0, onvalue=1, command=lambda: self.data_atual_legalizar(self.check_valor2.get()))
        self.mensagem_legalizacao = Label(frame_atualizar_status, text="", font="sylfaen 12 bold", fg='red' )
        self.button_confirm_legalizar = Button(frame_atualizar_status, bd=5, cursor='hand2', relief="raised", bg='#B0E0E6',
                                               text="Confirmar", font="sylfaen 12 bold", command=lambda:self.atualizar_legalizacao(self.entry_data_legalizar.get(), self.entry_id_legalizar.get()))

        #POSICIONANDO A TABELA E OS WIDGETS NA FRAME
        self.tv_legalizar.grid(row=2, column=1, padx=8)
        self.tabela_legalizar()
        frame_atualizar_status.grid(row=3)
        self.label_id_legalizar.grid(row=1, column=0)
        self.entry_id_legalizar.grid(row=1, column=1)
        self.label_data_legalizar.grid(row=2, column=0)
        self.entry_data_legalizar.grid(row=2, column=1)
        self.check_data_atual.grid(row=2, column=2)
        self.mensagem_legalizacao.grid(row=3, column=0, columnspan=2)
        self.button_confirm_legalizar.grid(row=4, column=0, columnspan=2)
        frame_legalizar.grid(row=1)
        legalizar.pack(expand=TRUE, fill=BOTH)


    def data_atual_legalizar(self,valor):
        #FUNÇÃO PARA INSERIR AUTOMATICAMENTE A DATA ATUAL CASO A CHECKBOX ESTEJA MARCADA
        hoje = datetime.today()
        hoje = hoje.strftime("%d/%m/%Y")
        if valor == 1:
            self.entry_data_legalizar.delete(0,11)
            self.entry_data_legalizar.insert(0,hoje)
        if valor == 0:
            self.entry_data_legalizar.delete(0,11)
            self.entry_data_legalizar.insert(0,"DD/MM/AAAA")

    def tabela_legalizar(self):
        #QUERY PARA POPULAR A TABELA DE VEICULOS EM ALERTA PRÓXIMO A DATA DE LEGALIZAÇÃO
        self.tv_legalizar.delete(*self.tv_legalizar.get_children()) #excluindo tabelas ja existente
        data_atual = datetime.today()
        informacoes = [] #lista que vai receber as informações da tabela
        query_datas = ('SELECT id_veiculo, placa, data_de_aquisicao, ultima_legalizacao, proxima_legalizacao '
                       ' FROM automoveis ')
        datas_proxima_legalizacao = self.db_consulta(query_datas)
        for data in datas_proxima_legalizacao:
            #calculando quais itens estão com 10 dias de prioximidade da data de legalização
            data_proxima = datetime.strptime(data[4], "%d/%m/%Y")
            dias = data_proxima - data_atual
            if dias.days <= 10:
                data = list(data)
                data.append(dias.days + 1)
                informacoes.append(data)
        for item in informacoes:
            id, placa, data_de_aquisicao, ultima_legalizacao, proxima_legalizacao, dias_proxima_legalizacao = item
            nome_dias_proxima_legalizacao = "< 24 horas" if dias_proxima_legalizacao == 0 else (f"atrasado "
                    f"{- dias_proxima_legalizacao} dia") if dias_proxima_legalizacao == -1 else (f"atrasado "
                    f"{- dias_proxima_legalizacao} dias") if dias_proxima_legalizacao < -1 else (f"{dias_proxima_legalizacao}"
                    f" dia") if dias_proxima_legalizacao == 1 else f"{dias_proxima_legalizacao} dias"
            nome_ultima_legalizacao = "Primeira legalização" if ultima_legalizacao == None else ultima_legalizacao
            self.tv_legalizar.insert('', 'end', values=(id, placa, data_de_aquisicao, nome_ultima_legalizacao,
                                                        proxima_legalizacao, nome_dias_proxima_legalizacao))

    def testar_id(self, id):
        #TESTAR SE O ID INFORMADO EXISTE NA BASE DE DADOS
        query_placa = "SELECT id_veiculo FROM automoveis WHERE id_veiculo = ?"
        parametro_placa = [id]
        retorno = self.db_consulta(query_placa, parametro_placa)
        if len(retorno) != 0:
            return True
        else:
            return False

    def atualizar_legalizacao(self, ultima, id_veiculo):
        #TESTES PARA VERIFICAR SE OS DADOS INFORMADOS ESTÃO CORRETOS PARA FAZER A ATUALIZAÇÃO DO STATUS DA LEGALIZAÇÃO DO VEICULO
        self.mensagem_legalizacao['text'] = ""
        id_vazia = True if id_veiculo == '' else False #testando se o campo id está preenchido
        data_vazia = True if ultima == '' else False #testando se o campo data está preenchido
        padrao_data = r'\d{2}/\d{2}/\d{4}'
        padrao_data_legal = re.match(padrao_data, ultima) #testando se a data está no formato indicado
        if id_vazia:
            self.mensagem_legalizacao['text'] = "Campo 'ID' obrigatório!"
            return
        if data_vazia:
            self.mensagem_legalizacao['text'] = "Campo 'DATA' obrigatório!"
            return
        if not padrao_data_legal:
            self.mensagem_legalizacao['text'] = "Data informada inválida!"
            return
        if self.testar_id(id_veiculo) == False: #testando se o veiculo existe na base de dados
            self.mensagem_legalizacao['text'] = "Veiculo não encontrado!"
            return
        proxima = datetime.strptime(ultima, "%d/%m/%Y") + timedelta(days=1826)
        # se tudo estiver corredo a proxima legalização deve ser a partir de 5 anos

        proxima = proxima.strftime("%d/%m/%Y")
        query_update_legalizacao = ("UPDATE automoveis SET ultima_legalizacao = ?,"
                                    " proxima_legalizacao = ? WHERE id_veiculo = ?")
        parametros_update_legalizacao = ultima, proxima, id_veiculo
        self.db_consulta(query_update_legalizacao, parametros_update_legalizacao)
        self.mensagem_legalizacao['text'] = "Status atualizado com sucesso!"
        self.tabela_legalizar()

    def manutencao_page(self):
        #ABA PARA MOSTRAR OS VEICULOS EM ALERTA DE MANUTENÇÃO
        manutencao = Frame(self.frame2)
        frame_manutencao = LabelFrame(manutencao, text="VEICULOS EM ALERTA:", font="sylfaen 16 bold")
        self.tv_manutencao = ttk.Treeview(frame_manutencao, columns=('id_veiculo', 'placa', 'status','ultima',
                                                                     'proxima', 'n_utilizacoes', 'dias'), height=13, show='headings')
        self.tv_manutencao.column('id_veiculo', minwidth=0, width=40)
        self.tv_manutencao.column('placa', minwidth=0, width=80)
        self.tv_manutencao.column('status', minwidth=0, width=100)
        self.tv_manutencao.column('ultima', minwidth=0, width=120)
        self.tv_manutencao.column('proxima', minwidth=0, width=100)
        self.tv_manutencao.column('n_utilizacoes', minwidth=0, width=80)
        self.tv_manutencao.column('dias', minwidth=0, width=100)
        self.tv_manutencao.heading('id_veiculo', text='ID')
        self.tv_manutencao.heading('placa', text='PLACA')
        self.tv_manutencao.heading('status', text='STATUS')
        self.tv_manutencao.heading('ultima', text='ULTIMA MAN.')
        self.tv_manutencao.heading('proxima', text='PRÓXIMA MAN.')
        self.tv_manutencao.heading('n_utilizacoes', text='UTILIZAÇÕES')
        self.tv_manutencao.heading('dias', text='PRÓXIMA MANUTENÇÃO EM')
        self.label_manutencao = Label(frame_manutencao, text='''Veiculos com 50 utilizações ou perto da data
         de manutenção ficarão em alerta até serem regularizados''', font='sylfaen 12 bold', fg='blue')

        self.tv_manutencao.grid(row=0)
        self.label_manutencao.grid(row=1)
        self.tabela_manutencao()

        ##--- FRAME QUE VAI RECEBER AS INFORMAÇÕES PARA INSERIR UMA MANUTENÇÃO ---#
        self.frame_att_manutencao = LabelFrame(frame_manutencao, text='Enviar para manutenção', font='sylfaen 12 bold' )
        self.lb_id_manut = Label(self.frame_att_manutencao, text="ID do veiculo:", font='sylfaen 12 bold')
        self.ent_id_veic = Entry(self.frame_att_manutencao)
        self.lb_dias_manut = Label(self.frame_att_manutencao, text="Dias em manutenção:", font='sylfaen 12 bold')
        self.ent_dias_manut = Entry(self.frame_att_manutencao)
        self.lb_detalhes_manut = Label(self.frame_att_manutencao, text="Detalhes da manutenção: ", font='sylfaen 12 bold')
        self.ent_detalhes = Entry(self.frame_att_manutencao)
        self.lb_data_inicio_manu = Label(self.frame_att_manutencao, text="Data de inicio\n da manutenção:", font='sylfaen 12 bold')
        self.ent_data_inicio = Entry(self.frame_att_manutencao)
        self.ent_data_inicio.insert(0,"DD/MM/AAAA")
        self.check_valor3 = IntVar()
        self.check_atual = Checkbutton(self.frame_att_manutencao, text="Data atual", font='sylfaen 10 bold', variable=self.check_valor3,
                                            offvalue=0, onvalue=1, command=self.data_atual_manutencao)

        self.mensagem_atualizar = Label(self.frame_att_manutencao, text='', font="sylfaen 12 bold", fg='red')
        self.btt_enviar_manutencao = Button(self.frame_att_manutencao, cursor='hand2', bd=5, relief="raised", bg='#B0E0E6',
                                text="Confirmar", font="sylfaen 12 bold", command=lambda: self.atualizar_manutencao
            (self.ent_id_veic.get(), self.ent_dias_manut.get(), self.ent_data_inicio.get(), self.ent_detalhes.get()))
        icone_pesquisa = tkinter.PhotoImage(file='recursos/magnifying_glass.png')
        self.buttom_pesquisar_manutencao = Button(self.frame_att_manutencao, cursor='hand2', text='Pesquisar\nveiculo', font="sylfaen 10 bold", image=icone_pesquisa,
                                       compound='left', background='#B0E0E6', command=self.pesquisar_manutencao)
        self.buttom_pesquisar_manutencao.image = icone_pesquisa

        #POSICIONANDO OS WIDGETS NA FRAME
        self.lb_id_manut.grid(row=0,column=0, sticky='w')
        self.ent_id_veic.grid(row=0,column=1, sticky='w')
        self.lb_dias_manut.grid(row=0,column=2, sticky='w')
        self.ent_dias_manut.grid(row=0,column=3, sticky='w')
        self.lb_data_inicio_manu.grid(row=1,column=0)
        self.ent_data_inicio.grid(row=1,column=1)
        self.check_atual.grid(row=1, column=2, sticky='w')
        self.lb_detalhes_manut.grid(row=2,column=0, columnspan=4, padx=10)
        self.ent_detalhes.grid(row=3,column=0,columnspan=4,rowspan=3, padx=10, sticky='we')
        self.buttom_pesquisar_manutencao.grid(row=1, column=3, rowspan=2, padx=5, sticky='e')
        self.mensagem_atualizar.grid(row=6,column=0, columnspan=4, sticky='we')
        self.btt_enviar_manutencao.grid(row=7, column=0, columnspan=4)
        self.frame_att_manutencao.grid(row=2,column=0,padx=53, sticky='we')
        frame_manutencao.grid(row=1, padx=20)
        manutencao.pack(expand=TRUE, fill=BOTH)

    def tabela_manutencao(self):
        # QUERY PARA POPULAR A TABELA DE VEICULOS EM ALERTA QUE PRECISAM DE MANUTENÇÃO
        self.tv_manutencao.delete(*self.tv_manutencao.get_children()) #excluindo tabelas ja existente
        data_atual = datetime.today()
        informacoes = []
        query_dados_manutencao = ('SELECT id_veiculo, placa, disponibilidade, ultima_manutencao, proxima_manutencao, utilizacoes '
                                  'FROM automoveis ORDER BY utilizacoes DESC')
        datas_proxima_manutencao = self.db_consulta(query_dados_manutencao)
        for item in datas_proxima_manutencao:
            data_proxima = datetime.strptime(item[4], "%d/%m/%Y")
            dias = data_proxima - data_atual
            if item[5] >= 50: #se o veiculo tiver 50 ou mais utilizações entrará em alerta
                item = list(item)
                item.append(dias.days + 1)
                informacoes.append(item)
            elif dias.days <= 10: #se o veiculo estiver a 10 dias de proximidade da data de manutenção entrará em alerta
                item = list(item)
                item.append(dias.days + 1)
                informacoes.append(item)
        for item in informacoes:
            id, placa, disponibilidade, ultima_m, proxi, utl, dias = item
            dias = "< 24 horas" if dias == 0 else (f"atrasado "
                    f"{- dias} dia") if dias == -1 else (f"atrasado "
                    f"{- dias} dias") if dias < -1 else (f"{dias}"
                    f" dia") if dias == 1 else f"{dias} dias"
            ultima_m = "sem registro" if ultima_m == None else ultima_m
            self.tv_manutencao.insert('', 'end', values= (id, placa, disponibilidade, ultima_m, proxi, utl, dias))

    def atualizar_manutencao(self,ent_id_veic, ent_dias_manut, dt_inicio, detalhes):
        #FUNÇÃO PARA FAZER A INSERÇÃO DE UMA NOVA MANUTENÇÃO
        #TESTES PARA VERIFICAR SE OS DADOS INFORMADOS ESTÃO CORRETOS
        self.mensagem_atualizar['text'] = "" #limpando campo de mensagem de erros
        id_vazia = True if ent_id_veic == '' else False #verificar se o id está vazio
        dias_vazia = True if ent_dias_manut == '' else False #verificar se os dias de manutenção está preenchido
        data_vazia = True if dt_inicio == '' else False #verificar se a data está preenchida
        padrao_data = r'\d{2}/\d{2}/\d{4}'
        padrao_data_manut = re.match(padrao_data, dt_inicio) #verificar se a data está no padrão correto

        if id_vazia:
            self.mensagem_atualizar['text'] = "Campo 'ID' obrigatório!"
            return
        if dias_vazia:
            self.mensagem_atualizar['text'] = "Campo 'Dias em manutenção' obrigatório!"
            return
        try:
            int(ent_dias_manut)
        except ValueError as e:
            self.mensagem_atualizar['text'] = "Campo 'Dias em manutenção' incorreto!"
            return
        if data_vazia:
            self.mensagem_atualizar['text'] = "Campo 'DATA' obrigatório!"
            return
        if not padrao_data_manut:
            self.mensagem_atualizar['text'] = "Data informada inválida!"
            return

        query_status = 'SELECT disponibilidade FROM automoveis WHERE id_veiculo = ?'
        parametros_status = [ent_id_veic] #VERIFICANDO SE O VEICULO ENCONTRA-SE DISPONIVEL!
        resultado_status = self.db_consulta(query_status, parametros_status)
        if resultado_status[0][0] == 'ocupado' or resultado_status[0][0] == 'em manutenção':
            self.mensagem_atualizar['text'] = "O veiculo não encontra-se disponivel!"
            return

        #INSERINDO NOVA MANUTENÇÃO
        query_update_manutencao = "INSERT INTO manutencao (veiculo, detalhes, data, duracao) VALUES (?,?,?,?)"
        parametros_update_manutencao = ent_id_veic, detalhes, dt_inicio, ent_dias_manut
        self.db_consulta(query_update_manutencao, parametros_update_manutencao)

        dt_inicio = datetime.strptime(dt_inicio, '%d/%m/%Y')
        ocupado_ate = dt_inicio + timedelta(int(ent_dias_manut))
        proxima_manu = ocupado_ate + timedelta(365)
        dt_inicio = dt_inicio.strftime('%d/%m/%Y')
        ocupado_ate = ocupado_ate.strftime('%d/%m/%Y')
        proxima_manu = proxima_manu.strftime('%d/%m/%Y')

        #ATUALIZANDO STATUS/DADOS NA BASE DE DADOS DOS VEICULOS
        query_update_veic = ("UPDATE automoveis SET disponibilidade = 'em manutencao', utilizacoes = 0, disponivel_em = ?,"
                             "ultima_manutencao = ?, proxima_manutencao = ? WHERE id_veiculo = ?")
        parametros_update_veic = ocupado_ate,dt_inicio,proxima_manu,ent_id_veic
        self.db_consulta(query_update_veic, parametros_update_veic)
        self.mensagem_atualizar['text'] = "Status atualizado com sucesso!"
        self.tabela_manutencao()

    def pesquisar_manutencao(self):
        #JANELA PARA PESQUISAR MANUTENÇÕES DOS VEICULOS
        self.janela_pesquisar_m = Toplevel()
        self.janela_pesquisar_m.title("Pesquisar manutenções") #titulo da janela
        icon_lupa = PhotoImage(file="recursos/lupa")
        self.janela_pesquisar_m.iconphoto(False, icon_lupa) #icone
        self.janela_pesquisar_m.resizable(FALSE,FALSE) #impedir que a janela seja redimensionada
        self.janela_pesquisar_m.geometry("600x300+500+200") #posicionamento e tamanho da janela

        #INSERINDO FRAME E WIDGETS NA JANELA DE PESQUISA
        self.frame_pesquisar_m = Frame(self.janela_pesquisar_m)
        self.lb_id_m = Label(self.frame_pesquisar_m, text="ID ou PLACA", font="sylfaen 10 bold" )
        self.lb_id_manutencao_m = Label(self.frame_pesquisar_m, text="ID manutenção", font="sylfaen 10 bold")
        self.ent_id_m = Entry(self.frame_pesquisar_m)
        self.ent_id_manutencao = Entry(self.frame_pesquisar_m)
        self.bttm_id_m = Button(self.frame_pesquisar_m, cursor='hand2',text="OK", font="sylfaen 10 bold", bd=5,
                                relief="raised", bg='#B0E0E6',
                                command= lambda: self.buscar_manutencoes(self.ent_id_m.get(), self.ent_id_manutencao.get()))
        self.mensagem_erro_m = Label(self.frame_pesquisar_m, text=" ", font="sylfaen 10 bold", fg='red')

        #INSERINDO TABELA QUE VAI RECEBER O RESULTADO NA JANELA DE PESQUISA
        self.tabela_pesquisa_m = ttk.Treeview(self.frame_pesquisar_m, columns=('id_veiculo', 'id_manutencao', 'placa',
                                                            'detalhes', 'data', 'duracao'), height=8, show='headings' )
        self.tabela_pesquisa_m.column('id_veiculo', minwidth=0, width=90)
        self.tabela_pesquisa_m.column('id_manutencao', minwidth=0,width=90)
        self.tabela_pesquisa_m.column('placa', minwidth=0, width=70)
        self.tabela_pesquisa_m.column('detalhes', minwidth=0, width=180)
        self.tabela_pesquisa_m.column('data', minwidth=0, width=90)
        self.tabela_pesquisa_m.column('duracao', minwidth=0, width=70)
        self.tabela_pesquisa_m.heading('id_veiculo', text='ID Veiculo')
        self.tabela_pesquisa_m.heading('id_manutencao', text='ID Manutencao')
        self.tabela_pesquisa_m.heading('placa', text='PLACA')
        self.tabela_pesquisa_m.heading('detalhes', text='detalhes')
        self.tabela_pesquisa_m.heading('data', text='INICIO')
        self.tabela_pesquisa_m.heading('duracao', text='Duração')
        self.lb_id_m.grid(row=0, column=0, padx=5, sticky='E')
        self.lb_id_manutencao_m.grid(row=1, column=0, padx=5, sticky='E')
        self.ent_id_m.grid(row=0, column=1, padx=5, sticky='WE')
        self.ent_id_manutencao.grid(row=1, column=1, padx=5, sticky='WE')

        self.bttm_id_m.grid(row=0, column=2, rowspan=2, padx=5, sticky='W')
        self.mensagem_erro_m.grid(row=2, column=0, columnspan=2)
        self.tabela_pesquisa_m.grid(row=3, columnspan=3)
        self.frame_pesquisar_m.pack()

    def buscar_manutencoes(self, id_placa, id_m):
        #FUNÇÃO PARA BUSCAR O RESULTADO DA PESQUISA
        self.tabela_pesquisa_m.delete(*self.tabela_pesquisa_m.get_children()) #deletando tabela anteriores
        registros_db = []
        if len(id_placa) == 0 and len(id_m) == 0: #erro caso nenhum campo seja informado
            self.mensagem_erro_m['text'] = 'Inserir informação!'
            return

        if len(id_placa) != 0: #busca por PLACA ou ID do veiculo usando o left join caso ainda não haja manutenção para o veiculo informado
            query_pesquisa = ('SELECT id_veiculo, id_manutencao, placa, detalhes, data, duracao FROM automoveis '
                              'LEFT JOIN manutencao ON automoveis.id_veiculo = manutencao.veiculo WHERE id_veiculo = ? OR placa = ?')
            id_placa = id_placa.upper()
            id_parametro = id_placa, id_placa
            registros_db = self.db_consulta(query_pesquisa, id_parametro)
            if registros_db == []: #mensagem de erro caso a placa ou ID não pertença a nenhum veiculo
                self.mensagem_erro_m['text'] = 'Não há veiculo com os dados informados!'
                return

        elif len(id_m) != 0: #busca por ID de manutenção usando o left join caso ainda não haja manutenção para o veiculo informado
            query_pesquisa = ('SELECT id_veiculo, id_manutencao, placa, detalhes, data, duracao FROM automoveis '
                              'LEFT JOIN manutencao ON automoveis.id_veiculo = manutencao.veiculo WHERE id_manutencao = ?')
            id_parametro = [id_m]
            registros_db = self.db_consulta(query_pesquisa, id_parametro)
            if registros_db == []:
                self.mensagem_erro_m['text'] = 'Manutenção não encontrada!'
                return

        self.mensagem_erro_m['text'] = ''
        for item in registros_db:
            id_veiculo, id_manutencao, placa, detalhes, data, duracao = item
            id_manutencao = '' if id_manutencao == None else id_manutencao
            detalhes = 'SEM REGISTROS ANTERIORES' if detalhes == None else detalhes
            duracao = '' if duracao == None else f" {duracao} dia" if duracao == 1 else f"{duracao} dias"
            data = '' if data == None else data
            duracao = '' if duracao == None else duracao
            self.tabela_pesquisa_m.insert('', END, values=(id_veiculo, id_manutencao, placa, detalhes, data, duracao))

    def data_atual_manutencao(self):
        #FUNÇÃO PARA INSERIR A DATA ATUAL NA ENTRY CASO O CHECKBOX ESTEJA MARCADO
        hoje = datetime.now()
        hoje = hoje.strftime("%d/%m/%Y")
        if self.check_valor3.get() == 1:
            self.ent_data_inicio.delete(0,11)
            self.ent_data_inicio.insert(0,hoje)
        if self.check_valor3.get() == 0:
            self.ent_data_inicio.delete(0,11)
            self.ent_data_inicio.insert(0,"DD/MM/AAAA")

    def page_sair(self):
        #ABA PARA VOLTAR A TELA DE LOGIN
        teste = Frame(self.frame2)
        lb = LabelFrame(teste, text="SAIR", font='sylfaen 12 bold')
        botao_sair2 = Button(lb, text="Voltar ao menu inicial", font='sylfaen 12 bold', command=self.sair)
        botao_sair2.grid()
        lb.grid(pady=265, padx=252)
        teste.pack()
    def sair(self):
        #destroir a frame atual e voltar a frame inicial de login
        self.destroy()
        voltar = Window(root)

if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.mainloop()
