# Programmer: Keven Quevedo-----Date Finished: 26/Apr/2023
# This program is about a Face Recognition that will find your Face.
# It also includes a Login System plus a Background Remover using Removebg api.

"""
NOTE: test again, i fix the database problem,
however now last time i used it didn't work, and lets find it.
error:
    - camera show incorrect angle 

"""





# KivyMD
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.camera import Camera
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from remove_bg_api import RemoveBg

# libraries that will are used in program
import mysql.connector
import cv2
import face_recognition
import time
import re

# The Window size for every window
Window.size = (410, 580)

# The GUI, using KivyMD
KV = """
# Here you can see the different pages in the application
ScreenManager:
    DefaultMain:
        name: "defaultmain"
    LoginScreen:
        name: "login"
    VerifiedLogin:
        name: "verifiedlogin"
    SignUp:
        name: "signup"
    OptionScreen:
        name: "optionscreen"
    ChangeBackground:
        name: "changebackground"
    OpenCamera:
        name: "alloption"
    ShowResult:
        name: "showresult"
    BgRemove:
        name: "bgremove"



<DefaultMain>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        Image:
            source: "assets/face_logo.jpeg"
            pos_hint: {"center_x":0.095,"center_y":0.92}
            size_hint: 0.2, 0.2
        MDLabel:
            text:"H E L L O  !"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .85
            pos_hint: {"center_y":0.8,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        MDLabel:
            text:"Best place to do Face Recognition plus with more exiting options"
            font_name: "Roboto-Bold"
            font_size: "15sp"
            size_hint_x: .60
            pos_hint: {"center_y":0.6,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        Button:
            text: "Login"
            size_hint: 0.66,0.065
            pos_hint: {"center_x":0.5,"center_y":0.18}
            background_color: 0,0,0,0
            font_name: "Roboto"
            on_release:
                root.manager.transition.direction = "left"
                root.manager.current = "login"
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [5]
        Button:
            text: "Sign Up"
            size_hint: 0.66,0.065
            pos_hint: {"center_x":0.5,"center_y":0.09}
            background_color: 0,0,0,0
            font_name: "Roboto"
            color: rgba(3, 138, 255, 255)
            on_release:
                root.manager.transition.direction = "left"
                root.manager.current = "signup"
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 255)
                Line:
                    width: 1.2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100

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
        text: "Login"
        font_name: "Roboto"
        halign: "center"
        pos_hint: {"center_x":0.5,"center_y":0.60}
        font_size: "35sp"
        color: rgba(4, 59, 92, 255)
    MDTextField:
        id: UsernameText
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: (0.7,0.1)
        hint_text : 'Username'
        helper_text: 'ONLY EMAIl ACCEPTED'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
    MDTextField:
        id: PasswordText
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint: (0.7,0.1)
        password: True
        hint_text : 'Password'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color

    Button:
        id: DisabledButton
        text: "Login"
        size_hint: 0.50,0.065
        pos_hint: {"center_x":0.5,"center_y":0.28}
        background_color: 0,0,0,0
        font_name: "Roboto"
        on_press: root.receive_data(UsernameText,PasswordText)
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]
    MDLabel:
        text: "Dont have account!!"
        font_name: "Roboto"
        halign: "center"
        pos_hint: {"center_x": 0.44, "center_y": 0.21}
        font_size: "12sp"
        color: rgba(4, 59, 92, 255)
    MDTextButton:
        text:"Sign up"
        color: 98/255, 170/255, 243/255, 1
        pos_hint: {"center_x": 0.64, "center_y": 0.21}
        font_size: "12sp"
        on_press:
            root.manager.transition.direction = "left"
            root.manager.current = "signup"     

<VerifiedLogin>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
    Button:
        text: "Logout"
        pos_hint: {"center_y":0.96}
        size_hint: 0.2,0.06
        background_color: 0,0,0,0
        color: rgba(3, 138, 255, 255)
        on_release:
            root.manager.transition.direction = "right"
            root.manager.current = "defaultmain"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
    MDLabel:
        text: "Hello, Welcome to READ ME"
        halign: "center"
        pos_hint: {"center_x":0.5,"center_y":0.75}
        font_size: "21sp"
    MDFlatButton:
        text: "Options"
        halign: "center"
        pos_hint: {"center_x":0.5,"center_y":0.45}
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press: 
            root.manager.transition.direction = "left"
            root.manager.current = "optionscreen"
    MDBottomNavigation:
        panel_color: 0,0,0,0
        

<SignUp>:
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
        text:"Sign Up!"
        font_name: "Roboto-Bold"
        font_size: "30sp"
        pos_hint: {"center_y":0.65,"center_x":0.5}
        halign: "center"
        color: rgba(4, 59, 92, 255)
    MDTextField:
        id: UsernameText
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: (0.7,0.1)
        hint_text : 'Username'
        helper_text: 'ONLY EMAIl ACCEPTED'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
    MDTextField:
        id: PasswordText
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint: (0.7,0.1)
        password: True
        hint_text : 'Password'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
    MDLabel:
        text: "Already have account!!"
        font_name: "Roboto"
        halign: "center"
        pos_hint: {"center_x": 0.44, "center_y": 0.21}
        font_size: "12sp"
        color: rgba(4, 59, 92, 255)
    MDTextButton:
        text:"Login"
        color: 98/255, 170/255, 243/255, 1
        pos_hint: {"center_x": 0.64, "center_y": 0.21}
        font_size: "12sp"
        on_press:
            root.manager.transition.direction = "left"
            root.manager.current = "login"
    Button:
        text: "Sign Up"
        size_hint: 0.50,0.065
        pos_hint: {"center_x":0.5,"center_y":0.28}
        background_color: 0,0,0,0
        font_name: "Roboto"
        on_press: root.send_data(UsernameText,PasswordText)
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]

<OptionScreen>
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
            root.manager.current = "verifiedlogin"
    MDFlatButton:
        text: "Facial Recognition"
        halgin: "center"
        pos_hint: {"center_x":0.5,"center_y":0.45}
        icon: "face-recognition"
        text_color:"black"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press:
            root.manager.current = "alloption"

<ChangeBackground>
    MDFloatLayout:
        md_bg_color: 1,1,1,1
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
            on_release: root.start_process(save_as.text, extension.text)
        MDFlatButton:
            text: "See Result"
            pos_hint: {"center_x":0.5,"center_y":0.05}
            on_release: root.manager.current = "bgremove"

<BgRemove>
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
                root.manager.current = "verifiedlogin"
        MDFlatButton:
            text: "show it"
            pos_hint: {"center_x": 0.5,"center_y":0.95}
            on_press: root.returnimage()
            

<OpenCamera>:
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
            root.manager.current = "verifiedlogin"

    MDFlatButton:
        text: "2 Capture New Face"
        halgin: "center"
        pos_hint: {"center_x":0.2,"center_y":0.35}
        icon: "face-recognition"
        text_color:"blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press: root.take_new_pic()
        
    MDFlatButton:
        text: "3 Find MY Face"
        halgin: "center"
        pos_hint: {"center_x":0.2,"center_y":0.15}
        icon: "face-recognition"
        text_color:"blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press: root.findME()
        
    Camera:
        id: camera
        halgin: "center"
        pos_hint: {"center_x":0.5,"center_y":0.70}
        size_hint_x: 0.7
        size_hint_y: 0.5
        index: 0
        resolution: (640,480)
        play: False
        
    MDFlatButton:
        text: "4 Turn Off Camera"
        halgin: "center"
        pos_hint: {"center_x":0.8,"center_y":0.15}
        icon: "face-recognition"
        text_color:"blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press: camera.play = False
        
    MDFlatButton:
        text: "1 Activate Camera"
        pos_hint: {"center_x":0.8,"center_y":0.35}
        on_press: camera.play = not camera.play
        text_color: "blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
    
    MDFlatButton:
        text: "5 Go to Result Page"
        halgin: "center"
        pos_hint: {"center_x":0.5,"center_y":0.25}
        icon: "face-recognition"
        text_color: "blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press:
            root.manager.transition.direction = "right"
            root.manager.current = "showresult"
           
 
<ShowResult>:
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
            root.manager.current = "verifiedlogin"

    MDFlatButton:
        text: "show it"
        halgin: "center"
        pos_hint: {"center_x":0.5,"center_y":0.25}
        icon: "face-recognition"
        text_color: "blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press: root.showit()
        
    MDFlatButton:
        text: "Change background of image"
        halgin: "center"
        pos_hint: {"center_x":0.5,"center_y":0.15}
        icon: "face-recognition"
        text_color:"blue"
        canvas.before:
            Color:
                rgb: rgba(50, 138, 255, 255)
            Line:
                width: 1.2
                rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
        on_press:
            root.manager.current = "changebackground"

"""


