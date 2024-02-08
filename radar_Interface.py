import customtkinter
import os
from PIL import Image, ImageDraw
import cv2

ASSET_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
WEBCAM = 0
SAMPLE_VID = os.path.join(ASSET_PATH, "sample.mp4")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # self.minsize(1280, 720)
        # self.maxsize(1920, 1080)


        self.title("Radar Station MacRobomaster 2024 Interface")
        self.geometry("1280x1000")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.blue_labels = []
        self.blue_slides = []
        self.red_labels = []
        self.red_slides = []

        # image loading
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.battleground_img = Image.open(os.path.join(self.image_path, "battleground.png")).resize((560,300))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "MacRM_logo_black.png")), size=(26, 26))
        self.minimap = customtkinter.CTkImage(self.battleground_img, size=(560,300))

        

        self.vidcap = cv2.VideoCapture(SAMPLE_VID)
        _, frame = self.vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = customtkinter.CTkImage(Image.fromarray(frame).resize((640, 480)), size=(640, 480))
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
        self.home_frame_video_feed = customtkinter.CTkLabel(self.home_frame, corner_radius=0, text="Video IN\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", image=self.video_feed)
        self.home_frame_video_feed.grid(row=1, column=0, padx=20, pady=10)

        # create info box in home frame
        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Ref package info\n\n" + "Blue Standard 3 : 10, 20\nBlue Standard 3 : 7, 14\nBlue Hero 1 : 5, 10 \n\n" )

        # create robot info box in home frame
        self.robot_info_frame = customtkinter.CTkFrame(self.home_frame,fg_color=("gray80", "gray15"))
        self.robot_info_frame.grid(row=1, column=1,padx=(20, 0), pady=(20, 0), sticky="n")
        self.get_robot_status_frame()

        # quit button
        self.quit_button = customtkinter.CTkButton(self.home_frame, text="Quit", command=self.destroy)
        self.quit_button.grid(row=0, column=2, padx=(20,0),  pady=(20, 0), sticky="n")

        # select default frame
        self.time = 0
        self.update()

    def update(self):
        self.locations = [(100+self.time, 100+self.time),(20+self.time, 120+self.time)]
        self.update_minimap(self.locations)
        self.update_video_feed()
        self.time+=1
        self.after(10, self.update)

    #Get robot status Widget setup.
    def get_robot_status_frame(self):
        for team_num in range(2): 
            for i in range(7):
                if team_num == 0:
                    self.blue_labels.append(customtkinter.CTkLabel(self.robot_info_frame, text="Blue "+str(i)+" : ").grid(row=i, column=team_num*2, padx=10))
                    self.blue_slides.append(customtkinter.CTkProgressBar(self.robot_info_frame, orientation="horizontal",width = 100).grid(row=i, column=team_num+1,padx=(0,5)))
                else:
                    self.red_labels.append(customtkinter.CTkLabel(self.robot_info_frame, text="Red "+str(i)+" : ").grid(row=i, column=team_num*2, padx=10))
                    self.red_slides.append(customtkinter.CTkProgressBar(self.robot_info_frame, orientation="horizontal",width = 100).grid(row=i, column=team_num*2+1,padx=(0,5)))
    
    def update_minimap(self, locations):
        copy = self.battleground_img.copy()
        for location in locations:
            x, y = location
            ImageDraw.Draw(copy).polygon([(x-3, y-3),(x-3, y+3),(x+3, y+3),(x+3, y-3)], fill="red",width=2)

        self.minimap.configure(dark_image=copy)
    
    def update_video_feed(self):
        success, frame = self.vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame).resize((640, 480))

        if success:
            self.video_feed.configure(dark_image=frame)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    #app._state_before_windows_set_titlebar_color = 'zoomed'
    app.mainloop()