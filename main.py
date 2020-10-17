#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2020 Timéo Arnouts <dogm@dogm-s-pc>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import configparser
import datetime
import dbus
import os
import random
import time


stallman_images_path = os.path.join(os.getcwd(), "img")
list_stallman_images = os.listdir(stallman_images_path)

def logging(path):
    """Returns a logging message."""
    return "%s: Current wallpaper at path %s" % (time.strftime("%X"), path)


def settings_reader(parameter, configuration_file_path):
    """Returns the value of the parameter contained in "parameters" section of given .conf file. """
    config_file = os.path.join(os.getcwd(), configuration_file_path)

    settings = configparser.ConfigParser()
    settings.read(config_file)

    return settings["parameters"][parameter]


def image_selector(directory_path):
    """Returns the path of a new randomly selected wallpaper in the given directory path."""
    return random.choice(list_stallman_images)


def path_formatter(path):
    """Returns the script formatted with the path of a given image """

    return """var allDesktops = desktops();
print (allDesktops);
for (i=0;i<allDesktops.length;i++) {
    d = allDesktops[i];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
    d.writeConfig("Image", "file:%s")
}
""" % path


def main():
    """Main function."""
    # Time between changes of each wallpaper in seconds.
    sleep_duration = int(settings_reader("sleep_duration", "config.conf"))

    bus = dbus.SessionBus()
    plasma_shell = dbus.Interface(
                                  bus.get_object("org.kde.plasmashell", "/PlasmaShell"),
                                  dbus_interface="org.kde.PlasmaShell"
                                 )

    while 1:
        selected_wallpaper_path =  os.path.join(stallman_images_path, image_selector(list_stallman_images))
        print(logging(selected_wallpaper_path))
        plasma_shell.evaluateScript(path_formatter(selected_wallpaper_path))
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
