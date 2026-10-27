import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import tempfile
import unittest
from pathlib import Path
from PySide2.QtWidgets import QApplication
from PySide2.QtPrintSupport import QPrinter
from app.model import Store
from app.main import Window

class DesktopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application=QApplication.instance() or QApplication([])
        cls.folder=tempfile.TemporaryDirectory()
        cls.store=Store(Path(cls.folder.name)/'test.sqlite3',Path(__file__).resolve().parents[1]/'assets'/'template.xlsx')
        cls.window=Window(cls.store)
        cls.window.show()
        cls.application.processEvents()

    @classmethod
    def tearDownClass(cls):
        cls.window.close()
        cls.store.connection.close()
        cls.folder.cleanup()

    def test_native_create_edit_navigation_and_print(self):
        w=self.window
        w.new()
        code=w.values()[0]
        w.sheets['Cadastro'].put(self.store.cad[1],'TESTE DESKTOP')
        w.save(True)
        self.assertEqual(self.store.get(code)[0][1],'TESTE DESKTOP')
        row=next(row for row,value in w.data_codes.items() if value==code)
        w.sheets['Dados'].item(row,1).setText('TESTE EDITADO')
        self.assertEqual(self.store.get(code)[0][1],'TESTE EDITADO')
        self.assertIn('TESTE EDITADO',w.document().toPlainText())
        output=Path(self.folder.name)/'ficha.pdf'
        printer=QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(str(output))
        w.document().print_(printer)
        self.assertTrue(output.read_bytes().startswith(b'%PDF-'))
        self.assertGreater(output.stat().st_size,1000)
        w.move(-1)
        self.assertEqual(w.current_code,code)
        self.store.delete(code)
        w.refresh_data()

    def test_sections_payments_and_drawing_actions(self):
        w=self.window
        w.run_macro('menuInfantil')
        self.assertTrue(w.sheets['Config'].isRowHidden(11))
        self.assertFalse(w.sheets['Config'].isRowHidden(36))
        w.sheets['Config'].put('F38','Pagamento de teste')
        self.assertEqual(self.store.overrides('Config')['F38'],'Pagamento de teste')
        w.run_macro('menuIF')
        self.assertFalse(w.sheets['Cadastro'].isRowHidden(45))
        self.assertTrue(w.sheets['Cadastro'].isRowHidden(12))
        w.run_macro('mFicha')
        self.assertIs(w.tabs.currentWidget(),w.sheets['Ficha'])
        self.application.processEvents()

if __name__=='__main__':unittest.main()
