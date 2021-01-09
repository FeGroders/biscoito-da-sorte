#Criado por: Fernando Groders
#Linguagem: Python 3.8.7
#Data da última atualização: 09/01/2021

import tweepy
import time
import csv
import os
from os import environ
from random import randint

API_KEY = environ['API_KEY'] #Autenticadores do Twitter
API_KEY_SECRET = environ['API_KEY_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) #Autentica a conta
nome_arquivo_frases = 'frases.csv'
nome_arquivo = 'ultimo_id_lido.txt'

def le_frases(): #Função que abre o arquivo .csv de frases e lê elas adicionando-as em um vetor
    
    frases = []
    with open(nome_arquivo_frases, newline='', encoding='utf-8') as csvfile: #'encoding: utf-8' serve para ler o arquivo em utf-8, assim evitando problemas com acentuação
        leitor = csv.reader(csvfile, delimiter=';') 
        for linha in leitor:
            frases.append(linha)
    return frases

def le_ultimo_id_lido(nome_arquivo): #Função que lê o ultimo id lido pelo bot que fica salvo em um .txt separado
    f_read = open(nome_arquivo, 'r')
    ultimo_id_lido = int(f_read.read().strip())
    f_read.close()
    return ultimo_id_lido

def guarda_ultimo_id_lido(ultimo_id_lido, nome_arquivo): #Função que salva o ultimo id lido pelo bot
    f_write = open(nome_arquivo, 'w')
    f_write.write(str(ultimo_id_lido))
    f_write.close()
    return

def gerar_numeros_sorte(): #Função que gera seis números aleatórios de 0 a 60 e então os salva em um vetor
    i=0
    numeros = []
    while i<6:
        numeros.append(randint(0,60))
        i+=1
    numeros.sort() #Ordena o vetor em ordem crescente
    return numeros


def respondendo_tweets():
    print('BOT TRABALHANDO...')
    frases = le_frases()
    ultimo_id_lido = le_ultimo_id_lido(nome_arquivo)
    mentions = api.mentions_timeline(ultimo_id_lido , tweet_mode='extended') #Lê as menções ao bot e salva em um vetor
    for mention in reversed(mentions): #'reserved(mentions)' serve para ler o vetor do mais velho para o mais novo
        numeroAleatorio = randint(0,69)
        fraseFormatada = str(frases[numeroAleatorio]).replace('[', '').replace(']', '') #Formata a frase      
        numerosSorte = gerar_numeros_sorte()
        numerosSorteStr = str(numerosSorte[0])+', '+str(numerosSorte[1])+', '+str(numerosSorte[2])+', '+str(numerosSorte[3])+', '+str(numerosSorte[4])+', ' +str(numerosSorte[5]) #Formata os números
        print(str(mention.id) + ' - ' + mention.full_text)
        ultimo_id_lido = mention.id
        guarda_ultimo_id_lido(ultimo_id_lido, nome_arquivo) #Salva o id lido
        if '@biscoitosort' in mention.full_text.lower(): #Verificação apenas para garantir que o bot vai ler todas menções, independente de letra maiúscula ou minúscula
            print('Respondendo tweet')
            api.update_status('Olá @' + mention.user.screen_name + '! 🥠 Seu biscoito da sorte é: '+ fraseFormatada + '   🍀 Seus números da sorte são: '+ numerosSorteStr, mention.id)

while True: #Loop que a atualiza o bot a cada 60 segundos
    respondendo_tweets()    
    time.sleep(60)

