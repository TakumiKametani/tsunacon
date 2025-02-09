import os
from io import BytesIO
from django.core.management.base import BaseCommand
from reportlab.pdfgen import canvas
from django.conf import settings
import boto3
from invoice.models import Invoice
from datetime import datetime

class Command(BaseCommand):
    help = 'Generate PDF invoices and upload to AWS S3 or save locally'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Generate invoices for all clients')
        parser.add_argument('--client_id', type=int, help='Generate invoice for a specific client ID')
        parser.add_argument('--year_month', type=str, help='Generate invoices for a specific year and month (format: YYYY-MM)')

    def handle(self, *args, **kwargs):
        all_invoices = kwargs['all']
        client_id = kwargs['client_id']
        year_month = kwargs['year_month']

        if all_invoices:
            invoices = Invoice.objects.all()
            self.stdout.write(self.style.SUCCESS(f"Generating invoices for all clients"))
        elif client_id is not None and year_month is None:
            invoices = Invoice.objects.filter(client_id=client_id)
            self.stdout.write(self.style.SUCCESS(f"Generating invoice for client ID {client_id}"))
        elif year_month is not None and client_id is None:
            try:
                year, month = map(int, year_month.split('-'))
                invoices = Invoice.objects.filter(issue_date__year=year, issue_date__month=month)
                self.stdout.write(self.style.SUCCESS(f"Generating invoices for {year}-{month}"))
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid year_month format. Use YYYY-MM"))
                return
        elif year_month is not None and client_id is not None:
            try:
                year, month = map(int, year_month.split('-'))
                invoices = Invoice.objects.filter(issue_date__year=year, issue_date__month=month, client_id=client_id)
                self.stdout.write(self.style.SUCCESS(f"Generating invoices for client ID {client_id} in {year}-{month}"))
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid year_month format. Use YYYY-MM"))
                return
        else:
            self.stdout.write(self.style.ERROR("Please specify --all, --client_id, or --year_month"))
            return

        for invoice in invoices:
            self.generate_pdf(invoice)

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
            self.stdout.write(self.style.SUCCESS(f"Saved PDF locally for invoice {invoice.id}"))
        else:
            s3 = boto3.client('s3')
            s3.upload_fileobj(buffer, settings.AWS_STORAGE_BUCKET_NAME, filename)
            self.stdout.write(self.style.SUCCESS(f"Uploaded PDF to S3 for invoice {invoice.id}"))

        buffer.close()
