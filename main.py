import argparse
import json
import pyperclip
from fpdf import FPDF
import textwrap
import os
from os import path
from datetime import datetime


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
    if template.get('intro') is None or template.get('end') is None:
        print("intro/end key not found. Intro and End entries are required to generate your cover letter")
        return
    intro = template['intro'].strip('.') + '.'
    desc = parse_format_keywords(template, ['desc'])
    mid = parse_format_keywords(template, keywords)
    end = template['end'].strip('.') + '.'
    covlet_gen = intro + '\n\n' + desc + '\n\n' + mid + '\n\n' + end
    return covlet_gen


def generate_covlet(role, keywords):
    template = read_template_file()
    out_covlet = ''
    if role is not None:
        out_covlet = generate(keywords, template[role[0]])
    else:
        out_covlet = generate(keywords, template)
    raw_sign = template['signature']
    sign = raw_sign[0] + ",\n" + raw_sign[1]
    return out_covlet + '\n\n' + sign


def generate_pdf(text, filename):
    pdf = FPDF(orientation='p', format='A4')
    pdf.set_margins(25, 25)
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    splitted = text.split('\n')
    for line in splitted:
        if line == '':
            pdf.ln()
            continue
        lines = textwrap.wrap(line, 95)
        for wrap in lines:
            pdf.cell(0, 5, wrap, ln=1)

    pdf.output(filename, 'F')


def check_data_store(data, company, pos=None):
    app_profile = data.get(company)
    if app_profile and pos in app_profile:
        ts = app_profile.get(pos)
        return {
            'dupl': True,
            'ts': ts
        }
    return 0


def append_data_store(ds, company, pos=None):
    dt = datetime.now()
    if company in ds:
        ds[company][pos] = dt.isoformat()
    ds[company] = {
        pos: dt.isoformat()
    }
    json_obj = json.dumps(ds, indent=4)
    with open("store.json", "w") as outfile:
        outfile.write(json_obj)
    print("Datastore updated successfully!")


def main():
    '''
    Parse CMD arguments. Arguments format
    main.py --keyword product
    ^ This will use a top level template as follows:
    {
        intro: [],
        desc: [],
        product: [],
        end: []
    }

    main.py --role fe --keyword product complex
    ^ This will use a nested structure as follows:
    {
        fe: {
            intro: [],
            desc: [],
            product: [],
            complex: [],
            end: []
        }
    }
    '''
    parser = argparse.ArgumentParser(
        prog='covlet-gen',
        description='extract specialized cover letters faster')
    parser.add_argument('--role', nargs=1, required=False,
                        help='specify the role of the cover letter as defined in your template.json')
    parser.add_argument(
        '--keyword', nargs='*', required=False, help='specify the keyword(s) to use. These in your template will be a list of sentences ' +
        'demonstrating your achievements that match that keyword.'
    )
    parser.add_argument(
        '--out', nargs=1, required=False, help='specify the output file name the generated pdf will use'
    )
    parser.add_argument(
        '--company', nargs='*', required=False, help='specifies the company name to use to replace the @company variable in users ' +
        'template.json keyword entry'
    )
    parser.add_argument(
        '--position', nargs='*', required=False, help='specifies the job name to use to replace the @job variable in users' +
        'template.json keyword entry'
    )
    parser.add_argument(
        '--search', action='store_true', required=False, help='Allows user to search and check if they have already created a cover letter for the ' +
        'company and position entered'
    )
    args = vars(parser.parse_args())
    # define covlet-gen specific vars
    cv_role = args.get('role')
    cv_keywords = args.get('keyword')
    company_list = args.get('company')
    pos_list = args.get('position')
    cv_search = args.get('search')

    cv_company = ' '.join(company_list) if company_list else None
    cv_pos = ' '.join(pos_list) if pos_list else None

    app_status = {'dupl': False}
    data_store = {}
    if cv_company and path.exists('store.json'):
        with open('store.json') as f:
            data_store = json.load(f)
            app_status = check_data_store(data_store, cv_company, cv_pos)

    if app_status.get('dupl'):
        print("Previous application for %s as %s Found\n" % (cv_company, cv_pos) +
              "Application date: %s\n" % (app_status.get('ts')))
        print("[Q] - Quit\nPress any other key to continue")
        opt = input()
        if opt == 'q' or opt == 'Q':
            return

    if cv_role or cv_keywords:
        cv_generated = generate_covlet(cv_role, cv_keywords)
        if cv_generated is not None:
            repl_company = cv_generated.replace(
                '@company', cv_company) if cv_company else cv_generated
            cv_fmt = repl_company.replace(
                '@position', cv_pos) if cv_pos else repl_company

            print('Your cover letter has been generated', '\n\n', cv_fmt,
                  '\n', '\n[C] - copy to clipboard', '\n[G] - generate as pdf')

            out_method = input()
            if out_method == 'c' or out_method == 'C':
                pyperclip.copy(cv_fmt)
            if out_method == 'g' or out_method == 'G':
                fname = args.get('out')[0]
                if fname is None:
                    print("output name required")
                if not path.exists('output/'):
                    os.mkdir('output')
                generate_pdf(cv_fmt, 'output/'+fname+'.pdf')
            dt = datetime.now()
            append_data_store(data_store, cv_company, cv_pos)


if __name__ == '__main__':
    main()
