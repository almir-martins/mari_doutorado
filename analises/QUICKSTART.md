# 🚀 Guia Rápido de Início

## ⚡ Instalação Rápida (5 minutos)

### 1. Verificar Python

```bash
python --version
# Deve ser Python 3.8 ou superior
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar caminhos dos dados

Edite `config.py` e ajuste os caminhos:

```python
CAMINHO_2022 = "../dados/csv/2022"  # Ajuste conforme necessário
CAMINHO_2023 = "../dados/csv/2023"
CAMINHO_2024 = "../dados/csv/2024"
```

### 5. Testar instalação

```bash
python test_instalacao.py
```

### 6. Executar análises

```bash
# Análise completa (com gráficos na tela)
python main.py

# Análise rápida (apenas estatísticas)
python main.py --rapido

# Salvar gráficos em arquivo
python main.py --salvar ./meus_graficos
```

---

## 🌐 Usar como API (Opcional)

### 1. Instalar Flask (se ainda não instalou)

```bash
pip install flask gunicorn
```

### 2. Iniciar servidor

```bash
# Desenvolvimento
python app.py

# Produção
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Testar API

Abra o navegador em: `http://localhost:5000`

Ou use curl:

```bash
curl http://localhost:5000/status
curl http://localhost:5000/analise/urgenza
curl http://localhost:5000/analise/resumo
```

---

## 📚 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `config.py` | Configurações e constantes |
| `utils.py` | Funções utilitárias |
| `analise_urgenza.py` | Análises de Categoria Urgenza |
| `analise_geral.py` | Análises gerais |
| `main.py` | Script principal |
| `app.py` | API Flask |
| `test_instalacao.py` | Teste de validação |

---

## 🎯 Comandos Mais Usados

```bash
# Executar análise completa
python main.py

# Análise sem gráficos (mais rápido)
python main.py --rapido

# Salvar gráficos
python main.py --salvar ./output

# Testar instalação
python test_instalacao.py

# Iniciar API
python app.py

# Ver ajuda
python main.py --help
```

---

## 🐛 Problemas Comuns

### Erro: "Module not found"

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "No such file or directory"

- Verifique os caminhos em `config.py`
- Certifique-se que as pastas de dados existem

### Gráficos não aparecem

- Em servidor sem GUI, use sempre `--salvar`
- Ou use a API Flask

### Memória insuficiente

- Use `python main.py --rapido`
- Reduza o número de workers no Gunicorn

---

## 📖 Documentação Completa

- **README.md** - Documentação geral
- **DEPLOY.md** - Guia de deploy em servidor
- **EXEMPLOS_API.md** - Exemplos de uso da API

---

## ✅ Checklist de Validação

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] Caminhos configurados em `config.py`
- [ ] Dados CSV disponíveis
- [ ] `test_instalacao.py` executado com sucesso
- [ ] `main.py` executado com sucesso

---

## 💡 Próximos Passos

1. **Desenvolvimento Local**
   - Executar análises
   - Personalizar gráficos
   - Adicionar novas análises

2. **Deploy em Servidor**
   - Seguir `DEPLOY.md`
   - Configurar Nginx/Apache
   - Configurar SSL

3. **Automatização**
   - Configurar cron jobs
   - Agendar relatórios
   - Monitorar execução

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique `test_instalacao.py`
2. Consulte a documentação completa
3. Verifique logs de erro

---

**Versão:** 1.0  
**Última atualização:** Dezembro 2025
