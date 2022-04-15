import argparse
import json
import pyperclip
from fpdf import FPDF
import textwrap

def read_template_file():
    with open('template.json', 'r') as f:
        raw_data = f.read()
        json_data = json.loads(raw_data)
        return json_data

def parse_format_keywords(template, keywords):
    out_para = ''
    for key in keywords:
        lines = template[key]
        for line in lines:
            out_para += line.strip('.') + '. '
    return out_para

def generate(keywords, template):
    intro = template['intro']
    mid = parse_format_keywords(template, keywords)
    end = template['end']
    covlet_gen = intro + '\n' + mid + '\n' + end
    return covlet_gen

def nested_generate(role, keywords, template):
    return generate(keywords, template[role[0]])    

def generate_covlet(role, keywords):
    template = read_template_file()
    if role is not None:
        return nested_generate(role, keywords, template)
    return generate(keywords, template)

def text_to_pdf(text, filename):
    pdf = FPDF(orientation='p', format='A4')
    pdf.set_margins(25,25)
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, 95)
        for wrap in lines:
            pdf.cell(0, 5, wrap, ln=1)
        pdf.ln()
    
    pdf.output(filename, 'F')

if __name__ == '__main__':
    '''
    Parse CMD arguments. Arguments format
    main.py --keyword product 
    ^ This will use a top level template as follows:
    {
        intro: [],
        product: [],
        end: []
    }

    main.py --role fe --keyword product complex
    ^ This will use a nested structure as follows:
    {
        fe: {
            intro: [],
            product: [],
            complex: [],
            end: []
        }
    }
    '''
    parser = argparse.ArgumentParser(
        prog='covlet-gen',
        description='extract specialized cover letters faster')
    parser.add_argument('--role', nargs=1, required=False, help='specify the role of the cover letter as defined in your template.json')
    parser.add_argument(
        '--keyword', nargs='*', required=True, help='specify the keyword(s) to use. These in your template will be a list of sentences '+ \
        'demonstrating your achievements that match that keyword.'
        )
    args = vars(parser.parse_args())
    # define covlet-gen specific vars
    cv_role = args.get('role')
    cv_keywords = args.get('keyword')
    cv_generated = generate_covlet(cv_role,cv_keywords)
    print('Your cover letter has been generated','\n\n',cv_generated,
    '\n','\n[C] - copy to clipboard', '\n[G] - generate as pdf')
    out_method = input()
    if out_method == 'c' or out_method == 'C':
        pyperclip.copy(cv_generated)
    if out_method == 'g' or out_method == 'G':
        text_to_pdf(cv_generated, 'test.pdf')

