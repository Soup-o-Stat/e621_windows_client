from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QHBoxLayout, QLineEdit, QPushButton)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from pypresence import Presence
import threading
import time
import sys
import os

ver = "0.0.2"

class E621Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"E621 Client {ver}")
        self.setGeometry(100, 100, 1200, 1000)

        try:
            self.setWindowIcon(QIcon("icon.ico"))
        except:
            pass

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        profile_name = "e621-persistent-profile"
        data_path = os.path.join(base_path, profile_name)
        os.makedirs(data_path, exist_ok=True)

        downloads_path = os.path.join(base_path, "downloads")
        os.makedirs(downloads_path, exist_ok=True)

        self.profile = QWebEngineProfile(profile_name, self)
        self.profile.setDownloadPath(downloads_path)
        self.profile.setPersistentStoragePath(data_path)
        self.profile.setCachePath(os.path.join(data_path, "cache"))
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.downloadRequested.connect(self.on_download_requested)

        self.page = QWebEnginePage(self.profile, self)
        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)

        self.browser = QWebEngineView()
        self.browser.setPage(self.page)
        self.browser.setUrl(QUrl("https://e621.net/"))

        self.setup_ui()

        self.browser.urlChanged.connect(self.update_urlbar)

        threading.Thread(target=self.run_discord_rpc, daemon=True).start()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)

        self.back_btn = QPushButton("←")
        self.back_btn.setToolTip("Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setFixedSize(30, 30)

        self.forward_btn = QPushButton("→")
        self.forward_btn.setToolTip("Forward")
        self.forward_btn.clicked.connect(self.go_forward)
        self.forward_btn.setFixedSize(30, 30)

        self.reload_btn = QPushButton("↻")
        self.reload_btn.setToolTip("Reload")
        self.reload_btn.clicked.connect(self.browser.reload)
        self.reload_btn.setFixedSize(30, 30)

        self.home_btn = QPushButton("🏠")
        self.home_btn.setToolTip("Home")
        self.home_btn.clicked.connect(self.go_home)
        self.home_btn.setFixedSize(30, 30)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.url_bar)

        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.browser)

        main_widget.setLayout(main_layout)

    def go_home(self):
        self.browser.setUrl(QUrl("https://e621.net/"))

    def go_back(self):
        if self.browser.page().history().canGoBack():
            self.browser.page().history().back()

    def go_forward(self):
        if self.browser.page().history().canGoForward():
            self.browser.page().history().forward()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))

    def update_urlbar(self, url):
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def on_download_requested(self, download):
        url = download.url().toString()
        filename = os.path.basename(url)

        downloads_dir = self.profile.downloadPath()
        file_path = os.path.join(downloads_dir, filename)

        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(file_path):
            filename = f"{base_name}_{counter}{ext}"
            file_path = os.path.join(downloads_dir, filename)
            counter += 1

        download.setDownloadFileName(filename)
        download.accept()
        print(f"Downloading: {filename} → {downloads_dir}")

    def run_discord_rpc(self):
        try:
            CLIENT_ID = "1430473078936178698"
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            print("[Discord RPC] Connected")

            start_time = int(time.time())

            while True:
                rpc.update(
                    state="Browsing e621.net",
                    details="  ",
                    large_image="icon",
                    large_text="E621 Client",
                    small_image=None,
                    start=start_time,
                )
                time.sleep(15)
        except Exception as e:
            print(f"[Discord RPC] Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("E621 Client")
    app.setOrganizationName("E621 Client")
    app.setOrganizationDomain("e621.net")

    window = E621Client()
    window.show()

    sys.exit(app.exec())
