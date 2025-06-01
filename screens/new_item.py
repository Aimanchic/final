from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import database

Builder.load_file("kivy_files/new_item.kv")

class New_It_Scr(Screen):
    def on_pre_enter(self):
        self.ids.ingredient_box.clear_widgets()
        self.ingredient_list = []
        self.product_dict = database.get_all_products_dict()

        for product_id, name in self.product_dict.items():
            row = BoxLayout(size_hint_y=None, height=70, spacing=5)
            label = Label(text=name, size_hint_x=0.6)
            qty_input = TextInput(hint_text="Кол-во", input_filter='int', size_hint_x=0.4)
            row.add_widget(label)
            row.add_widget(qty_input)
            self.ids.ingredient_box.add_widget(row)

    def save_item(self):
        name = self.ids.item_name.text.strip()
        price_text = self.ids.price_input.text.strip()

        if not name or not price_text:
            self.ids.message.text = "Введите название и цену"
            return

        try:
            price = float(price_text)
        except ValueError:
            self.ids.message.text = "Неверная цена"
            return

        ingredients = []
        for i, (product_id, _) in enumerate(self.product_dict.items()):
            qty_input = self.ids.ingredient_box.children[::-1][i].children[0]
            qty_text = qty_input.text.strip()
            if qty_text.isdigit() and int(qty_text) > 0:
                ingredients.append((product_id, int(qty_text)))

        if not ingredients:
            self.ids.message.text = "Укажите хотя бы один ингредиент"
            return

        database.add_item(name, ingredients, price)
        self.ids.item_name.text = ""
        self.ids.price_input.text = ""
        self.ids.message.text = ""
        self.manager.current = "products"
