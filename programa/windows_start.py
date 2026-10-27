"""Native Windows launcher with a readable startup error report."""
import ctypes
import os
from pathlib import Path
import sys
import traceback

# Retain DLL directory handles for the whole process. The portable build ships
# the VC runtime and Qt beside its own Python runtime, rather than using the
# machine's potentially older C++ runtime.
_dll_handles = []
if sys.platform == 'win32' and hasattr(os, 'add_dll_directory'):
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    for folder in (base, base/'PySide2', base/'shiboken2'):
        if folder.is_dir():
            _dll_handles.append(os.add_dll_directory(str(folder)))

if __name__ == '__main__':
    try:
        from app.main import main
        main()
    except Exception:
        folder = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'SICAD' / 'SICADvolleyballTeste'
        folder.mkdir(parents=True, exist_ok=True)
        report = folder/'erro-inicializacao.txt'
        version = str(sys.getwindowsversion()) if sys.platform == 'win32' else sys.platform
        report.write_text('SICAD Volleyball — edição Windows 10 10240\n'+version+'\n'+traceback.format_exc(), encoding='utf-8')
        if sys.platform == 'win32':
            ctypes.windll.user32.MessageBoxW(None,
                'O programa não conseguiu iniciar.\n\nO diagnóstico foi salvo em:\n'+str(report)+'\n\nEnvie o conteúdo desse arquivo para corrigirmos o problema.',
                'SICAD Volleyball — falha na inicialização', 0x10)
        raise SystemExit(1)
