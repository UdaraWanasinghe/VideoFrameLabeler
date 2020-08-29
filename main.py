import vlc
from tkinter import *


class VideoTagger:
    def __init__(self):
        self.root_window = Tk()
        self.root_window.title('Video Tagger')
        self.root_window.wm_attributes("-topmost", 1)
        self.root_window.geometry("400x300")
        self.media_player = None
        self.is_playing = False
        main_pane = PanedWindow(self.root_window, orient=VERTICAL)
        self.url_input_entry = self.build_load_bar(main_pane)
        self.play_button = self.build_control_bar(main_pane)
        self.build_build_label_menu(main_pane)
        self.build_save_button(main_pane)
        main_pane.pack()
        self.root_window.mainloop()

    def build_load_bar(self, master):
        paned_window = PanedWindow(master, orient=HORIZONTAL)
        url_input_entry = Entry(paned_window)
        load_button = Button(paned_window, text="Load", command=self.build_load_media_callback())
        paned_window.add(url_input_entry)
        paned_window.add(load_button)
        master.add(paned_window)
        return url_input_entry

    def build_control_bar(self, master):
        paned_window = PanedWindow(master, orient=HORIZONTAL)
        play_button = Button(paned_window, text="Play", command=self.build_play_button_callback())
        forward_button = Button(paned_window, text=">", command=self.build_forward_button_callback())
        fast_forward_button = Button(paned_window, text=">>", command=self.build_fast_forward_button_callback())
        backward_button = Button(paned_window, text="<", command=self.build_backward_button_callback())
        fast_backward_button = Button(paned_window, text="<<", command=self.build_fast_backward_button_callback())
        paned_window.add(fast_backward_button)
        paned_window.add(backward_button)
        paned_window.add(play_button)
        paned_window.add(forward_button)
        paned_window.add(fast_forward_button)
        master.add(paned_window)
        return play_button

    def build_build_label_menu(self, master):
        string_var = StringVar(self.root_window)
        option_menu = OptionMenu(master, string_var, *{'Option1', 'Option2'})
        master.add(option_menu)

    def build_save_button(self, master):
        save_button = Button(master, text='Save')
        master.add(save_button)

    def build_load_media_callback(self):
        def paused(event):
            self.media_player.is_playing = False
            self.play_button['text'] = 'Play'

        def playing(event):
            self.media_player.is_playing = True
            self.play_button['text'] = 'Pause'

        def callback():
            if self.media_player is not None:
                self.media_player.release()
            self.media_player = vlc.MediaPlayer(self.url_input_entry.get())
            self.play_button['text'] = 'Play'
            events = self.media_player.event_manager()
            events.event_attach(vlc.EventType.MediaPlayerPaused, paused)
            events.event_attach(vlc.EventType.MediaPlayerPlaying, playing)
            events.event_attach(vlc.EventType.MediaPlayerStopped, paused)
            self.media_player.play()

        return callback

    def build_play_button_callback(self):
        def play_button_callback():
            if self.is_playing:
                self.media_player.pause()
                self.play_button['text'] = "Play"
            else:
                self.media_player.play()
                self.play_button['text'] = "Pause"
            self.is_playing = not self.is_playing

        return play_button_callback

    def build_forward_button_callback(self):
        def callback():
            u_time = self.media_player.get_time() + 5000
            self.media_player.set_time(u_time)

        return callback

    def build_backward_button_callback(self):
        def callback():
            u_time = self.media_player.get_time() - 5000
            self.media_player.set_time(u_time)

        return callback

    def build_fast_forward_button_callback(self):
        def callback():
            self.media_player.set_rate(self.media_player.get_rate() + 1)

        return callback

    def build_fast_backward_button_callback(self):
        def callback():
            self.media_player.set_rate(self.media_player.get_rate() - 1)

        return callback


videoTagger = VideoTagger()
