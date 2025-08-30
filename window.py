import os
import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3

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
        self.login_button = Button(self.frame, text="Login", cursor='hand2', font="sylfaen 15 bold", bd=5, relief="raised",
                            bg='#B0E0E6', command=self.login) #criando botão de login que vai abrir a janela para inserir os dados de autenticação
        self.login_button.grid(row=0, column=0, pady=20, padx=200) #posicionando botão login
        self.cadastrar = Button(self.frame, text="Cadastrar usuário", cursor='hand2', font="sylfaen 15 bold",
                                bd=5, relief="raised", bg='#B0E0E6', command=self.cadastrar)
        self.cadastrar.grid(row=1, column=0)
        self.exit = Button(self.frame, text="Sair", cursor='hand2', font="sylfaen 15 bold", bd=5, relief="raised",
                           bg='#B0E0E6', command=self.exit) #criando botão de sair
        self.exit.grid(row=2, column=0, pady= 20) #posicionando botão de sair
        self.frame.grid(pady=200, padx=200) #posicionando frame
        self.login_button.focus_set()
        self.janela.bind('<Escape>', lambda event: self.janela.destroy())
        self.janela.bind('<Return>', self.enter_pressed)
        self.frame_inicial.grid() #posicionado frame inicial

    def enter_pressed(self, event):
        widget = self.janela.focus_get()
        if isinstance(widget, Button):
            widget.invoke()

    '''###########################--JANELA CADASTRO--#################################'''
    def cadastrar(self):
        self.janela_cadastro = Toplevel()
        self.janela_cadastro.title("CADASTRAR USUARIO")  # titulo
        icon2 = PhotoImage(file="recursos/icone2.png")
        self.janela_cadastro.iconphoto(False, icon2)  # mudando o icone
        self.janela_cadastro.resizable(False, False)
        self.janela_cadastro.geometry("550x300+400+200")  # tamanho e posição da janela
        frame_cadastro = Frame(self.janela_cadastro)
        id_usuario = Label(frame_cadastro, text="Insira seu ID:", font="sylfaen 15 bold")
        self.insert_id = Entry(frame_cadastro, width=45)
        nome = Label(frame_cadastro, text="Insira nome: ", font="sylfaen 15 bold")
        self.insert_nome = Entry(frame_cadastro, width=45)
        usuario_lb = Label(frame_cadastro, text="Insira usuário: ", font="sylfaen 15 bold") #etiqueta que mostra onde inserir o usuario
        self.insert_usuario = Entry(frame_cadastro, width=45)
        label_senha = Label(frame_cadastro, text="Senha: ", font="sylfaen 15 bold")  #etiqueta que mostra onde inserir a senha
        self.insert_senha = Entry(frame_cadastro, width=45)
        info_senha = Label(frame_cadastro, text="A senha deve conter no minimo\n8 digitos com letras e numeros.", font="sylfaen 12 italic")
        self.mensagem_cadastro=Label(frame_cadastro, text='', font="sylfaen 13 bold", fg="red")
        button_insert = Button(frame_cadastro, text="Confirmar dados", cursor='hand2', font="sylfaen 13 bold",
                               command=lambda: self.verificar_cadastro(self.insert_id.get(), self.insert_usuario.get(), 
                               self.insert_senha.get(), self.insert_nome.get()))

        id_usuario.grid(row=0)      ######### Posicionando os widgets na frame.
        self.insert_id.grid(row=0, column=1)
        nome.grid(row=1)
        self.insert_nome.grid(row=1, column=1)
        usuario_lb.grid(row=2, column=0)
        self.insert_usuario.grid(row=2, column=1)
        label_senha.grid(row=3, column=0)
        self.insert_senha.grid(row=3, column=1)
        info_senha.grid(row=4, columnspan=3)
        button_insert.grid(row=5, rowspan=3, columnspan=3)
        self.mensagem_cadastro.grid(row=8, columnspan=3)
        frame_cadastro.pack()
        self.janela_cadastro.bind('<Escape>', lambda event: self.janela_cadastro.destroy())
        self.janela_cadastro.bind('<Return>', lambda event: self.verificar_cadastro(self.insert_id.get(), 
                                self.insert_usuario.get(), self.insert_senha.get(), self.insert_nome.get()))
        self.janela_cadastro.grab_set()
        #self.janela_cadastro.focus_set()
        self.janela_cadastro.transient(self.janela)
        self.insert_id.focus()

    def verificar_cadastro(self, id, usuario, senha, nome):
        self.mensagem_cadastro['text'] = ''     #Limpando a mensagem
        senha_pequena = len(senha) < 8  #testando se a senha é menor que oito digitos
        senha_letras = senha.isalpha() #testando se a senha não tem numeros
        senha_numeros = senha.isnumeric() #testando se a senha não tem letras
        campos = [
        id,
        usuario,
        senha,
        nome
         ]
        if any(campo.strip() == "" for campo in campos):  # Verificando se algum campo está vazio
            self.mensagem_cadastro['text'] = "Preencha todos os campos!"
            return
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
        if id.isdigit():
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
                self.insert_id.delete(0, 'end')
                self.insert_nome.delete(0, 'end')
                self.insert_senha.delete(0, 'end')
                self.insert_usuario.delete(0, 'end')
                self.insert_id.focus()
                return
        else:
            self.mensagem_cadastro['text'] = 'Campo ID aceita apenas numeros'



    '''###########################--JANELA LOGIN--#################################'''
    def login(self):
        self.janela_login = Toplevel()  # abrindo a tela de login em uma janela menor
        self.janela_login.title("LOGIN") #titulo
        icon3 = PhotoImage(file="recursos/icone2.png")
        self.janela_login.iconphoto(False, icon3) #mudando o icone
        self.janela_login.resizable(False, False)
        self.janela_login.geometry("300x180+500+200") #tamanho e posição da janela
        frame_login = Frame(self.janela_login)
        usuario = Label(frame_login, text="Usuário: ", font="sylfaen 15 bold") #etiqueta que mostra onde inserir o usuario
        usuario.grid(row=0, sticky=W)
        senha = Label(frame_login, text="Senha: ", font="sylfaen 15 bold")  #etiqueta que mostra onde inserir a senha
        senha.grid(row=1, sticky=W)
        insert_usuario = Entry(frame_login)
        insert_usuario.grid(row=0, column=1, columnspan=2)
        insert_senha = Entry(frame_login, show='*')
        insert_senha.grid(row=1, column=1)
        confirmar = Button(frame_login, text="acessar", bd=5, cursor='hand2', relief="raised", bg='#B0E0E6', font="sylfaen 15 bold",
                           command= lambda: self.Validacao(insert_usuario.get(), insert_senha.get()))
        self.mensagem = Label(frame_login, text='')
        self.mensagem.grid(row=2,columnspan=2)
        confirmar.grid(row=3, column=1, columnspan=2)
        self.janela_login.bind('<Return>', lambda event: self.Validacao(insert_usuario.get(), insert_senha.get())) #ao pressionar enter tentar validar
        self.janela_login.bind('<Escape>', lambda event: self.janela_login.destroy()) #ao pressionar esc fecha a janela
        frame_login.grid(row=0, column=0, sticky="nsew")
        self.janela_login.grab_set()
        self.janela_login.focus_set()
        insert_usuario.focus()  # para iniciar com entry usuario
        self.janela_login.transient(self.janela)
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
            from menu import Menu
            menu = Menu(self.janela)
            menu.pack(fill='both', expand=True)
        else:
            self.mensagem['text'] = 'Usuario ou senhas incorreto'''

