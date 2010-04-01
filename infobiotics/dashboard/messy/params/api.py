# Params global functions ---
 
#TODO def trait_value_from_param_value(params, name, value):
def trait_value_from_parameter_value(params, name, value):
    ''' Return parameter trait value from a parameter value string. '''
    try:
        assert name in params.parameter_names()
    except AssertionError, e:
        print name, e
    trait = params.trait(name)
    type = trait.trait_type.__class__.__name__
    from infobiotics.dashboard.shared.dicts import key_from_value
    if type == 'DelegatesTo':
        _delegate = trait._delegate
        setattr(eval('params.%s' % (_delegate)), name, value)
        #FIXME should go in 'set_trait_value_from_parameter_value'
        return value
    elif type == 'Bool': # convert from lowercase truth values
        return True if value == 'true' else False
    elif type in ('Int', 'IntGreaterThanZero'):
        return int(value) 
    elif type in ('Long', 'LongGreaterThanZero'):
        return long(value)
    elif type in ('Float', 'FloatGreaterThanZero'):
        return float(value) 
#    elif type == 'Complex':
#        return complex(value)
    elif type == 'Str':
        return str(value) 
    elif type == 'Unicode':
        return unicode(value) 
    elif type == 'TraitMap': # set non-shadow trait with key from shadow_value in map
        try:
            dict = trait.handler.map
            key = key_from_value(dict, value)
        except ValueError, e:
            pass
        if key is None:
            pass
        else:
            return key
    elif type == 'Range':
        if isinstance(trait.default, int):
            return int(value)
        elif isinstance(trait.default, float):
            return float(value)   
        elif isinstance(trait.default, long):
            return long(value)
    elif type in ('Enum', 'File', 'Directory'):
        return str(value)    
    else:
        logger.warn('unswitched type in trait_value_from_parameter_value: type=%s, name=%s, value=%s' % (type, name, value))
        return value

#TODO could replace name with trait.metadata.parameter_name and return (new_name, value)
def parameter_value_from_trait_value(params, name):
    ''' Return parameter value string from a ParamsExperiment parameter trait. ''' 
    assert name in params.parameter_names()
    trait = params.trait(name)
    value = params.trait_get(name)[name] # trait_get returns dict
    type = trait.trait_type.__class__.__name__
    if type == 'Bool': # convert to lowercase truth values
        value = 'true' if value is True else 'false'
    elif type == 'TraitMap': # use shadow_value
        shadow_name = '%s_' % name
        shadow_value = params.trait_get(shadow_name)[shadow_name]
        # look for a trait with the name in shadow_value and if found return its value
        possible_shadow_trait_dictionary = params.trait_get(shadow_value)
        if len(possible_shadow_trait_dictionary) > 0:
            shadow_value = possible_shadow_trait_dictionary[shadow_value]
        else:
            value = shadow_value
#    elif type == 'File': value = os.path.basename(value) #FIXME
#    print name, value
    return str(value)

from params import Params
from params_xml_reader import ParamsXMLReader
from params_experiment import ParamsExperiment
from error_string_group import error_string_group  
from params_controller_actions import load_action, save_action, load_save_actions
from params_controller import ParamsController
from params_experiment_controller_actions import perform_action, load_save_perform_actions
from params_experiment_controller import ParamsExperimentController
from params_view import params_view