# Start of all classes
# removed bg window
class ShowResult(Screen):
    def showit(self):
        self.add_widget(Image(source="images/known_face.png"))


# FaceRecognition window
class OpenCamera(Screen):
    # function to take a pic when button is pressed.
    def take_new_pic(self, mirror=True):
        # this opens camera using OpenCv
        camera = cv2.VideoCapture(0)

        while True:
            ret_val, img = camera.read()
            if camera.isOpened():
                img = cv2.flip(img, 1)
                # here it saves the pic it just took
                cv2.imwrite("images/facepass.png", img)
                the_check = face_recognition.load_image_file("images/facepass.png")
                # change color of the pic necessary for face recognition
                the_check = cv2.cvtColor(the_check, cv2.COLOR_BGR2RGB)
                the_check_face = []

                # the try and except, to avoid big errors that would cause the program to end.
                try:
                    the_check_face = face_recognition.face_encodings(the_check)[0]

                except IndexError:
                    # if this IndexError is show then this error pops up in the window.
                    face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                    self.dialog = MDDialog(
                        title='face not found',
                        text="Face was not found, try again.",
                        size_hint=(0.7, 0.2),
                        buttons=[face_not_found])
                    self.dialog.open()
                break
        # this closes the OpenCV camera
        cv2.destroyAllWindows()

    # this function is used to close the popup error messages.
    def close_face_not_found_dialogue(self, obj):
        self.dialog.dismiss()

    # this function is used to find set the face to find
    def findME(self):
        # turn on camera
        camera = cv2.VideoCapture(0)

        # resting time, since without it the camera doesn't load correctly

        while True:
            ret_val, img = camera.read()
            if camera.isOpened():
                img = cv2.flip(img, 1)
                cv2.imwrite("images/known_face.png", img)
                the_check = face_recognition.load_image_file("images/known_face.png")
                the_check = cv2.cvtColor(the_check, cv2.COLOR_BGR2RGB)
                the_check_face = []
                try:
                    the_check_face = face_recognition.face_encodings(the_check)[0]

                except IndexError:
                    face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                    self.dialog = MDDialog(
                        title='face not found',
                        text="Face was not found, try again.",
                        size_hint=(0.7, 0.2),
                        buttons=[face_not_found])
                    self.dialog.open()
                break
        cv2.destroyAllWindows()

        # Open camera

        # Check if the webcam is opened correctly

        running = True
        if running:
            # variable baseing holding the image facepass.png
            baseing = face_recognition.load_image_file("images/facepass.png")
            baseing = cv2.cvtColor(baseing, cv2.COLOR_BGR2RGB)
            encodingmyface = []
            # the try and except, is used incase when loading image facepass.png there is no face
            try:
                encodingmyface = face_recognition.face_encodings(baseing)[0]
            # when IndexError is found, the popup error will appear
            except IndexError:
                face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                self.dialog = MDDialog(
                    title='face not found',
                    text="Face was not found, try again.",
                    size_hint=(0.7, 0.2),
                    buttons=[face_not_found])
                self.dialog.open()
            # loading the second image taken
            cameraimg = face_recognition.load_image_file("images/known_face.png")
            cameraimg = cv2.cvtColor(cameraimg, cv2.COLOR_BGR2RGB)
            encodepictaken = []
            # checking incase there is no face in the image
            try:
                encodepictaken = face_recognition.face_encodings(cameraimg)[0]
            # if no image then this IndexError is shown
            except IndexError:
                face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                self.dialog = MDDialog(
                    title='face not found',
                    text="Face was not found, try again.44",
                    size_hint=(0.7, 0.2),
                    buttons=[face_not_found])
                self.dialog.open()
            result = []
            # incase there is no face in either of the images being compared this try and except will start.
            try:
                # comparing to see if the faces match.
                result = face_recognition.compare_faces([encodingmyface], encodepictaken)
            # if face is not found ValueError will happen and then this message will be shown.
            except ValueError:
                face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                self.dialog = MDDialog(
                    title='face not found',
                    text="Face was not found, try again.55",
                    size_hint=(0.7, 0.2),
                    buttons=[face_not_found])
                self.dialog.open()
            # the final result will be held in this variable
            result_to_string = str(result)
            # open a file
            with open("whoisloginedin.txt", "r") as file:
                last_line = file.readlines()[-1]
                # split the email at the @ sign
                splited = last_line.split("@")
            # the new email, now just name will be held in this variable
            name_after_split = splited[0]
            # if result is True meaning the faces match it will continue
            if result_to_string == "[True]":
                name = name_after_split.upper()
                knownpictaken = face_recognition.face_locations(cameraimg)[0]
                # shows the green square around the face
                cv2.rectangle(cameraimg, (knownpictaken[3], knownpictaken[0]), (knownpictaken[1], knownpictaken[2]),(0, 255, 0), 2)
                # puts the text close to the square to show name of user
                cv2.putText(cameraimg, name, (knownpictaken[3], knownpictaken[0] + 260), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0, 2))
                # the new image is saved again but with the face found
                cv2.imwrite("images/known_face.png", cameraimg)
            else:
                # if not true then an error message shown
                def close_face_not_found_dialogue(self, obj):
                    self.dialog.dismiss()
                    # the error message
                    face_not_found = MDFlatButton(text='Retry', on_release=self.close_face_not_found_dialogue)
                    self.dialog = MDDialog(
                        title='NO FACE....?!?!',
                        text="Your Face not found",
                        size_hint=(0.7, 0.2),
                        buttons=[close_face_not_found_dialogue])
                    # close message
                    self.dialog.open()


