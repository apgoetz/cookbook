#!/bin/python


import glob
import markdown
import argparse
import os


class Recipe:
    def __init__(self, filename):
        self.filename = filename
        self.text = open(filename).read()
        self.html = markdown.markdown(self.text, extensions=['outline(wrapper_tag=div'])
        self.title = os.path.basename(filename)[:-3]


def get_rcp_files(rcpdir):
    return glob.glob(rcpdir + '/*.md')

def gen_page(recipe, dir):
    destfile = os.path.join(dir, recipe.title + '.html')
    f = open(destfile, 'w')
    f.write("<div id='header'> <b>"+ recipe.title +"</b> &nbsp; <a href='index.html'>Home</a></div>")
    f.write("<div id='recipe'>")
    f.write(recipe.html)
    f.write("</div>")



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
        
    for recipe in [Recipe(f) for f in get_rcp_files(recipedir)]:
        gen_page(recipe,outdir)

if(__name__ == '__main__'):
    main()
