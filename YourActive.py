import datetime
import subprocess
from PIL import Image
import customtkinter as ctk
import uptime
import pywinstyles
import os

language = 'eng'


def change_language(index):
    try:
        with open(f'./Localization/{language}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[index].strip() if index < len(lines) else f"Missing translation {index}"
    except FileNotFoundError:
        return f"Language file {language}.txt not found"

class TimeWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.show_time_above = False
        self.geometry('100x50+10+10')
        self.overrideredirect(True)
        self.configure(background='transparent')
        self.wm_attributes("-topmost", True)

        font = ctk.CTkFont(family="Minecart LCD", size=20)

        self.pc_current_time_text = ctk.CTkLabel(master=self,text="",fg_color="transparent",justify="center",width=600,height=50,font=font)
        self.pc_current_time_text.place(relx=0.5, rely=0.5, anchor="center")
        pywinstyles.set_opacity(self, 0.5, color="#000001")

class LanguageManager:

    @staticmethod
    def set_language(new_lang):
        global language
        language = new_lang
        return language


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(border_color='white', border_width=3, corner_radius=0, fg_color="gray20")

        self.update_language_ui()

    def update_language_ui(self):
        """Обновление интерфейса с учетом текущего языка"""
        # Очищаем предыдущие виджеты
        for widget in self.winfo_children():
            widget.destroy()

        font = ctk.CTkFont(family="Minecart LCD", size=20)

        # Заголовок настроек
        self.title_label = ctk.CTkLabel(
            self, text=change_language(4),
            font=("Minecart LCD", 24, "bold"), text_color="white"
        )
        self.title_label.pack(pady=20)

        # Кнопки выбора языка
        self.language_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.language_frame.pack(pady=20)

        rus_path = os.path.join(os.path.dirname(__file__), "assets", "rus.png")
        rus_img = ctk.CTkImage(light_image=Image.open(rus_path),dark_image=Image.open(rus_path),size=(40, 40))

        url_icon = “URL”
        response = requests.get(url_icon)
        img = Image.open(BytesIO(response.content))

        eng_path = os.path.join(os.path.dirname(__file__), "assets", "eng.png")
        eng_img = ctk.CTkImage(light_image=Image.open(eng_path),dark_image=Image.open(eng_path),size=(40, 40))

        self.rus_button = ctk.CTkButton(self.language_frame, image=rus_img, text='Русский',width=150, height=40, compound='left',fg_color="transparent", hover_color="gray30",font=font, border_width=2, corner_radius=0,border_color='white', text_color="white",command=lambda: self.change_app_language('rus'))
        self.rus_button.pack(side="left", padx=10)

        self.eng_button = ctk.CTkButton(self.language_frame, image=eng_img, text='English',width=150, height=40, compound='left',fg_color="transparent", hover_color="gray30",font=font, border_width=2, corner_radius=0,border_color='white', text_color="white",command=lambda: self.change_app_language('eng'))
        self.eng_button.pack(side="left", padx=10)

        # Кнопка возврата
        self.exit_button = ctk.CTkButton(self, text=change_language(6), text_color='white',command=self.close_settings, font=font,width=200, height=40, fg_color="transparent",hover_color="gray", corner_radius=0,border_color='white', border_width=3)
        self.exit_button.pack(pady=30)

    def change_app_language(self, new_lang):
        LanguageManager.set_language(new_lang)
        self.app.update_ui_language()
        self.update_language_ui()

    def close_settings(self):
        self.grid_forget()
        self.app.main_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.time_window = None
        self.geometry('650x400')
        self.title("YourActivity")


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.checkbox_var = ctk.BooleanVar()
        self.time_in_pc = ''

        self.create_main_frame()
        self.create_settings_frame()
        self.update_ui_language()

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(master=self, border_color='white',border_width=3, corner_radius=0)
        self.main_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        font = ctk.CTkFont(family="Minecart LCD", size=20)

        # Создаем виджеты
        self.pc_work_time_text = ctk.CTkLabel(master=self.main_frame, text='',fg_color="transparent", justify="center",width=600, height=50, font=font)
        self.pc_work_time_text.place(relx=0.5, rely=0.1, anchor="center")

        self.pc_boot_time_text = ctk.CTkLabel(master=self.main_frame, text='',fg_color="transparent", justify="center",width=600, height=50, font=font)
        self.pc_boot_time_text.place(relx=0.5, rely=0.2, anchor="center")

        self.pc_current_time_text = ctk.CTkLabel(master=self.main_frame, text='',fg_color="transparent", justify="center",width=600, height=50, font=font)
        self.pc_current_time_text.place(relx=0.5, rely=0.3, anchor="center")

        self.checkbox = ctk.CTkCheckBox(self.main_frame, text='',font=font, fg_color='white',border_color='white', corner_radius=0,hover=False, variable=self.checkbox_var,command=self.toggle_time_window)
        self.checkbox.place(relx=0.5, rely=0.5, anchor="center")

        settings_path = os.path.join(os.path.dirname(__file__), "assets", "icons8-settings-100.png")
        set_img = ctk.CTkImage(light_image=Image.open(settings_path),dark_image=Image.open(settings_path),size=(40, 40))
        self.settings_button = ctk.CTkButton(self.main_frame, image=set_img, text='',width=50, height=50, fg_color="transparent",hover_color="gray", font=font, border_width=3,corner_radius=0, border_color='white',command=self.show_settings)
        self.settings_button.place(relx=0.5, rely=0.7, anchor="center")

        self.ver_text = ctk.CTkLabel(master=self.main_frame, text='',bg_color="transparent", fg_color="transparent",justify="center", width=600, height=10, font=font)
        self.ver_text.place(relx=0.5, rely=0.85, anchor="center")

    def create_settings_frame(self):
        """Создание фрейма настроек"""
        self.settings_frame = SettingsFrame(self, self)
        self.settings_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.settings_frame.grid_forget()

    def update_ui_language(self):
        """Обновление текстовых элементов интерфейса"""
        self.pc_boot_time_text.configure(text=f"{change_language(1)}: {get_wakeup_time()}")
        self.checkbox.configure(text=change_language(3))
        self.ver_text.configure(text="v0.0.2")

    def show_settings(self):
        self.main_frame.grid_forget()
        self.settings_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def update(self):
        pc_work_time = uptime.uptime()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        hours, remainder = divmod(pc_work_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        date_time_obj1 = datetime.datetime.strptime(get_wakeup_time(), '%H:%M')
        date_time_obj2 = datetime.datetime.strptime(current_time, '%H:%M')
        self.time_in_pc = date_time_obj2 - date_time_obj1

        self.pc_work_time_text.configure(text=f"{change_language(0)}: {formatted_time}")
        self.pc_current_time_text.configure(text=f"{change_language(2)}: {self.time_in_pc}")

        if self.time_window and self.time_window.winfo_exists():
            self.time_window.pc_current_time_text.configure(text=f"{self.time_in_pc}")

        self.after(500, self.update)

    def toggle_time_window(self):
        if self.checkbox_var.get():
            if not self.time_window or not self.time_window.winfo_exists():
                self.time_window = TimeWindow()
        else:
            if self.time_window and self.time_window.winfo_exists():
                self.time_window.destroy()


def get_wakeup_time():
    cmd = 'wevtutil qe System "/q:*[System[EventID=1]]" /rd:true /c:1 /f:text'
    output = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout

    for line in output.splitlines():
        if "Date:" in line:
            wake_time_str = line.split("Date:")[1]
            for j in wake_time_str:
                if "T" in j:
                    wake_time_str = line.split("T")[1]
            return wake_time_str[:5]


app = App()
app.update()
app.mainloop()