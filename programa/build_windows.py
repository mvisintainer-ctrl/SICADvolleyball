"""Build with Windows Python, bundling the app-local Microsoft VC runtime."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import pefile

if sys.platform != 'win32':
    raise SystemExit('Execute com Python para Windows (nativo ou sob Wine).')
root=Path(__file__).resolve().parent
package_root=Path(importlib.util.find_spec('PySide2').origin).parent
shiboken_root=Path(importlib.util.find_spec('shiboken2').origin).parent
candidates={}
for directory in (Path(sys.base_prefix),package_root,shiboken_root):
    for pattern in ('vcruntime140*.dll','msvcp140*.dll','concrt140.dll'):
        for dll in directory.glob(pattern):
            pe=pefile.PE(str(dll),fast_load=False)
            version=pe.VS_FIXEDFILEINFO[0]
            key=(version.FileVersionMS,version.FileVersionLS)
            pe.close()
            previous=candidates.get(dll.name.lower())
            if previous is None or key>previous[0]:candidates[dll.name.lower()]=(key,dll)
args=[sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onefile',
      '--windowed','--name','SICADvolleyball','--paths',str(root),
      '--add-data',str(root/'assets/template.xlsx')+';assets',
      '--distpath',str(root/'dist'),'--workpath',str(root/'build'),
      '--specpath',str(root/'build')]
for name,(version,dll) in sorted(candidates.items()):
    print('App-local runtime:',name,version,flush=True)
    args.extend(['--add-binary',str(dll)+';.'])
args.append(str(root/'windows_start.py'))
raise SystemExit(subprocess.call(args,cwd=root))
