#!/bin/env python3
import pdfplumber
import re

NAF_CODES = './Structure NAF 2025 Maj 2024-10-04.pdf'
out_codes_raw = './codes_raw.txt'
out_html_opt = './opt_codes_parsed.html'
out_html_opt_major = './opt_major_codes_parsed.html'
array_for_flask = './array_i_will_use_in_flask'


def main():
    pdf = pdfplumber.open(NAF_CODES)
    out_raw_str = ""
    out_html_str = ""
    out_html_major_str = ""
    aff_str = "{"

    aff = open(array_for_flask, 'w')
    out_html_major = open(out_html_opt_major, 'w')
    out_raw = open(out_codes_raw, 'w')
    out_html = open(out_html_opt, 'w')
    pdf_text = ""
    for i in range(1,25) :
        page = pdf.pages[i]
        pdf_text += page.extract_text()
        pdf.close()
    pdf_text = pdf_text.split('\n')
    for line in pdf_text :

        #fetch big category, will add % in html output
        acc_class = re.search(r'(^\d*)\s+(.*)',line)
        if acc_class :
            out_raw_str += acc_class.group(1) + '%' + '\n'
            out_html_str += f"<option value='{acc_class.group(1)}%'><strong>{acc_class.group(2)}</strong></option>\n"
            out_html_major_str += f"<option value='{acc_class.group(1)}%'><strong>{acc_class.group(2)}</strong></option>\n"
            #print(f"CODE : {acc_class.group(1)} NAME : {acc_class.group(2)}")
            continue

        #parse sub categories, will add % in html output
        sub_acc_class = re.search(r'(^\d*\.\d)\s+(.*)', line)
        if sub_acc_class :
            out_raw_str += sub_acc_class.group(1) + '%' + '\n'
            out_html_str += f"<option value='{sub_acc_class.group(1)}%'><strong>{sub_acc_class.group(2)}</strong></option>\n"
            #print(f"CODE : {sub_acc_class.group(1)} NAME : {sub_acc_class.group(2)}")
            continue
            
        #parse sub category specialization
        spec_acc = re.search(r'(^\d*\.\d*)\s+(\d*\.\d*Y)\s+(.*)', line)
        if spec_acc :
            out_raw_str += spec_acc.group(1) + '\n' + spec_acc.group(2) + '\n'
            out_html_str += f"<option value='{spec_acc.group(2)}'>{spec_acc.group(3)}</option>\n"
            aff_str += f",\n\"{spec_acc.group(2)}\" : \"{spec_acc.group(3)}\""
            #print(f"CODE : {spec_acc.group(1)} CODE Y : {spec_acc.group(2)} NAME : {spec_acc.group(3)}")
            continue

        #parse alt sub categories
        alt_sub_acc_class = re.search(r'(^\d*\.\d*)\s+(.*)', line)
        if alt_sub_acc_class :
            out_raw_str += alt_sub_acc_class.group(1) + '\n'
            out_html_str += f"<option value='{alt_sub_acc_class.group(1)}%'><strong>{alt_sub_acc_class.group(2)}</strong></option>\n"
            #print(f"CODE : {alt_sub_acc_class.group(1)} NAME : {alt_sub_acc_class.group(2)}")
            continue

        #alt_cats
        spec_acc_alt = re.search(r'(\d*\.\d*[A-Z])\s+(.*)', line)
        if spec_acc_alt :
            out_raw_str += spec_acc_alt.group(1) + '\n'
            out_html_str += f"<option value='{spec_acc_alt.group(1)}'>{spec_acc_alt.group(2)}</option>\n"
            aff_str += f",\n\"{spec_acc_alt.group(1)}\" : \"{spec_acc_alt.group(2)}\""
            #print(f"CODE [A-Z] : {spec_acc_alt.group(1)} NAME : {spec_acc_alt.group(2)}")
            continue
    aff_str += '}'
    out_raw.write(out_raw_str)
    out_html.write(out_html_str)
    out_html_major.write(out_html_major_str)
    aff.write(aff_str)

    aff.close()
    out_html_major.close()
    out_raw.close()
    out_raw.close()

if __name__ == "__main__" :
    main()
