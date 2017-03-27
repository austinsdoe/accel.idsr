from exceptions import ValueError
from operator import itemgetter

_stepforms = {}


def registerStepForm(clazz, step, substep=1):
    idstep = step[0].lower()
    idsubstep = str(substep)
    if idstep not in _stepforms:
        _stepforms[idstep] = {'substeps': {}, 'title': step[1]}
    _stepforms[idstep]['substeps'][idsubstep] = clazz


def _getRegisteredStepForm(step, substep=1):
    substeps = _stepforms.get(step.lower(), {'substeps': {}})
    clazz = substeps['substeps'].get(str(substep), None)
    if clazz:
        return clazz
    raise ValueError("No form registered for step '{0}.{1}'"
                     .format(step, str(substep)))


def getStepIds(clazzname):
    for k, v in _stepforms.items():
        for y, z in v['substeps'].items():
            if z.__name__ == clazzname:
                return (k, y)
    raise ValueError("No form registered for '{0}}'".format(clazzname))


def getAvailableSteps():
    steps = [{'id': k, 'title': v['title']} for k, v in _stepforms.items()]
    sortedlist = sorted(steps, key=itemgetter('id'), reverse=False)
    return sortedlist

def getAvailableSubsteps(step):
    return _stepforms.get(step.lower(), {'substeps': {}})['substeps']


def getStepTitle(step):
    return _stepforms.get(step.lower(), {'title': ''}).get('title', '')


def getNextStepId(step, substep=None):
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
    if not step:
        raise ValueError("No step passed in")
    substep = substep if substep else 1
    substeps = getAvailableSubsteps(step)
    if substeps:
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
            return '{0}_{1}'.format(prevstep, steps[-1:])
        return '{0}'.format(prevstep)
    # Ooops, we reached the end of the wizard form. No further step, return 0
    return ''


def newStepFormInstance(step, substep=1):
    clazz = _getRegisteredStepForm(step, substep)
    obj = clazz()
    obj.initDefaults()
    return obj


def loadStepFormInstance(requestform=None):
    if requestform is None:
        raise NotImplementedError("No requestform object passed in")
    # By default, set A.1 as fallback
    step = requestform.get('stepform', 'A')
    substep = requestform.get('substepform', 1)
    clazz = _getRegisteredStepForm(step, substep)
    return clazz(requestform)


# Import custom forms to be loaded dynamically here
from accelidsr.mod_idsrentry.forms import a
from accelidsr.mod_idsrentry.forms import b
from accelidsr.mod_idsrentry.forms import c
from accelidsr.mod_idsrentry.forms import d
