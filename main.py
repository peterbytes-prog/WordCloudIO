from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.popup import Popup
class FileChoosePopUp(Popup):
    ref = ObjectProperty()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def Open(self,path,selection):
        print(path,selection)
        self.ref.from_file_path = selection[0]
        self.dismiss()
    pass
class WORDCLOUD(AnchorLayout):
    from_file_path = StringProperty('')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.file_chooser_popup = FileChoosePopUp(ref=self)
    def on_from_file_path(self,ins,val):
        self.from_file_path_input.text = self.from_file_path
        return
    pass

class MainApp(App):
    def build(self):
        return WORDCLOUD()
if __name__ == '__main__':
    MainApp().run()
