# Student Management System - Docker Swarm Deployment

Este projeto implementa um sistema de gerenciamento de estudantes usando Flask, PostgreSQL e Docker Swarm com 2 réplicas.

## 👨‍💻 Informações do Desenvolvedor

- **Nome:** Nguyễn Minh Phúc
- **Profissão:** Estudante do 4º ano em Ciência da Computação  
- **Foco:** DevSecOps

## 🏗️ Arquitetura do Sistema

### Componentes Principais:
- **Frontend:** HTML e CSS puro
- **Backend:** Python Flask com APIs REST
- **Banco de dados:** PostgreSQL
- **Load Balancer:** Nginx
- **Orquestração:** Docker Swarm
- **Repositório de Imagens:** Docker Hub

### Funcionalidades:
1. **Página inicial** - Apresentação pessoal
2. **Sistema de autenticação** - Login para acesso administrativo
3. **Gerenciamento de estudantes:**
   - Visualizar lista de estudantes
   - Adicionar novos estudantes
   - Editar informações dos estudantes
   - Excluir estudantes

### Campos dos Estudantes:
- Código do Estudante (ID único)
- Nome completo
- Idade
- Curso/Área de estudo
- Ano de ingresso
- GPA (Média de notas)

## 🚀 Guia de Implantação

### Pré-requisitos:
- Docker Engine 20.10+
- Docker Compose 2.0+
- Conta no Docker Hub
- Sistema Linux/Ubuntu

### 1. Preparação do Ambiente

```bash
# Clone ou baixe os arquivos do projeto
git clone <seu-repositorio>
cd student-management-system

# Copie o arquivo de configuração
cp .env.example .env

# Edite o arquivo .env com suas credenciais
nano .env
```

### 2. Configuração das Credenciais

Edite o arquivo `.env` e atualize:

```env
# Credenciais do Docker Hub
DOCKER_HUB_USERNAME=seu_usuario_dockerhub
DOCKER_HUB_TOKEN=seu_token_dockerhub
IMAGE_NAME=student-management-system

# Credenciais do Banco de Dados (altere para produção)
DB_PASSWORD=SuaSenhaSegura123!
SECRET_KEY=sua-chave-secreta-super-segura

# Credenciais do Admin (altere para produção)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=suaSenhaAdmin123!
```

### 3. Desenvolvimento Local

Para testar localmente com Docker Compose:

```bash
# Dar permissão aos scripts
chmod +x *.sh

# Iniciar ambiente de desenvolvimento
./dev-start.sh

# Parar ambiente de desenvolvimento
./dev-stop.sh
```

Acesse: http://localhost

### 4. Build e Push das Imagens

```bash
# Construir e enviar imagens para Docker Hub
./build-and-push.sh
```

### 5. Implantação com Docker Swarm

```bash
# Implantar no Docker Swarm (2 réplicas)
./deploy-swarm.sh

# Remover implantação
./remove-stack.sh
```

## 🔧 Estrutura do Projeto

```
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── home.html          # Página inicial
│   ├── login.html         # Página de login
│   └── dashboard.html     # Dashboard de gerenciamento
├── static/css/            # Arquivos CSS
│   └── style.css          # Estilos principais
├── Dockerfile             # Dockerfile da aplicação
├── Dockerfile.db          # Dockerfile do PostgreSQL
├── Dockerfile.nginx       # Dockerfile do Nginx
├── docker-compose.yml     # Configuração para desenvolvimento
├── docker-stack.yml       # Configuração para Docker Swarm
├── nginx.conf             # Configuração do Nginx
├── init-db.sql            # Scripts de inicialização do banco
├── .env                   # Variáveis de ambiente
├── .env.example           # Exemplo de configuração
└── scripts/               # Scripts de implantação
    ├── build-and-push.sh  # Build e push das imagens
    ├── deploy-swarm.sh    # Implantação no Swarm
    ├── dev-start.sh       # Iniciar desenvolvimento
    ├── dev-stop.sh        # Parar desenvolvimento
    └── remove-stack.sh    # Remover stack
```

## 🌐 URLs de Acesso

### Desenvolvimento Local:
- **Aplicação principal:** http://localhost
- **Acesso direto Flask:** http://localhost:5000
- **Banco de dados:** localhost:5432

### Produção (Docker Swarm):
- **Aplicação principal:** http://localhost (através do Nginx)
- **Visualizador do Swarm:** http://localhost:8080

## 🔐 Credenciais Padrão (ALTERE EM PRODUÇÃO!)

```
Usuário: admin
Senha: admin123
```

## 📊 Monitoramento e Gerenciamento

### Comandos Úteis do Docker Swarm:

```bash
# Ver status dos serviços
docker service ls

# Ver detalhes do stack
docker stack ps student-management

# Ver logs do serviço
docker service logs student-management_webapp

# Escalar serviço (alterar número de réplicas)
docker service scale student-management_webapp=4

# Atualizar serviço
docker service update student-management_webapp

# Ver nós do Swarm
docker node ls

# Ver visualizador do Swarm
# Acesse: http://localhost:8080
```

### Comandos de Debug:

```bash
# Executar bash dentro do container
docker exec -it $(docker ps -q -f name=webapp) bash

# Ver logs em tempo real
docker service logs -f student-management_webapp

# Verificar saúde dos serviços
docker service inspect student-management_webapp
```

## 🛡️ Considerações de Segurança

### Para Produção:
1. **Altere todas as senhas padrão**
2. **Use HTTPS com certificados SSL**
3. **Configure firewall apropriado**
4. **Use secrets do Docker Swarm para credenciais**
5. **Implemente backup regular do banco de dados**
6. **Monitor logs e métricas**

### Implementação de HTTPS:

```bash
# Gerar certificados SSL
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx-selfsigned.key -out nginx-selfsigned.crt

# Atualizar nginx.conf para usar SSL
# Adicionar certificados ao container Nginx
```

## 🔄 Pipeline CI/CD Sugerido

1. **Development:** Push para branch develop
2. **Build:** Automatizar build com GitHub Actions
3. **Test:** Executar testes automatizados
4. **Deploy to Staging:** Deploy automático para ambiente de teste
5. **Production:** Deploy manual após aprovação

## 📈 Escalabilidade

### Escalar Horizontalmente:
```bash
# Aumentar réplicas da aplicação
docker service scale student-management_webapp=5

# Adicionar nós ao Swarm
docker swarm join --token <token> <manager-ip>:2377
```

### Escalar Verticalmente:
- Aumentar recursos nos arquivos de configuração
- Atualizar limites de CPU e memória nos services

## 🚨 Troubleshooting

### Problemas Comuns:

1. **Serviço não inicia:**
   ```bash
   docker service logs student-management_webapp
   ```

2. **Banco de dados não conecta:**
   - Verificar credenciais no .env
   - Verificar se o serviço database está rodando

3. **Imagens não encontradas:**
   - Verificar se as imagens foram enviadas para Docker Hub
   - Verificar credenciais do Docker Hub

4. **Portas em uso:**
   - Parar outros serviços usando as mesmas portas
   - Alterar portas no docker-stack.yml

## 📞 Suporte

Para problemas ou dúvidas:
- Verificar logs dos serviços
- Consultar documentação do Docker Swarm
- Verificar issues no repositório

## 📄 Licença

Este projeto é para fins educacionais e demonstração de DevSecOps com Docker Swarm.

---
**Desenvolvido por Nguyễn Minh Phúc** - Estudante de Ciência da Computação focado em DevSecOps