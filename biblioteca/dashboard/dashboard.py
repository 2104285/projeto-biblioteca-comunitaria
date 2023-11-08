import dash
from dash import dcc, html, dash_table
import pandas as pd
import numpy as np
from django_plotly_dash import DjangoDash
from plotly.express import scatter, bar
from biblioteca.models import TbLeitor, TbEmprestimo, TbLivro
from datetime import date
import plotly.graph_objects as go
"""
lista de tarefas:
Relatórios
Filtro de tempo
    Quantidade de livros emprestados #cartão <--
    Quantidade de leitores cadastrados #cartão 
    Quantidade de leitores 'distintos' que fizeram empréstimos #cartão
    Ranking dos leitores, quantidade de livros emprestados por cada um
    Ranking dos bairros, quantidade de livros emprestados por cada um

    Para o relatório pensamos nos seguintes dados: 

    Número total de livros emprestados (por gênero literário); 
    Relatório de leitores em atraso, e de entrega;
    Se  possível, relatório por bairro dos usuários (CEP).

"""
def get_emprestimo(data="emprestimo"):
    df_leitor = pd.DataFrame(TbLeitor.objects.all().values())
    df_leitor["bairro"] = df_leitor["bairro"].str.capitalize()
    df_leitor["bairro"] = df_leitor["bairro"].str.strip()
    df_leitor["bairro"] = df_leitor["bairro"].str.replace(".","")
    df_leitor["bairro"] = df_leitor["bairro"].str.replace("Jardim","Jd")
    if data=="leitor":
        return df_leitor
    df_livro = pd.DataFrame(TbLivro.objects.all().values())
    if data=="livro":
        return df_livro
    df_emprestimo = pd.DataFrame(TbEmprestimo.objects.all().values())

    df_emprestimo = df_emprestimo.merge(df_leitor, left_on="leitor_id", right_on="leitor_id")
    df_emprestimo = df_emprestimo.merge(df_livro, left_on="livro_id", right_on="livro_id")
    df_emprestimo["data_emprestimo"] = pd.to_datetime(df_emprestimo["data_emprestimo"])
    return df_emprestimo

df_leitor = get_emprestimo(data="leitor")
dropdown = np.sort(df_leitor["bairro"].unique())
dropdown = np.concatenate([["Todos"],dropdown])

app = DjangoDash('SimpleExample')   # replaces dash.Dash

#count = df_leitor["bairro"].value_counts()
#count_empresstimo = df_emprestimo["bairro"].value_counts()
#fig = go.Figure(data=[go.Bar(x=count.index, y=count.values,name="Cadastros"),
#                 go.Bar(x=count_empresstimo.index, y=count_empresstimo.values, name="Emprestimos")])
#fig.update_layout(
#    xaxis_title="Bairro",
#    yaxis_title="Quantidade de cadastros",
#    title_text="Quantidade de cadastros e emprestimos por bairro",)

app.layout = html.Div([
    html.Div([html.Div([html.P("Emprestimos por Bairro"),
            dcc.Dropdown(dropdown, id="dropdown", value="Todos",style={'width': '300px'})],
            style={'margin':'10px'}),
            html.Div([html.P("Filtro data de emprestimo"),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                month_format='MMMM Y',
                display_format='D-M-Y',
                start_date=date(2022, 1, 1),
                end_date=date.today(),
                min_date_allowed=date(2022, 1, 1),
                initial_visible_month=date.today(),
                style={'width': '300px'}
            )],style={'margin':'10px'})]
            ,style={'width': '100%','display':'flex','align-items': 'center', 'justify-content': 'center'}),
    dcc.Graph(id="count_cadastro_emprestimo", style={'width': '90%', 'height': '100%', 'line-break': 'after'}),
    html.Div([html.P("Emprestimos por Usuários"),
        dash_table.DataTable(
            id='table_top_leitores',
            page_size=5)],style={'width': '50%'}),
    html.Div([dcc.Graph(id="livro_p_emprestimo")],style={'width': '40%'}),
    html.Div([dcc.Graph(id="livro_status")],style={'width': '40%'})
    ],
    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center','flex-wrap': 'wrap'}
    )

