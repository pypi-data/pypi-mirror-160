from urllib import response
import pandas as pd

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from learntools_dados_ufv.core import *

root_df = pd.read_excel('./OnlineRetail.xlsx')

def run_df_processing(steps=0):
    answer = root_df.copy()
    if (steps == 0): 
        return answer
    
    answer['Description'] = answer['Description'].str.strip()
    if (steps == 1): 
        return answer
    
    answer = answer.dropna(axis=0, subset=['InvoiceNo'])
    if (steps == 2): 
        return answer

    answer['InvoiceNo'] = answer['InvoiceNo'].astype('str')
    if (steps == 3): 
        return answer

    answer = answer[answer['Country'] == 'Germany']
    if (steps == 4): 
        return answer
    
    answer = answer.groupby(['InvoiceNo', 'Description'])
    if (steps == 5): 
        return answer
    
    answer = answer['Quantity'].sum()
    if (steps == 6): 
        return answer
    
    answer = answer.unstack().reset_index().fillna(0).set_index('InvoiceNo')
    if (steps == 7): 
        return answer

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    answer = answer.applymap(encode_units)
    if (steps == 8): 
        return answer

    answer = answer.drop('POSTAGE', axis=1)
    if (steps == 9): 
        return answer

    answer = apriori(answer, min_support=0.04, use_colnames=True)
    if (steps == 10): 
        return answer
    
    rules = association_rules(answer, min_threshold=0.5)
    if (steps == 11): 
        return rules
    
    if (steps == 12): 
        return rules[(rules['support'] >= 0.015) & (rules['confidence'] >= 0.75)]
    
    if (steps == 13): 
        return rules[(rules['lift'] >= 4) & (rules['confidence'] >= 0.8)]

# q1.a
class Q1A(CodingProblem):
    _var = 'df'
    _hints = [
        'Pesquise sobre a função `strip` do tipo str em Python.',
        'Você pode usar as funções nativas do tipo str em uma coluna Pandas usando a sintaxe `dataframe["Coluna"].str.funcao()`.',
        'Altere uma coluna usando a sintaxe `df.Coluna = df.Coluna.algumacoisa()`.',
    ]

    _solution = ''

    def check(self, df):
        assert_isinstance(pd.DataFrame, df, name='df')

        answer = run_df_processing(1)
        assert_df_equals(df, answer, name='df')

# q1.b
class Q1B(CodingProblem):
    _var = 'df'
    _hints = [
        'Pesquise sobre a função `pd.DataFrame.dropna` do tipo DataFrame Pandas.',
        'Pesquise sobre os parâmetros `subset` e `axis` da função `dropna`.',
        'Altere um dataframe usando a sintaxe `df = df.algumacoisa()`.',
    ]

    _solution = ''

    def check(self, df):
        assert_isinstance(pd.DataFrame, df, name='df')

        answer = run_df_processing(2)
        assert_df_equals(df, answer, name='df')

# q1.c
class Q1C(CodingProblem):
    _var = 'df'
    _hints = [
        'Pesquise sobre a função `astype` de uma coluna de DataFrame Pandas.',
        'Converta para o tipo `str`',
    ]

    _solution = ''

    def check(self, df):
        assert_isinstance(pd.DataFrame, df, name='df')

        answer = run_df_processing(3)
        assert_df_equals(df, answer, name='df')


# q1
Q1 = MultipartProblem(Q1A, Q1B, Q1C)

# q2.a
class Q2A(CodingProblem):
    _var = 'df_germany'
    _hints = [
        'Faça um filtro simples com `dataframe[filtro]`.',
        'Altere um dataframe usando a sintaxe `df = df[filtro]`.',
    ]

    _solution = ''

    def check(self, df_germany):
        assert_isinstance(pd.DataFrame, df_germany, name='df_germany')

        answer = run_df_processing(4)
        assert_df_equals(df_germany, answer, name='df_germany')

# q2.b
class Q2B(CodingProblem):
    _var = 'df_germany_grouped'
    _hints = [
        'Utilize a função `groupby` do Pandas.',
        'Você pode passar uma lista para a função `groupby`.',
        'A ordem da lista importa!',
    ]

    _solution = ''

    def check(self, df_germany_grouped):
        answer = run_df_processing(5)

        v = df_germany_grouped.apply(lambda x: x.equals(answer.get_group(x.name)) if x.name in answer.groups else False)
        failing_rows = len(v[v == False])

        assert failing_rows == 0, "O grupo fornecido possui pelo menos {} registros incorretos.".format(failing_rows)

