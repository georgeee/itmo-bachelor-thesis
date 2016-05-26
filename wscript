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
            '2_Applications',
            '3_PWN',
            '4_RussNets',
            '5_YARN',
        ]),
        ('02', [ #Постановка задачи
            '1_Problem',
            '2_Previous',
            '3_BalkaNet',
            '4_Task',
        ]),
        ('03', [ #YARN, methodology and current state
            '1_Croudsourcing',
            '2_Current_state', #Current state overview
            '3_Problems',
        ]),
        ('04', [ #Automatic resolution approach
            '1_Graph',
            '2_Jaccard', #Measure core, naive approach
            '3_Problem_resolution', #Major problems resolution
            '4_Improvements',  #Additional improvemets on measure
            '5_Testing',
            '6_Unused', #Improvements, that weren't implemented (or tested)
        ]),
        ('05', [ #Crowdsourcing approach
            '1_Motivation',
            '2_Prerequisites',
            '3_Task_formulation',
            '4_Workflow',
            '5_Result_processing',
            '6_Testing',
        ]),
        ('06', [ #Major task processing, results, future work (проведение выравнивания)
            '1_Task_preparation',
            '2_Experiment',
            '3_Results',
            '4_Future_work',
        ]),
        ('07', [ #Implementation
            '1_Dictionaries',
            '2_Graph_CLI',
            '3_PWN_version_mapping',
            '4_Croudsourcing_workflow',
            '5_Imagenet_downloading',
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
