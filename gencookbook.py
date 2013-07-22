#!/usr/bin/env python


import glob
import markdown
import argparse
import os
import shutil
import operator
import codecs
import re
from bs4 import BeautifulSoup
class Recipe:
    def __init__(self, filename):
        filename = os.path.abspath(filename)
        self.filename = filename
        self.text = codecs.open(filename, encoding='utf-8').read()
        self.html = markdown.markdown(self.text, extensions=['attr_list', 'outline(wrapper_tag=div)'])
        self.gitdir = os.path.dirname(filename)
        self.title = os.path.basename(self.gitdir)
        self.htmlfile = self.title + '.html'
        soup = BeautifulSoup(self.html)
        sections = ['ingredients', 'instructions', 'variations', 'suggestions' 'about']
        regexmap = dict()
        for s in sections:
            regexmap[re.compile(s,re.IGNORECASE)] = s
        for header in soup.find_all('h1'):
            div = header.previous_element
            # if the user overrode the id, don't try to match up the section
            if div.has_attr('id'):
                break

            for (regex, section_name) in regexmap.items():
                if regex.match(header.text):
                    div['id'] = section_name
        self.html = soup.prettify()


def get_rcp_files(rcpdir):
    recipes = list()
    for name in [os.path.join(rcpdir,name) for name in os.listdir(rcpdir)]:
        if os.path.isdir(name):
            for file in [os.path.join(name,file) for file in os.listdir(name)]:
                if file.endswith('.md'):
                    recipes.append(os.path.abspath(file))
    return recipes

def get_header(title):
    return "<div id='header'> <b>"+ title +"</b> &nbsp; <a href='index.html'>Home</a></div>"

def print_html(stylesheet, destfile, text):
    f = codecs.open(destfile, encoding='utf-8', mode='w')
    f.write("""
    <html>
    <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="{}">
    </head>
    <body>
    """.format(os.path.basename(stylesheet)))
    f.write(text)
    f.write('</body></html>')
    f.close()

def get_index(recipes):
    html = get_header('My Cookbook')
    html += '<ul>'
    
    for r in recipes:
        html += "<li><a href='{}'>{}<a></li>".format(r.htmlfile, r.title)
    html += '</ul>'
    return html

def gen_page(recipe):
    text = get_header(recipe.title)
    text+= "<div id='recipe'>"
    text +=recipe.html
    text += "</div>"
    text += '<div id=footer>My Cookbook</div>'
    return text



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-dir", help="Output Directory", required=True)
    parser.add_argument("-r", "--recipe-dir", help="Recipe Directory", required=True)
    parser.add_argument("-s", "--style-file", help="CSS style file", required=True)

    args = parser.parse_args()

    outdir = os.path.abspath(args.output_dir)
    recipedir = os.path.abspath(args.recipe_dir)
    stylefile = os.path.abspath(args.style_file)

    if os.path.exists(outdir) and not os.path.isdir(outdir):
        print('output_dir {} is not a directory!\n'.format(outdir))

    if not os.path.isdir(recipedir):
        print('recipe_dir {} is not a directory!\n'.format(recipedir))

    if not os.path.isfile(stylefile):
        print('stylefile {} is not a file!\n'.format(stylefile))
        
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        
    recipes = [Recipe(f) for f in get_rcp_files(recipedir)]
    recipes.sort(key=operator.attrgetter('title'))
    for recipe in recipes:
        print_html(stylefile, os.path.join(outdir, recipe.htmlfile), gen_page(recipe))

    print_html(stylefile, os.path.join(outdir, 'index.html'), get_index(recipes))

    shutil.copyfile(stylefile, os.path.join(outdir, os.path.basename(stylefile)))


if(__name__ == '__main__'):
    main()
