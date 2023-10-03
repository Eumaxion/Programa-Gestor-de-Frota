from tkinter import ttk
from tkinter import *
import sqlite3

'''################## CLASSE FROTA/ JANELA INICIAL ###################################################'''
class Window:
    db_usuarios = 'database/Usuarios.db'  # variavel para acessar o banco de dados de usuarios
    def __init__(self, root): #construtor recebe a rota
        self.janela = root #janela inicial vai receber root
        self.janela.title(
        "Sistema de Gerenciamento de Frota Luxury Wheels")  # Adicionando um titulo a janela principal do programa

        self.janela.geometry(f"900x600+200+50")  # redimensionando o tamanho e posição da janela do programa de acordo com o tamanho da tela
        self.janela.wm_iconbitmap('recursos/icone1.ico')  # alterando o icone da janela
        self.janela['bg'] = '#B0E0E6' #alterando a cor de fundo da janela inicial
        #criando frame inicial com botão de login e exit

        self.frame_inicial = Frame(self.janela) #Criando o frame inicial que vai receber a tela para login ou sair
        self.frame = LabelFrame(self.frame_inicial, text="Sistema de Gerenciamento de Frota Luxury Wheels", bd=8, relief="groove", font="sylfaen 15 bold", bg="#E6E6FA") #frame com login ou sair
        self.login = Button(self.frame, text="Login", font="sylfaen 15 bold", bd=5, relief="raised", bg='#B0E0E6', command=self.login) #criando botão de login que vai abrir a janela para inserir os dados de autenticação
        self.login.grid(row=0, column=0, pady=20, padx=200) #posicionando botão login
        self.exit = Button(self.frame, text="Sair", font="sylfaen 15 bold", bd=5, relief="raised", bg='#B0E0E6', command=self.exit) #criando botão de sair
        self.exit.grid(row=1, column=0, pady= 20) #posicionando botão de sair
        self.frame.grid(pady=200, padx=200) #posicionando frame
        self.frame_inicial.grid() #posicionado frame inicial

    def exit(self): #metodo para encerrar o programa
        self.janela.destroy()
    def login(self):
        self.janela_login = Toplevel()  # abrindo a tela de login em uma janela menor
        self.janela_login.title("LOGIN") #titulo
        self.janela_login.wm_iconbitmap("recursos/icone2.ico") #mudando o icone
        self.janela_login.resizable(TRUE, TRUE)
        self.janela_login.geometry("250x150+500+200") #tamanho e posição da janela
        frame_login = Frame(self.janela_login)
        usuario = Label(frame_login, text="Usuário: ", font="sylfaen 15 bold") #etiqueta que mostra onde inserir o usuario
        usuario.grid(row=0, sticky=W)
        senha = Label(frame_login, text="Senha: ", font="sylfaen 15 bold")  #etiqueta que mostra onde inserir a senha
        senha.grid(row=1, sticky=W)
        insert_usuario = Entry(frame_login)
        insert_usuario.grid(row=0, column=1)
        insert_senha = Entry(frame_login)
        insert_senha.grid(row=1, column=1)
        confirmar = Button(frame_login, text="acessar", bd=5, relief="raised", bg='#B0E0E6', font="sylfaen 15 bold",
                           command= lambda: self.Validacao(insert_usuario.get(), insert_senha.get()))
        self.mensagem = Label(frame_login, text='')
        self.mensagem.grid(row=2, columnspan=2)
        confirmar.grid(row=3, column=1, columnspan=2)
        insert_usuario.focus()  # para iniciar com entry usuario
        frame_login.grid(row=1)

    def db_consulta(self, consulta, parametros=()): #função para acessar a base de dados e fazer consulta de usuario
        with sqlite3.connect(self.db_usuarios) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return resultado

    def Validacao(self, user, senha): #metodo para verificar se a senha e usuario estão corretos
        query = 'SELECT * FROM Usuarios WHERE nome = ? and senha = ?'
        parametros = user, senha

        teste1 = self.db_consulta(query, parametros)
        resposta = teste1.fetchall()

        print(resposta)
        if len(resposta) != 0:
            self.aba_menu()
        else:
            self.mensagem['text'] = 'Usuario ou senhas incorreto'''

    def aba_menu(self):
        self.janela_login.destroy()
        self.frame_inicial.destroy()
        menu = Menu(self.janela)
        menu.grid()


