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
        ('01', [ #Обзор предметной области
            '1_Thesauri',
            #'2_Applications',
            '3_PWN',
            '4_RussNets',
            '5_YARN',
        ]),
        ('02', [ #Постановка задачи
            '1_Problem',
            '2_Previous',
            '4_Task',
        ]),
        ('04', [ #Automatic resolution approach
            '1_Graph',
            '2_Jaccard', #Measure core, naive approach
            '3_Problem_resolution', #Major problems resolution
            '4_Improvements',  #Additional improvemets on measure
            '5_Testing',
            '6_Unused', #Improvements, that weren't implemented (or tested)
            '7_BCs'
        ]),
        ('05', [ #Crowdsourcing approach
            '2_Prerequisites',
            '3_Task_formulation',
            '4_Workflow',
            '5_Result_processing',
            '6_Testing',
            '7_Future_work'
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