@app.callback(
    dash.dependencies.Output("count_cadastro_emprestimo", "figure"),
    [dash.dependencies.Input("dropdown", "value"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_graph_count_cadastro_emprestimo(value,start_date,end_date):
    df_emprestimo = get_emprestimo()
    df_emprestimo = df_emprestimo[(df_emprestimo["data_emprestimo"] >= start_date) & (df_emprestimo["data_emprestimo"] <= end_date)]
    if value != "Todos":
        df_emprestimo = df_emprestimo[df_emprestimo["bairro"] == value]
    count_empresstimo = df_emprestimo["bairro"].value_counts()
    fig = go.Figure(data=[go.Bar(x=count_empresstimo.index, y=count_empresstimo.values, name="Emprestimos")])
    fig.update_layout(
        xaxis_title="Bairro",
        yaxis_title="Quantidade de cadastros",
        title_text="Quantidade de emprestimos por bairro",)
    return fig

@app.callback(
    dash.dependencies.Output("livro_p_emprestimo", "figure"), 
    [dash.dependencies.Input("dropdown", "value"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_graph_livro_p_empresstimo(value,start_date,end_date):
    df_emprestimo = get_emprestimo()
    df_emprestimo_livro = df_emprestimo[(df_emprestimo["data_emprestimo"] >= start_date) & (df_emprestimo["data_emprestimo"] <= end_date)]
    df_emprestimo_livro = df_emprestimo_livro[["bairro","classificacao"]]
    df_emprestimo_livro["classificacao"] = df_emprestimo_livro["classificacao"].str.capitalize()
    df_emprestimo_livro["classificacao"] = df_emprestimo_livro["classificacao"].str.strip()
    df_emprestimo_livro["count"] = 1
    df_emprestimo_livro = df_emprestimo_livro.groupby(["bairro","classificacao"]).sum().reset_index()
    if value == "Todos":
        figure1 = bar(df_emprestimo_livro, x="classificacao", y="count",color="bairro",title="Livros por Classificação")
        figure1.update_layout(
            xaxis_title="Classificação",
            yaxis_title="Quantidade de livros",
            title_text="Livros por Classificação")
        return figure1
    else:
        df_emprestimo_livro = df_emprestimo_livro[df_emprestimo_livro["bairro"] == value]
        figure1 = bar(df_emprestimo_livro, x="classificacao", y="count", title="Livros por Classificação")
        figure1.update_layout(
            xaxis_title="Classificação",
            yaxis_title="Quantidade de livros",
            title_text="Livros por Classificação")
        return figure1
    

@app.callback(
    dash.dependencies.Output("table_top_leitores", "data"), 
    [dash.dependencies.Input("dropdown", "value"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_table_top_leitores(value,start_date,end_date):
    df_emprestimo = get_emprestimo()
    df_emprestimo_livro = df_emprestimo[(df_emprestimo["data_emprestimo"] >= start_date) & (df_emprestimo["data_emprestimo"] <= end_date)]
    if value == "Todos":
        count_emprestimo_status = df_emprestimo_livro["leitor_id"].value_counts().to_frame().reset_index()
        #merge para pegar o nome do leitor
        count_emprestimo_status = count_emprestimo_status.merge(df_leitor, left_on="leitor_id", right_on="leitor_id")
        count_emprestimo_status = count_emprestimo_status[["nome","bairro","count"]].rename(columns={"count":"Quantidade"})
        count_emprestimo_status.rename(columns={"nome":"Nome","bairro":"Bairro"}, inplace=True)
        return count_emprestimo_status.to_dict('records')
    else:
        df_emprestimo_livro = df_emprestimo_livro[df_emprestimo_livro["bairro"] == value]
        count_emprestimo_status = df_emprestimo_livro["leitor_id"].value_counts().to_frame().reset_index()
        #merge para pegar o nome do leitor
        count_emprestimo_status = count_emprestimo_status.merge(df_leitor, left_on="leitor_id", right_on="leitor_id")
        count_emprestimo_status = count_emprestimo_status[["nome","bairro","count"]].rename(columns={"count":"Quantidade"})
        count_emprestimo_status.rename(columns={"nome":"Nome","bairro":"Bairro"}, inplace=True)
        return count_emprestimo_status.to_dict('records')

@app.callback(
    dash.dependencies.Output("livro_status", "figure"), 
    [dash.dependencies.Input("dropdown", "value"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_graph_livro_status(value,start_date,end_date):
    def status(teste):
        if pd.isna(teste.data_devolucao)  and teste.data_devolucao_prevista >= date.today():
            return "Não Entregue"
        elif pd.isna(teste.data_devolucao) and teste.data_devolucao_prevista < date.today():
            return "Atrasado"
        else:
            return "Entregue"
    df_emprestimo = get_emprestimo()
    df_emprestimo_livro = df_emprestimo[(df_emprestimo["data_emprestimo"] >= start_date) & (df_emprestimo["data_emprestimo"] <= end_date)]
    if value != "Todos":
        df_emprestimo_livro = df_emprestimo_livro[df_emprestimo_livro["bairro"] == value]
    df_emprestimo_livro["status"] = df_emprestimo_livro.apply(lambda x: status(x), axis=1)
    df_emprestimo_livro["count"] = 1
    df_emprestimo_livro = df_emprestimo_livro[["status","count","bairro"]]
    df_emprestimo_livro = df_emprestimo_livro.groupby(["status"]).sum().reset_index()
    figure1 = bar(df_emprestimo_livro, x="status", y="count", title="Livros por Status")
    figure1.update_layout(
        xaxis_title="Status",
        yaxis_title="Quantidade de livros",
        title_text="Livros por Status")
    return figure1