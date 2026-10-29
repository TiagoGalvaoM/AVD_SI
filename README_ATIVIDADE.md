# Atividade Aula 10 - Classificador de Vacinas COVID-19

## 📋 Objetivo

Melhorar o classificador que prevê qual vacina de COVID-19 uma pessoa tomou até obter **mais de 80% de acurácia** no conjunto de teste, usando exclusivamente `DecisionTreeClassifier`.

## ✅ Regras Seguidas

| Regra | Status |
|-------|--------|
| Mesma camada Silver (sem alterações no ETL) | ✅ |
| Mesmo método `dividir()` (`test_size=0.2, random_state=42, stratify=y`) | ✅ |
| Coluna `lote` NÃO utilizada (vazamento de dados) | ✅ |
| Somente `DecisionTreeClassifier` (nenhum outro algoritmo) | ✅ |
| Código organizado em classes | ✅ |
| Validação cruzada aplicada APENAS no treino | ✅ |
| Teste usado uma única vez ao final | ✅ |

## 📁 Estrutura do Projeto

```
etl-vacinacao-recife/
├── atividade_aula10_classificador.ipynb  # ⭐ Notebook principal da atividade
├── README_ATIVIDADE.md                    # Este arquivo
├── CHECKLIST_FINAL.md                     # Checklist de validação
├── resultados_experimentos.csv            # (gerado) Tabela de tentativas
├── matriz_confusao_final.png              # (gerado) Visualização
├── arvore_decisao.png                     # (gerado) Árvore interpretada
├── src/
│   ├── extract.py                         # Lê dados da Silver
│   ├── ml_model.py                        # Classificador original
│   ├── transform.py                       # Transformações ETL
│   ├── load.py                            # Carregamento de dados
│   └── config.py                          # Configurações
├── .env                                    # ⚠️ CRIAR: Credenciais (não versionado)
└── requirements.txt                       # Dependências Python
```

## 🚀 Como Executar

### 1️⃣ Pré-requisitos

```bash
# Verificar versão do Python (3.8+)
python --version

# Navegar até o diretório do projeto
cd "/Users/tiagomonteiro/Exercício Decision Tree/etl-vacinacao-recife"

# Instalar dependências
pip install -r requirements.txt

# Instalar Jupyter (se necessário)
pip install jupyter ipykernel notebook
```

### 2️⃣ ⚠️ Configurar Credenciais (OBRIGATÓRIO)

Crie um arquivo `.env` na raiz do projeto:

```bash
# Criar arquivo .env
touch .env
```

Adicione suas credenciais no arquivo `.env`:

```env
# MongoDB Atlas (camada BRONZE)
MONGO_URI=mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/

# NeonDB (camada SILVER  - PostgreSQL)
NEON_URL=postgresql://usuario:senha@ep-xxxxx.sa-east-1.aws.neon.tech/neondb?sslmode=require
```

**IMPORTANTE:**
- Substitua `usuario` e `senha` pelas suas credenciais reais
- O arquivo `.env` já está no `.gitignore` e não será versionado
- Sem o `.env` configurado, o notebook NÃO funcionará

### 3️⃣ Executar o Notebook

#### Opção A: Jupyter Notebook (Recomendado)

```bash
cd "/Users/tiagomonteiro/Exercício Decision Tree/etl-vacinacao-recife"
jupyter notebook atividade_aula10_classificador.ipynb
```

No navegador:
- Execute todas as células: **Cell → Run All**
- Ou execute célula por célula: **Shift + Enter**

#### Opção B: Jupyter Lab

```bash
jupyter lab
```

Abra `atividade_aula10_classificador.ipynb` e execute.

#### Opção C: VS Code

1. Abra o VS Code
2. Instale a extensão "Jupyter"
3. Abra o arquivo `.ipynb`
4. Execute as células

### 4️⃣ Verificar Resultados

Após a execução, serão gerados:

- ✅ `resultados_experimentos.csv` - Tabela com todos os experimentos
- ✅ `matriz_confusao_final.png` - Matriz de confusão do modelo final
- ✅ `arvore_decisao.png` - Visualização da árvore

## 📊 Metodologia

### Fluxo Completo

```
┌─────────────────────┐
│  Ler Silver (Neon)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Análise Inicial    │
│  - Distribuição     │
│  - Valores ausentes │
│  - Classes          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Preparação Dados   │
│  - Features         │
│  - Repr. Temporal   │
│  - dividir()        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Treino / Teste     │
│  (80% / 20%)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Linha de Base      │
│  (DummyClassifier)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Modelo Original    │
│  (max_depth=4)      │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│  EXPERIMENTOS (CV no treino) │
│  1. Repr. Temporal           │
│  2. Novas Features           │
│  3. Hiperparâmetros          │
└──────────┬───────────────────┘
           │
           ▼
┌─────────────────────┐
│  Escolher Melhor    │
│  (maior CV)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Treinar Final      │
│  (todo o treino)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AVALIAR NO TESTE   │
│  (UMA ÚNICA VEZ)    │
└─────────────────────┘
```

### Experimentos Realizados

#### 🕐 Representação Temporal

| Exp | Representação | Descrição |
|-----|---------------|-----------|
| 0   | `ano + mes`   | Baseline (original) |
| 1   | `dias_desde_inicio` | Dias desde a primeira vacinação |
| 2   | `mes_continuo` | ano * 12 + mês (ordinal) |
| 3   | `dia_ano` | Dia do ano + ano |

**Hipótese:** Representações contínuas capturam melhor a evolução temporal da campanha.

#### 🏷️ Features Adicionais

| Exp | Features Novas | Justificativa |
|-----|----------------|---------------|
| 4   | `grupo` | Grupo prioritário da campanha |
| 5   | `categoria` | Categoria adicional |

