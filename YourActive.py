import datetime
import subprocess
import customtkinter
import uptime
import pywinstyles

pc_work_time = uptime.uptime()
#------------------------------------------------------------------------------------------------------

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

wakeup_time = get_wakeup_time()


#------------------------------------------------------------------------------------------------------

class TimeWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.show_time_above = False
        self.geometry('100x50+10+10')
        self.title("YourActivity")
        self.overrideredirect(True)
        self.configure(background='None')
        self.wm_attributes("-topmost", True)

        font = customtkinter.CTkFont(family="Minecart LCD", size=20)

        self.pc_current_time_text = customtkinter.CTkLabel(master= self, text="", fg_color="transparent", justify = "center",width = 600,height=50,font=font)
        self.pc_current_time_text.place(relx=0.5, rely=0.5, anchor= "center")
        pywinstyles.set_opacity(self,0.5, color="#000001")

#------------------------------------------------------------------------------------------------------

class App(customtkinter.CTk):
    def __init__(self):
        self.time_window = None
        super().__init__()
        self.geometry('600x400')
        self.title("YourActivity")
        self.iconbitmap('C:/Users/banan/Documents/YourActivity/YourActive.ico')

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        font = customtkinter.CTkFont(family="Minecart LCD", size=20)
        self.checkbox_var = customtkinter.BooleanVar()
        self.time_in_pc = ''


        self.pc_work_time_text = customtkinter.CTkLabel(master= self, text=f"ВРЕМЯ РАБОТЫ ПК: {pc_work_time}", fg_color="transparent", justify = "center",width = 600,height=50,font=font)
        self.pc_work_time_text.place(relx=0.5, rely=0.2, anchor= "center")

        self.pc_boot_time_text = customtkinter.CTkLabel(master= self, text=f"КОМПЬЮТЕР БЫЛ ЗАПУЩЕН В: {wakeup_time}", fg_color="transparent", justify = "center",width = 600,height=50,font=font)
        self.pc_boot_time_text.place(relx=0.5, rely=0.3, anchor= "center")

        self.pc_current_time_text = customtkinter.CTkLabel(master= self, text= '', fg_color="transparent", justify = "center",width = 600,height=50,font=font)
        self.pc_current_time_text.place(relx=0.5, rely=0.4, anchor= "center")

        self.checkbox= customtkinter.CTkCheckBox(self, text= 'включить отображение времени',font=font,fg_color = 'white',border_color = 'white',corner_radius = 0,hover = False,variable=self.checkbox_var,command=self.toggle_time_window)
        self.checkbox.place(relx=0.5, rely=0.6, anchor= "center")


    def update(self):
        pc_work_time = uptime.uptime()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        hours, remainder = divmod(pc_work_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        date_time_obj1 = datetime.datetime.strptime(wakeup_time, '%H:%M')
        date_time_obj2 = datetime.datetime.strptime(current_time, '%H:%M')
        self.time_in_pc = date_time_obj2 - date_time_obj1

        self.pc_work_time_text.configure(text=f"ВРЕМЯ РАБОТЫ ПК: {formatted_time}")
        self.pc_current_time_text.configure(text=f"ВРЕМЯ ПРОВЕДЕННОЕ ЗА ПК: {self.time_in_pc}")

        if self.time_window and self.time_window.winfo_exists():
            self.time_window.pc_current_time_text.configure(text=f"{self.time_in_pc}")

        self.after(500, self.update)

    def toggle_time_window(self):
        if self.checkbox.get():
            if not self.time_window or not self.time_window.winfo_exists():
                self.time_window = TimeWindow()
        else:
            if self.time_window and self.time_window.winfo_exists():
                self.time_window.destroy()

#------------------------------------------------------------------------------------------------------

app = App()
app.update()
app.mainloop()