# q2.c
class Q2C(CodingProblem):
    _var = 'df_germany_grouped_sum'
    _hints = [
        'Utilize a função `sum` de uma coluna agrupada do Pandas.',
        'Utilize a sintaxe `group[coluna].funcao()`',
    ]

    _solution = ''

    def check(self, df_germany_grouped_sum):
        answer = run_df_processing(6)
        assert_equal(df_germany_grouped_sum, answer, name='df_germany_grouped_sum')

# q2.d
class Q2D(CodingProblem):
    _var = 'df_germany_basket'
    _hints = [
        'Pesquise sobre a função `unstack` do Pandas.',
        'Pesquise sobre a função `reset_index` do Pandas.',
        'Pesquise sobre a função `fillna` do Pandas.',
        'Pesquise sobre a função `set_index` do Pandas.',
        'Utilize as dicas anteriores em sequência.',
    ]

    _solution = ''

    def check(self, df_germany_basket):
        assert_isinstance(pd.DataFrame, df_germany_basket, name='df_germany_basket')

        answer = run_df_processing(7)
        assert_df_equals(df_germany_basket, answer, name='df_germany_basket')

# q2.e
class Q2E(CodingProblem):
    _var = 'df_germany_basket'
    _hints = [
        'Crie uma função auxiliar que recebe um valor numérico e retorna 0 ou 1 com a condição esperada.',
        'Pesquise sobre a função `applymap` do Pandas.',
    ]

    _solution = ''

    def check(self, df_germany_basket):
        assert_isinstance(pd.DataFrame, df_germany_basket, name='df_germany_basket')

        answer = run_df_processing(8)
        assert_df_equals(df_germany_basket, answer, name='df_germany_basket')

# q2.f
class Q2F(CodingProblem):
    _var = 'df_germany_basket'
    _hints = [
        'Pesquise sobre a função `dataframe.drop` do Pandas.',
        'Você quer dropar uma **coluna**. Então, lembre-se de passar o parâmetro `axis` corretamente.',
    ]

    _solution = ''

    def check(self, df_germany_basket):
        assert_isinstance(pd.DataFrame, df_germany_basket, name='df_germany_basket')

        answer = run_df_processing(9)
        assert_df_equals(df_germany_basket, answer, name='df_germany_basket')

# q2
Q2 = MultipartProblem(Q2A, Q2B, Q2C, Q2D, Q2E, Q2F)

# q3.a
class Q3A(CodingProblem):
    _var = 'germany_frequent_itemsets'
    _hints = [
        'Utilize a função `apriori` como mostrado no roteiro.',
        'Você deve passar os paramêtros na descrição do problema.',
        'Você adicionou os parâmetros `use_colnames` e `min_support`?',
    ]

    _solution = ''

    def check(self, germany_frequent_itemsets):
        answer = run_df_processing(10)
        assert_equal(germany_frequent_itemsets, answer, name='germany_frequent_itemsets')

# q3.b
class Q3B(CodingProblem):
    _var = 'germany_rules'
    _hints = [
        'Utilize a função `association_rules` como mostrado no roteiro.',
        'Você deve passar os paramêtros na descrição do problema.',
        'Você adicionou o parâmetro `min_threshold`?',
    ]

    _solution = ''

    def check(self, germany_rules):
        answer = run_df_processing(11)
        assert_equal(germany_rules, answer, name='germany_rules')

# q3
Q3 = MultipartProblem(Q3A, Q3B)

# q4.a
class Q4A(CodingProblem):
    _var = 'germany_rules_a'
    _hints = [
        'Utilize um filtro, como mostrado no roteiro.',
    ]

    _solution = ''

    def check(self, germany_rules_a):
        assert_isinstance(pd.DataFrame, germany_rules_a, name='germany_rules_a')

        answer = run_df_processing(12)
        assert_df_equals(germany_rules_a, answer, name='germany_rules_a')

# q4.b
class Q4B(CodingProblem):
    _var = 'germany_rules_b'
    _hints = [
        'Utilize um filtro, como mostrado no roteiro.',
    ]

    _solution = ''

    def check(self, germany_rules_b):
        assert_isinstance(pd.DataFrame, germany_rules_b, name='germany_rules_b')

        answer = run_df_processing(13)
        assert_df_equals(germany_rules_b, answer, name='germany_rules_b')

# q4.c
class QBC(ThoughtExperiment):
    _hint = 'Cite 2 ou 3 pares/trios de produtos interpretando os resultados obtidos em `germany_rules`.'


# q4
Q4 = MultipartProblem(Q4A, Q4B)


qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
], var_format='q{n}')

__all__ = list(qvars)
