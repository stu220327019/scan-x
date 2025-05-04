# Prerequisites

-   Python 3.12 or above.
-   VirusTotal [API key](https://www.virustotal.com/gui/my-apikey).
-   Qt is usually not required to be installed separately. But since we use [Qt WebEgine](https://doc.qt.io/qt-6/qtwebengine-overview.html) for graph chart rendering, which is not a Qt core module, you will need to install it via [Qt Online Installer](https://www.qt.io/download-qt-installer-oss).


# Setup

1.  Create a `config.ini` in the project root folder with the following contents:
    
    ```conf
    [VirusTotal]
    apikey = YOUR_VIRUSTOTAL_API_KEY
    ```

2.  Install Python dependendies via `pip` or `pipenv`:
    
    ```sh
    $ pip install -r requirements.txt
    ```
    
    ```sh
    $ pipenv install
    ```

3.  Run `python main.py`.
