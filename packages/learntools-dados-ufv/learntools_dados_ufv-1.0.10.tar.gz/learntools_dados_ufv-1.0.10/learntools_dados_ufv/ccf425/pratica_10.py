import pandas as pd

from learntools_dados_ufv.core import *

# q1
class Q1(CodingProblem):
    _var = 'df'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `weatherHistory.csv`'

    _solution = ''

    def check(self, df):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_df_equals(df, pd.read_csv('./weatherHistory.csv'), name='df')

# q2
class Q2(ThoughtExperiment):
    _hints = [
        'Aplique o K-Means utilizando todas as features válidas, exceto `Precip Type`, e obviamente a `Target`',
        'Utilize a mesma quantidade de clusters que possui nos grupos reais da base.',
    ]

# q3
class Q3(ThoughtExperiment):
    _hints = [
        'Revisite o roteiro e faça gráficos parecidos com os que estão lá.',
        'Descreva a diferença entre eles e o que significa cada grupo...',
        'Talvez seja útil utilizar a função `classification_report` do módulo `sklearn.metrics`',
    ]

# q4
class Q4(ThoughtExperiment):
    _hints = [
        'Tente visualizar a correlação de Pearson e utilizar as features com maior correlação com a precipitação',
        'Aplique o processo de clusterização e plotagem de gráfico para cada feature relevante.',
    ]

# q5
class Q5(ThoughtExperiment):
    _hints = [
        'Compare os valores do teste da silhueta, quais os melhores? E os piores, por que são piores?',
    ]

# q6
class Q6(ThoughtExperiment):
    _hints = [
        'Pesquise a resposta e verifique se já existe alguma função pronta nas bibliotecas utilizadas pra facilitar sua vida.',
    ]

# q7
class Q7(ThoughtExperiment):
    _hints = [
        'Pesquise a resposta e verifique se já existe alguma função pronta nas bibliotecas utilizadas pra facilitar sua vida.',
        'É esperado que seja analisado algumas facetas como tempo de execução, performance, tipo de agrupamento, premissas, etc.',
    ]


qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6,
    Q7,
], var_format='q{n}')

__all__ = list(qvars)
