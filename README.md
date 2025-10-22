# E621 Windows Client

A lightweight **desktop client for [e621.net](https://e621.net/)** built with Python and PyQt6.
It uses the Chromium-based `QWebEngineView` for rendering, supports file downloads, persistent storage, and simple browser navigation.

## Features

* Browse **e621.net** directly without an external browser
* Persistent profile with local cache and history
* Built-in download manager
* Basic navigation controls:

  * Back / Forward
  * Reload page
  * Home
---

## Interface Overview

| Control | Function                                                    |
| ------- | ----------------------------------------------------------- |
| ← / →   | Navigate backward / forward through browsing history        |
| ↻       | Reload current page                                         |
| 🏠      | Go to the homepage ([https://e621.net/](https://e621.net/)) |

## Requirements

* **Python 3.10+**
* **PyQt6**
* **PyQt6-WebEngine**

Install dependencies with:

```bash
pip install PyQt6 PyQt6-WebEngine
```

## How to Run

### Run Python file
1. Clone or download this repository
2. Open a terminal in the project folder
3. Run:

```bash
python main.py
```

### Run exe file
1. Download the latest build from [Realeases](https://github.com/Soup-o-Stat/e621_windows_client/releases)
2. Run E621.exe

## Notes
E621 is blocked in some regions, so maybe you need to use proxy or VPN

![screenshot_1](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/1.png)
![screenshot_2](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/2.png)
![screenshot_3](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/3.png)
![screenshot_4](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/4.png)
![screenshot_5](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/5.png)
![screenshot_5](https://github.com/Soup-o-Stat/e621_windows_client/blob/main/screenshots/6.png)