# where all the options will be
class OptionScreen(Screen):
    pass


# change the background window
class ChangeBackground(Screen):
    # when this window and class starts this will happen
    def on_enter(self):
        # add_widget(Kivymd) add the image
        self.add_widget(Image(
            source="images/known_face.png",
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        ))

    # the function to save the image of background removed.
    def start_process(self, save_as, extension):
        # RemoveBg is an online background remover with the option of python use.
        # Using the api to remove backgrounds.
        # this is the api key.
        remove_bg = RemoveBg("ucDtXii5Jb4t5s9YQG6CPNmX")
        # this is the process of saving the file with the correct name and extension.
        remove_bg.remove_bg_file(input_path="images/known_face.png", out_path=save_as + "." + extension,
                                 size="preview", raw=False)
        # a file write the name of file and the extension for later use
        f = open("path_image","a")
        f.write(save_as + "." + extension)


# Background Remove Window
class BgRemove(Screen):
    def returnimage(self):
        # here I use the file to read the content, which would contain the name and the extension.
        file = open("path_image", "r")
        # variable holding the name and extension.
        location_of_image = file.read()
        # then once with the name and the extension, we can display the image.
        self.add_widget(Image(
            source=location_of_image,
            pos_hint={"center_x":0.5,"center_y":0.5}
            ))


