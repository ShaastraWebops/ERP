#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the views that generate the PDFs for the DTV Picker feature."""

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from erp.prizes.models import Participant, BarcodeMap
from erp.department.models import Department

# reportlab imports are for pdf generation

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent

def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height


def initNewPDFPage(pdf, doc_title, page_no, (pageWidth, pageHeight)):
    """
    Paints the headers on every new page of the PDF document.
    Also returns the coordinates (x, y) where the last painting operation happened.
    """

    y = pageHeight

    # Leave a margin of one cm at the top

    y = pageHeight - cm

    # Set font for 'SHAASTRA 2013'

    lineheight = PDFSetFont(pdf, 'Times-Roman', 18)

    # SHAASTRA 2013 in centre

    pdf.drawCentredString(pageWidth / 2, y, 'SHAASTRA 2013')
    y -= lineheight + cm

    # Set font for Document Title

    lineheight = PDFSetFont(pdf, 'Times-Roman', 16)

    # Document Title in next line, centre aligned

    pdf.drawCentredString(pageWidth / 2, y, doc_title)

    # Set font for Document Title

    PDFSetFont(pdf, 'Times-Roman', 9)

    # Page number in same line, right aligned

    pdf.drawRightString(pageWidth - cm, y, '#%d' % page_no)

    y -= lineheight + cm

    return y


@login_required
def generateEventParticipationPDF(department_id):
    """
    Generates and returns a PDF containing the DTV Summary (by venue).
    Accessible by cores only.
    """

    try:
        department = Department.objects.get(id = int(department_id))
    except Department.DoesNotExist:
        raise Http404('Department not found.')

    participantsList = department.participants.all()
    if not paticipants:
        return HttpResponse('The event has no participants.')

    # Create the HttpResponse object with the appropriate PDF headers.

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = \
        'attachment; filename=%s-participation-summary.pdf' % event.title

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(response, pagesize=A4)

    # Define the title of the document as printed in the document header.

    doc_title = '%s Participation Summary' % event.title

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Page number

    pageNo = 1

    # Setting x to be a cm from the left edge

    x = cm
    
    # Paint the headers and get the coordinates
    y = initNewPDFPage(pdf, doc_title, pageNo, A4)

    # Construct the table data

    tableData = [[
        'S.No.',
        'Name',
        'Shaastra ID',
        'Gender',
        'Age',
        'Branch',
        'Mobile',
        'College',
        ]]
    sNo = 0
    for particpant in ParticipantsList:
        sNo += 1
        tableData.append([
            sNo,
            participant.name,
            participant.shaastra_id,
            participant.gender,
            participant.age,
            participant.branch,
            participant.mobile_number,
            participant.college,
            ])

    t = Table(tableData, repeatRows=1)

    # Set the table style

    tableStyle = TableStyle([  # Font style for Table Data
                               # Font style for Table Header
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
    t.setStyle(tableStyle)
    
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    tableSplit = t.split(availableWidth, availableHeight)  # find required space
    for splitPortion in tableSplit:
        (tableWidth, tableHeight) = splitPortion.wrap(availableWidth, availableHeight)
        splitPortion.drawOn(pdf, x, y - tableHeight)
        pdf.showPage()
        pageNo += 1
        if tableSplit[-1] != splitPortion:  # If it is not the last iteration.
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)  # There are more pages. Paint the header.
        
    pdf.save()

    return response

