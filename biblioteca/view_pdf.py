import io
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import FileResponse
from reportlab.lib import colors
from biblioteca.models import TbLeitor, TbLivro, TbEmprestimo
from reportlab.lib.styles import getSampleStyleSheet
import datetime as dt

def generate_pdf_leitor(request):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer,pagesize=A4)
    leitor = TbLeitor.objects.filter(visivel=True)

    data = [["ID","Nome", "Telefone","Bairro"]]
    for x in leitor:
        data.append([x.leitor_id,x.nome,x.telefone,x.bairro])

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    # Close the PDF object cleanly, and we're done.
    elements = []
    elements.append(Paragraph(f'Extração Leitores', getSampleStyleSheet()['Title']))
    elements.append(Paragraph(f'Extraido na data de {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f'', getSampleStyleSheet()['Normal']))
    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='leitor.pdf')

def generate_pdf_acervo(request):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer)
    livro = TbLivro.objects.filter(visivel=True).order_by("titulo")

    data = [["Tombo","Titulo", "Autor","Classificação","Status"]]
    for x in livro:
        data.append([x.tombo,
                     Paragraph(x.titulo,getSampleStyleSheet()['Normal']),
                     Paragraph(x.autor,getSampleStyleSheet()['Normal']),
                     Paragraph(x.classificacao, getSampleStyleSheet()['Normal']), 
                     x.status])

    table = Table(data,colWidths=[40,150,150,100,70])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 1), (-1, -1), 1),  # Enable word wrapping
    ])
    table.setStyle(style)
    # Close the PDF object cleanly, and we're done.
    elements = []
    elements.append(Paragraph(f'Extração Acervo', getSampleStyleSheet()['Title']))
    elements.append(Paragraph(f'Extraido na data de {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f'', getSampleStyleSheet()['Normal']))
    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='leitor.pdf')

def generate_pdf_emprestimo(request):
    """
    Generates a PDF file containing a table with information about all book loans.

    Args:
        request: A Django request object.

    Returns:
        A Django FileResponse object containing the generated PDF file.
    """
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer,pagesize=landscape(A4))
    emprestimo = TbEmprestimo.objects.all().order_by("data_emprestimo")
    normal_style = getSampleStyleSheet()['Normal']
    normal_style.fontName = 'Helvetica-Bold'
    data = [[Paragraph("ID", normal_style), Paragraph("Leitor", normal_style), Paragraph("Endereço", normal_style), 
             Paragraph("Livro", normal_style), Paragraph("Tombo", normal_style), 
             Paragraph("Data Empréstimo", normal_style), Paragraph("Data Devolução", normal_style), 
             Paragraph("Status", normal_style)]]

    for x in emprestimo:
        data.append([x.id,
                     Paragraph(x.leitor.nome,getSampleStyleSheet()['Normal']),
                     Paragraph(x.leitor.endereco,getSampleStyleSheet()['Normal']),
                     Paragraph(x.livro.titulo, getSampleStyleSheet()['Normal']),
                     Paragraph(str(x.livro.tombo), getSampleStyleSheet()['Normal']),
                     Paragraph(str(x.data_emprestimo), getSampleStyleSheet()['Normal']),
                     Paragraph(str(x.data_devolucao) if x.data_devolucao else "", getSampleStyleSheet()['Normal']),
                     Paragraph(x.status, getSampleStyleSheet()['Normal'])])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Set title text color to black
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 1), (-1, -1), 1),  # Enable word wrapping
    ])
    table = Table(data,colWidths=[40,150,150,100,70])
    table.setStyle(style)
    # Close the PDF object cleanly, and we're done.
    elements = []
    elements.append(Paragraph(f'Extração Emprestimos', getSampleStyleSheet()['Title']))
    elements.append(Paragraph(f'Extraido na data de {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', getSampleStyleSheet()['Normal']))
    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='emprestimos.pdf')