'''################################ CLASSE MENU ###############################'''
class Menu(Frame):
    db_auto = 'database/Automoveis.db'  # variavel para acessar o banco de dados da frota
    def __init__(self, master):
        super().__init__()
        self['height'] = 150
        self['width'] = 600
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
        b_frota = Button(self.frame, text="ADICIONAR\nVEICULOS", font="sylfaen 13 bold", bd=0, background="#ADD8E6",
                         command=lambda: self.indicar(self.indicador_frota, self.frota_page))
        b_frota.place(x=50, y=400)
        self.indicador_frota = Label(self.frame, text='', bg="#ADD8E6")
        self.indicador_frota.place(x=10, y=400, width=10, height=60)

        self.frame.pack(side=LEFT)  # posicionando

        self.frame2 = Frame(self, highlightbackground='black', highlightthickness=2, bg='#B0E0E6', width=700,
                            height=600)

        self.frame2.pack(side=RIGHT)

    def veiculos_page(self):
        veiculos_frame = LabelFrame(self.frame2, text="FROTA", font="sylfaen 16 bold", width=700, height=600)
        self.tabela = ttk.Treeview(veiculos_frame, columns=('placa', 'tipo', 'disponivel', 'utilizacoes', 'data_de_aquisicao', 'legalizacao', 'disponivel em'), show='headings')
        self.tabela.column('placa', minwidth=0,width=70)
        self.tabela.column('tipo', minwidth=0, width=70)
        self.tabela.column('disponivel', minwidth=0, width=100)
        self.tabela.column('utilizacoes', minwidth=0, width=100)
        self.tabela.column('data_de_aquisicao', minwidth=0, width=110)
        self.tabela.column('legalizacao', minwidth=0, width=110)
        self.tabela.column('disponivel em', minwidth=0, width=100)
        self.tabela.heading('placa', text='Placa')
        self.tabela.heading('tipo', text='tipo')
        self.tabela.heading('disponivel', text='Disponibilidade')
        self.tabela.heading('utilizacoes', text='nº de utilizações')
        self.tabela.heading('data_de_aquisicao', text='Data de Aquisição')
        self.tabela.heading('legalizacao', text='Ultima legalização')
        self.tabela.heading('disponivel em', text='Disponivel em:')
        self.tabela.grid()
        self.frota()
        veiculos_frame.pack(anchor='center', side='top')

        '''#####################---ADICIONAR NOVO VEICULO--- #####################'''
        adicionar_veiculo = LabelFrame(veiculos_frame, text="Inserir novo veiculo", font="sylfaen 16 bold")
        self.label_placa = Label(adicionar_veiculo, text="Placa:", font="sylfaen 12 bold" )
        self.nova_placa = Entry(adicionar_veiculo)
        self.label_placa.grid(row=0, column=0)
        self.nova_placa.grid(row=0, column=1)
        self.label_tipo = Label(adicionar_veiculo, text="Tipo:", font="sylfaen 12 bold" )
        self.nova_tipo = Entry(adicionar_veiculo)
        self.label_tipo.grid(row=0, column=2)
        self.nova_tipo.grid(row=0, column=3)
        self.label_aquisicao = Label(adicionar_veiculo, text="Data de aquisição:", font="sylfaen 12 bold" )
        self.nova_aquisicao = Entry(adicionar_veiculo)
        self.label_aquisicao.grid(row=0, column=4)
        self.nova_aquisicao.grid(row=0, column=5)
        self.inserir_dados = Button(adicionar_veiculo, text="Confirmar", font="sylfaen 12 bold", bd=5, relief="raised", bg='#B0E0E6',)
        self.inserir_dados.grid(row=1, columnspan=6, sticky='e')
        adicionar_veiculo.grid()


    def frota(self):
        self.tabela.delete(*self.tabela.get_children())
        query = 'SELECT * FROM automoveis ORDER BY placa DESC'
        informacoes = self.db_consulta(query)
        for item in informacoes:
            self.tabela.insert('', 'end', values=item)


    def db_consulta(self, consulta, parametros=()): #função para acessar a base de dados e fazer consulta
        with sqlite3.connect(self.db_auto) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            dados = resultado.fetchall()
            con.commit()
            return dados
    def legalizar_page(self):
        teste = Frame(self.frame2)
        lb = Label(teste, text="LEGALIZAR", font="sylfaen 16 bold")
        lb.pack()
        teste.pack(pady=10)

    def manutencao_page(self):
        manutencao = Frame(self.frame2)
        frame_manutencao = LabelFrame(manutencao, text="VEICULOS EM ALERTA:", font="sylfaen 16 bold", width=700, height=600)
        self.label_manutencao = Label(frame_manutencao, text='''Veiculos com com 50 utilizações ou mais deverão ser enviados para manutenção, 
        após a regularização do veiculo o administrador deve atualizar o status na base de dados.''')
        self.tabela_3 = ttk.Treeview(frame_manutencao, columns=('utilizacoes', 'placa', 'tipo', 'disponivel', 'disponivel em'), show='headings')
        self.tabela_3.column('utilizacoes', minwidth=0, width=100)
        self.tabela_3.column('placa', minwidth=0, width=70)
        self.tabela_3.column('tipo', minwidth=0, width=70)
        self.tabela_3.column('disponivel', minwidth=0, width=100)
        self.tabela_3.column('disponivel em', minwidth=0, width=100)
        self.tabela_3.heading('utilizacoes', text='nº de utilizações')
        self.tabela_3.heading('placa', text='Placa')
        self.tabela_3.heading('tipo', text='tipo')
        self.tabela_3.heading('disponivel', text='Disponibilidade')
        self.tabela_3.heading('disponivel em', text='Disponivel em:')
        self.tabela_3.grid()
        self.tabela_manutencao()
        ################--- ATUALIZAR MANUTENÇÃO ---#####################
        self.mensagem_atualizar = Label(frame_manutencao, text='')
        self.atualizar_manutencao = Button(frame_manutencao, text="Manutenção Concluida", font="sylfaen 12 bold", command= self.atualizar_manutencao)
        self.label_manutencao.grid()
        self.mensagem_atualizar.grid()
        self.atualizar_manutencao.grid()
        frame_manutencao.pack()
        manutencao.pack()

    def tabela_manutencao(self):
        self.tabela_3.delete(*self.tabela_3.get_children())
        query = 'SELECT utilizacoes,placa, tipo, disponibilidade, disponivel_em FROM automoveis WHERE utilizacoes >= 50 ORDER BY utilizacoes DESC'
        informacoes = self.db_consulta(query)
        for item in informacoes:
            self.tabela_3.insert('', 'end', values=item)
    def atualizar_manutencao(self):
        self.mensagem_atualizar['text'] = ''
        try:
            self.tabela_3.item(self.tabela_3.selection())['text'][0]
        except IndexError as erro:
            self.mensagem_atualizar['text'] = 'Por favor, selecione um produto.'
            return
        num_manutencoes = self.tabela_3.item(self.tabela_3.selection())['placa']
        aaa = num_manutencoes.get()
        query = 'UPDATE Automoveis SET utilizacoes = 0 WHERE placa = ?'
        parametros = aaa
        self.db_consulta(query,parametros)
        self.tabela_manutencao()


    def frota_page(self):
        teste = Frame(self.frame2)
        lb = Label(teste, text="ADICIONAR FROTA", font="arial 30")
        lb.pack()
        teste.pack(pady=10)

    def delet_pages(self):
        for item in self.frame2.winfo_children():
            item.destroy()

    def remover_indicador(self):
        self.indicador_disponiveis.config(bg='#ADD8E6')
        self.indicador_frota.config(bg='#ADD8E6')
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
