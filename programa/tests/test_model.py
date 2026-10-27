import tempfile
import unittest
from pathlib import Path
from app.model import Store

TEMPLATE=Path(__file__).resolve().parents[1]/'assets'/'template.xlsx'

class StoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory()
        cls.path=Path(cls.folder.name)/'test.sqlite3'
        cls.store=Store(cls.path,TEMPLATE)

    @classmethod
    def tearDownClass(cls):
        cls.store.connection.close()
        cls.folder.cleanup()

    def test_import_fields_and_existing_records(self):
        self.assertEqual(len(self.store.fields),37)
        self.assertEqual(len(self.store.records()),0)
        self.assertEqual(self.store.cad[1],'K13')

    def test_create_edit_photo_duplicate_delete(self):
        data=['']*37
        data[0]='TEST-1000';data[1]='Atleta de teste';data[19]='Mirim'
        self.store.save(data,b'photo',True)
        with self.assertRaises(ValueError):self.store.save(data,None,True)
        data[20]='Central'
        self.store.save(data,b'photo',False)
        self.assertEqual(self.store.get(data[0]),(data,b'photo'))
        self.store.update_field(data[0],1,'Nome editado')
        self.assertEqual(self.store.get(data[0])[0][1],'Nome editado')
        self.store.delete(data[0])
        self.assertIsNone(self.store.get(data[0]))
        self.assertEqual(len(self.store.records()),0)

    def test_validation_and_missing_record(self):
        with self.assertRaises(ValueError):self.store.save(['']*37,None,True)
        data=['missing','Nome']+['']*35
        with self.assertRaises(ValueError):self.store.save(data,None,False)

    def test_cell_and_backup_persist(self):
        self.store.set_cell('Config','F12','Pagamento teste')
        self.assertEqual(self.store.overrides('Config')['F12'],'Pagamento teste')
        backup=Path(self.folder.name)/'backup.sqlite3'
        self.store.backup(backup)
        other=Store(backup,TEMPLATE)
        self.assertEqual(len(other.records()),0)
        self.assertEqual(other.overrides('Config')['F12'],'Pagamento teste')
        other.connection.close()

if __name__=='__main__': unittest.main()