# First window when program starts
class DefaultMain(Screen):
    pass


# the login window
class LoginScreen(Screen):
    # the database connection
    database = mysql.connector.Connect(host="localhost", user="root", password="12345678;", database="loginform")
    cursor = database.cursor()

    # the function to check the login username and password
    def receive_data(self, UsernameText, PasswordText):
        # open file
        file_object = open('whoisloginedin.txt', 'a')
        # write in file the username
        file_object.write(f'{UsernameText.text}\n')
        # close file
        file_object.close()
        # write MySQL script
        self.cursor.execute("select * from logindata")
        username_list = []
        # add the username from database to the username_list[]
        for i in self.cursor.fetchall():
            username_list.append(i[0])
        # if the username is found in the username list then select the password for usernametext
        if UsernameText.text in username_list and UsernameText.text != "":
            self.cursor.execute(f"select password from logindata where email = '{UsernameText.text}'")
            for j in self.cursor:
                # if the password is correct
                if PasswordText.text == j[0]:
                    # switch to verifiedlogin window if correct
                    MDApp.get_running_app().root.current = "verifiedlogin"
                else:
                    # if not then the message is shown
                    cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                    self.dialog = MDDialog(
                        title='Password Incorrect',
                        text="Incorrect Password",
                        size_hint=(0.7, 0.2),
                        buttons=[cancel_btn_username_dialogue])
                    self.dialog.open()
        else:
            # if username is invalid then this message is shown
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Invailed Username',
                text="Email doesn't exist",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

    # close the popups function
    def close_username_dialogue(self, obj):
        self.dialog.dismiss()


