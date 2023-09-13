import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

palette = ["#171821", "#F10040", "#ff7131", "#fe3d67"]
palette

plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)


def plot_countplots(data, coluna_hue, grupos, figsize=(12, 8)):
    num_grupos = len(grupos)
    cols = 2
    linhas = int(np.ceil(num_grupos/cols))

    fig, axes = plt.subplots(nrows=linhas, ncols=cols, figsize=figsize)
    axes = axes.flatten()

    for i, grupo in enumerate(grupos):
        if i < num_grupos:
            eixo = axes[i]
            sns.countplot(x=grupo,
                          data=data,
                          hue=coluna_hue,
                          palette=palette,
                          alpha=0.8,
                          ax=eixo)

            sns.despine(right=True, top=True)
            eixo.legend([], [], frameon=False)
            eixo.set_xlabel(grupo.split('.')[-1])
            eixo.set_ylabel('Frequência')

            # Adiciona o valor da frequência em cima de cada barra
        for p in eixo.patches:
            x = p.get_x() + p.get_width() / 2
            y = p.get_height()
            eixo.annotate(f'{y}\n({y/len(data)*100:.2f}%)\n', (x, y),
                          ha='center', va='bottom', color='gray')

    for i in range(num_grupos, linhas*cols):
        fig.delaxes(axes[i])

    handles, labels = eixo.get_legend_handles_labels()
    legenda = fig.legend(handles,
                         labels,
                         loc='upper center',
                         bbox_to_anchor=(0.5, 1.13),
                         ncol=2)
    legenda.set_title('Churn')

    plt.tight_layout()


def adicionar_estatisticas(ax, dados, metrica, texto_y, cor):
    valores_estatisticos = dados.groupby(
        'Churn')[metrica].agg(['mean', 'median', 'min', 'max'])

    texto = f'Média: {valores_estatisticos["mean"][0]:.2f} | {valores_estatisticos["mean"][1]:.2f}\n'
    texto += f'Mediana: {valores_estatisticos["median"][0]:.2f} | {valores_estatisticos["median"][1]:.2f}\n'
    texto += f'Mínimo: {valores_estatisticos["min"][0]:.2f} | {valores_estatisticos["min"][1]:.2f}\n'
    texto += f'Máximo: {valores_estatisticos["max"][0]:.2f} | {valores_estatisticos["max"][1]:.2f}'

    ax.text(0.5, texto_y, texto, transform=ax.transAxes,
            fontsize=12, color=cor, ha='center')

'''
def plot_countplot_2(dados, x, titulo, label_x: str = 'churn', show_x_label: bool = True, figsize: tuple = (8, 5), hue=None, small: bool = False):
    plt.figure(figsize=figsize)
    custom_params = {"axes.spines.right": False, "axes.spines.top": False,
                     "axes.spines.left": False, "axes.spines.bottom": False}

    sns.set_theme(style="ticks", rc=custom_params)
    ax = sns.countplot(x=x, hue=hue, data=dados, palette='viridis')

    ax.get_yaxis().set_visible(False)

    plt.title(titulo, fontsize=22, loc='left', pad=20, fontweight="bold")
    plt.xlabel(label_x, fontsize=17)
    plt.xticks(fontsize=15)

    if (not show_x_label):
        plt.xlabel('')
        plt.xticks([])

    for container in ax.containers:
        ax.bar_label(container, fontsize=15)

    plt.show()
'''


def heatmap_corr(df, figsize: tuple = (8, 6)):
    corr = df.corr(numeric_only=True)

    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=figsize)

    ax = sns.heatmap(corr,
                     xticklabels=corr.columns.values,
                     yticklabels=corr.columns.values,
                     annot=True,
                     cmap='viridis',
                     mask=mask)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)


def plot_matriz_confusao(y_true_teste, y_pred_teste, group_names=None,
                         categories='auto', count=True, cbar=True,
                         xyticks=True, sum_stats=True, figsize=None,
                         cmap='viridis', title=None):

    cf = confusion_matrix(y_true_teste, y_pred_teste)

    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    box_labels = [f"{v1}{v2}".strip()
                  for v1, v2 in zip(group_labels, group_counts)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0], cf.shape[1])

    if sum_stats:
        accuracy = accuracy_score(y_true_teste, y_pred_teste)
        precision = precision_score(y_true_teste, y_pred_teste)
        recall = recall_score(y_true_teste, y_pred_teste)
        f1_score_metric = f1_score(y_true_teste, y_pred_teste)

        stats_text = "Acurácia = {:0.3f}\nPrecisão = {:0.3f}\nRecall = {:0.3f}\nF1 Score = {:0.3f}".format(
            accuracy, precision, recall, f1_score_metric)
    else:
        stats_text = ""

    if figsize is None:
        figsize = plt.rcParams.get('figure.figsize')

    if xyticks is False:
        categories = False

    plt.figure(figsize=figsize)
    sns.set(font_scale=1.4)  # for label size
    sns.heatmap(cf, annot=box_labels, fmt="", cmap=cmap, cbar=cbar,
                xticklabels=categories, yticklabels=categories)
    plt.ylabel('Valores verdadeiros', fontsize=17)

    # Adicione as métricas no lado direito do gráfico
    plt.text(cf.shape[1] + 0.7, cf.shape[0] / 2.0,
             stats_text, ha='left', va='center', fontsize=16)

    plt.xlabel('Valores preditos', fontsize=17)

    if title:
        plt.title(title, fontsize=20, pad=20)


def compara_modelos_metricas(metrica, nomes_modelos, y_true_treino, y_pred_treinos, y_true_teste, y_pred_testes):
    """

    metrica: {'Acurácia Treino', 'Acurácia Teste', 'Precisão', 'Recall', 'F1-Score'}

    Returns:
        DataFrame ordenado de acordo com a métrica passada. 
    """

    acc = []
    precision = []
    recall = []
    f1 = []

    for y_pred_teste in y_pred_testes:
        acc.append(accuracy_score(y_true_teste, y_pred_teste))
        precision.append(precision_score(y_true_teste, y_pred_teste))
        recall.append(recall_score(y_true_teste, y_pred_teste))
        f1.append(f1_score(y_true_teste, y_pred_teste))

    acc_treino = []
    for y_pred_treino in y_pred_treinos:
        acc_treino.append(accuracy_score(y_true_treino, y_pred_treino))

    tabela = pd.DataFrame({'Modelo': nomes_modelos,  'Acurácia Treino': acc_treino,
                          'Acurácia Teste': acc, 'Precisão': precision, 'Recall': recall, 'F1-Score': f1})

    return tabela.sort_values(by=metrica, ascending=False).reset_index(drop=True)
