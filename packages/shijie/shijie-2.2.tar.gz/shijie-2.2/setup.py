from distutils.core import  setup

setup(name='shijie',
      version='2.2',
      description='mHapTk is a tool kit for analysis of DNA methylation haplotypes. It has 5 sub-commands: tanghulu, stat, genomeWide, R2 and MHBDiscovery',
      author='ckw',
      author_email='1353595807@qq.com',

      packages=['secuer'],#import shangchuan
      entry_points={
            'console_scripts': [#console_srcipts是固定的不能改
                  'secuer = console.console:main'#shangchuan(服务器唤醒的命令，相当于ls等） = mhaptkckw.mhap_console:main
            ]
      }# linux

      )

