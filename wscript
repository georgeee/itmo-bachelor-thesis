# vim: set filetype=python :

import os.path

def configure(conf):
    conf.load('tex')
    conf.load('pandoc', tooldir='.')

def build(bld):
    def make_sources(parts):
        sources = []
        for ch in parts:
            if isinstance(ch, basestring):
                sources.append(ch + '.pd')
            elif isinstance(ch, tuple):
                chdir = 'ch_' + ch[0]
                sources.append(os.path.join(chdir, 'chapter.pd'))
                for sec in ch[1]:
                    sources.append(os.path.join(chdir, 'sec_' + sec + '.pd'))
                sources.append(os.path.join(chdir, 'conclusion.pd'))
            else:
                raise TypeError('Wrong part')
        return ' '.join(sources)
    sources = make_sources([
        'Introduction',
        ('01', [
            'Linux',
            'Unionfs',
            'ZSH',
        ]),
        ('02', [
            'Problem',
            'Goal',
            'Task',
            'Similar',
            'Tools',
        ]),
        ('03', [
            'Gshell',
            'Functions',
            'Main',
            'DirTree',
            'Graph',
            'Workflow',
            'Implementation',
            'Examples',
        ]),
        'Conclusion',
    ])
    bld(features='pandoc-merge', source=sources + ' bib.bib', target='main.latex',
            disabled_exts='fancy_lists', 
            flags='-R -S --latex-engine=xelatex --listings --chapters',
            linkflags='--toc --chapters -R', template='template.latex')

    # Outputs main.pdf
    bld(features='tex', type='xelatex', source='main.latex', flags='--shell-escape', 
            prompt=True)
    bld.add_manual_dependency(bld.bldnode.find_or_declare('main.pdf'),
                              bld.srcnode.find_node('utf8gost705u.bst'))
