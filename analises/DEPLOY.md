# Guia de Deploy - Análise Mari Doutorado

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Acesso SSH ao servidor
- 4GB RAM (mínimo)

## 🚀 Deploy em Servidor Linux

### 1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3 python3-pip python3-venv -y

# Criar diretório do projeto
mkdir -p ~/mari_analise
cd ~/mari_analise
```

### 2. Upload dos Arquivos

Transfira os arquivos para o servidor:

```bash
# Usando scp (do seu computador local)
scp -r analises/* usuario@servidor:~/mari_analise/

# Ou usando rsync
rsync -avz analises/ usuario@servidor:~/mari_analise/
```

### 3. Configurar Ambiente Virtual

```bash
cd ~/mari_analise

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 4. Configurar Caminhos

Edite `config.py` para ajustar os caminhos dos dados:

```bash
nano config.py
```

Ajuste as variáveis:
```python
CAMINHO_BASE = "/caminho/completo/para/dados/csv"
CAMINHO_2022 = "/caminho/completo/para/dados/csv/2022"
CAMINHO_2023 = "/caminho/completo/para/dados/csv/2023"
CAMINHO_2024 = "/caminho/completo/para/dados/csv/2024"
```

### 5. Testar Execução

```bash
# Teste rápido
python main.py --rapido

# Se funcionar, teste completo
python main.py --salvar ./output
```

## 🌐 Deploy da API Flask

### Opção 1: Servidor de Desenvolvimento (Teste)

```bash
# Adicionar Flask ao requirements
echo "flask>=2.3.0" >> requirements.txt
pip install flask

# Executar API
python app.py
```

Acesse: `http://seu-servidor:5000`

### Opção 2: Produção com Gunicorn

#### Instalar Gunicorn

```bash
pip install gunicorn
```

#### Criar arquivo de serviço systemd

```bash
sudo nano /etc/systemd/system/mari-api.service
```

Conteúdo:

```ini
[Unit]
Description=Mari Doutorado API
After=network.target

[Service]
User=seu_usuario
Group=www-data
WorkingDirectory=/home/seu_usuario/mari_analise
Environment="PATH=/home/seu_usuario/mari_analise/venv/bin"
ExecStart=/home/seu_usuario/mari_analise/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

#### Iniciar serviço

```bash
sudo systemctl daemon-reload
sudo systemctl start mari-api
sudo systemctl enable mari-api
sudo systemctl status mari-api
```

### Opção 3: Com Nginx como Reverse Proxy

#### Instalar Nginx

```bash
sudo apt install nginx -y
```

#### Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/mari-api
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /home/seu_usuario/mari_analise/output;
    }
}
```

#### Ativar site

```bash
sudo ln -s /etc/nginx/sites-available/mari-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## ⏰ Execução Agendada (Cron)

### Criar script de execução

```bash
nano ~/mari_analise/run_analysis.sh
```

Conteúdo:

```bash
#!/bin/bash
cd /home/seu_usuario/mari_analise
source venv/bin/activate
python main.py --salvar /var/www/html/graficos >> logs/analise.log 2>&1
```

Tornar executável:

```bash
chmod +x ~/mari_analise/run_analysis.sh
mkdir -p ~/mari_analise/logs
```

### Configurar Cron

```bash
crontab -e
```

Adicionar linha (executa diariamente às 2:00 AM):

```cron
0 2 * * * /home/seu_usuario/mari_analise/run_analysis.sh
```

Ou semanalmente (Domingo às 3:00 AM):

```cron
0 3 * * 0 /home/seu_usuario/mari_analise/run_analysis.sh
```

## 🐳 Deploy com Docker (Avançado)

### Criar Dockerfile

```bash
nano Dockerfile
```

Conteúdo:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar diretório para outputs
RUN mkdir -p /app/output

# Expor porta
EXPOSE 5000

# Comando padrão
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Criar docker-compose.yml

```yaml
version: '3.8'

services:
  mari-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./dados:/app/dados:ro
      - ./output:/app/output
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### Build e Executar

```bash
docker-compose up -d
```

## 🔐 Segurança

### 1. Firewall

```bash
# Permitir apenas portas necessárias
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. HTTPS com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```

### 3. Autenticação na API (Opcional)

Adicione autenticação básica no Nginx:

```bash
sudo apt install apache2-utils -y
sudo htpasswd -c /etc/nginx/.htpasswd usuario
```

Configure no Nginx:

```nginx
location / {
    auth_basic "Área Restrita";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://127.0.0.1:5000;
}
```

## 📊 Monitoramento

### Logs

```bash
# Ver logs da aplicação
tail -f ~/mari_analise/logs/analise.log

# Ver logs do Gunicorn
journalctl -u mari-api -f

# Ver logs do Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Verificar Uso de Recursos

```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# Processos Python
ps aux | grep python
```

## 🔄 Atualização

### Atualizar Código

```bash
cd ~/mari_analise
source venv/bin/activate

# Backup
cp -r . ../mari_analise_backup_$(date +%Y%m%d)

# Atualizar arquivos
# (fazer upload dos novos arquivos)

# Reinstalar dependências se necessário
pip install -r requirements.txt --upgrade

# Reiniciar serviço
sudo systemctl restart mari-api
```

## 🐛 Troubleshooting

### API não inicia

```bash
# Verificar logs
journalctl -u mari-api -n 50

# Verificar permissões
ls -la ~/mari_analise

# Verificar ambiente virtual
source venv/bin/activate
which python
```

### Memória insuficiente

Reduzir workers do Gunicorn:

```bash
# Em vez de -w 4, usar -w 2
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

### Erros de importação

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 📞 Comandos Úteis

```bash
# Status do serviço
sudo systemctl status mari-api

# Parar serviço
sudo systemctl stop mari-api

# Iniciar serviço
sudo systemctl start mari-api

# Reiniciar serviço
sudo systemctl restart mari-api

# Ver logs em tempo real
journalctl -u mari-api -f

# Testar Nginx
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

---

**Importante:** Sempre teste em ambiente de desenvolvimento antes de fazer deploy em produção!
