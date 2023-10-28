import dash
from dash import dcc, html, dash_table
import pandas as pd
from django_plotly_dash import DjangoDash
from plotly.express import scatter, bar
from biblioteca.models import TbLeitor, TbEmprestimo, TbLivro

df_leitor = pd.DataFrame(TbLeitor.objects.all().values())
df_livro = pd.DataFrame(TbLivro.objects.all().values())
df_emprestimo = pd.DataFrame(TbEmprestimo.objects.all().values())

df_emprestimo = df_emprestimo.merge(df_leitor, left_on="leitor_id", right_on="leitor_id")
df_emprestimo = df_emprestimo.merge(df_livro, left_on="livro_id", right_on="livro_id")

count_emprestimo_status = df_emprestimo["nome"].value_counts().to_frame().reset_index().rename(columns={"count": "quantidade", "index": "nome"})
count = df_leitor["bairro"].value_counts()

app = DjangoDash('SimpleExample')   # replaces dash.Dash

fig = bar(count, x=count.index, y=count.values, title="Cadastros por Bairro")
fig.update_layout(
    xaxis_title="Bairro",
    yaxis_title="Quantidade de cadastros")
fig2 = dash_table.DataTable(count_emprestimo_status.to_dict('records'), page_size=5)


app.layout = html.Div([
    dcc.Graph(figure=fig, style={'width': '50%', 'height': '100%'}),
    html.Div([html.P("Emprestimos por Usuários"),fig2],style={'width': '40%'})
    ],
    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center','flex-wrap': 'wrap'}
    )

