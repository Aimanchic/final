from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import database

Builder.load_file("kivy_files/new_prod.kv")

class New_Prod_Scr(Screen):
    def add_product(self):
        name = self.ids.name_input.text
        category = self.ids.category_input.text
        quantity = int(self.ids.quantity_input.text)
        price = float(self.ids.price_input.text) if self.ids.price_input.text else 0
        database.add_product(name, category, quantity, price)
        self.manager.current = "products"