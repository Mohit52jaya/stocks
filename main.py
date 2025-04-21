import os, json
from datetime import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# ------------  DATA  ------------
BOOKS = {  # (same big dictionary as before)  **truncated here for brevity**
   "STATIC GK Hindi 3rd": 219, "STATIC GK English 3rd": 155,
    "Rambaan Railway Samanya vigyan.": 11, "Railway Samanya adhyayan 17000": 112,
    "RRB group D English practice sets": 7, "RRB group D Hindi practice sets": 154,
    "Brahmastra Railway STATIC GK": 96, "Railway studies English 17000": 65,
    "RRB group D Solved Paper": 472, "UPSSSC computer Hindi": 57,
    "Railway science English": 106, "ब्रह्मास्त्र रेलवे सामान्य विज्ञान": 156,
    "RRB group D रीजनिंग": 354, "RRB group D गणित": 232,
    "Current affairs": 14, "रेलवे ग्रुप डी सामान्य ज्ञान सामान्य विज्ञान": 151,
    "UP police Samanya adhyayan": 40, "SSC GD samanya adhyayan": 101,
    "UP police Samanya Hindi": 0, "SSC GD samanya Hindi.": 71,
    "UP police MATHS": 0, "SSC GD MATHS": 61,
    "UP police रीजनिंग": 26, "SSC GD रीजनिंग": 64,
    "दिल्ली पुलिस कांस्टेबल कंप्यूटर": 146, "Brahmastra STATIC GK सामान्य ज्ञान": 40,
    "SSC constable GD 12 practice": 93, "SSC CGL computer English": 4,
    "STATIC GK English 2nd": 45, "STATIC GK Hindi 2nd": 28,
    "Computer English": 10, "NTPC practice sets": 39,
    "Uttar Pradesh GK current affairs": 26, "RRB technician grade English": 26,
    "RRB Railway junior English": 30, "RRB technician grade Hindi": 41,
    "RRB Railway junior Hindi": 91, "ROARO Samanya adhyayan": 20,
    "ROARO Samanya. Hindi": 20, "RPF RPSF SI Practice sets": 32,
    "RPF RPSF constable practice": 41, "UPSSSC कनिष्ठ सहायक प्रैक्टिस": 19,
    "Railway STATIC GK purani wali": 18, "UP police constable practice set": 44,
    "RRB ALP practice set": 54, "SSC GD samanya Hindi purani": 13,
    "UPSSSC computer English": 50
}

SECTIONS = [
    ("Total Stocks",       "total"),
    ("Flipkart Orders",    "flipkart_orders"),
    ("Flipkart Returns",   "flipkart_returns"),
    ("Meesho Orders",      "meesho_orders"),
    ("Meesho Returns",     "meesho_returns"),
    ("Given to Shops",     "given_to_shops"),
    ("Arrived from Delhi", "arrived_from_delhi"),
    ("Return to Delhi",    "return_to_delhi"),
    ("Amazon Orders",      "amazon_orders"),
    ("Others",             "others"),
    ("Other Returns",      "other_returns")
]

# +1  → ADD to stock,  -1 → SUBTRACT from stock
SECTION_EFFECT = {
    "flipkart_orders":   -1,
    "meesho_orders":     -1,
    "amazon_orders":     -1,
    "given_to_shops":    -1,
    "return_to_delhi":   -1,
    "others":            -1,

    "flipkart_returns":  +1,
    "meesho_returns":    +1,
    "other_returns":     +1,
    "arrived_from_delhi":+1
}

# ------------  FILE HELPERS ------------
def load_json(path, default=None):
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default if default else {}, f, indent=2, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ----------  TOTAL STOCKS  ----------
class TotalStocksScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        # build UI once ------------
        lay = BoxLayout(orientation="vertical")
        scr = ScrollView()
        self.box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.box.bind(minimum_height=self.box.setter("height"))
        scr.add_widget(self.box)
        lay.add_widget(scr)

        self.total_lbl = Label(
    color=(1, 0, 0, 1),          # R,G,B,A  →  pure red, fully opaque
    size_hint_y=None,
    height=120
)
        lay.add_widget(self.total_lbl)
        lay.add_widget(Button(text="Save", size_hint_y=None, height=100, on_press=self.save))
        lay.add_widget(Button(text="Back", size_hint_y=None, height=100, on_press=self.go_back))
        self.add_widget(lay)

        # create dicts for inputs
        self.inputs = {}
        self._build_rows()               # first fill

    # ---- reload data every time screen is shown ----
    def on_pre_enter(self):
        self.data = load_json("data/total_stocks.json", BOOKS.copy())
        for b, qty in self.data.items():
            if b in self.inputs:
                self.inputs[b].text = str(qty)
        self.update_total()

    # build rows only once
    def _build_rows(self):
        self.data = load_json("data/total_stocks.json", BOOKS.copy())
        for book, qty in self.data.items():
            row = BoxLayout(size_hint_y=None, height=60)
            row.add_widget(Label(text=book, size_hint_x=.7))
            ti = TextInput(text=str(qty), multiline=False, size_hint_x=.3)
            self.inputs[book] = ti
            row.add_widget(ti)
            self.box.add_widget(row)

    def update_total(self):
        self.total_lbl.text = f"Total Books: {sum(int(e.text) for e in self.inputs.values())}"

    def save(self, _):
        for b, e in self.inputs.items():
            try: self.data[b] = int(e.text)
            except: pass
        save_json("data/total_stocks.json", self.data)
        self.update_total()

    def go_back(self, _):
        self.manager.current = "main"

