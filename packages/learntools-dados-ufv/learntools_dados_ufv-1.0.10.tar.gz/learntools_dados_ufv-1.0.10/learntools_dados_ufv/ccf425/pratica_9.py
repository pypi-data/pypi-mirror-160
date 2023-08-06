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
class Q2(CodingProblem):
    _vars= ['df', 'X_train', 'Y_train', 'X_test', 'Y_test']
    _hint = 'Utilize a função `train_test_split` do módulo `sklearn.model_selection`.'

    _solution = ''

    def check(self, df, X_train, Y_train, X_test, Y_test):
        assert_isinstance(pd.DataFrame, X_train, name='X_train')
        assert_isinstance(pd.DataFrame, X_test, name='X_test')
        assert_isinstance(pd.Series, Y_train, name='Y_train')
        assert_isinstance(pd.Series, Y_test, name='Y_test')

        expected_length_train = round(0.7 * len(df))
        expected_length_test = round(0.3 * len(df))

        assert_len(X_train, expected_length_train, name='X_train')
        assert_len(Y_train, expected_length_train, name='Y_train')
        assert_len(X_test, expected_length_test, name='X_test')
        assert_len(Y_test, expected_length_test, name='Y_test')

# q3
class Q3(ThoughtExperiment):
    _hints = [
        'Faça um plot de distribuição com a coluna de interesse (Y).',
        'Revisite as práticas anteriores para entender como fazer uma análise gráfica de um modelo desconhecido.',
    ]

# q4
class Q4(ThoughtExperiment):
    _hints = [
        'Existem inúmeros algoritmos de IA supervisionados. Visite alguns vistos nas aulas téoricas presentes no `scikit-learn`.',
        'Verifique as condições que os algoritmos assumem que os dados possuem antes de os adotar.',
        'Instancie o modelo e faça o treinamento passando apenas o conjunto de treinamento.',
    ]

# q5
class Q5(ThoughtExperiment):
    _hints = [
        'Visite o roteiro para ver como é calculado a acurácia, precisão e revogação.',
        'Pesquise sobre os métodos presentes no módulo `sklearn.stats` e `sklearn.metrics`.',
    ]

# q6
class Q6(ThoughtExperiment):
    _hints = [
        'Tente aplicar o que aprendeu sobre identificar quais as features mais importantes em um conjunto de dados.',
        'Experimente o treinamento do modelo passando outros argumentos intrínsecos ao algoritmo.',
        'Experimente o treinamento do modelo passando um conjunto de atributos diferente.',
        'Experimente o treinamento do modelo tratando antes os dados de alguma maneira.',
    ]

# q7
class Q7(ThoughtExperiment):
    _hints = [
        'Faça novamente o treinamento e validação calculando o tempo gasto.',
        'Pesquise sobre como realizar um benchmark de tempo em python usando o pacote `time`.',
    ]

# q8
class Q8(ThoughtExperiment):
    _hints = [
        'Busque nos pacotes do `scikit-learn` uma forma fácil de calcular a matriz de confusão.',
    ]


qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6,
    Q7,
    Q8
], var_format='q{n}')

__all__ = list(qvars)
