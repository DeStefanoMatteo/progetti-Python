#! python3

# CREATE PDF REPORT

import create_html
import pdfkit
import datetime


def create_pdf_file():
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    
    html_file = 'weight_report.html'
    pdf_file = f'weight_report_{datetime.date.today().strftime("%Y%m%d")}.pdf'
    options = {
      "enable-local-file-access": None
    }

    pdfkit.from_file(html_file, f'reports/{pdf_file}',
        configuration=config, options=options)


def main():
    # Create report in html
    create_html.main()
    print('"weight_report.html" created.')

    # Create report in pdf
    create_pdf_file()


if __name__ == '__main__':
    main()