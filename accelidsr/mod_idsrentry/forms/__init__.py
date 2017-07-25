from exceptions import ValueError
from operator import itemgetter
from accelidsr.mod_idsrentry.models.idsr import Idsr

_stepforms = {}


def registerStepForm(clazz, step, substep=1):
    """
    Registers the Form to be dynamically loaded for a given step and substep.
    As an example, given a form with a name IdsrEntryStepA2Form, the value for
    the param 'step' would probably be 'A' and substep=2

    :param clazz: the type of the FlaskForm to to be instantiated
    :type clazz: type of FlaskForm
    :param step: the step for which the passed in type of form must be loaded
    :type step: string
    :param substep: the substep for which the passed in type of form and passed
        in step must be loaded
    :type substep: int
    """
    idstep = step[0].lower()
    idsubstep = str(substep)
    if idstep not in _stepforms:
        _stepforms[idstep] = {'substeps': {}, 'title': step[1]}
    _stepforms[idstep]['substeps'][idsubstep] = clazz


def _getRegisteredStepForm(step, substep=1):
    """
    Private function that returns the type of Form to be loaded when the passed
    in step and substep are requested

    :param step: the step for which the passed in type of form must be loaded
    :type step: string
    :param substep: the substep for which the passed in type of form and passed
        in step must be loaded
    :type substep: int
    :returns: the type of the Form to be loaded
    :rtype: type of FlaskForm
    """
    substeps = _stepforms.get(step.lower(), {'substeps': {}})
    clazz = substeps['substeps'].get(str(substep), None)
    if clazz:
        return clazz
    raise ValueError("No form registered for step '{0}.{1}'"
                     .format(step, str(substep)))


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
        for y, z in v['substeps'].items():
            if z.__name__ == clazzname:
                return (k, y)
    raise ValueError("No form registered for '{0}}'".format(clazzname))


def getAvailableSteps():
    """
    Returns a list that contains all the available steps and substeps
    registered previously in the system through the function registerStepForm,
    sorted by id ascending. E.g: ['a','b','c','d']

    :returns: a list with the registered top-level steps, sorted by id asc
    :rtype: A list of strings
    """
    steps = [{'id': k, 'title': v['title']} for k, v in _stepforms.items()]
    sortedlist = sorted(steps, key=itemgetter('id'), reverse=False)
    return sortedlist


def getAvailableSubsteps(step):
    """
    Returns the list of substeps registered for the passed in step.
    :param step: the step from which the substeps must be retrieved
    :type step: string
    :returns: the list of substeps associated to the passed in step
    :rtype: A list of strings
    """
    return _stepforms.get(step.lower(), {'substeps': {}})['substeps']


def getStepTitle(step):
    """
    Returns the title associated to the passed in step
    :param step: te step from which the associated title must be retrieved
    :type step: string
    :returns: The title associated to the passed in step
    :rtype: string
    """
    return _stepforms.get(step.lower(), {'title': ''}).get('title', '')


def getNextStepId(step, substep=None):
    """
    Returns the next step (and/or substep) that follows the step (and substep)
    passed in. If the substep passed in is the last substep from the step, the
    function will return the first substep of the next available step, but only
    if the passed in step is not the last step from within a sequence.
    Otherwise, returns an empty string.
    As an example if step='b' and substep=2, the function will return 'b_3'. If
    there is no substep 3 for b, then will return c_1. If in turn, there is no
    step 'c' registered, then will return ''

    :param step: the current step
    :type step: string
    :param substep: the current substep.
    :type substep: int
    :returns: The next step id that follows the current step and substep
    :rtype: string
    """
    if not step:
        raise ValueError("No step passed in")
    substep = substep if substep else 1
    substeps = getAvailableSubsteps(step)
    if substeps:
        sortedss = sorted(substeps.keys())
        pos = [i for i, x in enumerate(sortedss) if x == str(substep)]
        if pos and pos[0] < (len(sortedss) - 1):
            return '{0}_{1}'.format(step.lower(), sortedss[pos[0] + 1])
    # The substep passed in is the last one from the step. Return the first
    # substep from the next top-level step
    steps = [k['id'] for k in getAvailableSteps()]
    pos = [i for i, x in enumerate(steps) if x == str(step)]
    if pos and pos[0] < (len(steps) - 1):
        return '{0}'.format(steps[pos[0]+1])
    # Ooops, we reached the end of the wizard form. No further step, return 0
    return ''


