from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import database

Builder.load_file("kivy_files/edit_prod.kv")

class Edit_Prod_Scr(Screen):
    def on_pre_enter(self):
        product = self.manager.current_product
        self.ids.name_input.text = product[1]
        self.ids.category_input.text = product[2]
        self.ids.quantity_input.text = str(product[3])
        self.ids.price_input.text = str(product[4])

    def save_changes(self):
        pid = self.manager.current_product[0]
        name = self.ids.name_input.text
        category = self.ids.category_input.text
        qty = int(self.ids.quantity_input.text)
        price = float(self.ids.price_input.text)
        database.update_product(pid, name, category, qty, price)
        self.manager.current = "products"

    def delete_product(self):
        pid = self.manager.current_product[0]
        database.delete_product(pid)
        self.manager.current = "products"