# the window verified login
class VerifiedLogin(Screen):
    pass


# Sign up Window
class SignUp(Screen):
    # the regex is used later for checking if it is an email or not
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # connect to the database I made with MySQL
    database = mysql.connector.Connect(host="localhost", user="root", password="12345678;", database="loginform")
    # used to write MySQL script
    cursor = database.cursor()

    # function to check username and password
    def send_data(self, UsernameText, PasswordText):
        # check the username if it is an email
        if re.fullmatch(self.regex, UsernameText.text):
            # the MySQL to get the email with the username input
            self.cursor.execute(f"SELECT email FROM logindata WHERE email='{UsernameText.text}'")
            checkUsername = self.cursor.fetchone()
            # check if username exist in database
            if checkUsername != None:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_error)
                self.dialog = MDDialog(
                    title='Email Already in use',
                    text="Email already in use",
                    size_hint=(0.7, 0.2),
                    buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
            else:
                # if username is not found put username and password in database to store as a login detail
                self.cursor.execute(f"insert into logindata values ('{UsernameText.text}','{PasswordText.text}');")
                self.database.commit()
                UsernameText.text = ''
                PasswordText.text = ''
                # goes to the main window after sign up in valid
                MDApp.get_running_app().root.current = "verifiedlogin"
        else:
            # if the username isn't an email this message will appear
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(
                title='Invailed Username',
                text="Invaild Username, has to be an email",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

    # function to close pop up message
    def close_username_dialogue(self, obj):
        self.dialog.dismiss()


# the start of Program class
class ReadME(MDApp):
    def build(self):
        # this will load the GUI part of the code named KV at the beginning
        GUI = Builder.load_string(KV)
        return GUI

    # when the window closes these are the last actions to do
    def on_stop(self):
        # open a file
        f = open("whoisloginedin.txt", "a")
        f.seek(0)
        # delete all contents in file
        f.truncate()
        f = open("path_image","a")
        f.seek(0)
        f.truncate()
        # turn of camera
        Camera(play=False)


# run the Class ReadME
ReadME().run()
