from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class TutorialApp(App):
    def build(self):
        mylayout = BoxLayout(orientation = "vertical")
        mylabel = Label(text = "My App")
        mybutton = Button(text="Hello World! Click me!!")
        mylayout.add_widget(mylabel)
        mybutton.bind(on_press = lambda a:print(mylabel.text))
        mylayout.add_widget(mybutton)
        return mylayout

TutorialApp().run()

