from tkinter import *
import pygame
import os
import threading
import time
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror,askquestion,showinfo
from tkinter import ttk
from PIL import Image,ImageTk

class Player:
    def  __init__(self, master) -> None:
        self.master = master
        pygame.init()
        pygame.mixer.init()

        def get_icon():
            self.winicon = PhotoImage(file="Al2mpY.jpg")
            master.iconphoto(False, self.winicon)

        def icon():
            threads = threading.Thread(target=get_icon)
            threads.start()
        icon()        

        PLAY = "▶"
        PAUSE = "⏸️"
        PREV = "⏪"
        NEXT = "⏩"
        STOP = "⏹️"
        UNPAUSE = "⏸"
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1

        #listbox
        self.scroll = Scrollbar(master)
        self.play_list = Listbox(master, font="Sasarif 12 bold", bd=5,
              bg="white", width=37, height=19, selectbackground="black")
        self.play_list.place(x=600,y=77)
        self.scroll.place(x=946,y=80,height=389, width=15)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)

        file = "Al2mpY.jpg"
        self.back_img = Image.open(file)
        self.back_img = self.back_img.resize((600,470), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.back_img)
        self.img_label= Label(master)
        self.img_label.grid(row=0, column=0)
        self.img_label["compound"] = LEFT
        self.img_label["image"] = self.img

        self.var = StringVar()
        self.var.set("....................................................................")
        self.song_title = Label(master, font="Helvetica 12 bold", bg="black",
                            fg="white", width=60, textvariable= self.var)
        self.song_title.place(x=3, y=0)

        #########################################################################################

        def add_songs():
            try:
                directory = askdirectory()
                os.chdir(directory)
                song_list = os.listdir()
                song_list.reverse()
                for song in song_list:
                    pos=0
                    if song.endswith(('mp3')):
                        self.play_list.insert(pos, song)
                        pos += 1

                index = 0
                self.play_list.selection_set(index)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)

            except:
                showerror("File selected error", "Please choose a file correctly")

        def add_songs_playlist():
            threads = threading.Thread(target=add_songs)
            threads.start()

        def get_time():
            current_time = pygame.mixer.music.get_pos() / 1000
            formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            next_one = self.play_list.curselection()
            song = self.play_list.get(next_one)
            song_timer = MP3(song)
            song_length = int(song_timer.info.length)
            format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            self.label_time.config(text=f"{format_for_length} / {formated_time} ")
            self.progress["maximum"] = song_length
            self.progress["value"] = int(current_time)
            master.after(100, get_time)

        def play_music():
            try:
                track = self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()
            except:
                showerror("No Music", "Please load the music you want to play")    
        
        def repeat():
            try:
                index = 0
                self.play_list.select_clear(0,END)
                self.play_list.selection_set(index, lost=NONE)
                self.play_list.activate(index)
                self.play_list.select_anchor(index)
                track= self.play_list.get(index)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
            except:
                showerror("No song in playlist", "Please add music")

        def repeat():
            threads= threading.Thread(target=repeat)
            threads.start()

        def pause_unpause():
            if self.pause["text"] == PAUSE:
                pygame.mixer.music.pause()
                self.pause["text"] = UNPAUSE 
            elif self.pause["text"] == UNPAUSE:
                pygame.mixer.music.unpause()
                self.pause["text"] = PAUSE 
        
        def play_thread():
            threads = threading.Thread(target=play_music)
            threads.start()

        master.bind("<space>, lambda x: play_thread()")
        
        def stop():
            pygame.mixer.music.stop()
        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        def muted():
            if self.mute["text"] == unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.mute["fg"] = "red"
                self.mute["text"] = mute
            elif self.mute["text"] ==mute:   
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.mute["fg"] = "green"
                self.mute["text"] = unmute

        def next_song():
            next_one = self.play_list.curselection()
            next_one = next_one[0]+1
            song = self.play_list.get(next_one)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one, last=None)
            self.var.set(song)
            get_time()
            self.play_list.see(next_one)

        def next():
            threads = threading.Thread(target=next_song)
            threads.start()       


        def prev_song():
            next_one = self.play_list.curselection()
            next_one = next_one[0]-1
            song = self.play_list.get(next_one)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one, last=None)
            self.var.set(song)
            get_time()
            self.play_list.see(next_one) 

        def prev():
            threads = threading.Thread(target=prev_song)
            threads.start() 

        self.master.bind("<Left>", lambda x: prev())
        self.master.bind("<Right>", lambda x: next())

            
        def exit():
            msgbox = askquestion(
                'Exit Application', 'Are you sure you want to exit the music player.', icon='warning')
            
            if msgbox =="yes":
                master.quit()
                master.after(100, exit)
            else:
                showinfo('Return', 'Continue playing your awesome music')
            return

        def help():
            top = Toplevel()
            top.title("help")
            top.geometry("350, 554+500+80")
            top.resizable(width=0, height=0) 
            user_manual = [
                "MUSIC PLAYER USER MANUAL:\n",
                "1.play button = ▶"
                "2.pause button =⏸️"
                "3.unpause button =⏸️"
                "4.next button =⏩"
                "5.previous button =⏪"
                "6.mute button =🔇"
                "7.unmute symbol =\U0001F50A"
                "8.stop button =⏹️"
                "\n\n|ade by manucho | Copyright @2023 |\n"
            ]   
            for i in user_manual:
                manual = Label(top,Text= i, width=50, height=3, font="Helvetica , 12", bg="black", fg="white")
                manual.pack(side=TOP, fill="both")   
        ## ######################################################################################
        self.menu  = Menu(self.img_label, font="helvetica 3 ")
        master.config(menu=self.menu)
        self.menu.add_command(label="HELP", command=help)
        self.menu.add_command(label="EXIT", command=exit)

        self.separator = ttk.Separator(self.img_label, orient="horizontal")
        self.separator.place(relx=0, rely=0.87, relwidth=1,relheight=1)

        self.play=Button(self.master, text=PLAY, width=4,bd=5,bg="black",
                    fg="white", font="Helvetica, 15", command=play_thread)
        self.play.place(x=160,y=415)

        self.stop = Button(self.master, text=STOP,width=5,bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=stop)
        self.stop.place(x=225, y=415)

        self.prev = Button(self.master, text=PREV,width=5,bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=prev)
        self.prev.place(x=10, y=415)

        self.next = Button(self.master, text=NEXT,width=4,bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=next)
        self.next.place(x=300, y=415)

        self.pause = Button(self.master, text=PAUSE, width=5,bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=pause_unpause)
        self.pause.place(x=85, y=415)
        
        self.mute = Button(self.master, text=unmute, width=2,bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=muted)
        self.mute.place(x=430, y=415)
        
        self.repeat = Button(self.master, text="\U0001F501" ,width=3, bd=5, bg="Black",
                    fg="white", font="Helvetica, 15", command=repeat)
        self.repeat.place(x=375, y=415)
        
        self.load_music = Button(self.master, text="🎵Click Here To Load The Music🎵" ,width=43,bd=5, bg="Black",
                    fg="white", font="Helvetica, 11", command=add_songs_playlist)
        self.load_music.place(x=605, y=45)

        self.style = ttk.Style()
        self.style.configure("myStyle.Horizontal.Tscale", background = "#505050")
        self.volume_slider = ttk.Scale(self.img_label, from_=0, to=1, orient= HORIZONTAL,
                     value=1, length=120, style="myStyle.Horizontal.TScale", command=volume)
        self.volume_slider.place(x=475, y=424)

        self.progress = ttk.Progressbar(self.img_label, orient=HORIZONTAL, value=0, length=453, mode="determinate")
        self.progress.place(x=0, y=385)

        self.label_time = Label(master, text="00:00:00 / 00:00:00", width=17, font="Helvetica, 10", bg="black", fg="white" )
        self.label_time.place(x=460,y=387)

        self.label_playlist = Label(master, text="🎵Music Playlist🎵", width=38, font="helvetica,12")
        self.label_playlist.place(x=610,y=5)


def main():
    root = Tk()
    ui = Player(root)
    root.geometry("963x470+200+100")
    root.title("Mp3 Music Player")
    root.configure(bg="black")
    root.resizable(width=0,height=0)
    root.mainloop()

if __name__ == "__main__":
    main()            