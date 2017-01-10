#!/usr/bin/env python
"""
Script to create a tar with the downloadable files and html for the pseudo-dojo.org website.
"""

from __future__ import unicode_literals, division, print_function, absolute_import

import sys
import os
from shutil import copyfile
from pseudo_dojo.util.notebook import write_notebook_html
#from pseudo_dojo.util.convert import make_upf
from pseudo_dojo.ppcodes.ppgen import OncvGenerator


def make_upf(pseudo_path, calctype, mock=False):
    """
    converter takes a path to a psp8 file, assumes the same .in file is present changes the .in file to upf,
    runs oncvpsp to generate hte upf file and finally changes the .in file back

    ?? polymorfic? if a .in file is provided it works with the .in ?

    Args:
        pseudo_path: path to a psp8 file

    Returns: the path to the generated upf

    """
    in_path = pseudo_path.split('.')[0] + '.in'
    upf_path = pseudo_path.split('.')[0] + '.upf'

    if mock:
        with open(upf_path, 'w') as f:
            f.write('upf mock file')
        return upf_path

    # the actual upf creation
    generator = OncvGenerator.from_file(path=in_path, calc_type=calctype)
    generator._input_str = generator._input_str.replace('psp8', 'upf')
    generator.format = 'upf'
    generator.start()
    generator.wait()
    parser = generator.OutputParser(generator.stdout_path)
    parser.scan()
    with open(upf_path, 'w') as f:
        f.write(parser.get_pseudo_str())

    return upf_path


PSEUDOS_TO_INCLUDE = ['ONCVPSP-PBE-PDv0.3', 'ONCVPSP-PW-PDv0.3', 'ONCVPSP-PBEsol-PDv0.3']


ACCURACIES = ['standard', 'high']


def main():
    website = 'website'

    usage = "Usage: " \
            "create_dojosite_tar.py path\n" \
            "creates the tar for the pseudo dojo website. To change the pseudos included change the list\n" \
            "PSEUDOS_TO_INCLUDE in create_dojosite_tar.py"
    if "--help" in sys.argv or "-h" in sys.argv:
        print(usage)
        return 1
    try:
        path = sys.argv[1]
    except:
        print(usage)
        return 1

    mock = False

    #  create the main directory for the website file-system

    if os.path.isdir(website):
        print('directory website already exists first move it away then rerun.')
        return
    else:
        os.makedirs(website)

    #  walk the current tree, create the directory structure and copy the .in, .psp8, and .djrepo files
    print('copying selected pseudos:\n%s' % PSEUDOS_TO_INCLUDE)
    a = 0

    for pseudo_set in PSEUDOS_TO_INCLUDE:
        xc = pseudo_set.split('-')[1]
        for acc in ACCURACIES:
            with open(os.path.join(pseudo_set, acc)) as f:
                pseudos = f.readlines()
            name = "%s_%s_SR" % (xc, acc[0].capitalize())
            for fmt in ['PSP8', 'UPF', 'HTML', 'DJREPO']:
                os.makedirs(os.path.join(website, '%s_%s' % (name, fmt)))
            for pseudo in pseudos:
                p = pseudo.strip()
                try:
                    for extension in ['in', 'psp8', 'djrepo', 'out']:
                        copyfile(os.path.join(pseudo_set, p).replace('psp8', extension),
                                 os.path.join(website, name + "_PSP8", os.path.split(p)[1].replace('psp8', extension)))
                    write_notebook_html(os.path.join(website, name + "_psp8", os.path.split(p)[1]), mock=mock)
                    os.rename(os.path.join(website, name + "_PSP8", os.path.split(p)[1].replace('psp8', 'html')),
                              os.path.join(website, name + "_HTML", os.path.split(p)[1].replace('psp8', 'html')))
                    make_upf(os.path.join(website, name + "_PSP8", os.path.split(p)[1]), mock=mock,
                             calctype="scalar-relativistic")
                    os.rename(os.path.join(website, name + "_PSP8", os.path.split(p)[1].replace('psp8', 'upf')),
                              os.path.join(website, name + "_UPF", os.path.split(p)[1].replace('psp8', 'upf')))
                    os.rename(os.path.join(website, name + "_PSP8", os.path.split(p)[1].replace('psp8', 'djrepo')),
                              os.path.join(website, name + "_DJREPO", os.path.split(p)[1].replace('psp8', 'djrepo')))
                    print('%s %s %s %s ' % ('mocked' if mock else 'done', xc, acc, p))
                except IOError:
                    print('missing %s %s ' % (pseudo_set, p))
                    pass
                a += 1
                if a > 10:
                    mock = True
    return


if __name__ == "__main__":
    sys.exit(main())
