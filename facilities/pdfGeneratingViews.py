"""This module contains the views that generate the PDFs for the facilities app."""

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from erp.facilities.models import FacilitiesObject
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
    ascent, descent = getAscentDescent(font_name, font_size)
    return (ascent - descent)  # Returns line height
    
    
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
    pdf.drawCentredString(pageWidth/2, y, 'SHAASTRA 2013')
    y -= (lineheight + cm)
    
    # Set font for Document Title
    lineheight = PDFSetFont(pdf, 'Times-Roman', 16)
    
    # Document Title in next line, centre aligned
    pdf.drawCentredString(pageWidth/2, y, doc_title)
    
    # Set font for Document Title
    PDFSetFont(pdf, 'Times-Roman', 9)

    # Page number in same line, right aligned
    pdf.drawRightString(pageWidth - cm, y, '#%d' % page_no)
    
    y -= (lineheight + cm)

    return y
    
@login_required
def generateOverallPDF(request):
    """
    Generates and returns a PDF containing the FacilitiesObject.
    """
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=FacilitiesOverview.pdf'
    
    # Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response, pagesize = A4)
    
    # Define the title of the document as printed in the document header.
    doc_title = 'Facilities'

    # Get the width and height of the page.
    A4Width, A4Height = A4
    
    # Page number
    pageNo = 1

    # Paint the headers and get the coordinates
    y = initNewPDFPage(pdf, doc_title, pageNo, A4)
    
    # Setting x to be a cm from the left edge
    x = cm
    
    # Print the contents of the PDF
    
    # Get all event objects
    eventsList = Department.objects.filter(is_event = 1)
    
    for event in eventsList:
    
        # Get all rounds for the event
        facilitiesObjects = FacilitesObject.objects.filter(creator__department = event).order_by('-round')
        totalRounds = facilitiesObjects[0].round

        for roundNum in range(1, totalRounds+1):  # This range will generate: [1, 2, ..., totalRounds]
        
            # Get all Facilities required during the round
            Round_FacilitesList = FacilitesObject.objects.filter(creator__department = event).filter(roundno = roundNum).order_by('department')
            
            # Construct the table data
            tableData = [ ['Name', 'Qty.', 'Approved Qty.', ], ]
            for facility in Round_FacilitiesList:
                tableData.append([facility.name, 
                                  facility.quantity,
                                  facility.approved_quantity,])
            t = Table(tableData, repeatRows = 1)
            
            # Set the table style
            tableStyle = TableStyle([('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),   # Font style for Table Data
                                     ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),     # Font style for Table Header
                                     ('FONTSIZE', (0,0), (-1,-1), 12),
                                     ('ALIGN', (0,0), (-1,-1), 'CENTRE'),
                                     ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                     ('GRID', (0,0), (-1,-1), 1, colors.black),
                                     ])
            t.setStyle(tableStyle)
            
            # Set the font for the event title
            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            availableWidth = A4Width - 2*cm  # Leaving margins of 1 cm on both sides
            availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
            tableWidth, tableHeight = t.wrap(availableWidth, availableHeight) # find required space
            if tableHeight <= availableHeight:

                # Paint the event title
                pdf.drawString(x, y, event.Dept_Name + '  -  Round ' + roundNum)
                # Add spacing
                y -= (lineheight + 0.2*cm)

                t.drawOn(pdf, x, y-tableHeight)
                y -= (tableHeight + cm)  # Find next position for painting
            else:
                pdf.showPage()
                pageNo += 1
                y = initNewPDFPage(pdf, doc_title, pageNo, A4)

                # Set the font for the event title
                lineheight = PDFSetFont(pdf, 'Times-Roman', 14)            
                # Paint the event title
                pdf.drawString(x, y, event.Dept_Name + '  -  Round ' + roundNum)
                # Add spacing
                y -= (lineheight + 0.2*cm)

                availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
                tableWidth, tableHeight = t.wrap(availableWidth, availableHeight)

                t.drawOn(pdf, x, y-tableHeight)
                y -= (tableHeight + cm)  # Find next position for painting

        pdf.showPage()
        
    pdf.showPage()
    pdf.save()
    
    return response
    
@login_required
def generateEventPDF(request, event_id):
    """
    Generates and returns a PDF containing the FacilitiesObject.
    """
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=FacilitiesOverview.pdf'
    
    # Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response, pagesize = A4)
    
    # Define the title of the document as printed in the document header.
    doc_title = 'Facilities'

    # Get the width and height of the page.
    A4Width, A4Height = A4
    
    # Page number
    pageNo = 1

    # Paint the headers and get the coordinates
    y = initNewPDFPage(pdf, doc_title, pageNo, A4)
    
    # Setting x to be a cm from the left edge
    x = cm
    
    # Print the contents of the PDF
    
    # Get the event object
    try:
        eventList = Department.objects.filter(is_event = 1).filter(pk = event_id)
    except:
        assert False
    
    for event in eventsList:
    
        # Get all rounds for the event
        facilitiesObjects = FacilitesObject.objects.filter(creator__department = event).order_by('-round')
        totalRounds = facilitiesObjects[0].round

        for roundNum in range(1, totalRounds+1):  # This range will generate: [1, 2, ..., totalRounds]
        
            # Get all Facilities required during the round
            Round_FacilitesList = FacilitesObject.objects.filter(creator__department = event).filter(roundno = roundNum).order_by('department')
            
            # Construct the table data
            tableData = [ ['Name', 'Qty.', 'Approved Qty.', ], ]
            for facility in Round_FacilitiesList:
                tableData.append([facility.name, 
                                  facility.quantity,
                                  facility.approved_quantity,])
            t = Table(tableData, repeatRows = 1)
            
            # Set the table style
            tableStyle = TableStyle([('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),   # Font style for Table Data
                                     ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),     # Font style for Table Header
                                     ('FONTSIZE', (0,0), (-1,-1), 12),
                                     ('ALIGN', (0,0), (-1,-1), 'CENTRE'),
                                     ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                     ('GRID', (0,0), (-1,-1), 1, colors.black),
                                     ])
            t.setStyle(tableStyle)
            
            # Set the font for the event title
            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            availableWidth = A4Width - 2*cm  # Leaving margins of 1 cm on both sides
            availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
            tableWidth, tableHeight = t.wrap(availableWidth, availableHeight) # find required space
            if tableHeight <= availableHeight:

                # Paint the event title
                pdf.drawString(x, y, event.Dept_Name + '  -  Round ' + roundNum)
                # Add spacing
                y -= (lineheight + 0.2*cm)

                t.drawOn(pdf, x, y-tableHeight)
                y -= (tableHeight + cm)  # Find next position for painting
            else:
                pdf.showPage()
                pageNo += 1
                y = initNewPDFPage(pdf, doc_title, pageNo, A4)

                # Set the font for the event title
                lineheight = PDFSetFont(pdf, 'Times-Roman', 14)            
                # Paint the event title
                pdf.drawString(x, y, event.Dept_Name + '  -  Round ' + roundNum)
                # Add spacing
                y -= (lineheight + 0.2*cm)

                availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
                tableWidth, tableHeight = t.wrap(availableWidth, availableHeight)

                t.drawOn(pdf, x, y-tableHeight)
                y -= (tableHeight + cm)  # Find next position for painting

        pdf.showPage()
        
    pdf.showPage()
    pdf.save()
    
    return response
