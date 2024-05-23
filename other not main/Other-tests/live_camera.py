from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

import cv2




class DefaultMain(Screen):
    pass


class LoginScreen(Screen):
    pass





Builder.load_string("""

ScreenManager:

    DefaultMain:
        name: "defaultmain"
    LoginScreen:
        name: "login"

<DefaultMain>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
    MDIconButton:
        icon: "arrow-left"
        pos_hint: {"center_y":0.95}
        user_font_size: "30sp"
        theme_text_color: "Custom"
        text_color: rgba(50, 138, 255, 255)
        on_release:
            root.manager.transition.direction = "right"
            root.manager.current = "login"
    MDLabel:
        text:"default page !"
        font_name: "Roboto-Bold"
        font_size: "25sp"
        size_hint_x: .85
        pos_hint: {"center_y":0.8,"center_x":0.5}
        halign: "center"
        color: rgba(4, 59, 92, 255)
    Button:
        text: "go to live"
        size_hint: 0.66,0.065
        pos_hint: {"center_x":0.5,"center_y":0.09}
        background_color: 0,0,0,0
        font_name: "Roboto"
        color: rgba(3, 138, 255, 255)
        on_release:
            root.manager.transition.direction = "left"
            root.manager.current = "login"


<LoginScreen>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
    MDIconButton:
        icon: "arrow-left"
        pos_hint: {"center_y":0.95}
        user_font_size: "30sp"
        theme_text_color: "Custom"
        text_color: rgba(50, 138, 255, 255)
        on_release:
            root.manager.transition.direction = "right"
            root.manager.current = "defaultmain"
    MDLabel:
        text:"login !"
        font_name: "Roboto-Bold"
        font_size: "25sp"
        size_hint_x: .85
        pos_hint: {"center_y":0.8,"center_x":0.5}
        halign: "center"
        color: rgba(4, 59, 92, 255)
    Button:
        text: "go back main page"
        size_hint: 0.66,0.065
        pos_hint: {"center_x":0.5,"center_y":0.2}
        background_color: 0,0,0,0
        font_name: "Roboto"
        color: rgba(3, 138, 255, 255)
        on_release:
            root.manager.transition.direction = "right"
            root.manager.current = "defaultmain"
    Button:
        text: "activate"
        size_hint: 0.66,0.065
        pos_hint: {"center_x":0.5,"center_y":0.09}
        background_color: 0,0,0,0
        font_name: "Roboto"
        color: rgba(3, 138, 255, 255)
        on_press: root.activelive()
        on_release: root.update()
""")
class CamApp(MDApp):

    def build(self):
        self.img1 = Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        # opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0 / 33.0)
        return layout
    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, -1)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()
