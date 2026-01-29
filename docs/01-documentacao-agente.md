# 📋 Documentação do Agente Financeiro

## 1. Caso de Uso

### Problema que o Agente Resolve

O **Adam** é um consultor financeiro virtual que resolve os seguintes problemas:

1. **Falta de Orientação Personalizada**: Muitas pessoas não têm acesso a consultoria financeira profissional
2. **Dificuldade em Tomar Decisões**: Escolher entre diversos produtos financeiros pode ser confuso
3. **Desconhecimento do Próprio Perfil**: As pessoas não sabem identificar seu perfil de risco
4. **Gastos Descontrolados**: Falta de visibilidade sobre onde o dinheiro está sendo gasto
5. **Baixo Nível de Educação Financeira**: Desconhecimento sobre conceitos básicos de investimento

### Soluções Oferecidas

- ✅ **Consultoria Proativa**: Antecipa necessidades baseado no perfil e histórico
- ✅ **Recomendações Personalizadas**: Sugere produtos adequados ao perfil de risco
- ✅ **Análise de Gastos**: Identifica padrões e oportunidades de economia
- ✅ **Educação Financeira**: Explica conceitos de forma acessível
- ✅ **Segurança nas Respostas**: Sistema anti-alucinação garante informações confiáveis

---

## 2. Persona e Tom de Voz

### Identidade do Agente

**Nome**: Adam  
**Papel**: Consultor Financeiro Pessoal  
**Personalidade**: Profissional, empático, educativo e encorajador

### Características do Tom de Voz

- **Profissional mas Acessível**: Usa linguagem técnica quando necessário, mas sempre explica de forma clara
- **Empático**: Entende as preocupações e objetivos do cliente
- **Educativo**: Ensina conceitos ao invés de apenas dar respostas prontas
- **Encorajador**: Motiva o cliente a tomar decisões melhores
- **Transparente**: Admite quando não sabe algo e sugere alternativas

### Exemplos de Interação

**❌ Incorreto (tom técnico demais):**
> "Seu portfólio apresenta uma alocação inadequada em ativos de renda variável considerando seu baixo apetite ao risco."

**✅ Correto (tom do Adam):**
> "Olá! Notei que você tem alguns investimentos em ações, mas seu perfil indica que você prefere segurança. Que tal conversarmos sobre rebalancear sua carteira para produtos mais conservadores como CDBs? Posso te explicar as diferenças!"

---

## 3. Arquitetura do Sistema

### Fluxo de Dados

```
┌─────────────────┐
│   Usuário       │
│  (Interface)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit      │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AgenteFinanceiro│
│   (Orquestrador)│
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌─────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ Ollama  │ │Perfil│ │Transações│ │Produtos│
│  (LLM)  │ │ JSON │ │   CSV    │ │  JSON  │
└─────────┘ └──────┘ └────────┘ └────────┘
```

### Componentes Principais

1. **Interface (Streamlit)**
   - Apresenta chat interativo
   - Exibe análises visuais
   - Mostra recomendações

2. **Agente (Python)**
   - Orquestra conversas
   - Processa dados do cliente
   - Verifica segurança das respostas

3. **LLM (Ollama)**
   - Gera respostas em linguagem natural
   - Usa modelo Llama 3.1
   - Executa localmente (gratuito)

4. **Base de Conhecimento**
   - Perfil do investidor (JSON)
   - Histórico de transações (CSV)
   - Produtos disponíveis (JSON)
   - Histórico de atendimento (CSV)

---

## 4. Segurança e Anti-Alucinação

### Estratégias Implementadas

#### 4.1. Validação de Valores
```python
# Verifica valores muito altos nas respostas
if valor > MAX_VALOR_SUGESTAO_INVESTIMENTO:
    adicionar_alerta("Valor elevado detectado")
```

#### 4.2. Detecção de Promessas Inadequadas
```python
# Palavras proibidas que indicam alucinação
palavras_proibidas = [
    'garantido', 
    'garantia de retorno', 
    'sem risco', 
    'lucro certo'
]
```

#### 4.3. Contexto Restrito
- O agente **só usa dados fornecidos**
- Não inventa informações sobre produtos
- Admite quando não sabe algo

#### 4.4. Verificação de Perfil
- Respeita o perfil de risco do cliente
- Não sugere produtos inadequados
- Alerta sobre riscos

### Exemplo de Resposta Segura

**Pergunta do usuário**: "Quanto vou ganhar se investir R$ 10.000?"

**❌ Resposta com Alucinação:**
> "Você vai ganhar com certeza R$ 2.000 ao ano sem nenhum risco!"

**✅ Resposta Segura do FinanceAI:**
> "O retorno depende do produto escolhido e das condições do mercado. Por exemplo, um CDB que rende 100% do CDI (cerca de 12,5% ao ano) poderia gerar aproximadamente R$ 1.250 em um ano, mas isso não é garantido pois o CDI pode variar. Quer que eu te mostre algumas opções adequadas ao seu perfil moderado?"

---

## 5. Funcionalidades Principais

### 5.1. Conversação Inteligente
- Chat interativo
- Memória de contexto
- Respostas personalizadas

### 5.2. Análise Financeira
- Dashboard com métricas
- Gráficos de gastos
- Insights automáticos

### 5.3. Recomendação de Produtos
- Filtragem por perfil
- Score de adequação
- Simulação de retorno

### 5.4. Educação Financeira
- Conceitos explicados
- Recursos úteis
- Exemplos práticos

---

## 6. Diferenciais Competitivos

| Característica | FinanceAI | Chatbots Tradicionais |
|----------------|-----------|----------------------|
| Personalização | ✅ Alta | ❌ Baixa |
| Proatividade | ✅ Antecipa necessidades | ❌ Apenas reativo |
| Segurança | ✅ Anti-alucinação | ❌ Pode inventar dados |
| Educação | ✅ Ensina conceitos | ❌ Apenas responde |
| Gratuito | ✅ Usa Ollama local | ❌ APIs pagas |

---

## 7. Limitações e Melhorias Futuras

### Limitações Atuais
- Dados mockados (não conectado a banco real)
- Sem persistência de conversas
- Ollama precisa estar instalado localmente

### Melhorias Planejadas
- [ ] Integração com Open Banking
- [ ] Histórico de conversas
- [ ] Alertas proativos por email/SMS
- [ ] Análise preditiva com ML
- [ ] Suporte a múltiplos idiomas

---

## 8. Casos de Uso Expandidos

### Caso 1: Cliente Quer Comprar Imóvel
**Objetivo**: Auxiliar no planejamento de compra

**Fluxo**:
1. Agente pergunta valor do imóvel desejado
2. Analisa capacidade de poupança
3. Sugere consórcio ou financiamento
4. Recomenda investimentos para acumular entrada
5. Cria plano de ação mensalizado

### Caso 2: Cliente Quer Começar a Investir
**Objetivo**: Orientar primeiro investimento

**Fluxo**:
1. Identifica perfil de risco
2. Verifica reserva de emergência
3. Sugere produtos adequados
4. Explica conceitos básicos
5. Simula retornos

### Caso 3: Cliente Quer Economizar
**Objetivo**: Reduzir gastos desnecessários

**Fluxo**:
1. Analisa histórico de transações
2. Identifica categorias com gastos altos
3. Sugere alternativas de economia
4. Define metas mensais
5. Monitora progresso

---

**Data de Criação**: Janeiro 2026  
**Versão**: 1.0.0  
**Autor**: Walter Fonseca
