# 🎯 Atividade Aula 11 - Previsão e Camada Gold

**Equipe:** Tiago Monteiro, Luis Felipe Brigido, João Pedro Gomes, Pedro Calazans
**Disciplina:** Análise e Visualização de Dados
**Objetivo:** Usar o modelo da Aula 10 para prever vacinas de perfis novos e gravar na camada Gold

---

## ✅ Status: ATIVIDADE CONCLUÍDA

### Resultados
- ✅ Modelo salvo e carregado corretamente
- ✅ Acurácia validada: **81.50%** (igual ao train.py)
- ✅ 7 perfis novos criados e previstos
- ✅ Previsões gravadas na tabela `gold_previsoes`
- ✅ Código organizado em classes
- ✅ `modelos/` no .gitignore

---

## 📁 Estrutura do Projeto

```
etl-vacinacao-recife/
├── src/
│   ├── extract.py          # Extração da Silver
│   ├── load.py             # Carga na Gold
│   └── ml_model.py         # Classificador (salvar/carregar/prever)
├── train.py                # Treina e salva modelo
├── prever.py               # Carrega modelo e faz previsões
├── consultar_gold.py       # Consulta gold_previsoes
├── modelos/                # Modelo salvo (.joblib) - NÃO vai pro Git
│   └── modelo_final.joblib
└── .gitignore              # Inclui modelos/
```

---

## 🚀 Como Executar

### 1. Treinar e Salvar Modelo

```bash
python train.py
```

**O que faz:**
- Lê dados da `silver_vacinados`
- Prepara features (dias_desde_inicio, grupo, etc.)
- Treina DecisionTreeClassifier (max_depth=12)
- Salva modelo em `modelos/modelo_final.joblib`
- **Resultado esperado:** Acurácia de 81.50%

### 2. Carregar Modelo e Fazer Previsões

```bash
python prever.py
```

**O que faz:**
- Carrega modelo salvo (NUNCA retreina)
- Valida acurácia no teste (deve ser igual ao train.py)
- Cria 7 perfis novos para previsão
- Faz previsões com confiança
- Cria tabela `gold_previsoes` (se não existir)
- Grava previsões em modo append

### 3. Consultar Previsões na Gold

```bash
python consultar_gold.py
```

**Ou no SQL Editor do Neon:**
```sql
SELECT * FROM gold_previsoes ORDER BY data_previsao DESC;
```

---

## 🧪 Perfis de Teste Criados

| # | Descrição | Idade | Dose | Data | Categoria Especial |
|---|-----------|-------|------|------|--------------------|
| 1 | Criança | 5 | 1 | 2022-03-15 | Grupo pediátrico |
| 2 | Adulto reforço | 45 | 3 | 2022-02-10 | 3ª dose |
| 3 | Idoso prioritário | 75 | 1 | 2021-06-20 | Início da campanha |
| 4 | Distrito inexistente | 30 | 2 | 2021-12-15 | **Categoria NOVA** |
| 5 | Data futura | 28 | 1 | 2025-01-01 | **Data FORA do período** |
| 6 | Criança 2ª dose | 8 | 2 | 2022-04-20 | Vacina pediátrica |
| 7 | Jovem início | 22 | 1 | 2021-05-10 | Início da campanha |

---

## 📊 Resultados das Previsões

### Previsões Realizadas

```
Perfil 1 (Criança 5 anos):
  → CORONAVAC - SINOVAC (BUTANTAN)
  → Confiança: 50%

Perfil 2 (Adulto reforço):
  → COMIRNATY (PFIZER)
  → Confiança: 100%

Perfil 3 (Idoso prioritário):
  → CHADOX1NCOV-19 - OXFORD/ASTRAZENECA (FIOCRUZ)
  → Confiança: 100%

Perfil 4 (Distrito inexistente):
  → CORONAVAC - SINOVAC (BUTANTAN)
  → Confiança: 100%

Perfil 5 (Data futura):
  → COMIRNATY (PFIZER)
  → Confiança: 100%

Perfil 6 (Criança 2ª dose):
  → CORONAVAC - SINOVAC (BUTANTAN) PEDIÁTRICA
  → Confiança: 100%

Perfil 7 (Jovem início campanha):
  → JANSSEN COVID-19 VACCINE (JOHNSON & JOHNSON)
  → Confiança: 100%
```

### Análise

**✅ Acertos Esperados:**
- Perfil 3 (Idoso, 2021): AstraZeneca → correta para início da campanha
- Perfil 6 (Criança 2ª dose): Coronavac Pediátrica → identificou vacina infantil
- Perfil 7 (2021): Janssen → vacina de dose única comum no início

**⚠️ Baixa Confiança:**
- Perfil 1 (Criança): 50% de confiança → modelo menos certo para 1ª dose pediátrica

**🔧 Categorias Novas:**
- Perfil 4 (DS INEXISTENTE): Modelo tratou como categoria desconhecida (zero em todas as dummies)
- Perfil 5 (Data 2025): `dias_desde_inicio` muito alto → modelo extrapolou

