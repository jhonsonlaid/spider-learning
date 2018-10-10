import urllib.request
import re


def get_pdf(addr):
    page = urllib.request.urlopen(addr)
    html = page.read()
    print(html)
    reg = r'http://www.ijcai.org/proceedings/2017/\d*.pdf'
    pdfre = re.compile(reg)
    pdf_list = re.findall(pdfre, html)
    print(pdf_list)
    for i, pdf in enumerate(pdf_list):
        print(pdf)
        # urllib.urlretrieve(pdf, '%s.pdf' % i)


def get_pdf_direct():
    pdf_prefix = "http://www.ijcai.org/proceedings/2017/"
    for i in range(100):
        pdf_idx = '0' + str(i + 400)
        pdf_addr = pdf_prefix + pdf_idx + '.pdf'
        print(pdf_addr)
        urllib.request.urlretrieve(pdf_addr, 'paper/%s.pdf' % pdf_idx)


get_pdf_direct()
