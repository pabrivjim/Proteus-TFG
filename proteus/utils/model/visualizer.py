# ==========================================================================
# File: visualizer.py
# Description: File where is located the visualizers.
# Date: 
# Version: 1.0.0
# Author: Gamaza
# ==========================================================================
import json
from os import pardir
from os.path import abspath, dirname, join
from lxml import etree as ET
import markdown
from PyQt5.QtCore import QUrl, pyqtSignal, QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from lxml import etree
from proteus.model.object import Object

from proteus.model.project import Project
from ..config import Config
import proteus
import os


# DEBUG INSPECTOR 
DEBUG_PORT = '5588'
DEBUG_URL = 'http://127.0.0.1:%s' % DEBUG_PORT
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT


def send_to_view(project, page, index=0):
    """
    Sends project data to view in JSON format.
    """
    proteus.logger.info('visualizer - send to view')
    
    message = {
        "action": "update",
        "content": {
            "data": project,
            "currentDocument": index
        }
    }
    data = json.dumps(message)
    page.runJavaScript(f"handleMessage({data})")


def convert_markdown(elements):
    """
    Convert XSLT element to markdown.
    """
    proteus.logger.info('visualizer - convert markdown')
    
    try:
        return markdown.markdown(elements[0].text, extensions=['md_mermaid', 'extra', 'codehilite'])
    except Exception:
        return elements[0].text


views = Config.load_views()


class Visualizer(QWebEngineView):
    """
    Class to render and visualizing views.
    """
    toHtmlFinished = pyqtSignal()

    def __init__(self):
        proteus.logger.info('Init Visualizer')
        super(Visualizer, self).__init__()
        self.view = 0

        # DEBUG INSPECTOR 
        self.inspector = QWebEngineView()
        self.inspector.setWindowTitle('Web Inspector')
        self.inspector.load(QUrl(DEBUG_URL))
    
    # DEBUG INSPECTOR 
    def handleLoaded(self, ok):
        if ok:
            self.page().setDevToolsPage(self.inspector.page())
            self.inspector.show()

    def setView(self, view: int) -> None:
        """
        Sets current view.

        :param view: Current view index.
        """
        proteus.logger.info('visualizer - set view')
        
        self.view = view

    def load(self, view: str, project: Project, index: int):
        """
        Compiles current view and set html to QWebEngineView.

        :param view: view to load.
        :param project: project data.
        :param index: selected document index.
        """
        proteus.logger.info('visualizer - load')

        update_actions = {
            "html": self.update_html,
            "xslt": self.update_xslt
        }

        # Select action to perform
        # self.view = view
        perform_action = update_actions[views[self.view]["type"]]
        perform_action(project, index)

    def focus(self, id: str) -> None:
        """
        Focus an object in html document.

        :param id: Id of object to focus.
        """
        proteus.logger.info('visualizer - focus')
        
        self.page().runJavaScript(f"""
            var object = document.getElementById('{id}');
            if (object) object.scrollIntoView();
        """)

    def update(self, project: dict, index: int) -> None:
        """
        Updates view on project changes.

        :param project: updated project dict.
        :param index: selected document index.
        """
        proteus.logger.info('visualizer - update')
        
        if project.documents:
            self.load(None, project, index)
        else:
            self.page().setHtml("")

    def update_html(self, project: dict, index: int) -> None:
        """
        Send project data to html view.

        :param project: project data.
        :param index: current document index.
        """
        proteus.logger.info('visualizer - update html')
        
        path = abspath(join(dirname(__file__), pardir,
                            views[self.view]["path"]))
        super().load(QUrl.fromLocalFile(path))

        self.page().loadFinished.connect(lambda: send_to_view(project,
                                                              self.page(),
                                                              index))

    def update_xslt(self, project: Project, index: int) -> None:
        """
        Compiles XSLT view and set updated html to page.

        :param project: project data.
        :param index: current document index.
        """
        proteus.logger.info('visualizer - update xslt')
        
        ns = etree.FunctionNamespace("https://proteus.us.es")
        ns.prefix = "proteus"
        ns['markdown'] = lambda context, content: convert_markdown(content)

        path = abspath(join(dirname(__file__), pardir,
                            views[self.view]["path"]))
        
        if(index == len(project.documents)):
            index = index-1
        current_document: Object = list(project.documents.values())[index]
        xml = current_document.generate_xml()
        xml.tag = "document"

        dom = etree.fromstring(ET.tostring(xml).decode())
        xslt = etree.parse(path)
        transform = etree.XSLT(xslt)
        new_dom = transform(dom)

        super().setHtml(etree.tostring(new_dom).decode())

    def save_pdf(self, save_path: str) -> None:
        """
        Saves view onto a pdf document.

        :param save_path: file path.
        """
        proteus.logger.info('visualizer - save pdf')
        
        self.page().printToPdf(save_path)


    #https://stackoverflow.com/questions/47067050/is-there-any-way-to-call-synchronously-the-method-tohtml-which-is-qwebenginepa
    def store_html(self, html):
        proteus.logger.info('visualizer - store html')
        self.html = html
        self.toHtmlFinished.emit()

    def save_html(self, save_path: str) -> None:
        """
        Saves view onto a html document.

        :param save_path: file path.
        """
        proteus.logger.info('visualizer - save html')
        
        current_page = self.page()
        current_page.toHtml(self.store_html)
        loop = QEventLoop()
        self.toHtmlFinished.connect(loop.quit)
        loop.exec_()
        with open(save_path, "w") as f:
            f.write(self.html)
