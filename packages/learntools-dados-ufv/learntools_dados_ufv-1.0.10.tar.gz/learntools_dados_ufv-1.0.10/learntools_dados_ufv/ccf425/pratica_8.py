from learntools_dados_ufv.core import *

# q1
class Q1(ThoughtExperiment):
    _hints = [
        'Revisite a lista de análise exploratória. Quais informações você consegue extrair dessa base?',
        'Tente visualizar um conjunto de gráficos par-a-par de cada coluna. No roteiro tem um exemplo.',
        'Tente traçar uma linha no gráfico par a par. É fácil de ter uma reta que intercepta a maioria dos pontos?',
    ]

# q2
class Q2(ThoughtExperiment):
    _hints = [
        'Identifique e atribua os valores de X e Y para ser alimentado em uma regressão linear.',
        'Talvez você precise fazer um `reshape` com o eixo X, assim como está no roteiro.',
        'Utilize do `LinearRegression` do sklearn como apresentado no roteiro.',
        'Pesquise sobre o `coef_` e `score` do LinearRegression',
    ]

# q3
class Q3(ThoughtExperiment):
    _hints = [
        'Identifique e atribua os valores de X e Y para ser alimentado em uma regressão linear.',
        'Talvez você precise fazer um `reshape` com o eixo X, assim como está no roteiro.',
        'Utilize do `LinearRegression` do sklearn como apresentado no roteiro.',
        'Pesquise sobre o `coef_` e `score` do LinearRegression',
    ]

# q4
class Q4(ThoughtExperiment):
    _hints = [
        'Identifique e atribua os valores de X e Y para ser alimentado em uma regressão linear.',
        'Talvez você precise fazer um `reshape` com o eixo X, assim como está no roteiro.',
        'Lembre-se que você precisa passar múltiplas colunas como parte do eixo X',
        'Utilize do `LinearRegression` do sklearn como apresentado no roteiro.',
        'Pesquise sobre o `coef_` e `score` do LinearRegression',
    ]

# q5
class Q5(ThoughtExperiment):
    _hints = [
        'Tente fazer uma regressão linear com todas as colunas.',
        'Interprete os scores e coeficientes retornados em uma regressão linear.',
        'O que é mais importante para ter uma alta correlação?',
    ]


qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
], var_format='q{n}')

__all__ = list(qvars)
