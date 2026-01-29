#!/bin/bash

# Script de Instalação Automática - FinanceAI
# Execute: bash setup.sh

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          💰 FinanceAI - Instalação Automática            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Verificar Python
echo -e "\n${YELLOW}[1/5]${NC} Verificando Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo -e "${RED}✗${NC} Python não encontrado!"
    echo -e "${YELLOW}Por favor, instale Python 3.8+ em: https://www.python.org/downloads/${NC}"
    exit 1
fi

# Verificar versão do Python
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}✗${NC} Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
    exit 1
fi

# 2. Verificar pip
echo -e "\n${YELLOW}[2/5]${NC} Verificando pip..."
if command_exists pip3; then
    echo -e "${GREEN}✓${NC} pip encontrado"
    PIP_CMD="pip3"
elif command_exists pip; then
    echo -e "${GREEN}✓${NC} pip encontrado"
    PIP_CMD="pip"
else
    echo -e "${RED}✗${NC} pip não encontrado!"
    echo -e "${YELLOW}Instalando pip...${NC}"
    $PYTHON_CMD -m ensurepip --default-pip
    PIP_CMD="pip"
fi

# 3. Verificar Ollama
echo -e "\n${YELLOW}[3/5]${NC} Verificando Ollama..."
if command_exists ollama; then
    echo -e "${GREEN}✓${NC} Ollama encontrado"
    
    # Verificar se modelo está instalado
    if ollama list | grep -q "llama3.2"; then
        echo -e "${GREEN}✓${NC} Modelo llama3.2 já instalado"
    else
        echo -e "${YELLOW}Modelo llama3.2 não encontrado.${NC}"
        read -p "Deseja baixar agora? (s/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            echo -e "${YELLOW}Baixando llama3.2... (isso pode levar alguns minutos)${NC}"
            ollama pull llama3.2
            echo -e "${GREEN}✓${NC} Modelo baixado com sucesso!"
        else
            echo -e "${YELLOW}⚠${NC} Você precisará baixar o modelo manualmente:"
            echo "   ollama pull llama3.2"
        fi
    fi
else
    echo -e "${RED}✗${NC} Ollama não encontrado!"
    echo -e "${YELLOW}Por favor, instale Ollama:${NC}"
    echo "   Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   Windows:   https://ollama.ai/download/OllamaSetup.exe"
    exit 1
fi

# 4. Instalar dependências Python
echo -e "\n${YELLOW}[4/5]${NC} Instalando dependências Python..."
cd src
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependências instaladas"
else
    echo -e "${RED}✗${NC} Arquivo requirements.txt não encontrado!"
    exit 1
fi
cd ..

# 5. Verificar estrutura de dados
echo -e "\n${YELLOW}[5/5]${NC} Verificando estrutura de dados..."
if [ -d "data" ]; then
    echo -e "${GREEN}✓${NC} Pasta data/ encontrada"
    
    # Verificar arquivos necessários
    FILES=("perfil_investidor.json" "produtos_financeiros.json" "transacoes.csv" "historico_atendimento.csv")
    ALL_FILES_OK=true
    
    for file in "${FILES[@]}"; do
        if [ -f "data/$file" ]; then
            echo -e "  ${GREEN}✓${NC} $file"
        else
            echo -e "  ${RED}✗${NC} $file não encontrado"
            ALL_FILES_OK=false
        fi
    done
    
    if [ "$ALL_FILES_OK" = false ]; then
        echo -e "${YELLOW}⚠${NC} Alguns arquivos de dados estão faltando"
    fi
else
    echo -e "${RED}✗${NC} Pasta data/ não encontrada!"
    exit 1
fi

# Resumo e próximos passos
echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           ✅ Instalação Concluída com Sucesso!           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📝 Próximos Passos:${NC}"
echo ""
echo "1️⃣  Inicie o Ollama (em um terminal separado):"
echo -e "   ${YELLOW}ollama serve${NC}"
echo ""
echo "2️⃣  Execute o FinanceAI:"
echo -e "   ${YELLOW}cd src${NC}"
echo -e "   ${YELLOW}streamlit run app.py${NC}"
echo ""
echo "3️⃣  Ou teste via CLI:"
echo -e "   ${YELLOW}cd src${NC}"
echo -e "   ${YELLOW}$PYTHON_CMD test_agente.py${NC}"
echo ""
echo -e "${GREEN}💡 Dica:${NC} Mantenha o terminal do Ollama aberto enquanto usa o FinanceAI"
echo ""

# Perguntar se quer iniciar agora
read -p "Deseja iniciar o FinanceAI agora? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "\n${YELLOW}Verificando se Ollama está rodando...${NC}"
    
    # Tentar conectar ao Ollama
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama está rodando!"
        echo -e "\n${YELLOW}Iniciando FinanceAI...${NC}"
        cd src
        streamlit run app.py
    else
        echo -e "${RED}✗${NC} Ollama não está rodando!"
        echo -e "${YELLOW}Execute 'ollama serve' em outro terminal primeiro${NC}"
        echo ""
        read -p "Pressione Enter para continuar quando o Ollama estiver rodando..."
        cd src
        streamlit run app.py
    fi
fi

echo -e "\n${BLUE}Boa jornada financeira com IA! 💰🤖${NC}"
