# 📊 Estratégia de Base de Conhecimento

## Visão Geral

A base de conhecimento do FinanceAI é composta por **dados estruturados** que alimentam o agente com informações contextuais sobre o cliente e produtos disponíveis.

---

## 1. Estrutura de Dados

### 1.1. Transações do Cliente (`transacoes.csv`)

**Objetivo**: Rastrear movimentações financeiras para análise de padrões

**Estrutura**:
```csv
data,descricao,categoria,valor,tipo
2024-01-15,Supermercado Extra,Alimentação,-250.00,debito
```

**Campos**:
- `data`: Data da transação (YYYY-MM-DD)
- `descricao`: Descrição da transação
- `categoria`: Categoria do gasto (Alimentação, Transporte, etc.)
- `valor`: Valor (positivo = receita, negativo = despesa)
- `tipo`: Tipo de transação (debito, credito, transferencia)

**Uso pelo Agente**:
- Análise de padrões de gastos
- Identificação de categorias com maiores despesas
- Cálculo de taxa de poupança
- Sugestões de economia

---

### 1.2. Perfil do Investidor (`perfil_investidor.json`)

**Objetivo**: Armazenar informações do cliente para personalização

**Estrutura**:
```json
{
  "cliente_id": "CLI-2024-001",
  "nome": "Maria Silva Santos",
  "idade": 35,
  "perfil_investidor": "moderado",
  "objetivos_financeiros": [...],
  "situacao_atual": {...}
}
```

**Seções Principais**:

#### Dados Demográficos
- Nome, idade, ocupação
- Estado civil, dependentes
- Escolaridade

#### Perfil de Risco
- `conservador`: Prioriza segurança
- `moderado`: Equilibra risco e retorno
- `arrojado`: Aceita riscos maiores

#### Objetivos Financeiros
- Comprar imóvel
- Criar reserva de emergência
- Planejar aposentadoria

#### Situação Atual
- Saldo em conta corrente
- Investimentos totais
- Dívidas
- Score de crédito

**Uso pelo Agente**:
- Personalizar tom de voz
- Filtrar produtos adequados
- Definir estratégias de investimento
- Calcular capacidade de poupança

---

### 1.3. Produtos Financeiros (`produtos_financeiros.json`)

**Objetivo**: Catálogo de produtos disponíveis para recomendação

**Estrutura**:
```json
{
  "produtos": [
    {
      "id": "PROD-001",
      "nome": "CDB Liquidez Diária",
      "tipo": "renda_fixa",
      "rentabilidade": "100% CDI",
      "perfil_recomendado": ["conservador", "moderado"]
    }
  ]
}
```

**Campos Principais**:
- `id`: Identificador único
- `nome`: Nome do produto
- `tipo`: Categoria (renda_fixa, fundos_imobiliarios, etc.)
- `rentabilidade`: Descrição da rentabilidade
- `rentabilidade_anual_estimada`: Percentual estimado
- `liquidez`: Prazo para resgate (D+0, D+1, etc.)
- `investimento_minimo`: Valor mínimo de aplicação
- `risco`: Nível de risco (muito_baixo, baixo, médio, alto)
- `tributacao`: Tipo de tributação
- `garantia_fgc`: Coberto pelo Fundo Garantidor de Créditos
- `perfil_recomendado`: Perfis adequados

**Uso pelo Agente**:
- Recomendação personalizada
- Comparação de produtos
- Cálculo de simulações
- Educação sobre produtos

---

### 1.4. Histórico de Atendimento (`historico_atendimento.csv`)

**Objetivo**: Manter contexto de interações anteriores

**Estrutura**:
```csv
data,tipo_atendimento,resumo,resolucao
2024-01-10,Dúvida,Cliente perguntou sobre taxas de investimento em CDB,Explicado taxas e rentabilidade
```

**Campos**:
- `data`: Data do atendimento
- `tipo_atendimento`: Tipo (Dúvida, Solicitação, Reclamação)
- `resumo`: Descrição breve
- `resolucao`: Como foi resolvido

**Uso pelo Agente**:
- Evitar repetir explicações
- Identificar padrões de dúvidas
- Personalizar abordagem
- Priorizar questões recorrentes

---

## 2. Pipeline de Dados

### Fluxo de Ingestão

```
┌─────────────────┐
│  Fontes de      │
│  Dados          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validação      │
│  (Schemas)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Normalização   │
│  (Limpeza)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Armazenamento  │
│  (CSV/JSON)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agente         │
│  (Consumo)      │
└─────────────────┘
```

