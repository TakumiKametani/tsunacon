from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from .models import Invoice
from .forms import InvoiceForm
from io import BytesIO
from reportlab.pdfgen import canvas
import boto3
from django.conf import settings
import os


class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = '/invoices/'

    def form_valid(self, form):
        invoice = form.save()
        self.generate_pdf(invoice)
        return redirect(self.success_url)

    def generate_pdf(self, invoice):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, f"Invoice ID: {invoice.id}")
        p.drawString(100, 730, f"Client Name: {invoice.client_name}")
        p.drawString(100, 710, f"Client Address: {invoice.client_address}")
        p.drawString(100, 690, f"Issue Date: {invoice.issue_date}")
        p.drawString(100, 670, f"Due Date: {invoice.due_date}")
        p.drawString(100, 650, f"Total Amount: {invoice.total_amount}")
        p.showPage()
        p.save()

        buffer.seek(0)
        filename = f"invoice_{invoice.id}.pdf"

        if settings.DEBUG:
            with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as f:
                f.write(buffer.getvalue())
        else:
            s3 = boto3.client('s3')
            s3.upload_fileobj(buffer, settings.AWS_STORAGE_BUCKET_NAME, filename)

        buffer.close()


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
