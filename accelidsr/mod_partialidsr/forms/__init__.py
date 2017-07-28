from exceptions import ValueError
from operator import itemgetter
from accelidsr.mod_idsrentry.models.idsr import Idsr

_stepforms = {}


def registerStepForm(clazz, step):
    """
    Registers the Form to be dynamically loaded for a given step.
    As an example, given a form with a name IdsrEntryStepA2Form, the value for
    the param 'step' would probably be 'A'

    :param clazz: the type of the FlaskForm to to be instantiated
    :type clazz: type of FlaskForm
    :param step: the step for which the passed in type of form must be loaded
    :type step: string
    """
    idstep = step[0].lower()
    if idstep not in _stepforms:
        _stepforms[idstep] = {'step': clazz, 'title': step[1]}


def _getRegisteredStepForm(step):
    """
    Private function that returns the type of Form to be loaded

    :param step: the step for which the passed in type of form must be loaded
    :type step: string
    :returns: the type of the Form to be loaded
    :rtype: type of FlaskForm
    """
    tokens = _stepforms.get(step.lower(), {'step': '', 'title': ''})
    clazz = tokens['step']
    if clazz:
        return clazz
    raise ValueError("No form registered for step '{0}'".format(step))


def getStepIds(clazzname):
    """
    Return a 2-tuple. The first item is the step and the second item is substep
    associated to the passed in type name. If no type has been registered
    previously for the passed in clazzname, raises a ValueError.

    :param clazzname: the type of the form from which the 2-tuple with the step
        and substep must be retrieved.
    :type clazzname: the type of the Form to be loaded
    :rtype: type of FlaskForm
    """
    for k, v in _stepforms.items():
        if v.get('step', None):
            if v['step'].__name__ == clazzname:
                return (k)
    raise ValueError("No form registered for '{0}}'".format(clazzname))


def getAvailableSteps():
    """
    Returns a list that contains all the available steps registered previously in the system through the
    function registerStepForm,
    sorted by id ascending. E.g: ['a','b','c','d']

    :returns: a list with the registered top-level steps, sorted by id asc
    :rtype: A list of strings
    """
    steps = [{'id': k, 'title': v['title']} for k, v in _stepforms.items()]
    sortedlist = sorted(steps, key=itemgetter('id'), reverse=False)
    return sortedlist


def getStepTitle(step):
    """
    Returns the title associated to the passed in step
    :param step: te step from which the associated title must be retrieved
    :type step: string
    :returns: The title associated to the passed in step
    :rtype: string
    """
    return _stepforms.get(step.lower(), {'title': ''}).get('title', '')


def getNextStepId(step):
    """
    Returns the next step that follows the step passed in.

    :param step: the current step
    :type step: string
    :returns: The next step id that follows the current step
    :rtype: string
    """
    if not step:
        raise ValueError("No step passed in")
    steps = [k['id'] for k in getAvailableSteps()]
    pos = [i for i, x in enumerate(steps) if x == str(step)]
    if pos and pos[0] < (len(steps) - 1):
        return '{0}'.format(steps[pos[0]+1])
    # Ooops, we reached the end of the wizard form. No further step, return 0
    return ''


def getPrevStepId(step):
    """
    Returns the previous step before the step passed in.

    :param step: the current step
    :type step: string
    :returns: The next step id before the current step and substep
    :rtype: string
    """
    if not step:
        raise ValueError("No step passed in")
    steps = [k['id'] for k in getAvailableSteps()]
    pos = [i for i, x in enumerate(steps) if x == str(step)]
    if pos and pos[0] > 0:
        prevstep = steps[pos[0] - 1]
        return '{0}'.format(prevstep)
    # Ooops, we reached the end of the wizard form. No further step, return 0
    return ''


def newStepFormInstance(step):
    """
    Returns an instance of the FlaskForm associated to the step passed in that were registered previously
    through registerStepForm function

    :param step: the step associated to the form to be instantiated.
    :type step: string
    :returns: The instance of the FlaskForm associated to the step and substep
        passed in
    :rtype: a FlaskForm object
    """
    clazz = _getRegisteredStepForm(step)
    obj = clazz()
    obj.initDefaults()
    return obj


def loadStepFormInstance(requestform=None):
    """
    Returns an instance of the FlaskForm associated to the step passed as parameters in the request form ('stepform').
    If the keys 'stepform' is not found in the passed in requestform, returns the instance of step 'A')

    :param requestform: the request's where the desired step for obtaining the FlaskForm to be instantiated are defined.
    :returns: The instance of the FlaskForm associated to the step passed in via the requestform
    :rtype: a FlaskForm object
    """
    if requestform is None:
        raise NotImplementedError("No requestform object passed in")
    # By default, set A as fallback
    step = requestform.get('stepform', 'A')
    clazz = _getRegisteredStepForm(step)
    obj = clazz(requestform)
    idobj = requestform.get('idobj', '')
    if idobj:
        idsrobj = Idsr.fetch(idobj)
        idsrobj.update(requestform)
        obj.setIdsrObject(idsrobj)
    return obj

# Import custom forms to be loaded dynamically here
from accelidsr.mod_partialidsr.forms import a
from accelidsr.mod_partialidsr.forms import b
from accelidsr.mod_partialidsr.forms import c
from accelidsr.mod_partialidsr.forms import d
