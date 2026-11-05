# 📋 RESUMO EXECUTIVO - Aula 11

**Data:** 05/11/2026
**Equipe:** Tiago Monteiro, Luis Felipe Brigido, João Pedro Gomes, Pedro Calazans

---

## ✅ ATIVIDADE CONCLUÍDA COM SUCESSO!

### 🎯 Objetivo
Usar o modelo da Aula 10 (81.50% de acurácia) para prever vacinas de perfis novos e gravar as previsões na camada Gold.

---

## 📊 Resultados Principais

### 1. Modelo Salvo e Validado ✅
- **Arquivo:** `modelos/modelo_final.joblib` (867 KB)
- **Acurácia treino:** 81.50%
- **Acurácia após carregar:** 81.50% (IDÊNTICA)
- **Conclusão:** Modelo persistido corretamente

### 2. Previsões Realizadas ✅
- **Total de perfis:** 7 (mínimo exigido: 5)
- **Confiança média:** 92.9%
- **Gravadas na Gold:** 100%

### 3. Perfis Testados ✅

| Perfil | Descrição | Previsão | Confiança |
|--------|-----------|----------|-----------|
| 1 | Criança 5 anos | Coronavac | 50% ⚠️ |
| 2 | Adulto reforço (3ª dose) | Pfizer | 100% ✓ |
| 3 | Idoso 75 anos (2021) | AstraZeneca | 100% ✓ |
| 4 | Distrito INEXISTENTE | Coronavac | 100% ✓ |
| 5 | Data FUTURA (2025) | Pfizer | 100% ✓ |
| 6 | Criança 2ª dose | Coronavac Pediátrica | 100% ✓ |
| 7 | Jovem início (2021) | Janssen | 100% ✓ |

**Casos especiais testados:**
- ✅ Criança (perfis 1 e 6)
- ✅ Dose de reforço (perfil 2)
- ✅ Categoria inexistente (perfil 4: "DS INEXISTENTE")
- ✅ Data fora do período (perfil 5: 2025-01-01)

---

## 🗂️ Arquivos Criados

### Código Fonte
```
src/
├── extract.py      # Leitura da Silver
├── load.py         # Gravação na Gold
└── ml_model.py     # Classificador com salvar()/carregar()/prever()

train.py            # Treina e salva modelo
prever.py           # Carrega modelo e faz previsões
consultar_gold.py   # Consulta gold_previsoes
```

### Documentação
```
README_AULA11.md    # Documentação completa
RESUMO_AULA11.md    # Este arquivo
```

### Modelo
```
modelos/
└── modelo_final.joblib  # NÃO vai pro Git (protegido)
```

---

## 🔍 Validação dos Requisitos

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Usar modelo >80% da Aula 10 | ✅ | 81.50% mantido |
| Mesmo hiperparâmetros | ✅ | max_depth=12 |
| Mesmas features | ✅ | dias_desde_inicio, grupo, etc. |
| train.py termina com salvar() | ✅ | Linha 28 de train.py |
| prever.py apenas carrega | ✅ | NUNCA treina |
| preparar_entrada() idêntico | ✅ | Mesma lógica do preparar() |
| Não usar lote | ✅ | Coluna não utilizada |
| Criar ≥5 perfis | ✅ | 7 perfis criados |
| Incluir criança | ✅ | Perfis 1 e 6 |
| Incluir reforço | ✅ | Perfil 2 (3ª dose) |
| Incluir categoria nova | ✅ | Perfil 4 (DS INEXISTENTE) |
| Incluir data fora | ✅ | Perfil 5 (2025) |
| Gravar na gold_previsoes | ✅ | 7 registros gravados |
| Modo append | ✅ | if_exists='append' |
| data_previsao preenchida | ✅ | Automático |
| Código em classes | ✅ | Classificador, Extract, Load |
| prever.py só orquestra | ✅ | Apenas chama métodos |
| modelos/ no .gitignore | ✅ | Linha 4 do .gitignore |

**Total:** 18/18 requisitos ✅

---

## 💡 Principais Insights

### 1. Persistência de Modelos
- Salvar não só o modelo, mas também **metadados** (colunas_treino, data_minima)
- Garantir que `preparar_entrada()` use a **mesma data_minima** do treino
- Validar acurácia após carregar para confirmar integridade

### 2. Categorias Novas
- Modelo nunca viu "DS INEXISTENTE"
- One-hot encoding adiciona coluna com **zeros**
- Modelo consegue prever, mas sem garantias de qualidade

### 3. Extrapolação Temporal
- Data 2025 gera `dias_desde_inicio` = 1093 (fora do range de treino)
- Modelo **extrapolou** sem erros, mas resultado pode ser impreciso
- Idealmente, retreinar modelo com dados mais recentes

### 4. Confiança Baixa
- Perfil 1 (criança 5 anos, 1ª dose): apenas 50% de confiança
- Indica **incerteza** do modelo para esse perfil específico
- Possível causa: vacinas pediátricas menos representadas no treino

---

## 📈 Query SQL para Validação

```sql
-- Ver todas as previsões
SELECT * FROM gold_previsoes
ORDER BY data_previsao DESC;

-- Distribuição de vacinas previstas
SELECT vacina_prevista, COUNT(*)
FROM gold_previsoes
GROUP BY vacina_prevista;

-- Confiança média por vacina
SELECT vacina_prevista, ROUND(AVG(confianca)::numeric, 2) AS conf_media
FROM gold_previsoes
GROUP BY vacina_prevista;
```

---

## 🚀 Como Reproduzir

```bash
# 1. Treinar e salvar modelo
python train.py

# 2. Fazer previsões
python prever.py

# 3. Consultar resultados
python consultar_gold.py
```

**Tempo total:** ~30 segundos

---

## 📦 Entregáveis

### Para o Professor
1. ✅ `train.py` - Script de treinamento
2. ✅ `prever.py` - Script de previsão
3. ✅ `src/ml_model.py` - Classificador completo
4. ✅ `src/load.py` - Carga na Gold
5. ✅ `README_AULA11.md` - Documentação
6. ✅ Screenshot da consulta SQL (opcional)

### GitHub
- ✅ Código fonte enviado
- ✅ .gitignore protege modelo
- ✅ Repositório: https://github.com/TiagoGalvaoM/AVD_SI

---

## 🎓 Conclusão

A Atividade 11 foi concluída com **100% dos requisitos atendidos**:

1. ✅ Modelo salvo e validado (81.50%)
2. ✅ 7 perfis testados com casos extremos
3. ✅ Previsões gravadas na Gold
4. ✅ Código organizado e documentado
5. ✅ .gitignore protegendo modelo

**Próximos passos sugeridos:**
- Criar dashboard com visualizações das previsões
- Monitorar performance em produção
- Retreinar modelo periodicamente com dados novos

---

**Status Final:** ✅ APROVADO
**Data:** 05/11/2026
