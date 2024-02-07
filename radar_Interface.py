import customtkinter
import os
from PIL import Image, ImageDraw


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Radar Station MacRobomaster 2024 Interface")
        self.geometry("1200x800")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.battleground_img = Image.open(os.path.join(image_path, "battleground.png")).resize((560,300))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "MacRM_logo_black.png")), size=(26, 26))
        self.battle_ground = customtkinter.CTkImage(self.battleground_img, size=(560,300))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Radar Station", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, sticky="nsew")

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.battle_ground)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Ref package info\n\n" + "Blue Standard 3 : 10, 20\nBlue Standard 3 : 7, 14\nBlue Hero 1 : 5, 10 \n\n" )
        # select default frame
        self.time = 0
        self.update()


    def update(self):
        self.after(1000, self.update)
        self.locations = [(100+self.time, 100+self.time),(20+self.time, 120+self.time)]
        self.update_point(self.locations)
        self.time+=1


    def update_point(self, locations):
        battleground_img = Image.open("./assets/battleground.png").resize((560,300))
        for location in locations:
            x, y = location
            ImageDraw.Draw(battleground_img).polygon([(x-3, y-3),(x-3, y+3),(x+3, y+3),(x+3, y-3)], fill="red",width=2)

        battleground_img.save("./assets/battleground_update.png")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.battle_ground.configure(dark_image= Image.open(os.path.join(image_path, "battleground_update.png")))


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":

    app = App()
    app.mainloop()