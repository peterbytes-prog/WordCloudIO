import kivy
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout


class WORDCLOUD(AnchorLayout):
    pass

class MainApp(App):
    def build(self):
        return WORDCLOUD()
if __name__ == '__main__':
    MainApp().run()
