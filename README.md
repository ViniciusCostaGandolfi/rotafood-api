# Backend RotaFoodAPI

Olá, eu me chamo Vinícius e estou desenvolvendo a aplicação RotaFood. Esta 
aplicação é basicamente um sistema para roterização para estabelecimentos de 
entrega de comida com um sistema para gestão de pedidos, rotas, menu, etc acoplado.

Roterizar suas entregas poupa o tempo para gerenciar seus entregadores, poupa 
o tempo para relizar todas as suas entregas, fideliza seus clientes pois a 
coomida chegará mais rapido e quente na cada deles. Mande os pedidos para a 
cozinha por ROTA, logo, haverá menos tempo entre um pedido ficar pronto e sair 
para entrega!

# Porque Dividi em Dois Serviços?

Pela natureza do problema resolvido, o Capacited Vehicle Routine Problemn foi necessário 
dividir o backend em dois serviços, um que cuida do banco de dados, outro que cuida da 
roterização em si, que por mais otmizada que eu, Saulo e Cristiano tenhamos deixado o 
nosso modelo, cerca de 100 pontos de entrega roterizados por segundo. Deixar tudo em grande 
monolito poderia acarretar demora em algum usuário que sómente quisesse ver o cardapio, 
pela competição dos recursos da maquina.
Em relação a microserviços, não tenho usuários ainda, logo Monolitics First!!! Microserviços 
apenas iriam atrasar o desenvlvimento deste aplicativo. No futuro se precisar irei dividir, 
atualmente vou apenas retirar a camada de Roterização poque ela é demorada.
(Machine Learning && Operation Research is SLOW)

# Porque utilizar FastAPI invez de Django?

Escolhi o framework FastAPI porque além de ja ter suporte a async e await do python, ele 
utiliza o Pydantic para validar fortemente os tipos e entruturas de dados. O Python por 
mais que seja dinamicamente tippado, atualmente este esta desenvolvendo ferramentas para 
tippagem de dados.
(For APIs FastAPI WIN!)


# Postgres ou MongoDB?

Escolhi o banco de dados Postgres pois para a maioria dos projetos um banco relacional é 
mais do que o necessário, NoSQL é bom, porem não havia necessidade neste projeto. 
Além disso o Postgres é open source!
(I prefer Relational DataBases)



## Entidades do Banco de Dados

***
## Estas entidades cuidam da authenticação, usuários e restaurantes
### Merchant
### MerchantUser

***
## Esta entidades cuida dos Endereços
### Address

***
## Estas entidades cuida dos produtos e suas opções
### Product
### ProductOptionGroup
### ProductOption

***
## Estas entidades cuida dos pedidos e suas opções
### Order
### OrderDelivery
### OrderCustomer
### OrderPayment
### OrderItem
### OrderItemOption

***
## Estas entidades cuida das rotas
### Route
### RouteOrder

***
## Estas entidades cuidam dos menus
### Catalog
### CatalogItem

***
## Estas entidades cuidam da integração com IFood
### IFoodMerchant
### IFoodOrder
### IFoodProduct
