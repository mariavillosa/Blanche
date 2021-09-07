#!/usr/bin/env python3

from tkinter import *
from pathlib import Path
import subprocess

class BlanchControl:
    def __init__(self):
        self.whitelist_path = f'{Path.home()}/.whitelist'
        self.enabled = 'none' not in subprocess.check_output('gsettings get org.gnome.system.proxy mode'.split()).decode('ascii')

    def _formatted_domains(self):
        return [f'*.{i}' for i in self.read_config().split('\n') if i != '']

    def enable_proxy(self):
        self.enabled = True
        commands = [cmd.strip() for cmd in f"""
            gsettings set org.gnome.system.proxy mode 'manual'
            gsettings set org.gnome.system.proxy.socks port 9001
            gsettings set org.gnome.system.proxy.socks host 'localhost'
            gsettings set org.gnome.system.proxy ignore-hosts "{self._formatted_domains()}"
        """.split('\n') if cmd.strip() != '']
        for cmd in commands:
            subprocess.run(cmd, shell=True)

    def disable_proxy(self):
        self.enabled = False
        cmd = "gsettings set org.gnome.system.proxy mode 'none'"
        subprocess.run(cmd.split())

    def read_config(self):
        try:
            with open(self.whitelist_path) as config_file:
                return config_file.read()
        except FileNotFoundError:
            return 'example1.test\nexample2.fakesite.test'

    def save_config(self, config):
        with open(self.whitelist_path, 'w+') as config_file:
            config_file.write(config)

class BlancheGui:
    def __init__(self):
        self.controller = BlanchControl()
        self.window = Tk()
        width = 280
        height = 210
        self.window.geometry(f'{width}x{height}')
        self.window.title("Blanche Domain Whitelister")
        self.add_whitelist_toggle()
        self.add_whitelist_text()
        self.add_save_btn()
        self.window.mainloop()

    def add_whitelist_toggle(self):
        btn_text = StringVar()
        def toggle(btn):
            if self.controller.enabled:
                self.controller.disable_proxy()
                toggle_btn.config(relief='raised')
                btn_text.set('Enforce whitelist')
            else:
                self.controller.enable_proxy()
                toggle_btn.config(relief='sunken')
                btn_text.set('Disable whitelist')

        toggle_btn = Button(self.window, textvariable=btn_text, width=12, relief="sunken" if self.controller.enabled else "raised")
        toggle_btn.config(command=lambda: toggle(toggle_btn))
        btn_text.set(f"{'Disable' if self.controller.enabled else 'Enforce'} whitelist")
        toggle_btn.pack(pady=5)

    def add_whitelist_text(self):
        lbl = Label(self.window, text="    allowed domains:")
        lbl.pack(anchor='w')
        T = Text(self.window, height=5, width=30)
        T.pack()
        T.insert(END, self.controller.read_config())
        self.text = T

    def add_save_btn(self):
        save_text = StringVar()
        save_text.set('Save')
        save_button = Button(self.window, textvariable=save_text, width=12, relief="raised")
        def save_config():
            self.controller.save_config(self.text.get('1.0', 'end-1c'))
            save_text.set('Saving...')
            save_button.config(relief='sunken')
            self.window.after(500, lambda: (save_text.set('Save') or True) and save_button.config(relief='raised'))

        save_button.config(command=save_config)
        save_button.pack(pady=5)

if __name__ == '__main__':
    gui = BlancheGui()
