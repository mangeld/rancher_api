import re

import git
import click
#from setuptools import sandbox
#sandbox.run_setup('setup.py', ['clean', 'bdist_wheel'])

repo = git.Repo()

def last_version():
    last_tag = sorted(repo.tags, key=lambda e: e.name, reverse=True)[0]
    version = last_tag.name.split('.')
    return [int(i) for i in version]

def increse_major(last_tag):
    last_tag[0] += 1
    return last_tag

def increase_minor(last_tag):
    last_tag[1] += 1
    return last_tag

def increase_patch(last_tag):
    last_tag[2] += 1
    return last_tag

def create_tag(version):
    repo.create_tag(".".join(str(i) for i in version))

def update_init(version):
    with open('rancher/__init__.py', 'w') as f:
        version_str = '__version__="{}"'.format(".".join(str(i) for i in version))
        f.write(version_str)

def update_setup(version):
    version_str = ".".join(str(i) for i in version)
    with open('setup.py', 'r') as f:
        data = f.read()
        result = re.sub(
            r'(version=")[\.\d]+',
            r'\g<1>{}'.format(version_str),
            data,
            flags=re.MULTILINE
        )
    with open('setup.py', 'w+') as f:
        f.write(result)

def commit(version):
    version_str = ".".join(str(i) for i in version)
    import ipdb; ipdb.set_trace()
    repo.index.add(['setup.py', '__init__.py'])
    repo.index.commit("Bump version to: {}".format(version_str))

def create_release(increase_type):
    last = last_version()
    new = None
    if increase_type == 'major':
        new = increse_major(last)
    elif increase_type == 'minor':
        new = increase_minor(last)
    else:
        new = increase_patch(last)
    update_init(new)
    update_setup(new)
    commit(new)
    create_tag(new)


@click.command()
@click.option('--patch', 'increase_type', flag_value='patch', default=True)
@click.option('--minor', 'increase_type', flag_value='minor')
@click.option('--major', 'increase_type', flag_value='major')
def main(increase_type):
    create_release(increase_type)

if __name__ == "__main__":
    main()
