import redis
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://Mariana:MatPetErAt@cluster0.jgkawuu.mongodb.net/mercadolivre")
db = client.test

global mydb
mydb = client.mercadolivre

dbRedis = redis.Redis(host='redis-13198.c289.us-west-1-2.ec2.cloud.redislabs.com',
                      port=13198,
                      password='BatatinhaQuandoNasce')


def Login(cpf):
    mycol = mydb.usuario
    usuario = {"cpf": cpf}

    usu = mycol.find_one(usuario)
    print(usu)

    status = dbRedis.hget('usu:' + cpf, 'status')

    if (status != None):
        print('O usuário está logado')
    else:
        dbRedis.hset('usu:' + usu['cpf'], 'status', 'logged in')
        print(dbRedis.hget('usu:' + usu['cpf'], 'status'))

#Login("123.456.789.01")

def Logout(cpf):
    mycol = mydb.usuario
    usuario = {"cpf": cpf}
    usu = mycol.find_one(usuario)
    status = dbRedis.hget('usu:' + cpf, 'status')

    if (status == None):
        dbRedis.hset('usu:' + usu['cpf'], 'status', 'logged out')
        print(dbRedis.hget('user:' + usu['cpf'], 'status'))
    else:
        print('O usuário está deslogado!')

#Logout("123.456.789.01")

def AtualizarPrecoProd(id, preco):
    mycol = mydb.produto
    produto = mycol.find_one(ObjectId(id))

    dbRedis.hset('produto:' + id, 'preco', preco)

    mycol.update_one({"_id": ObjectId(id)}, {"$set": {
        "preco": json.loads(dbRedis.hget("produto:" + id, 'preco')),
    }},
    upsert = True)

    print("Preço do produto atualizado")
    print(dbRedis.hget('produto:' + id, 'preco'))

#AtualizarPrecoProd("63613245fa706a8e279a9976", 10)

def AtualizarQuantProd(id, quantidade):
    mycol = mydb.produto
    produto = mycol.find_one(ObjectId(id))

    dbRedis.hset('produto:' + id, 'quantidade', quantidade)

    mycol.update_one({"_id": ObjectId(id)}, {"$set": {
        "quantidade": json.loads(dbRedis.hget("produto:" + id, 'quantidade')),
    }},
    upsert = True)

    print("Quantidade do produto atualizado")
    print(dbRedis.hget('produto:' + id, 'quantidade'))

#AtualizarQuantProd("636134956254f079e64a6554", "10")