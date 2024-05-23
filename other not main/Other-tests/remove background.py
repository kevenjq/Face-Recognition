# api = ucDtXii5Jb4t5s9YQG6CPNmX
# programmer: Keven Quevedo ------ Date: 25/Feb/2023
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from remove_bg_api import RemoveBg
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


KV = """
MDFloatLayout:
    MDCard:
        pos_hint:{'center_x':.5,'center_y':.7}
        size_hint: .5,.5
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: app.path
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

    path = StringProperty()

    def build(self):
        Window.bind(on_dropfile=self.on_file_drop)
        return Builder.load_string(KV)

    def on_file_drop(self, window, file_path):
        self.path = str(file_path.decode("utf-8"))
        print(self.path)

    def remove_bg(self, save_as, extension):
        remove_bg = RemoveBg("ucDtXii5Jb4t5s9YQG6CPNmX")
        try:
            remove_bg.remove_bg_file(input_path=self.path, out_path=save_as + "." + extension, size="preview", raw=False)
        except FileNotFoundError:
            pass
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='NO Image found',
                text="Please drag an image to the square, and Try Again",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

DragAndDrop().run()
