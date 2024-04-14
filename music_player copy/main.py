from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3


root = Tk()
root.geometry('500x350')
root.title("Lora's Winamp")

pygame.mixer.init()


def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    current_song = song_box.curselection()
    if current_song:  # Check if a song is selected
        song = song_box.get(current_song)
        song = f'/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/{song}'
        song_mut = MP3(song)
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')

    status_bar.after(1000, play_time)



def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 Files', '*.mp3'), ))
    song = song.replace('/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/', '')
    song_box.insert(END, song)


def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 Files', '*.mp3'),))

    for song in songs:
        song = song.replace('/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/', '')
        song_box.insert(END, song)


def play():
    song = song_box.get(ACTIVE)
    song = f'/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()


def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)


def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)

    song = f'/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)

    song = f'/Users/lorayordanova/PycharmProjects/small_projects/music_player/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def remove_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def remove_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()


global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


song_box = Listbox(root, bg='#6381a8', fg='black', width=60)  # Create Playlist box
song_box.pack(pady=20)

play_button_img = PhotoImage(file='play-3.png')
forward_button_img = PhotoImage(file='forward-2.png')
backward_button_img = PhotoImage(file='backward-2.png')
pause_button_img = PhotoImage(file='pause-2.png')
stop_button_img = PhotoImage(file='stop-2.png')

controls_frame = Frame(root)
controls_frame.pack()


backward_button = Button(controls_frame, image=backward_button_img, borderwidth=0, highlightthickness=0, command=previous_song)
play_button = Button(controls_frame, image=play_button_img, borderwidth=0, highlightthickness=0, command=play)
forward_button = Button(controls_frame, image=forward_button_img, borderwidth=0, highlightthickness=0, command=next_song)
pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0, highlightthickness=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_button_img, borderwidth=0, highlightthickness=0, command=stop)
backward_button.grid(row=0, column=0, padx=5)
forward_button.grid(row=0, column=1, padx=5)
play_button.grid(row=0, column=2, padx=5)
pause_button.grid(row=0, column=3, padx=5)
stop_button.grid(row=0, column=4, padx=5)

my_menu_bar = Frame(root, relief='raised', bd=2,)
my_menu_bar.pack(side='top', fill='x')

my_menu_button = Menubutton(my_menu_bar, text='Add/Remove Songs', font='Consolas')
my_menu_button.pack(side='left')

my_menu = Menu(my_menu_button, tearoff=0)
my_menu_button['menu'] = my_menu

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song To Playlist', command=add_song)

add_song_menu.add_command(label='Add Many Songs To The Playlist', command=add_many_songs)


remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Remove Song From Playlist', command=remove_song)
remove_song_menu.add_command(label='Remove All Songs From Playlist', command=remove_all_songs)

# status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar = Label(root, text='Time Elapsed: 00:00 of 00:00', bd=1, relief=GROOVE, anchor=E)

status_bar.pack(side='bottom', fill='x', ipady=2)

root.mainloop() #place window on computer screen and listens for events

