"""Read Excel drawing objects as local Qt labels/buttons. No VBA is executed."""
import posixpath
import xml.etree.ElementTree as ET
import zipfile

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QPushButton, QMenu, QInputDialog

NS = {'x':'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def objects(template, number):
    filename = f'xl/drawings/drawing{number}.xml'
    with zipfile.ZipFile(template) as archive:
        if filename not in archive.namelist():
            return []
        relationships = ET.fromstring(archive.read(f'xl/drawings/_rels/drawing{number}.xml.rels'))
        images = {r.attrib['Id']:posixpath.normpath(posixpath.join('xl/drawings',r.attrib['Target'])) for r in relationships if r.attrib.get('Type','').endswith('/image')}
        root = ET.fromstring(archive.read(filename))
        result=[]
        for node in root.iter():
            if node.tag not in ['{'+NS['x']+'}sp','{'+NS['x']+'}pic']:
                continue
            transform=node.find('x:spPr/a:xfrm',NS)
            if transform is None: continue
            off,ext=transform.find('a:off',NS),transform.find('a:ext',NS)
            if off is None or ext is None: continue
            name=node.find('.//x:cNvPr',NS)
            fill=node.find('x:spPr/a:solidFill/a:srgbClr',NS)
            font=node.find('.//a:rPr/a:solidFill/a:srgbClr',NS)
            text=''.join(n.text or '' for n in node.findall('.//a:t',NS))
            macro=node.attrib.get('macro','').split('!')[-1].split('.')[-1]
            item={'name':name.attrib.get('name','') if name is not None else '', 'text':text,
                  'macro':macro, 'link':node.attrib.get('textlink',''),
                  'x':int(off.attrib['x'])/9525, 'y':int(off.attrib['y'])/9525,
                  'w':int(ext.attrib['cx'])/9525, 'h':int(ext.attrib['cy'])/9525,
                  'background':'#'+fill.attrib['val'] if fill is not None else 'transparent',
                  'foreground':'#'+font.attrib['val'] if font is not None else '#203764'}
            blip=node.find('.//a:blip',NS)
            if blip is not None:
                target=images.get(blip.attrib.get('{'+NS['r']+'}embed'))
                if target: item['image']=archive.read(target)
            result.append(item)
        return result


class Drawings:
    def __init__(self, sheet, template, number, window):
        self.sheet=sheet
        self.window=window
        self.widgets=[]
        for obj in objects(template,number):
            if obj['macro']:
                widget=QPushButton(obj['text'],sheet.viewport())
                widget.clicked.connect(lambda checked=False,m=obj['macro']:window.run_macro(m))
            else:
                widget=QLabel(obj['text'],sheet.viewport())
                widget.setAlignment(Qt.AlignCenter)
            if 'image' in obj:
                pixmap=QPixmap()
                if pixmap.loadFromData(obj['image']):
                    if isinstance(widget,QLabel):
                        widget.setPixmap(pixmap)
                        widget.setScaledContents(True)
                    else:
                        from PySide2.QtGui import QIcon
                        from PySide2.QtCore import QSize
                        widget.setIcon(QIcon(pixmap))
                        widget.setIconSize(QSize(int(obj['w']),int(obj['h'])))
            widget.setStyleSheet(f"background:{obj['background']};color:{obj['foreground']};border:0;font-size:12px;font-weight:bold;")
            key='shape:'+obj['name']
            saved=sheet.store.overrides(sheet.sheet.title).get(key)
            if saved is not None: widget.setText(saved)
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(lambda pos,w=widget,k=key:self.edit_text(w,k))
            self.widgets.append((widget,obj))
        sheet.horizontalScrollBar().valueChanged.connect(self.position)
        sheet.verticalScrollBar().valueChanged.connect(self.position)
        for source in window.sheets.values():
            source.cellChanged.connect(self.update_text)
        self.position()
        self.update_text()

    def update_text(self, *args):
        for widget,obj in self.widgets:
            if obj["link"]:
                link=obj["link"].replace("$", "")
                name,address=link.split("!",1) if "!" in link else (self.sheet.sheet.title,link)
                if name in self.window.sheets:
                    widget.setText(self.window.sheets[name].text(address))

    def edit_text(self,widget,key):
        text,ok=QInputDialog.getText(self.sheet,'Editar texto','Texto do elemento:',text=widget.text())
        if ok:
            widget.setText(text)
            self.sheet.store.set_cell(self.sheet.sheet.title,key,text)

    def position(self):
        sheet=self.sheet
        for widget,obj in self.widgets:
            y=obj['y']
            original_y=0
            visible=True
            # Drawing positions use original row heights; collapse hidden rows like Excel.
            for row in range(sheet.rowCount()):
                dim=sheet.sheet.row_dimensions.get(row+1)
                height=max(12,int((dim.height if dim and dim.height else 16.5)*1.33))
                if original_y <= obj['y'] < original_y+height and sheet.isRowHidden(row):
                    visible=False
                    break
                if original_y+height <= obj['y'] and sheet.isRowHidden(row): y-=height
                original_y+=height
                if original_y>obj['y']:break
            widget.setVisible(visible)
            widget.setGeometry(int(obj['x']-sheet.horizontalScrollBar().value()),int(y-sheet.verticalScrollBar().value()),max(8,int(obj['w'])),max(8,int(obj['h'])))
