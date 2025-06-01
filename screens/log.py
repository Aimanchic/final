from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import database

Builder.load_file("kivy_files/log.kv")

class Log_Scr(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        role = database.authenticate_user(username, password)
        if role:
            app = self.manager.app
            app.user_role = role
            self.manager.current = "products"
        else:
            self.ids.message.text = "Неверный логин или пароль"