---

## 🔍 Validação dos Requisitos

### ✅ Modelo Final do Grupo
- [x] Mesmo modelo da Aula 10 (max_depth=12)
- [x] Mesmas features (dias_desde_inicio, grupo, idade, dose, etc.)
- [x] Mesmos hiperparâmetros
- [x] Acurácia mantida: 81.50%

### ✅ Treino vs Previsão
- [x] `train.py` treina e termina com `salvar()`
- [x] `prever.py` apenas carrega com `carregar()` e NUNCA treina
- [x] Validação: acurácia do modelo carregado = acurácia do train.py

### ✅ Preparação de Dados
- [x] `preparar_entrada()` reproduz exatamente o `preparar()`
- [x] Mesmas transformações (dias_desde_inicio, get_dummies, etc.)
- [x] Mesmas colunas do treino (adiciona zeros para colunas faltantes)

### ✅ Regras Mantidas
- [x] Coluna `lote` NÃO utilizada
- [x] Código em classes (`Classificador`, `Extract`, `Load`)
- [x] `prever.py` apenas orquestra chamadas

### ✅ Perfis de Teste
- [x] Criança (perfil 1 e 6)
- [x] Dose de reforço (perfil 2)
- [x] Categoria inexistente (perfil 4)
- [x] Data fora do período (perfil 5)
- [x] Total: 7 perfis (>5 obrigatórios)

### ✅ Camada Gold
- [x] Tabela `gold_previsoes` criada
- [x] Colunas: idade, sexo, distrito, dose, grupo, data_vacinacao, vacina_prevista, confianca, data_previsao
- [x] Modo append (não sobrescreve)
- [x] `data_previsao` preenchida automaticamente

### ✅ .gitignore
- [x] `modelos/` no .gitignore
- [x] `*.joblib` no .gitignore
- [x] Arquivo `.joblib` NÃO vai para o GitHub

---

## 🗂️ Schema da Tabela Gold

```sql
CREATE TABLE gold_previsoes (
    id SERIAL PRIMARY KEY,
    idade INTEGER,
    sexo VARCHAR(50),
    raca_cor VARCHAR(100),
    distrito_sanitario VARCHAR(100),
    dose INTEGER,
    grupo VARCHAR(200),
    data_vacinacao DATE,
    vacina_prevista VARCHAR(200),
    confianca FLOAT,
    data_previsao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 💡 Principais Aprendizados

### 1. Persistência de Modelos
- Usar `joblib.dump()` e `joblib.load()`
- Salvar não só o modelo, mas também metadados (colunas_treino, data_minima)
- Garantir que o modelo carregado seja EXATAMENTE igual ao treinado

### 2. Preparação de Dados Novos
- `preparar_entrada()` deve reproduzir EXATAMENTE o `preparar()`
- Usar a MESMA `data_minima` do treino para calcular `dias_desde_inicio`
- Garantir que X_novos tenha as mesmas colunas (adicionar zeros se necessário)

### 3. Categorias Novas
- Modelo não viu "DS INEXISTENTE" no treino
- One-hot encoding cria coluna com zeros para essa categoria
- Modelo consegue fazer previsão, mas pode ter comportamento inesperado

### 4. Extrapolação Temporal
- Data 2025 gera `dias_desde_inicio` muito alto
- Modelo pode extrapolar (mas sem garantias)
- Ideal: treinar com dados representativos de todo o período esperado

### 5. Confiança das Previsões
- `predict_proba()` retorna probabilidades para cada classe
- `max(probabilidades)` = confiança da previsão
- Confiança baixa (50%) indica incerteza do modelo

---

## 📈 Fluxo Completo

```
[API Recife]
     ↓
[main_direto_silver.py] → [silver_vacinados] (NeonDB)
     ↓
[train.py] → Treina modelo → [modelo_final.joblib]
     ↓
[prever.py] → Carrega modelo → Prevê perfis novos → [gold_previsoes] (NeonDB)
     ↓
[consultar_gold.py] → Consulta previsões
```

---

## 🎓 Conclusão

A atividade foi concluída com sucesso:

1. ✅ Modelo da Aula 10 (81.50%) foi salvo e carregado corretamente
2. ✅ Validação confirmou que o modelo carregado é idêntico ao treinado
3. ✅ 7 perfis novos foram criados, incluindo casos extremos (categoria inexistente, data futura)
4. ✅ Previsões foram feitas com confiança calculada
5. ✅ Tabela `gold_previsoes` foi criada e populada
6. ✅ Código foi organizado em classes reutilizáveis
7. ✅ `.gitignore` protege o modelo de ir para o GitHub

**Próximos passos:**
- Explorar análises na camada Gold
- Criar dashboards com as previsões
- Avaliar performance do modelo em produção

---

**Última atualização:** 29/10/2026
**Status:** ✅ COMPLETO
