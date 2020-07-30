from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
root=Tk()



root.title("MP3 Player")
root.geometry("500x400")

#Initialize Pygame
pygame.mixer.init()


#Create function To Deal with time
def play_time():
	#Grab current song time
	current_time=pygame.mixer.music.get_pos()/1000
	#Convert song time to Time format
	converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

	#Reconstruct song with directory structure
	song=playlist_box.get(ACTIVE)
	song=f'C:/mp3/audio/{song}.mp3'

	#Find Current song Length
	song_mut=MP3(song)
	global song_length
	song_length=song_mut.info.length
	#Convert to time format
	converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))





	#Add current time to status Bar
	if current_time >=1:
		status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length}   ')
	
	#Create Loop To check the time every second
	my_label.after(1000,play_time)



#Function to Add one song to the Playlist
def add_song():
	song=filedialog.askopenfilename(initialdir='audio/',title="choose a Song",filetypes=(("mp3 Files","*.mp3"),))
	#strip out directory sructure and .mp3 from song title
	song=song.replace("C:/mp3/audio/","")
	song=song.replace(".mp3","")
	#Add to end of Playlist
	playlist_box.insert(END, song)

#Function to add many songs to the Playlist
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/',title="choose a Song",filetypes=(("mp3 Files","*.mp3"),))

	#loop through songs to strip out directory structure and .mp3 from song name
	for song in songs:
		#strip out directory sructure and .mp3 from song title
		song=song.replace("C:/mp3/audio/","")
		song=song.replace(".mp3","")
		#Add to end of playlist
		playlist_box.insert(END, song)

#Create a Function to delete a song from the playlist

def delete_song():
	#Delete Highlighted song
	playlist_box.delete(ANCHOR)

#Create a Function to delete all songs from the Playlist

def delete_all_songs():
	#Delete all songs
	playlist_box.delete(0, END)

#Create play function
def play():
	#Reconstruct song with directory structure
	song=playlist_box.get(ACTIVE)
	song=f'C:/mp3/audio/{song}.mp3'
	
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#Get song time
	play_time()

#Create Stop Function
def stop():
	#Stop the song
	pygame.mixer.music.stop()
	#Clear Playlist Bar
	playlist_box.selection_clear(ACTIVE)


	status_bar.config(text='')


#Create function to play next_song
def next_song():
	#Get current song number
	next_one=playlist_box.curselection()
	#Add one to current song number tuple/list
	next_one=next_one[0]+1

	#Grab the song title from the playlist
	song=playlist_box.get(next_one)
	#Add directory structure
	song=f'C:/mp3/audio/{song}.mp3'
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#Clear Active Bar in PLaylist
	playlist_box.selection_clear(0, END)

	#Move active Bar to next song
	playlist_box.activate(next_one)

	#Set Active Bar to next song
	playlist_box.selection_set(next_one, last=None)


#Create function to play Previous song
def previous_song():
	#Get current song number
	next_one=playlist_box.curselection()
	#Subtract one to current song number tuple/list
	next_one=next_one[0]-1

	#Grab the song title from the playlist
	song=playlist_box.get(next_one)
	#Add directory structure
	song=f'C:/mp3/audio/{song}.mp3'
	#Load song with pygame mixer
	pygame.mixer.music.load(song)
	#Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#Clear Active Bar in PLaylist
	playlist_box.selection_clear(0, END)

	#Move active Bar to next song
	playlist_box.activate(next_one)

	#Set Active Bar to next song
	playlist_box.selection_set(next_one, last=None)




#Create Paused Variable
global paused
paused=False


#Create Pause Function
def pause(is_paused):
	global paused
	paused=is_paused

	if paused:
		#Unpause
		pygame.mixer.music.unpause()
		paused=False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused=True


#To add playlist box
playlist_box=Listbox(root,bg="black",fg="green",width=60,selectbackground="green",selectforeground="black")
playlist_box.pack(pady=20)

#Define Button images for controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

#Create Button Frame
control_frame=Frame(root)
control_frame.pack(pady=20)

#create Play/stop etc Buttons
back_button=Button(control_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_button=Button(control_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_button=Button(control_frame,image=play_btn_img,borderwidth=0,command=play)
pause_button=Button(control_frame,image=pause_btn_img,borderwidth=0,command=lambda: pause(paused))
stop_button=Button(control_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_button.grid(row=0, column=0,padx=10)
forward_button.grid(row=0, column=1,padx=10)
play_button.grid(row=0, column=2,padx=10)
pause_button.grid(row=0, column=3,padx=10)
stop_button.grid(row=0, column=4,padx=10)


#create Main Menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Create Add song menu Dropdowns
add_song_menu=Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
#Add one song
add_song_menu.add_command(label="Add One Song to Playlist",command=add_song)
#Add many songs
add_song_menu.add_command(label="Add Many Songs to Playlist",command=add_many_songs)

#Create Delete song menu Dropdowns
remove_song_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A song from Playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All songs from Playlist",command=delete_all_songs)

#Create Status Bar
status_bar=Label(root,text='',bd=1,relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#Temporary Label
my_label=Label(root,text='')
my_label.pack(pady=20)


root.mainloop()