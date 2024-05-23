# api = ucDtXii5Jb4t5s9YQG6CPNmX
# programmer: Keven Quevedo ------ Date: 23/Apr/2023
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from remove_bg_api import RemoveBg
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


KV = """
MDFloatLayout:
    md_bg_color: 1,1,1,1
    Image:
        source: "images/foundfaceforkivy.png"
        pos_hint: {"center_x":0.5,"center_y":0.68}
    MDTextField:
        id: save_as
        hint_text: "Save As"
        pos_hint:{'center_x':.5,'center_y':.35}
    MDTextField:
        id: extension
        hint_text: "Extension"
        pos_hint:{'center_x':.5,'center_y':.25}
    MDRaisedButton:
        text: "Remove Bg"
        pos_hint:{'center_x':.5,'center_y':.115}
        on_release: app.remove_bg(save_as.text, extension.text)

"""


class DragAndDrop(MDApp):

    def build(self):
        return Builder.load_string(KV)



    def remove_bg(self, save_as, extension):
        remove_bg = RemoveBg("ucDtXii5Jb4t5s9YQG6CPNmX")

        remove_bg.remove_bg_file(input_path="images/foundfaceforkivy.png", out_path=save_as + "." + extension, size="preview", raw=False)



DragAndDrop().run()
