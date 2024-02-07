import customtkinter
import os
from PIL import Image, ImageDraw
import cv2


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        self.title("Radar Station MacRobomaster 2024 Interface")
        self.geometry("1200x800")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        

        # image loading
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.battleground_img = Image.open(os.path.join(self.image_path, "battleground.png")).resize((560,300))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "MacRM_logo_black.png")), size=(26, 26))
        self.minimap = customtkinter.CTkImage(self.battleground_img, size=(560,300))

        self.vidcap = cv2.VideoCapture(os.path.join(self.image_path, "mem.mp4"))
        _, frame = self.vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = customtkinter.CTkImage(Image.fromarray(frame).resize((560,300)), size=(560, 300))
        self.video_feed = frame

        # create navigation frame / left sidebar
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="ns")
        self.navigation_frame.grid_rowconfigure(1, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Radar Station", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame / center frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, sticky="n")

        # create minimap in home frame
        self.home_frame_minimap = customtkinter.CTkLabel(self.home_frame, text="", image=self.minimap)
        self.home_frame_minimap.grid(row=0, column=0, padx=20, pady=10, sticky="s")

        # create video feed in home frame
        self.home_frame_video_feed = customtkinter.CTkLabel(self.home_frame, corner_radius=0, text="", image=self.video_feed)
        self.home_frame_video_feed.grid(row=1, column=0, padx=20, pady=10)

        # create info box in home frame
        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=250)
        self.textbox.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Ref package info\n\n" + "Blue Standard 3 : 10, 20\nBlue Standard 3 : 7, 14\nBlue Hero 1 : 5, 10 \n\n" )

        # select default frame
        self.time = 0
        self.update()


    def update(self):
        self.locations = [(100+self.time, 100+self.time),(20+self.time, 120+self.time)]
        self.update_minimap(self.locations)
        self.update_video_feed()
        self.time+=1
        print("UI refreshed")
        self.after(1, self.update)


    def update_minimap(self, locations):
        #!Writing to image slows down UI significantly
        battleground_img = Image.open("./assets/battleground.png").resize((560,300))
        for location in locations:
            x, y = location
            ImageDraw.Draw(battleground_img).polygon([(x-3, y-3),(x-3, y+3),(x+3, y+3),(x+3, y-3)], fill="red",width=2)
        
        battleground_img.save("./assets/battleground_update.png")
        #!Comment until here to remove lag
        self.minimap.configure(dark_image= Image.open(os.path.join(self.image_path, "battleground_update.png")))
    
    def update_video_feed(self):
        success, frame = self.vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame).resize((560,300))

        if success:
            self.video_feed.configure(dark_image=frame)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()