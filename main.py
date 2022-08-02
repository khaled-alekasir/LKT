from Control.Expedia import Expedia
from View.ConsoleView import ConsoleView
from View.WebView import WebView

expedia = Expedia()
view = ConsoleView(expedia)
view.run()