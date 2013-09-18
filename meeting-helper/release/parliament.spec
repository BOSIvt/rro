p = '/home/bshanks/prog/rro/parliament/'
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '/home/bshanks/prog/rro/parliament/parliament.py'],
             pathex=['/usr/local/lib/mcmillian_Installer'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildparliament/parliament',
          debug=0,
          strip=0,
          upx=0,
          console=1 )
coll = COLLECT( exe,
               a.binaries + \
	       [('rro_default_ruleset.py', p + 'rro_default_ruleset.py', 'BINARY')] + \
	       [('parliament.rsrc.py', p + 'parliament.rsrc.py', 'BINARY')] + \
	       [],
               strip=0,
               upx=0,
               name='distparliament')