### Validações Implementadas

#### Transações
- Data válida e no passado
- Valor numérico
- Categoria conhecida
- Tipo válido (debito/credito/transferencia)

#### Perfil
- Idade entre 18-100 anos
- Perfil de risco válido
- Renda mensal > 0
- Score de crédito entre 0-1000

#### Produtos
- ID único
- Rentabilidade válida
- Investimento mínimo > 0
- Perfis recomendados válidos

---

## 3. Estratégias de Enriquecimento

### 3.1. Agregações Automáticas

O agente calcula automaticamente:

**Por Período**:
- Gastos mensais por categoria
- Receita vs. Despesas
- Taxa de poupança

**Por Categoria**:
- Percentual de cada categoria no total
- Comparação com mês anterior
- Tendências de crescimento

**Métricas Derivadas**:
- Reserva de emergência necessária
- Capacidade de investimento mensal
- Score de saúde financeira

### 3.2. Contextualização Inteligente

Quando o usuário menciona:

| Palavra-chave | Dados Carregados |
|---------------|------------------|
| "investir" | Produtos recomendados ao perfil |
| "gastos" | Últimas transações negativas |
| "economizar" | Categorias com maiores despesas |
| "objetivos" | Objetivos financeiros do perfil |

---

## 4. Segurança e Privacidade

### Dados Sensíveis

**Não Armazenamos**:
- ❌ Senhas ou PINs
- ❌ Números de conta ou cartão
- ❌ CPF completo
- ❌ Dados biométricos

**Armazenamos com Segurança**:
- ✅ IDs anonimizados
- ✅ Agregações financeiras
- ✅ Preferências de investimento

### Compliance

**LGPD (Lei Geral de Proteção de Dados)**:
- Dados mockados para demonstração
- Em produção: criptografia end-to-end
- Anonimização de dados pessoais
- Consentimento explícito do usuário

---

## 5. Escalabilidade

### Atual (Mockado)
- 4 arquivos CSV/JSON
- ~20 transações
- 8 produtos
- 1 perfil de cliente

### Produção (Futuro)
- Banco de dados relacional (PostgreSQL)
- Milhões de transações
- Centenas de produtos
- Milhares de clientes

### Arquitetura Futura

```
┌─────────────────┐
│  Open Banking   │
│      API        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   (Dados)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Redis Cache   │
│   (Performance) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector DB      │
│  (Embeddings)   │
└─────────────────┘
```

---

## 6. Qualidade dos Dados

### Métricas de Qualidade

| Métrica | Alvo | Atual |
|---------|------|-------|
| Completude | >95% | 100% |
| Consistência | >98% | 100% |
| Atualização | Diária | Manual |
| Acurácia | >99% | 100% (mockado) |

### Monitoramento

Em produção, monitorar:
- Taxa de campos nulos
- Valores fora do esperado
- Duplicatas
- Integridade referencial

---

## 7. Exemplos de Queries

### Query 1: Gastos do Mês Atual
```python
df = pd.read_csv('transacoes.csv')
df['data'] = pd.to_datetime(df['data'])
mes_atual = df[df['data'].dt.month == datetime.now().month]
gastos = mes_atual[mes_atual['valor'] < 0]['valor'].sum()
```

### Query 2: Produtos para Perfil Moderado
```python
with open('produtos_financeiros.json') as f:
    produtos = json.load(f)
    
recomendados = [
    p for p in produtos['produtos']
    if 'moderado' in p['perfil_recomendado']
]
```

### Query 3: Categoria com Maior Gasto
```python
gastos_categoria = df[df['valor'] < 0].groupby('categoria')['valor'].sum()
maior_gasto = gastos_categoria.idxmin()
```

---

## 8. Roadmap de Dados

### Fase 1 (Atual) ✅
- Dados mockados em CSV/JSON
- Validações básicas
- Agregações simples

### Fase 2 (Próximos 3 meses)
- [ ] Integração com Open Banking
- [ ] Banco de dados relacional
- [ ] API de ingestão de dados

### Fase 3 (6 meses)
- [ ] Machine Learning para previsões
- [ ] Análise de sentimento de transações
- [ ] Detecção de anomalias

### Fase 4 (1 ano)
- [ ] Data Lake para analytics
- [ ] Embeddings para busca semântica
- [ ] Dashboard de BI para clientes

---

**Última Atualização**: Janeiro 2026  
**Responsável**: Equipe de Dados  
**Status**: ✅ Pronto para demonstração
