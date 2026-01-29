# 🚀 Guia de Início Rápido

## Instalação em 5 Minutos

### 1. Instale o Ollama

**Windows/Mac:**
- Acesse [ollama.ai](https://ollama.ai)
- Baixe e instale o executável
- Abra o terminal e execute:

```bash
ollama pull llama3.1
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1
ollama serve
```

### 2. Clone e Configure o Projeto

```bash
# Clone o repositório
git clone https://github.com/euwalteraugusto/agent-adam.git
cd agent-adam

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente (Windows)
venv\Scripts\activate

# Ative o ambiente (Linux/Mac)
source venv/bin/activate

# Instale dependências
cd src
pip install -r requirements.txt
```

### 3. Execute a Aplicação

```bash
streamlit run app.py
```

### 4. Acesse no Navegador

Abra: **http://localhost:8501**

---

## Solução de Problemas Comuns

### ❌ Erro: "Connection refused" ao Ollama

**Solução:**
```bash
# Certifique-se que o Ollama está rodando
ollama serve

# Em outro terminal, teste
ollama run llama3.1 "Olá"
```

### ❌ Erro: "Module not found"

**Solução:**
```bash
# Verifique se está no ambiente virtual
which python  # Deve mostrar path do venv

# Reinstale dependências
pip install -r requirements.txt
```

### ❌ Página em branco no Streamlit

**Solução:**
```bash
# Limpe o cache
streamlit cache clear

# Execute novamente
streamlit run app.py
```

---

## Primeiros Passos

### 1. Explore a Interface

- **💬 Aba Conversa**: Faça perguntas ao agente
- **📊 Aba Análise**: Veja gráficos de gastos
- **🎯 Aba Recomendações**: Produtos personalizados
- **📚 Aba Educação**: Aprenda conceitos

### 2. Perguntas para Testar

Experimente perguntar:

```
"Onde estou gastando mais dinheiro?"
"Quanto posso investir por mês?"
"Qual o melhor investimento para mim?"
"Como criar uma reserva de emergência?"
"Preciso de quanto para comprar uma casa em 5 anos?"
```

### 3. Personalize Seus Dados

Edite os arquivos em `data/`:

- **perfil_investidor.json**: Seu perfil e objetivos
- **transacoes.csv**: Suas transações
- **produtos_financeiros.json**: Produtos disponíveis

---

## Próximos Passos

1. ✅ Leia a [documentação completa](./docs/)
2. ✅ Customize o agente para seu caso de uso
3. ✅ Contribua com melhorias
4. ✅ Compartilhe com amigos!

---

**Precisa de ajuda?** Abra uma [issue](https://github.com/seu-usuario/agente-financeiro/issues)
