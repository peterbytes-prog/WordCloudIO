from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
class FileChoosePopUp(Popup):
    pass
class WORDCLOUD(AnchorLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.file_chooser_popup = FileChoosePopUp()
        self.file_chooser_popup.open()
    pass

class MainApp(App):
    def build(self):
        return WORDCLOUD()
if __name__ == '__main__':
    MainApp().run()
