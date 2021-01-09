#Final Version 
import tweepy
import time
import csv
import os
from os import environ
from random import randint

CONSUMER_KEY = environ['API_KEY'] #Autenticadores do Twitter
CONSUMER_SECRET = environ['API_KEY_SECRET']
ACCESS_KEY = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler('API_KEY','API_KEY_SECRET')
auth.set_access_token('ACCESS_TOKEN', 'ACCESS_SECRET')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
nome_arquivo_frases = 'frases.csv'
nome_arquivo = 'ultimo_id_lido.txt'

def le_frases():
    
    frases = []
    with open(nome_arquivo_frases, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile, delimiter=';') 
        for linha in leitor:
            frases.append(linha)

    return frases

def le_ultimo_id_lido(nome_arquivo):
    f_read = open(nome_arquivo, 'r')
    ultimo_id_lido = int(f_read.read().strip())
    f_read.close()
    return ultimo_id_lido

def guarda_ultimo_id_lido(ultimo_id_lido, nome_arquivo):
    f_write = open(nome_arquivo, 'w')
    f_write.write(str(ultimo_id_lido))
    f_write.close()
    return

def gerar_numeros_sorte():
    i=0
    numeros = []
    while i<6:
        numeros.append(randint(0,60))
        i+=1
    numeros.sort()
    return numeros


def respondendo_tweets():
    print('BOT TRABALHANDO...')
    frases = le_frases()
    ultimo_id_lido = le_ultimo_id_lido(nome_arquivo)
    mentions = api.mentions_timeline(ultimo_id_lido , tweet_mode='extended')
    for mention in reversed(mentions):
        numeroAleatorio = randint(0,69)
        fraseFormatada = str(frases[numeroAleatorio]).replace('[', '').replace(']', '')      
        numerosSorte = gerar_numeros_sorte()
        numerosSorteStr = str(numerosSorte[0])+', '+str(numerosSorte[1])+', '+str(numerosSorte[2])+', '+str(numerosSorte[3])+', '+str(numerosSorte[4])+', ' +str(numerosSorte[5])
        print(str(mention.id) + ' - ' + mention.full_text)
        ultimo_id_lido = mention.id
        guarda_ultimo_id_lido(ultimo_id_lido, nome_arquivo)
        if '@biscoitosort' in mention.full_text.lower(): 
            print('Respondendo tweet')
            api.update_status('Olá @' + mention.user.screen_name + '! 🥠 Seu biscoito da sorte é: '+ fraseFormatada + '   🍀 Seus números da sorte são: '+ numerosSorteStr, mention.id)

while True:
    respondendo_tweets()    
    time.sleep(60)

