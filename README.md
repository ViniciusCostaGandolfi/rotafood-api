## RotaFood API!

Me chamo Vinícius e estou desenvolvendo o [RotaFood](https://rotafood.com.br), ele é uma aplicação que resolve o problema de [roteirização](https://pt.wikipedia.org/wiki/Problema_de_roteamento_de_ve%C3%ADculos) de entregadores próprios de restaurantes. Utilizar entregadores por exemplo do IFood Entrega consome 27% do valor do pedido como taxa do IFood, tirando do fato de ter entregdores próprios garante entrega mais rápida. Inicialmente comecei fazer o backend completo do [RotaFood](https://rotafood.com.br) em Python com FastAPI, entretanto quando me deparei com um monolito tão grande utilizar o Javinha pareu fazer sentido. Além disso, quero aprender mais sobre Spring e Java!

Outro ponto que fez sentido é que as verções mais novas do Java como [Java 21](https://openjdk.org/projects/jdk/21/) (utilizado nestre projeto) tem acesso as [Virtual Threads](https://openjdk.org/jeps/444), deixando o Javinha +- parecido com Go, Kotlin ou Node. Com o Spring nessa versão que estou utilizando tambem posso utilizar clould native com [Spring Native](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html) se quiser containers menores.

### Arquitetura

Segui o [Monolithic First](https://medium.com/design-microservices-architecture-with-patterns/monolith-first-approach-before-moving-to-microservices-da969be8bf7c) para essa aplicação, posteriormente vou quebrar esse monolito em microserços, mas apenas quando necessário, por hora a única parte do backend do rotafood que não vai participar do monolito é o serviço de roteirização. Pois o mesmo pode demorar alguns segundo utilizando 100% da CPU para roteirizar multiplos pedidos ao mesmo tempo, travando o servidor de dados.

### Mensageria

Ainda estou cogitando utilizar [RabbitMQ](https://www.rabbitmq.com/) para mensageria assíncrona, como disse, o quando poder dessa aplicação esta na [roteirização](https://pt.wikipedia.org/wiki/Problema_de_roteamento_de_ve%C3%ADculos), que é feita em outro serviço que pode demorar +- 1s para roterizar 100 pontos, logo dependendo do fluxo de usuários será necessário.


### Containers

Com toda certeza vou utilizar [Docker](https://www.docker.com/) neste projeto, [Docker](https://www.docker.com/) auxilia demais para deploys automatizados! Estou usando uma hospedagem que chama Railway, que consiste basicamente em Dockerfiles.


### Banco de Dados

Optei por o bom e velho [PostgreSQL](https://www.postgresql.org/), para 99% das aplicações um banco de dados relacional como o [POSTGRESQL](https://www.postgresql.org/) é mais que o suficiente, além de ser open source e de licensa aberta.


### E o Frontend?

O [Frontend](https://github.com/ViniciusCostaGandolfi/rotafood-web) estou desenvolvendo em [Angular](https://angular.io/), inicialmente estou fazendo um SPA, entretanto estou cogitando alterar para SSR, um dos novos recursos do [Angular](https://angular.io/).
