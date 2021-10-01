from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty,ObjectProperty,BooleanProperty,ListProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
import os
from os import path
from PIL import Image as PilImage
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import wordcloud,ImageColorGenerator

def generate_freq(text,punctuations,uninteresting_words):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    # punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    # uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    # "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    # "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    # "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    # "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]
    freq = {}
    cur_wrd = ''
    for char in text:
        if char in punctuations:
            continue
        if char==' ':
            if (len(cur_wrd)>0) and (cur_wrd not in uninteresting_words) :
                freq[cur_wrd] = freq.get(cur_wrd,0)+1
            cur_wrd = ''
            continue
        cur_wrd += char.lower()
    return freq
def verify_file(file):
    content = False
    #check if file exit
    if os.path.exists(file):
        #check if file is txt
        if os.path.splitext(file)[1] == '.txt':
            content = open(file,'r').read()
    return content
class ErrorPopUp(Popup):
    text = StringProperty('')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    pass
class FileChoosePopUp(Popup):
    ref = ObjectProperty()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def Open(self,path,selection):
        verified_file = verify_file(selection[0])
        if verified_file:
            self.ref.from_file_path = selection[0]
            self.ref.text = verified_file
            self.dismiss()
        else:
            ErrorPopUp(text='Invalid Input File').open()
            self.ref.from_file_path_input_border = [1,0,0,1]
            pass
        return
    pass
class AdvanceSettingButton(ButtonBehavior,Label):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
class MyLabel(ToggleButtonBehavior, Label):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def on_release(self,*args):
        print('press',self.state)
    pass
class PillList(ScrollView):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        pass
class PillListHeader(GridLayout):
    textAdder = ObjectProperty()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        pass
    def add_item(self,*args):
        text = self.text_input.text
        self.text_input.text = ''
        self.textAdder(text)
        return

class SelectImage(AnchorLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        pass
class SelectShape(AnchorLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        pass

class MySETTINGS(TabbedPanel):
    load = BooleanProperty(False)
    img_bg_color = ListProperty([1,1,1,1])
    excluded_chars = ListProperty([char for char in '''!()-[]{};:'"\,<>./?@#$%^&*_~'''])
    excluded_words = ListProperty(["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"])
    excluded_words_el = ListProperty()
    excluded_chars_el = ListProperty()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.loading_timer = Clock.schedule_interval(self.loading,0.5);
        print('Init Children: ',self.children)
    def add_new_ex_chars(self,text):
        self.excluded_chars.append(text)
        lbl = MyLabel(text=text)
        self.ex_char_container.list.add_widget(lbl)
        return
    def add_new_ex_word(self,text):
        self.excluded_words.append(text)
        lbl = MyLabel(text=text)
        self.ex_word_container.list.add_widget(lbl)
        return
    def get_excluded_chars(self):
        rtn = []
        for char_lbl in self.ex_char_container.list.children:
            if char_lbl.state == 'normal':
                rtn.append(char_lbl.text)
        return rtn
    def get_excluded_words(self):
        rtn = []
        for word_lbl in self.ex_word_container.list.children:
            if word_lbl.state == 'normal':
                rtn.append(word_lbl.text)
        return rtn
    def loading(self,*args):
        print('Loading ......')
        if len(self.children)>0:
            self.load = True
            Clock.unschedule(self.loading_timer)
        return
    def on_load(self,*args):
        for word in self.excluded_words:
            lbl = MyLabel(text=word)
            self.ex_word_container.list.add_widget(lbl)
        for char in self.excluded_chars:
            lbl = MyLabel(text=char)
            self.ex_char_container.list.add_widget(lbl)
        return
    def goto(self,name):
        self.app_pager.current = name
        pass
    def select_masking(self,text):
        self.mask_type_container.clear_widgets()
        if text=='Shape':
            self.mask_type_container.add_widget(SelectShape())
        else:
            self.mask_type_container.add_widget(SelectImage())
        pass
    pass
class WORDCLOUD(AnchorLayout):
    from_file_path = StringProperty('')
    to_path = StringProperty('Untitled.png')
    from_file_path_input_border = ListProperty([0,0,0,0])
    text = ''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.file_chooser_popup = FileChoosePopUp(ref=self)
    def on_from_file_path(self,ins,val):
        self.from_file_path_input.text = self.from_file_path
        return
    def set_to_path(self,text):
        self.to_path = text
        return
    def generate(self):
        alice_coloring = np.array(PilImage.open("./assets/alice_coloring.jpeg"))
        alice_coloring = np.array(PilImage.open("./assets/bg2.jpg"))
        image_colors = ImageColorGenerator(alice_coloring)

        cloud = wordcloud.WordCloud(background_color="white",mask=alice_coloring)
        setting = self.app_pager.settings_screen_app
        if self.text:
            freq=generate_freq(self.text,punctuations=setting.get_excluded_chars(),uninteresting_words=setting.get_excluded_words())

            img = cloud.generate_from_frequencies(freq)


            fig, axes = plt.subplots(1, 3)
            axes[0].imshow(img, interpolation="bilinear")
            # recolor wordcloud and show
            # we could also give color_func=image_colors directly in the constructor
            axes[1].imshow(img.recolor(color_func=image_colors), interpolation="bilinear")
            axes[2].imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
            for ax in axes:
                ax.set_axis_off()
            plt.show()


            # image = img.to_image()
            # if self.to_path:
            #     if not self.to_path.endswith('.png'):
            #         self.to_path+='.png'
            # else:
            #     self.to_path = 'Untitled.png'
            # image.save(self.to_path)
            # image.show()
        else:
            ErrorPopUp(text='Input File (.txt) Field Cannot be empty').open()
            self.from_file_path_input_border = [1,0,0,1]
            return
        pass
    def goto(self,name):
        self.app_pager.current = name
    pass
class AppPages(ScreenManager):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class MainApp(App):
    pages = ObjectProperty()
    def build(self):
        self.pages = AppPages()
        return self.pages
if __name__ == '__main__':
    MainApp().run()
