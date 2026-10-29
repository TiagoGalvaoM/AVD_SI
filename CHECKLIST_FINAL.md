# ✅ Checklist Final - Atividade Aula 10

Use este checklist para verificar se todos os requisitos da atividade foram cumpridos antes de entregar.

## 📋 Regras Obrigatórias

### 1. Dados e ETL

- [ ] **Mesma camada Silver** - Não alterei `LIMITE_REGISTROS` nem o ETL
- [ ] **Silver inalterada** - Usei os dados exatamente como estão na camada Silver

### 2. Divisão Treino/Teste

- [ ] **Método `dividir()` mantido** - Não alterei o método
- [ ] **Parâmetros corretos:**
  - [ ] `test_size=0.2`
  - [ ] `random_state=42`
  - [ ] `stratify=y`

### 3. Features

- [ ] **Coluna `lote` NÃO utilizada** - Em nenhum experimento
- [ ] **Justificativa sobre `lote`** - Expliquei por que não pode ser usado (vazamento de dados)

### 4. Modelo

- [ ] **Somente DecisionTreeClassifier** - Não usei Random Forest, XGBoost, etc.
- [ ] **Nenhum outro algoritmo** - O classificador é exclusivamente árvore de decisão

### 5. Organização do Código

- [ ] **Código em classes** - Mantive organização POO
- [ ] **`PreparadorDados`** ou similar criado
- [ ] **Métodos claros e bem nomeados**

### 6. Metodologia (CRÍTICO)

- [ ] **Validação cruzada APENAS no treino** - Não usei o teste para escolher nada
- [ ] **Teste usado UMA ÚNICA VEZ** - Apenas para avaliação final
- [ ] **Não "espiei" o teste** - Nenhuma decisão foi baseada no conjunto de teste

## 📊 Experimentos e Análise

### 7. Experimentação Sistemática

- [ ] **Linha de base calculada** - DummyClassifier executado
- [ ] **Modelo original avaliado** - Registrei acurácia do modelo da aula (~63%)
- [ ] **Múltiplos experimentos** - Testei diferentes configurações
- [ ] **Tabela de tentativas criada** - Todas as tentativas documentadas

### 8. Features Investigadas

- [ ] **Representações temporais** - Testei alternativas a `ano + mes`
  - [ ] `dias_desde_inicio` ou similar
  - [ ] `mes_continuo` ou similar
- [ ] **Colunas da Silver analisadas** - Verifiquei quais não eram usadas
- [ ] **Novas features testadas** - Ex: `grupo`, `categoria`
- [ ] **Análise de vazamento** - Verifiquei que nenhuma feature vaza informação

### 9. Hiperparâmetros

- [ ] **`max_depth` variado** - Testei diferentes profundidades
- [ ] **Outros hiperparâmetros** - Ex: `min_samples_leaf`, `min_samples_split`
- [ ] **Regularização testada** - Verifiquei overfitting

### 10. Validação Cruzada

- [ ] **Estratégia definida** - StratifiedKFold ou cross_val_score
- [ ] **Aplicada ao treino** - Somente X_treino e y_treino
- [ ] **Média e desvio calculados** - Para cada experimento
- [ ] **Usada para escolher modelo** - A melhor config foi escolhida por CV

## 📈 Resultados e Avaliação

### 11. Modelo Final

- [ ] **Escolha automática** - Baseada na melhor acurácia de CV
- [ ] **Configuração documentada** - Features + hiperparâmetros claros
- [ ] **Treinado no treino completo** - Usando todo X_treino
- [ ] **Avaliado no teste** - Uma única vez

### 12. Métricas e Visualizações

- [ ] **Acurácia final reportada** - No conjunto de teste
- [ ] **Classification report** - Precision, recall, F1 por classe
- [ ] **Matriz de confusão gerada** - `matriz_confusao_final.png` criada
- [ ] **Análise da matriz** - Identifiquei maiores confusões

### 13. Interpretação

- [ ] **Feature importances** - Top 10 mostradas
- [ ] **Regras da árvore** - export_text() executado
- [ ] **Visualização da árvore** - plot_tree() gerado (ao menos parcial)
- [ ] **Interpretação faz sentido** - Regras condizem com campanha de vacinação

## 📝 Documentação

### 14. Tabela de Experimentos

- [ ] **CSV gerado** - `resultados_experimentos.csv` existe
- [ ] **Todas tentativas** - Cada experimento tem uma linha
- [ ] **Colunas completas:**
  - [ ] Número da tentativa
  - [ ] Descrição
  - [ ] Features utilizadas
  - [ ] Representação temporal
  - [ ] Hiperparâmetros
  - [ ] Acurácia CV (média)
  - [ ] Acurácia CV (desvio)
  - [ ] Observação
