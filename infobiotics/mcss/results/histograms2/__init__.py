#x = [None]
#print x
#x[0] = 1
#print x


def testing():
    import tables
#    h5 = tables.openFile('/home/jvb/phd/models/circularPattern_05.h5')
    h5 = tables.openFile('/home/jvb/reactions1.h5')
#    print h5.root
#    print h5.title # the root node's title
    attributes = h5.root.run1._v_attrs # gets AttributeSet reference
#    print attributes._v_attrnamesuser # ['main_loop_end_time', 'main_loop_start_time', 'number_of_compartments', 'number_of_timepoints', 'preprocess_end_time', 'preprocess_start_time', 'run_end_time', 'run_start_time', 'simulated_time', 'total_reactions_simulated']
    for attribute in attributes._v_attrnamesuser:
        print attribute, '=', eval('attributes.%s' % attribute)
    print
#    print attributes._v_node # /run1 (Group) ''
#    print attributes.__contains__('main_loop_end_time') # True
#    print attributes.__contains__('main_loop_bend_time') # False

    attributes = h5.root._v_attrs
    for attribute in attributes._v_attrnamesuser:
        print attribute, '=', eval('attributes.%s' % attribute)
    print    
        
    # last run might have terminated prematurely so instead of run1.number_of_timepoints we need to do
    number_of_timepoints = 0
#    for run in listOfRuns:
#        number_of_timepoints = run.number_of_timepoints if run.number_of_timepoints > number_of_timepoints  
    # just get last run
    runs = h5.root._g_listGroup(h5.root)[0]
#    lastRun = listOfRuns[-1]
#    print eval('h5.root.%s._v_attrs.number_of_timepoints' % lastRun)
    for run in runs:
        print eval('h5.root.%s._v_attrs.number_of_timepoints' % run)
    print

    h5.close()   
