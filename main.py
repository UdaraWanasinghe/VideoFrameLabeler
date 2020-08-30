#!/usr/bin/env python

import vlc
from tkinter import *
from tkinter import filedialog
import json
from tkinter import messagebox


class VideoFrameLabeler:
    def __init__(self):
        self._init_root_window()
        self._init_media_player()
        self._bind_keyboard_events()
        main_pane = PanedWindow(self.root_window, orient=VERTICAL)
        browse_media_pane = self._build_browse_media_pane(main_pane)
        media_control_pane = self._build_media_control_pane(main_pane)
        label_drop_down_menu = self._build_label_dropdown_menu(main_pane)
        save_button = self._build_save_button(main_pane)
        add_button = self._build_add_button(main_pane)
        delete_button = self._build_delete_button(main_pane)
        label_list = self._build_label_list(main_pane)
        main_pane.add(browse_media_pane)
        main_pane.add(media_control_pane)
        main_pane.add(label_drop_down_menu)
        main_pane.add(add_button)
        main_pane.add(delete_button)
        main_pane.add(label_list)
        main_pane.add(save_button)
        main_pane.pack()
        self.root_window.mainloop()

    def _init_root_window(self):
        self.root_window = Tk()
        self.root_window.title('Video Frame Labeler')
        self.root_window.wm_attributes("-topmost", 1)
        self.root_window.geometry("280x600")

    def _init_media_player(self):
        self.media_player = vlc.MediaPlayer()
        self.is_playing = False
        self.directory = './'
        events = self.media_player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerPaused, self._on_paused)
        events.event_attach(vlc.EventType.MediaPlayerPlaying, self._on_playing)
        events.event_attach(vlc.EventType.MediaPlayerStopped, self._on_paused)
        events.event_attach(vlc.EventType.MediaListEndReached, self._on_paused)

    def _bind_keyboard_events(self):
        root = self.root_window

        def play_callback(_):
            self._play_button_callback()

        def forward_callback(_):
            self._fast_forward_button_callback()

        def fast_forward_callback(_):
            self._fast_forward_button_callback()

        def backward_callback(_):
            self._backward_button_callback()

        def fast_backward_callback(_):
            self._fast_backward_button_callback()

        def browse_callback(_):
            self._build_load_media_callback()

        def add_callback(_):
            self._on_add_callback()

        def delete_callback(_):
            self._on_delete_callback()

        def save_callback(_):
            self._on_save_callback()

        def print_e(e):
            key_code = e.keycode
            if 9 < key_code < 20 or 23 < key_code < 34 or 37 < key_code < 47 or 51 < key_code < 59:
                code = -1
                if 9 < key_code < 20:
                    code = key_code - 10
                elif 23 < key_code < 34:
                    code = key_code - 14
                elif 37 < key_code < 47:
                    code = key_code - 18
                elif 51 < key_code < 59:
                    code = key_code - 23
                if -1 < code < len(self.label_list):
                    self.label_listbox.select_clear(0, 'end')
                    self.label_listbox.select_set(code)
                    self._on_add_callback()

        root.bind("<space>", play_callback)
        root.bind("<Right>", forward_callback)
        root.bind("<Left>", backward_callback)
        root.bind("<Up>", fast_forward_callback)
        root.bind("<Down>", fast_backward_callback)
        root.bind("<B>", browse_callback)
        root.bind("<D>", delete_callback)
        root.bind("<A>", add_callback)
        root.bind("<S>", save_callback)
        root.bind("<KeyPress>", print_e)

    def _build_browse_media_pane(self, master):
        pane = PanedWindow(master, orient=HORIZONTAL)
        self.url_input_entry = Entry(pane)
        self.browse_button = Button(pane, text="Browse", command=self._build_load_media_callback)
        pane.add(self.url_input_entry)
        pane.add(self.browse_button)
        return pane

    def _build_media_control_pane(self, master):
        pane = PanedWindow(master, orient=HORIZONTAL)
        self.play_button = Button(pane, text="Play", command=self._play_button_callback)
        forward_button = Button(pane, text=">", command=self._forward_button_callback)
        fast_forward_button = Button(pane, text=">>", command=self._fast_forward_button_callback)
        backward_button = Button(pane, text="<", command=self._backward_button_callback)
        fast_backward_button = Button(pane, text="<<", command=self._fast_backward_button_callback)
        pane.add(fast_backward_button)
        pane.add(backward_button)
        pane.add(self.play_button)
        pane.add(forward_button)
        pane.add(fast_forward_button)
        return pane

    def _build_label_dropdown_menu(self, master):
        self.label_list = self._load_option_list()
        self.label_listbox = Listbox(master, height=len(self.label_list))
        i = 0
        for l in self.label_list:
            self.label_listbox.insert(i, l)
            i = i + 1
        self.label_listbox.select_set(0)
        return self.label_listbox

    def _build_save_button(self, master):
        return Button(master, text='Save', command=self._on_save_callback)

    def _build_delete_button(self, master):
        return Button(master, text='Delete', command=self._on_delete_callback)

    def _build_add_button(self, master):
        return Button(master, text='Add', command=self._on_add_callback)

    def _build_label_list(self, master):
        self.video_label_listbox = Listbox(master, height=10)
        return self.video_label_listbox

    @staticmethod
    def _load_option_list():
        lines = []
        with open('option_list.txt') as file:
            for line in file:
                line = line.strip()
                lines.append(line)
        return lines

    def _build_load_media_callback(self):
        filename = filedialog.askopenfilename(initialdir=self.directory,
                                              title="Select a Video")
        if len(filename) > 0:
            self.url_input_entry.delete(0, 'end')
            self.url_input_entry.insert(0, filename)
            try:
                media = vlc.Media(filename)
                self.media_player.set_media(media)
                self.media_player.play()
                self.annotations = {}
                self._load_json()
            finally:
                self._reload_annotations()

    def _play_button_callback(self):
        if self.is_playing:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _forward_button_callback(self):
        u_time = self.media_player.get_time() + 5000
        self.media_player.set_time(u_time)

    def _backward_button_callback(self):
        u_time = self.media_player.get_time() - 5000
        self.media_player.set_time(u_time)

    def _fast_forward_button_callback(self):
        self.media_player.set_rate(self.media_player.get_rate() + 1)

    def _fast_backward_button_callback(self):
        self.media_player.set_rate(self.media_player.get_rate() - 1)

    def _reload_annotations(self):
        self.video_label_listbox.delete(0, 'end')
        for k, v in self.annotations.items():
            self.video_label_listbox.insert(0, str(k) + ":    " + v)
        self.video_label_listbox.select_set(0)

    def _on_paused(self, _):
        self.is_playing = False
        self.play_button['text'] = 'Play'

    def _on_playing(self, _):
        self.is_playing = True
        self.play_button['text'] = 'Pause'

    def _on_end_reached(self, _):
        self.media_player.set_time(0)

    def _on_add_callback(self):
        key = self.media_player.get_time()
        value = self.label_list[self.label_listbox.curselection()[0]]
        self.annotations[str(key)] = value
        self._reload_annotations()

    def _on_save_callback(self):
        filename = self._get_json_filename()
        with open(filename, 'w') as f:
            json.dump(self.annotations, f)
            messagebox.showinfo(title='Saved', message='Saved to ' + filename)

    def _on_delete_callback(self):
        selected = self.video_label_listbox.get(self.video_label_listbox.curselection()).split(':')[0]
        del self.annotations[selected]
        self._reload_annotations()

    def _get_json_filename(self):
        directory = self.url_input_entry.get().rsplit('/', 1)
        self.directory = directory[0]
        filename = directory[1].rsplit('.', 1)
        return directory[0] + '/' + filename[0] + '.json'

    def _load_json(self):
        filename = self._get_json_filename()
        with open(filename) as f:
            self.annotations = json.load(f)


VideoFrameLabeler()
