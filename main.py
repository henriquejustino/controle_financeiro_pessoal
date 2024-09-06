from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
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

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']


# Criando janela

# janela = ctk.CTk()
janela = Tk()
janela.title()
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



janela.mainloop()