- [ ] **Ordenada por desempenho** - Melhor experimento no topo

### 15. Perguntas para Discussão

Todas as 10 perguntas respondidas:

- [ ] **1. Vacina mais comum e proporção?**
- [ ] **2. Modelo supera linha de base?**
- [ ] **3. Regras fazem sentido?**
- [ ] **4. Onde o modelo erra?**
- [ ] **5. Mês é a melhor representação temporal?**
- [ ] **6. Quais colunas não usadas ajudaram?**
- [ ] **7. Por que `lote` não pode ser usado?** (vazamento)
- [ ] **8. Houve overfitting?**
- [ ] **9. Configuração final?**
- [ ] **10. Acurácia final?**

### 16. Conclusão

- [ ] **Desempenho inicial mencionado** - ~63%
- [ ] **Principais mudanças descritas** - Features, temporal, hiperparâmetros
- [ ] **Importância da CV explicada** - Por que foi crucial
- [ ] **Principal feature identificada** - Qual foi a mais importante
- [ ] **Resultado final claro** - Acurácia alcançada
- [ ] **Meta avaliada** - Disse se atingiu >80% ou não

### 17. Roteiro de Apresentação

- [ ] **Estrutura criada** - Slides 1-9 planejados
- [ ] **Tempo adequado** - 3-5 minutos
- [ ] **Inclui:**
  - [ ] Problema
  - [ ] Modelo original
  - [ ] Metodologia
  - [ ] Tentativas
  - [ ] Principal descoberta
  - [ ] Configuração final
  - [ ] Matriz de confusão
  - [ ] Resultado final
  - [ ] Conclusão
- [ ] **Texto para falar** - Em cada slide

## 📂 Arquivos da Entrega

### 18. Arquivos Principais

- [ ] **`atividade_aula10_classificador.ipynb`** - Notebook principal
- [ ] **`README_ATIVIDADE.md`** - Documentação completa
- [ ] **`resultados_experimentos.csv`** - Tabela de tentativas
- [ ] **`matriz_confusao_final.png`** - Visualização
- [ ] **`arvore_decisao.png`** (opcional) - Visualização da árvore
- [ ] **Código** - `src/ml_model.py` ou classes no notebook

### 19. Qualidade do Código

- [ ] **Executável** - Notebook roda do início ao fim sem erros
- [ ] **Reprodutível** - `random_state=42` em tudo
- [ ] **Limpo** - Sem células de debug ou código comentado desnecessário
- [ ] **Bem documentado** - Markdown explicando cada seção

## 🎯 Meta da Atividade

### 20. Resultado Final

- [ ] **Acurácia final > 80%?**
  - [ ] ✅ SIM - Meta atingida!
  - [ ] ❌ NÃO - Mas melhorei significativamente em relação ao original

## ⚠️ Verificações de Segurança

### 21. Dados Sensíveis

- [ ] **`.env` não versionado** - Não está no Git
- [ ] **Credenciais ocultas** - Não aparecem no notebook
- [ ] **Connection strings seguras** - Não expostas

## 📊 Qualidade Acadêmica

### 22. Apresentação

- [ ] **Gráficos legíveis** - Títulos, labels, legendas
- [ ] **Tabelas formatadas** - Fáceis de ler
- [ ] **Linguagem acadêmica** - Mas acessível
- [ ] **Sem erros de digitação** - Revisado

### 23. Honestidade Científica

- [ ] **Todos os resultados são reais** - Nada inventado
- [ ] **Métricas vêm da execução** - Não chutei números
- [ ] **Reconheço limitações** - Se não atingi 80%, admiti
- [ ] **Metodologia honesta** - Não "espiei" o teste

## 🏁 Pronto para Entregar?

**Contagem final:**

- Total de itens: 100+
- Itens marcados: ____
- Porcentagem: ____%

**Requisitos mínimos para entrega:**

- [ ] Todos os itens das seções 1-6 (Regras Obrigatórias) ✅
- [ ] Pelo menos 80% dos itens das seções 7-13 (Experimentos) ✅
- [ ] Todos os itens da seção 15 (Perguntas) ✅
- [ ] Todos os itens da seção 18 (Arquivos) ✅

## 📝 Notas Finais

**Lembre-se:**

1. A acurácia de >80% é o ideal, mas o processo é mais importante
2. Mostrar as tentativas (mesmo as que não funcionaram) é valorizado
3. Explicar POR QUE algo funcionou ou não demonstra aprendizado
4. A metodologia correta (não usar o teste) é fundamental
5. Honestidade científica é mais importante que o resultado final

**Boa sorte! 🍀**

---

**Data da verificação:** _____/_____/_____

**Assinatura:** _________________________