# ------------  ORDER / RETURN SCREEN ------------
class OrderScreen(Screen):
    def __init__(self, title, fname, effect, **kw):
        super().__init__(**kw)
        self.display_title = title
        self.fname  = fname
        self.effect = effect          # +1 add, -1 subtract

        lay = BoxLayout(orientation="vertical")
        self.date_in = TextInput(text=datetime.now().strftime("%Y-%m-%d"),
                                 size_hint_y=None, height=60)
        lay.add_widget(self.date_in)

        scr, box = ScrollView(), BoxLayout(orientation="vertical", size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        self.inputs = {}
        for b in BOOKS:
            row = BoxLayout(size_hint_y=None, height=60)
            row.add_widget(Label(text=b, size_hint_x=.7))
            ti = TextInput(text="0", multiline=False, input_filter="int", size_hint_x=.3)
            self.inputs[b] = ti
            row.add_widget(ti)
            box.add_widget(row)
        scr.add_widget(box)
        lay.add_widget(scr)

        lay.add_widget(Button(text="Save", size_hint_y=None, height=90, on_press=self.save))
        lay.add_widget(Button(text="View Records", size_hint_y=None, height=90, on_press=self.pick_date))
        lay.add_widget(Button(text="Back", size_hint_y=None, height=90, on_press=self.go_back))
        self.add_widget(lay)

    # ---- logic ----
    def save(self, _):
        date = self.date_in.text.strip()
        if not date: return
        stock  = load_json("data/total_stocks.json", BOOKS.copy())
        orders = load_json(f"data/{self.fname}.json", {})
        day    = orders.get(date, {})

        for b, e in self.inputs.items():
            q = int(e.text or 0)
            if q:
                day[b] = day.get(b, 0) + q
                stock[b] = max(stock.get(b, 0) + q * self.effect, 0)
                e.text = "0"

        orders[date] = day
        save_json(f"data/{self.fname}.json", orders)
        save_json("data/total_stocks.json", stock)

    def pick_date(self, _):
        data = load_json(f"data/{self.fname}.json", {})
        root, scr = BoxLayout(orientation="vertical"), ScrollView()
        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        box.bind(minimum_height=box.setter("height"))
        for d in sorted(data.keys(), reverse=True):
            btn = Button(text=d, size_hint_y=None, height=60)
            btn.bind(on_press=lambda bt,d=d: self.show_day(data, d))
            box.add_widget(btn)
        scr.add_widget(box)
        root.add_widget(scr)
        Popup(title="Select Date", content=root, size_hint=(.9,.9)).open()

    def show_day(self, data, date):
        text = f"[b]{date}[/b]\n" + "\n".join(f"• {b} - {q}" for b,q in data[date].items())
        Popup(title=self.display_title, content=Label(text=text, markup=True),
              size_hint=(.9,.9)).open()

    def go_back(self, _):
        self.manager.current = "main"

# ------------  MAIN MENU ------------
class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay, scr = BoxLayout(orientation="vertical"), ScrollView()
        inner = BoxLayout(orientation="vertical", size_hint_y=None, padding=10, spacing=10)
        inner.bind(minimum_height=inner.setter("height"))
        for lbl,nm in SECTIONS:
            btn = Button(text=lbl, size_hint_y=None, height=200)
            btn.bind(on_press=lambda _,n=nm: setattr(self.manager, "current", n))
            inner.add_widget(btn)
        scr.add_widget(inner)
        lay.add_widget(scr)
        self.add_widget(lay)

# ------------  APP ------------
class StockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))          # keep main first
        sm.add_widget(TotalStocksScreen(name="total"))

        for lbl,nm in SECTIONS[1:]:
            effect = SECTION_EFFECT.get(nm, -1)         # default subtract
            sm.add_widget(OrderScreen(lbl, nm, effect, name=nm))
        return sm

if __name__ == "__main__":
    StockApp().run()