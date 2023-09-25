install_requires=[
  'cmd2>=1,<2',
  ":sys_platform=='win32'": ['pyreadline3'],
]