def getPrevStepId(step, substep=None):
    """
    Returns the previous step (and/or substep) before the step (and substep)
    passed in. If the substep passed in is the first substep from the step, the
    function will return the last substep of the previous available step, but
    only if the passed in step is not the first step from within a sequence.
    Otherwise, returns an empty string.
    As an example if step='b' and substep=2, the function will return 'b_1'. If
    step='a' and substep='1', then will return ''

    :param step: the current step
    :type step: string
    :param substep: the current substep.
    :type substep: int
    :returns: The next step id before the current step and substep
    :rtype: string
    """
    if not step:
        raise ValueError("No step passed in")
    if not substep:
        substep = 1
    substeps = getAvailableSubsteps(step)
    if len(substeps) > 1:
        sortedss = sorted(substeps.keys())
        pos = [i for i, x in enumerate(sortedss) if x == str(substep)]
        if pos and pos[0] > 0:
            return '{0}_{1}'.format(step.lower(), sortedss[pos[0] - 1])
    # The substep passed in is the first one from the step. Return the last
    # substep from the previous top-level step
    steps = [k['id'] for k in getAvailableSteps()]
    pos = [i for i, x in enumerate(steps) if x == str(step)]
    if pos and pos[0] > 0:
        prevstep = steps[pos[0] - 1]
        substeps = getAvailableSubsteps(prevstep)
        if substeps:
            sortedss = sorted(substeps.keys())
            return '{0}_{1}'.format(prevstep, sortedss[-1:][0])
        return '{0}'.format(prevstep)
    # Ooops, we reached the end of the wizard form. No further step, return 0
    return ''


def newStepFormInstance(step, substep=1):
    """
    Returns an instance of the FlaskForm associated to the step and substep
    passed in that were registered previously through registerStepForm function

    :param step: the step associated to the form to be instantiated.
    :type step: string
    :param substep: the substep associated to the form to be instantiated
    :type substep: int
    :returns: The instance of the FlaskForm associated to the step and substep
        passed in
    :rtype: a FlaskForm object
    """
    clazz = _getRegisteredStepForm(step, substep)
    obj = clazz()
    obj.initDefaults()
    return obj


def loadStepFormInstance(requestform=None):
    """
    Returns an instance of the FlaskForm associated to the step and substep
    passed as parameters in the request form ('stepform' and 'substepform').
    If the keys 'stepform' and 'substepform' are not found in the passed in
    requestform, returns the instance associated to the first step (A.1)

    :param requestform: the request's where the desired step and substep for
        obtaining the FlaskForm to be instantiated are defined.
    :returns: The instance of the FlaskForm associated to the step and substep
        passed in via the requestform
    :rtype: a FlaskForm object
    """
    if requestform is None:
        raise NotImplementedError("No requestform object passed in")
    # By default, set A.1 as fallback
    step = requestform.get('stepform', 'A')
    substep = requestform.get('substepform', 1)
    clazz = _getRegisteredStepForm(step, substep)
    obj = clazz(requestform)
    idobj = requestform.get('idobj', '')
    if idobj:
        idsrobj = Idsr.fetch(idobj)
        idsrobj.update(requestform)
        obj.setIdsrObject(idsrobj)
    return obj


# Import custom forms to be loaded dynamically here
from accelidsr.mod_idsrentry.forms import a
from accelidsr.mod_idsrentry.forms import b
from accelidsr.mod_idsrentry.forms import c
from accelidsr.mod_idsrentry.forms import d
