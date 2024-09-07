from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date
from view import *

# import customtkinter as ctk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *

# cores
co0 = "#2e2d2b"   # Preta
co1 = "#feffff"   # branca
co2 = "#4fa882"   # verde
co3 = "#38576b"   # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # ++ verde
co10 = "#83a9e6"    #sei la que cor é essa
co11 = "#545454"

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# Criando janela
# janela = ctk.CTk()
janela = Tk()
janela.title('Controle Financeiro')
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

# janela._set_appearance_mode("system")
style = ttk.Style(janela)
style.theme_use("clam")

# criando frames para divisão da tela
FrameCima = Frame(janela, width=1043, height=50, background=co1, relief="flat")
FrameCima.grid(row=0, column=0)

FrameMeio = Frame(janela, width=1043, height=361, background=co1, pady=20, relief="raised")
FrameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

FrameBaixo = Frame(janela, width=1043, height=300, background=co1, relief="flat")
FrameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

# Trabalhando com FrameCima
# Acessando a imagem
app_img = Image.open('logo.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(FrameCima, image=app_img, text=" Controle Financeiro", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# Definindo tree como global
global tree

# Função inserir categoria
def inserir_categoria_b():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    #passando a lista para a função inserir gastos presente na view
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso!')

    e_categoria.delete(0,'end')

    #Pegando os valores categoria
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    #Atualizando a lista de categorias
    combo_categoria_despesas['values'] = (categoria)

# Função inserir receitas
def inserir_receita_b():
    nome = 'Receita'
    data = e_cal_receitas.get()
    valor = e_valor_receitas.get()

    lista_inserir = [nome, data, valor]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    # Chamando a função inserir receitas presente na view
    inserir_receita(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso!')

    e_cal_receitas.delete(0,'end')
    e_valor_receitas.delete(0,'end')

    #Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# Função inserir despesas
def inserir_despesas_b():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    valor = e_valor_despesas.get()

    lista_inserir = [nome, data, valor]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    # Chamando a função inserir despesas presente na view
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso!')

    combo_categoria_despesas.delete(0, 'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    #Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

#Função deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')

            #Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')

            #Atualizando dados
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')

# porcentagem -----------------------------------------
def porcentagem():
    l_nome = Label(FrameMeio, text="Porcentagem da Receita restante", height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(FrameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = porcentagem_valor()[0]
    
    valor = porcentagem_valor()[0]

    l_porcentagem = Label(FrameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

# Função para grafico bars --------------------------------------
def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    # ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    # create a list to collect the plt.patches data

    c = 0
    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, FrameMeio)
    canva.get_tk_widget().place(x=10, y=70)

# Função para resumo total --------------------------------------
def resumo():
    valor = bar_valores()

    l_linha = Label(FrameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg=co11)
    l_linha.place(x=309, y=52)
    l_sumario = Label(FrameMeio, text="Total Renda Mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario.place(x=309, y=35)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg=co11)
    l_sumario.place(x=309, y=70)

    l_linha = Label(FrameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg=co11)
    l_linha.place(x=309, y=132)
    l_sumario = Label(FrameMeio, text="Total Despesas Mensal   ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario.place(x=309, y=115)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg=co11)
    l_sumario.place(x=309, y=150)

    l_linha = Label(FrameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg=co11)
    l_linha.place(x=309, y=207)
    l_sumario = Label(FrameMeio, text="Total Saldo do Caixa      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario.place(x=309, y=190)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg=co11)
    l_sumario.place(x=309, y=220)

frame_gra_pie = Frame(FrameMeio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

# funcao grafico pie
def grafico_pie():

    #faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    #only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

porcentagem()
grafico_bar()
resumo()
grafico_pie()

# Criando Frame Baixo
frame_renda = Frame(FrameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(FrameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(FrameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2, padx=5)

# Tabela renda mensal --------------------------------------------------
app_tabela = Label(FrameMeio, text="Tabela, Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)

# Função para mostrar Renda
def mostrar_renda():
    #creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Valor']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    #vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    #horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        #adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_renda()

# Configuração Despesas ----------------------------------------
l_info = Label(frame_operacoes, text="Insira novas despesas", height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

# Categoria ----------------------------------------------------
l_categoria = Label(frame_operacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

# Pegando Categoria --------------------------------------------
categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=110, y=41)

# Despesas ----------------------------------------------------------
l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024, date_pattern='dd/mm/yyyy')
e_cal_despesas.place(x=110, y=71)

# Valor -------------------------------------------------------------
l_valor_despesas = Label(frame_operacoes, text='Valor Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)

# Botão Inserir -------------------------------------------------------
img_add_despesas = Image.open('add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, command=inserir_despesas_b, image=img_add_despesas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)

# Botão Excluir --------------------------------------------------------
l_excluir = Label(frame_operacoes, text='Excluir ação', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)

img_excluir = Image.open('trash.png')
img_excluir = img_excluir.resize((17,17))
img_excluir = ImageTk.PhotoImage(img_excluir)
botao_excluir = Button(frame_operacoes, command=deletar_dados, image=img_excluir, text=" Excluir".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_excluir.place(x=110, y=190)

# Configuração Receitas --------------------------------------------------
l_info = Label(frame_configuracao, text="Insira novas receitas", height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

# calendario receitas -----------------------------------------------------
l_cal_receitas = Label(frame_configuracao, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024, date_pattern='dd/mm/yyyy')
e_cal_receitas.place(x=110, y=41)

# Valor Receita -----------------------------------------------------------
l_valor_receitas = Label(frame_configuracao, text='Valor Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110, y=71)

# Botão Inserir Receitas---------------------------------------------------
img_add_receitas = Image.open('add.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao, command=inserir_receita_b, image=img_add_receitas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=111)

# Operação Nova Categoria ------------------------------------------------
l_info = Label(frame_configuracao, text="Categoria", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=160)

e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y=160)

# Botão Inserir Categoria ---------------------------------------------------
img_add_categoria = Image.open('add.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserircategoria = Button(frame_configuracao, command=inserir_categoria_b, image=img_add_categoria, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserircategoria.place(x=110, y=190)

janela.mainloop()