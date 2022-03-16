# Project name: Speech Synthesiser
#
# Authors: Marlena Krysiuk, Michalina Kopcińska, Paweł Frączkiewicz, Rafał Mycek
# WIEiT, Electronics 3rd grade students
#
# Project executing functionality of a Simple TTS
# The final result for Design Laboratory course
#
# Akademia Górniczno Hutnicza w Krakowie 2022
import pyttsx3
import re

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.image import Image



def speech(input):                            # Text input into string
    SpeechSynthesiser.engine.say(input)
    SpeechSynthesiser.engine.runAndWait()
    SpeechSynthesiser.engine.stop()

class SpeechSynthesiser(App):                 # Main class
    # Local vars
    vlevel = 0.5
    engRate = 125

    # pttsx3 Engine Settings
    engine = pyttsx3.init()  # initialization

    # Text speed rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', engRate)

    # Volume settings
    volume = engine.getProperty('volume')
    engine.setProperty('volume', vlevel)
    print(engine.getProperty('volume'))

    # Voice settings
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    def build(self):                        # Main UIX functionality
        self.window = FloatLayout()

        self.rec = Image(source='rec.jpg')  # Background image
        self.window.add_widget(self.rec)
        self.rec.pos_hint = {'x': 0.05, 'y': 0.1}
        self.rec.size_hint = (0.9, 1)

        self.greeting = Label(              # Label
                                text="TTS Speech Synthesizer",
                                font_size=32,
                                color='green',

                                )
        self.window.add_widget(self.greeting)
        self.greeting.pos_hint = {'center_x': 0.3, 'center_y': 0.9}
        self.greeting.size_hint = (0.3, 0.3)

        self.authors = Label(              # Label
                                text= "Design Laboratory project",
                                color= 'black',
                                font_size= 20,
                                halign= 'left'
        )
        self.window.add_widget((self.authors))
        self.authors.pos_hint = {'x': 0.08, 'y': 0.7}
        self.authors.size_hint = (0.3, 0.3)

        self.userText = TextInput(              # Text input bubble
                                    multiline=False,
                                    padding_y=(20, 20),
                                    size_hint=(0.5, 0.5)
                                    )
        self.window.add_widget(self.userText)
        self.userText.pos_hint = {'x': 0.1, 'y': 0.6}
        self.userText.size_hint = (0.4, 0.15)

        self.buttonPlay = Button(               # "PLAY" Button
                                        text="PLAY",
                                        size_hint=(1, 0.3),
                                        bold=True,
                                        background_color='green',
                                        )
        self.buttonPlay.bind(on_press=self.callback)
        self.window.add_widget(self.buttonPlay)
        self.buttonPlay.pos_hint = {'x': 0.53, 'y': 0.6}
        self.buttonPlay.size_hint = (0.3, 0.15)


        self.buttonAddVolume = Button(              # "VOLUME UP" Button
            text="Volume +",
            size_hint=(0.1, 0.3),
            bold=True,
            background_color='green'
        )
        self.buttonAddVolume.bind(on_press=self.change_volume_plus)
        self.buttonAddVolume.pos_hint = {'x':.2, 'y':.2}
        self.window.add_widget(self.buttonAddVolume)
        self.buttonAddVolume.pos_hint = {'x': 0.1, 'y': 0.4}
        self.buttonAddVolume.size_hint = (0.15, 0.15)


        self.buttonSubVolume = Button(             # "VOLUME DOWN" Button
            text="Volume -",
            size_hint=(0.1, 0.3),
            bold=True,
            background_color='green',
        )
        self.buttonSubVolume.bind(on_press=self.change_volume_minus)
        self.window.add_widget(self.buttonSubVolume)
        self.buttonSubVolume.pos_hint = {'x': 0.3, 'y': 0.4}
        self.buttonSubVolume.size_hint = (0.15, 0.15)

        # Rate Up and Down buttons - unused
        # # adding rate
        # self.buttonAddRate = Button(
        #     text="Rate +",
        #     size_hint=(1, 0.3),
        #     bold=True,
        #     background_color='green',
        # )
        # self.buttonAddRate.bind(on_press=self.change_rate_plus)
        # self.window.add_widget(self.buttonAddRate)
        #
        # # substracting rate
        # self.buttonSubRate = Button(
        #     text="Rate -",
        #     size_hint=(1, 0.3),
        #     bold=True,
        #     background_color='green',
        # )
        # self.buttonSubRate.bind(on_press=self.change_rate_minus)
        # self.window.add_widget(self.buttonSubRate)

        # self.VolumeControl = Slider(min=3, max=10)
        # self.window.add_widget(self.VolumeControl)
        # self.VolumeValue = Label()
        # self.VolumeControl.bind(value=self.Volume_value)

        self.rateText = Label(                  # Label
            text="Text read speed:",
            color='black',
            font_size=20,
            halign='left'
        )
        self.window.add_widget((self.rateText))
        self.rateText.pos_hint = {'x': 0.55, 'y': 0.37}
        self.rateText.size_hint = (0.3, 0.3)


        self.RateControl = Slider(min=100, max=300)     # Slider settings
        self.window.add_widget(self.RateControl)
        self.RateValue = Label()
        self.RateControl.bind(value=self.Rate_value)
        self.RateControl.pos_hint = {'x': 0.55, 'y': 0.4}
        self.RateControl.size_hint = (0.3, 0.1)


        self.wimg = Image(source='aghlogo.png')       # AGH Logo image
        self.window.add_widget(self.wimg)
        self.wimg.pos_hint = {'x': 0.6, 'y': 0.775}
        self.wimg.size_hint = (0.16, 0.16)


        Window.clearcolor = (0.7, 0.7, 0.71, 1)     # Background color


        return self.window

    # def Volume_value(self, instance, brightness2):
    #     self.VolumeValue.text = "%d" % brightness2
    #     self.vlevel= int(self.VolumeValue.text)
    #     self.vlevel=self.vlevel/10
    #     print(self.vlevel)
    #     self.engine.setProperty('volume', self.vlevel)

    def Rate_value(self, instance, brightness): # Get Rate value method
        self.RateValue.text = "%d" % brightness
        self.engRate= int(self.RateValue.text)
        # print(self.engRate)
        self.engine.setProperty('rate', self.engRate)

    def callback(self, instance, elsif=None): # Callback method
        keys = ".txt"
        match = re.findall(keys, self.userText.text)
        if match != [] :
            with open(self.userText.text, 'r') as f:
                lines = f.readlines()
            f.close()
            speech(lines)
        else:
            speech(self.userText.text)

    # def change_rate_plus(self,instance):
    #     # print(self.engRate)
    #     if self.engRate < 300:
    #         self.engRate = self.engRate + 10
    #         self.engine.setProperty('rate', self.engRate)
    #
    # def change_rate_minus(self, instance):
    #     # print(self.engRate)
    #     if self.engRate > 80:
    #         self.engRate = self.engRate - 10
    #         self.engine.setProperty('rate', self.engRate)

    def change_volume_plus(self,instance): #Volume Up method
        # print(self.vlevel)
        if self.vlevel < 0.9:
            self.vlevel = self.vlevel + 0.1
            self.engine.setProperty('volume', self.vlevel)

    def change_volume_minus(self, instance): #Volume Down method
        # print(self.vlevel)
        if self.vlevel > 0.3:
            self.vlevel = self.vlevel - 0.1
            self.engine.setProperty('volume', self.vlevel)



if __name__ == "__main__":                   # Build Main Window
     SpeechSynthesiser().run()







