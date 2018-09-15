#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#Autor @DN
import json
import requests
import getpass
from time import sleep
import random

User=""
Password=""

Apuestas=""

URL="http://api.playfulbet.com/"
Coins=0

def getDataConexion():
    code=0
    URLS=URL+"v2/sessions" 
    headers={'content-type':'application/x-www-form-urlencoded','Accept': 'application/json'}

    print("Introduce datos de inicio de sesión")
    while str(code) != '200':
        User=raw_input("Usuario: ")
        Password=str(getpass.getpass("Contraseña: "))

        Data='user_login[login]='+User+'&user_login[password]='+Password

        dt=requests.post(URLS,headers=headers,data=Data)
        code=dt.status_code
        if str(code) != '200':
            print("Introduzca los datos correctos")
    global Coins
    Coins=json.loads(dt.text)['points']
    dta={'auth_token':json.loads(dt.text)['auth_token']}#,'Coins':json.loads(dt.text)['points']}

    return dta
def getevent():
    
    dt=getDataConexion()
    
    print("0 Próximos")
    print("1 Populares")
    print("2 Social")

    tipo=input("Tipo: ")

    if tipo == 0:
        dt['type']='next'

    elif tipo == 1:
        dt['type']='popular'

    elif tipo == 2:
        dt['type']='social'

    else:
        dt['type']='next'


   
   


   
    global Coins
    limit=int(input("Introduce límite de coins: "))
    for i in range(1,32):
        
        if Coins>=limit and Coins>=200:
            dt['page'] =str(i)
            e=requests.get(URL+'v1/events/',data=dt)
            bet(comprubet(e.text),dt,limit)
        else:
            print("No quedan Puntos")
            break



def bet(data,dt,limit):
    headers={'content-type':'application/x-www-form-urlencoded'} #,'Host': 'api.playfulbet.com','Referer': 'http://api.playfulbet.com/eventos/286466'}
    #Coins = dt['Coins']
    global Coins
   
    #Coins = int(input("introduce el número de puntos a usar"))
    if Coins>=limit and Coins >=500:
        for i in data:
            if Coins>=500:
                idp=getID(i)
                dt['option_id']= idp# id
                dt['points']= 500 # coins
                e= requests.post(URL+'jugadas',data=dt,headers=headers)
                if e.status_code == 200:
                    Coins=Coins-200
                else:
                    break
            else:
                 break
            es=random.uniform(10,30)
            print('esperando ', es, 's')
            sleep(es)

    else:
        print("Sin coins")

    print("Hecho")


def comprubet(data):
    id=[]
    global Apuestas
    if Apuestas != 7:

        for i in json.loads(data):

            if len(i['current_user_coins_bet']) == 0 and i['sport_id'] == Apuestas:
                id.append(i['id'])

    else:
        
       for i in json.loads(data):

            if len(i['current_user_coins_bet']) == 0:
                id.append(i['id']) 


    return id


def getID(id):

    e=requests.get(URL+'v3/events/'+str(id))
    actual = json.loads(e.text)['markets'][0]['market_options'][0]['odds']
    num= json.loads(e.text)['markets'][0]['market_options'][0]['id']
    comparar=0
    for i in range(len(json.loads(e.text)['markets'][0]['market_options'])-1):
        comparar = json.loads(e.text)['markets'][0]['market_options'][i+1]['odds']
        if actual>comparar:
            actual=comparar
            num= json.loads(e.text)['markets'][0]['market_options'][i+1]['id']
        

    print (num, " nombre : ", json.loads(e.text)['name']," " ,actual)


    return num


def main():
    
    global Apuestas 
    
    print("Opción 0 Fútbol")
    print("Opción 1 Baloncesto")
    print("Opción 2 Tenis")
    print("Opción 3 e-sports")

    opcion = int(input("Introduce la opción de apuesta: "))

    if 0 == opcion:
        Apuestas=1
    elif 1 == opcion:
        Apuestas= 2
    elif 2 == opcion:
        Apuestas= 3
    elif 3 == opcion:
        Apuestas = 4

    else:
        Apuestas = 7
   
    print("Token...")
    getevent()

main()
