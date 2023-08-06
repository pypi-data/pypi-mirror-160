import os

template_dirs = os.environ.get('QUARREL_TEMPLATE_DIRS')
if template_dirs:
    template_dirs = template_dirs.split(',')
else:
    template_dirs = []


def setup_quarrel(*dirs):
    """
    initializes quarrel with the specified template directories
    """
    global template_dirs
    template_dirs.extend(dirs)
    return template_dirs
