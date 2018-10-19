import os
import exifread
from datetime import datetime
#from datetime import timedelta
import time
import sys

time.sleep(1)

divisorNomeOriginal = ' --'

#Receber Arquivos
def receberArquivos():
    dropped = sys.argv
    if len(dropped) > 1: #AQUI É SE EU JOGUEI UM ARQUIVO NO .py
                                            #dropped = ['C:\\Users\GutRe\PycharmProjects\RenomearFotos\FotosTeste\\20170908_222656.jpg']
                                            #dropped = ['C:\\Users\GutRe\PycharmProjects\RenomearFotos\FotosTeste\\IMG_20170917_163140759.jpg']
        diretorio = os.path.dirname(dropped[1])

    elif len(dropped) == 1: #AQUI É PELO PYCHARM ou sem jogar arquivo em cima
        #perguntar o nome da pasta
        diretorio = 'C:\\Users\GutRe\PycharmProjects\RenomearFotos\FotosTeste'

    listaArquivos = os.listdir(diretorio)
    nomesCompletosArquivos=[]
    for arquivo in listaArquivos:
        if '.jpg' in arquivo:
            nomesCompletosArquivos.append(diretorio + '\\' + arquivo)

    return nomesCompletosArquivos

#Ler e tratar os metadados de 1 arquivo - retorna um array de informações da foto já tratadas
def lerMetaDados(arquivo):
    #abrir e fechar o arquivo pra ler os metadados dele
    file = open(arquivo, 'rb')
    metaDados = exifread.process_file(file)
    file.close()
    dateTimeOriginal = metaDados['EXIF DateTimeOriginal'].printable #pega o valor original

    #arrumar o formato da data e hora
    dataHora = arrumarDataeHora(dateTimeOriginal)

    if 'EXIF SubSecTimeOriginal' in metaDados:
        subSecTimeOriginal = metaDados['EXIF SubSecTimeOriginal'].printable
        subSecTimeOriginal = '_'+subSecTimeOriginal #valor que talvez aparecerá depois dos segundos (com formatação de underline)
    else:
        subSecTimeOriginal = ''
    return dataHora,subSecTimeOriginal #e talvez a camera ou outras coisas no array de saída

#Arrumar Data e Hora - muda a formatação da String de data e hora para a formatação que eu quero
def arrumarDataeHora(dataHora):
    dataHora = datetime.strptime(dataHora, '%Y:%m:%d %H:%M:%S') #pega a string e transforma em valor de data
    dataHora = datetime.strftime(dataHora, '%Y-%m-%d %H_%M_%S') #pega a data e transforma em string formatada no formato que eu quero
    return dataHora


#Põe data e hora
def adicionarPrefixo(listaArquivos):
    for arquivo in listaArquivos:
        if divisorNomeOriginal not in arquivo:
            dataHoraOriginal, subSegHoraOriginal = lerMetaDados(arquivo)

            #Renomear Arquivos
            diretorio, nomeArquivoOriginal = os.path.split(arquivo)
            nomeArquivoNovo = dataHoraOriginal+subSegHoraOriginal+divisorNomeOriginal+nomeArquivoOriginal
            os.rename(arquivo,diretorio+'\\'+nomeArquivoNovo)
            print(nomeArquivoNovo)

    time.sleep(2)

#Tira data e hora
def removerPrefixo(listaArquivos):
    for arquivo in listaArquivos:
        if divisorNomeOriginal in arquivo:
            diretorio, nomeArquivo = os.path.split(arquivo)
            finder = nomeArquivo.find(divisorNomeOriginal)
            nomeArquivo = nomeArquivo[(finder+len(divisorNomeOriginal)):len(nomeArquivo)]
            os.rename(arquivo,diretorio+'\\'+nomeArquivo)
            print(arquivo)
    time.sleep(1)

def principal():
    listaFotos = receberArquivos()
    chave = input("Apagar digitar 'R' e Escrever digitar 'E'\n")
    print('Voce digitou ' + chave)
    if chave.upper() == 'R':
        removerPrefixo(listaFotos)
        time.sleep(2)
    elif chave.upper() == 'E':
        adicionarPrefixo(listaFotos)
    else:
        principal()

principal()