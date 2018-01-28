import pytest

from toxn.config import ToxConfig


@pytest.mark.asyncio
async def test_pytest(conf):
    env = conf('''
[build-system]
requires = ['setuptools >= 38.2.4']
build-backend = 'setuptools.build_meta'

[tool.toxn]
  envlist = ['py36']

[tool.toxn.task]
  python = 'python3.6'

[tool.toxn.task.py36]
  deps = ["pytest"]
  description = 'run the unit tests with pytest'
  commands = ["pytest tests"]
[tool.toxn.task.dev]
  commands = [""]
''')
    conf: ToxConfig = await env.conf()

    assert conf.build.build_backend == 'setuptools.build_meta'
    assert conf.build.build_requires == ['setuptools >= 38.2.4']

    assert conf.default_tasks == ['py36']
    assert conf.tasks == ['py36', 'dev']

    py36 = conf.task('py36')
    assert py36.description == 'run the unit tests with pytest'
    assert py36.commands == [['pytest', 'tests']]

    dev = conf.task('dev')
    assert dev.description is None
    assert dev.commands == []
    assert dev.deps == []
