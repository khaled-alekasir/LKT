from Control.Expedia import Expedia
from View.ConsoleView import ConsoleView
from View.WebView import WebView

expedia = Expedia()
c = WebView(expedia)
c.run()