**Atenção:** `lote` NÃO pode ser usado - seria vazamento de dados!

#### ⚙️ Hiperparâmetros

| Exp | Configuração | Objetivo |
|-----|--------------|----------|
| 6   | `max_depth=6` | Aumentar capacidade |
| 7   | `max_depth=8` | Capturar padrões complexos |
| 8   | `max_depth=10` | Verificar overfitting |
| 9   | `min_samples_leaf=10` | Regularização |
| 10  | `min_samples_split=20` | Regularização alternativa |
| 11  | `criterion=entropy` | Mudança de critério |

### ⚠️ Validação Cruzada - Regra de Ouro

**O conjunto de teste NÃO foi usado para:**
- ❌ Escolher features
- ❌ Escolher hiperparâmetros
- ❌ Comparar experimentos
- ❌ Tomar decisões sobre o modelo

**O conjunto de teste FOI usado para:**
- ✅ Avaliar o modelo final (uma única vez)
- ✅ Reportar a acurácia final
- ✅ Gerar a matriz de confusão final

Isso garante que a acurácia reportada é uma estimativa não enviesada.

## 📈 Resultados

### Modelo Original (Baseline)

- **Features:** idade, dose, ano, mês, sexo, raça_cor, distrito_sanitario
- **Hiperparâmetros:** `max_depth=4`
- **Acurácia (Teste):** ~63%
- **Linha de Base:** ~43% (sempre chutar a mais comum)

### Modelo Final

*Preencher após execução do notebook:*

| Métrica | Valor |
|---------|-------|
| **Experimento Vencedor** | # [número] |
| **Features Usadas** | [lista] |
| **Representação Temporal** | [tipo] |
| **max_depth** | [valor] |
| **min_samples_leaf** | [valor] |
| **Acurácia (CV)** | [X]% ± [Y]% |
| **Acurácia (Teste)** | **[Z]%** |
| **Meta Atingida (>80%)?** | [SIM ✅ / NÃO ❌] |

### Principais Descobertas

1. **Melhor Representação Temporal:** [após execução]
2. **Feature Mais Importante:** [após execução]
3. **Overfitting?** [análise após execução]

## 📝 Respostas para Discussão

### 1. Qual vacina é a mais comum e qual sua proporção?

*Responder após execução do notebook*

### 2. O modelo supera a linha de base?

*Comparação após execução*

### 3. As regras aprendidas fazem sentido?

*Análise da árvore e feature importance*

### 4. Onde o modelo mais erra?

*Análise da matriz de confusão*

### 5. Mês é a melhor forma de representar a data?

*Comparação dos experimentos temporais*

### 6. Quais colunas não usadas ajudaram?

*Análise dos experimentos 4 e 5*

### 7. Por que `lote` não pode ser usado?

**Resposta:** A coluna `lote` representa **vazamento de dados (data leakage)**.

Cada lote de vacina é um identificador que pertence a uma vacina específica. Usar o lote como feature seria como dar a resposta ao modelo - ele memorizaria "lote X = vacina Y" sem aprender nada sobre o perfil das pessoas vacinadas.

Na prática, para usar o modelo seria necessário já saber o lote, o que por definição revela qual vacina foi aplicada. É um exemplo clássico de usar informação que só está disponível **DEPOIS** de conhecer a resposta.

### 8. Houve overfitting?

*Comparação treino vs CV vs teste - responder após execução*

### 9. Qual foi a configuração final?

*Resumo após execução*

### 10. Qual foi a acurácia final?

*Resultado do teste*

## 📦 Dependências

```
pandas
numpy
scikit-learn
matplotlib
seaborn
sqlalchemy
psycopg2-binary
pymongo
python-dotenv
jupyter
ipykernel
```

Instalar tudo:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Erro: "No module named 'src'"

**Solução:** Execute o notebook a partir do diretório raiz do projeto:
```bash
cd "/Users/tiagomonteiro/Exercício Decision Tree/etl-vacinacao-recife"
jupyter notebook
```

### Erro: "No module named 'dotenv'"

**Solução:**
```bash
pip install python-dotenv
```

### Erro ao conectar no banco

**Verificar:**
1. Arquivo `.env` existe?
2. Credenciais estão corretas?
3. Internet funcionando?
4. MongoDB Atlas e NeonDB configurados corretamente?

Para testar a conexão:
```bash
python train.py
```

## 📚 Estrutura do Notebook

1. ✅ Imports e Configuração
2. ✅ Leitura da Silver
3. ✅ Análise Inicial
4. ✅ Preparação dos Dados (classe `PreparadorDados`)
5. ✅ Divisão Treino/Teste
6. ✅ Linha de Base
7. ✅ Modelo Original
8. ✅ Validação Cruzada
9. ✅ Experimentos com Representação Temporal
10. ✅ Experimentos com Features
11. ✅ Experimentos com Hiperparâmetros
12. ✅ Tabela de Tentativas
13. ✅ Escolha do Modelo Final
14. ✅ Treinamento Final
15. ✅ **Avaliação no Teste (UMA VEZ)**
16. ✅ Matriz de Confusão
17. ✅ Interpretação da Árvore
18. ✅ Respostas para Discussão
19. ✅ Conclusão
20. ✅ Roteiro para Apresentação

## 🎯 Checklist de Entrega

Consulte `CHECKLIST_FINAL.md` para verificar todos os requisitos antes de entregar.

## 👤 Autor

**Tiago Monteiro**
Disciplina: Análise e Visualização de Dados
Atividade: Aula 10 - Melhorando o Classificador de Vacinas

## 📄 Licença

Projeto educacional - Material para fins acadêmicos.

---

**Última atualização:** 29/10/2026
