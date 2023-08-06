import os
import threading
from jinja2.environment import Environment
from jinja2.loaders import PrefixLoader, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from ..settings import template_dirs


t_local = threading.local()


def jinja2_environment(loader=None, **options):
    key = 'quarrel_env'
    e = getattr(t_local, key, None)
    if e:
        return e
    loader = loader or FileSystemLoader(template_dirs)
    e = Environment(loader=loader, **options)
    setattr(t_local, key, e)
    return e


def load_sql(using, filename_or_sql, context=None):
    template = filename_or_sql
    if not template.endswith('.sql'):
        template = f'{template}.sql'
    env = jinja2_environment()
    try:
        t = env.get_template(template)
    except (TemplateNotFound, OSError):
        try:
            template = os.path.join(using, 'sql', template)
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
            t = env.from_string(content)
        except (FileNotFoundError, OSError):
            t = env.from_string(filename_or_sql)
    if context:
        sql = t.render(**context)
    else:
        sql = t.render()
    return sql
