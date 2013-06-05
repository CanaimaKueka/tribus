#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s.sh [MÓDULO] [PARÁMETROS] [...]
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import gtk, pango, vte, re

from canaimasemilla.config import *

def WindowContainer(c, title, outpad, inpad, spacing):
    window = gtk.Window()
    window.set_border_width(0)
    window.set_title(title)
    window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    window.set_size_request(window_width, window_height)
    window.set_resizable(False)
    window.set_icon_from_file(BAR_ICON)
    window.connect("destroy", gtk.main_quit)
    window.connect("delete-event", gtk.main_quit)

    outbox = gtk.VBox()
    outbox.set_border_width(outpad)

    inbox = gtk.VBox(spacing = spacing)
    inbox.set_border_width(inpad)

    return window, outbox, inbox

def CustomBox(c, box, align):
    if align == 'horizontal':
        custombox = gtk.HBox()
    elif align == 'vertical':
        custombox = gtk.VBox()

    box.pack_start(custombox, False, False, 0)

    return custombox

def CustomSeparator(c, box, align):
    if align == 'horizontal':
        customseparator = gtk.HSeparator()
    elif align == 'vertical':
        customseparator = gtk.VSeparator()

    box.pack_start(customseparator, False, False, 0)

    return customseparator

def TabbedBox(c, box, pos, tabs):
    notebook = gtk.Notebook()
    notebook.set_tab_pos(pos)

    boxes = []
    i = 0
    for text in tabs:
        i += 1
        label = gtk.Label(text)
        tab = gtk.VBox(spacing = 5)
        tab.set_border_width(10)
        notebook.append_page(tab, label)
        boxes.append(tab)

    box.pack_start(notebook, False, False, 0)

    return boxes

def Banner(c, box, image):
    banner = gtk.Image()
    banner.set_from_file(image)

    box.pack_start(banner, False, False, 0)

    return banner

def Title(c, box, text):
    title = gtk.Label()
    title.set_markup(text)
    title.set_line_wrap(True)
    title.set_size_request(window_width - box.get_border_width()*4, -1)

    box.pack_start(title, False, False, 0)

    return title

def Description(c, box, text):
    style = pango.AttrList()
    size = pango.AttrSize(8000, 0, -1)
    style.insert(size)

    description = gtk.Label()
    description.set_markup(text)
    description.set_line_wrap(True)
    description.set_size_request(window_width - box.get_border_width()*4, -1)
    description.set_attributes(style)

    box.pack_start(description, expand, fill, padding)

    return description

def TextEntry(c, box, maxlength, length, text, regex):
    textentry = gtk.Entry()
    textentry.set_width_chars(length)
    textentry.set_max_length(maxlength)
    textentry.set_text(text)
    textentry.set_sensitive(True)
    textentry.set_editable(True)
    textentry.set_visibility(True)
    textentry.connect('insert-text', LimitEntry, regex)
    textentry.connect('focus-in-event', ClearEntry, text)
    textentry.connect('focus-out-event', FillEntry, text)

    box.pack_start(textentry, False, False, 0)

    return textentry

def NumericSelector(c, box, init, lower, upper, inc_1, inc_2):
    adjustment = gtk.Adjustment(init, lower, upper, inc_1, inc_2, 0.0)
    spinner = gtk.SpinButton(adjustment, 0, 0)
    spinner.set_update_policy(gtk.UPDATE_IF_VALID)
    spinner.set_numeric(True)
    spinner.set_wrap(False)

    box.pack_start(spinner, False, False, 0)

    return spinner

def ActiveCombo(c, box, combolist, combodefault, entry, f_1 = False, p_1 = False,
    f_2 = False, p_2 = False, f_3 = False, p_3 = False
    ):

    if entry:
        combo = gtk.combo_box_entry_new_text()
    else:
        combo = gtk.combo_box_new_text()

    for item in combolist:
        combo.append_text(item)

    if f_1:
        combo.connect('changed', f_1, *p_1)
    if f_2:
        combo.connect('changed', f_2, *p_2)
    if f_3:
        combo.connect('changed', f_3, *p_3)

    combo.set_active(combodefault)

    box.pack_start(combo, False, False, 0)

    return combo

def CheckList(c, box, checklist, checkdefault = ''):
    items = gtk.VBox()

    for item in checklist:
        check = gtk.CheckButton(item)
        if checkdefault != '' and item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        items.pack_start(check, False, False, 0)

    box.pack_start(items, False, False, 0)

    return items

def OptionList(c, box, optionlist, optiondefault = ''):
    items = gtk.VBox()

    option = None
    for item in optionlist:
        option = gtk.RadioButton(option, item)
        if optiondefault != '' and item == optiondefault:
            option.set_active(True)
            option.set_sensitive(False)
        items.pack_start(option, False, False, 0)

    box.pack_start(items, False, False, 0)

    return items

def ScrolledFrame(c, box):
    frame = gtk.Frame()

    scrolledwindow = gtk.ScrolledWindow()
    scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    textview = gtk.TextView()
    textview.set_wrap_mode(gtk.WRAP_WORD)
    textview.set_editable(False)
    text = textview.get_buffer()

    scrolledwindow.add(textview)
    frame.add(scrolledwindow)
    box.pack_start(frame, True, True, 0)

    return text

def ActiveButton(c, box, text, width, height, f_1 = False, p_1 = False,
    f_2 = False, p_2 = False, f_3 = False, p_3 = False
    ):

    button = gtk.Button(stock = text)

    if width != 0 and height != 0:
        button.set_size_request(width, height)

    if f_1:
        button.connect('clicked', f_1, *p_1)
    if f_2:
        button.connect('clicked', f_2, *p_2)
    if f_3:
        button.connect('clicked', f_3, *p_3)

    box.pack_start(button, False, False, 0)

    return button

def ActiveCheck(c, box, text, active, f_1 = False, p_1 = False,
    f_2 = False, p_2 = False, f_3 = False, p_3 = False
    ):

    check = gtk.CheckButton(text)

    if active:
        check.set_active(True)

    if f_1:
        check.connect('toggled', f_1, *p_1)

    if f_2:
        check.connect('toggled', f_2, *p_2)

    if f_3:
        check.connect('toggled', f_3, *p_3)

    box.pack_start(check, False, False, 0)

    return check

def IconButton(c, box, icon, text_1, text_2, width, height, margin, f_1, p_1):
    hbox = gtk.HBox()
    hbox.set_border_width(margin)

    button = gtk.Button()
    button.set_size_request(width, height)
    button.connect("clicked", f_1, *p_1)

    inbox = gtk.VBox()
    inbox.set_border_width(5)

    image = gtk.Image()
    image.set_from_file(icon)

    attr = pango.AttrList()
    size = pango.AttrSize(20000, 0, -1)
    attr.insert(size)

    title = gtk.Label()
    title.set_markup(text_1)
    title.set_justify(gtk.JUSTIFY_CENTER)
    title.set_attributes(attr)

    description = gtk.Label()
    description.set_markup(text_2)
    description.set_line_wrap(True)
    description.set_justify(gtk.JUSTIFY_CENTER)

    inbox.pack_start(image, False, False, 0)
    inbox.pack_start(title, False, False, 0)
    inbox.pack_start(gtk.HSeparator(), False, False, 5)
    inbox.pack_start(description, False, False, 0)
    button.add(inbox)

    hbox.pack_start(button, False, False, 0)
    box.pack_start(hbox, False, False, 0)

    return button

def BottomButtons(c, box, width, height, fclose = False, pclose = False, 
        fhelp = False, phelp = False, fabout = False, pabout = False,
        fback = False, pback = False, fgo = False, pgo = False
        ):

    hbox = gtk.HBox(False, 2)
    hbox.set_border_width(2)

    if fclose:
        close = ActiveButton(
            c = c, box = hbox, text = gtk.STOCK_CLOSE,
            width = width, height = height,
            f_1 = fclose, p_1 = pclose
        )

    if fhelp:
        help = ActiveButton(
            c = c, box = hbox, text = gtk.STOCK_HELP,
            width = width, height = height,
            f_1 = fhelp, p_1 = phelp
        )

    if fabout:
        about = ActiveButton(
            c = c, box = hbox, text = gtk.STOCK_ABOUT,
            width = width, height = height,
            f_1 = fabout, p_1 = pabout
        )

    hbox.pack_start(gtk.HSeparator(), False, False, 140)

    if fback:
        back = ActiveButton(
            c = c, box = hbox, text = gtk.STOCK_GO_BACK,
            width = width, height = height,
            f_1 = fback, p_1 = pback
        )

    if fgo:
        go = ActiveButton(
            c = c, box = hbox, text = gtk.STOCK_GO_FORWARD,
            width = width, height = height,
            f_1 = fgo, p_1 = pgo
        )

    box.pack_start(gtk.HSeparator(), False, False, 2)
    box.pack_start(hbox, False, False, 0)

    return hbox

def UserSelect(c, title, action, entry, allfiltertitle, filter = False):

    dialog = gtk.FileChooserDialog(
        title = title, parent = None, action = action,
        buttons = (
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK
            )
        )

    dialog.set_default_response(gtk.RESPONSE_OK)

    if filter:
        f = gtk.FileFilter()
        f.set_name(filter['name'])
        for mimetype in filter['mimetypes']:
            f.add_mime_type(mimetype)
        dialog.add_filter(f)

    f = gtk.FileFilter()
    f.set_name(allfiltertitle)
    f.add_pattern('*')
    dialog.add_filter(f)

    response = dialog.run()

    if response == gtk.RESPONSE_OK:
        entry.set_text(dialog.get_filename())

    dialog.destroy()

    return response

def UserMessage(message, title, type, buttons,
                    c_1 = False, f_1 = False, p_1 = '',
                    c_2 = False, f_2 = False, p_2 = '',
                    c_3 = False, f_3 = False, p_3 = ''
                    ):

    dialog = gtk.MessageDialog(
        parent = None, flags = 0, type = type,
        buttons = buttons, message_format = message
        )
    dialog.set_title(title)
    response = dialog.run()
    dialog.destroy()

    if response == c_1:
        f_1(*p_1)
    if response == c_2:
        f_2(*p_2)
    if response == c_3:
        f_3(*p_3)

    return response

def AboutWindow():
    about = gtk.AboutDialog()
    about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    about.set_logo(gtk.gdk.pixbuf_new_from_file(ABOUT_IMAGE))
    about.set_name(app_name)
    about.set_copyright(app_copyright)
    about.set_comments(app_description)
    about.set_website(app_url)

    try:
        f = open(LICENSE_FILE, 'r')
        license = f.read()
        f.close()
    except Exception, msg:
        license =  'NOT FOUND'

    try:
        f = open(AUTHORS_FILE, 'r')
        a = f.read()
        authors = a.split('\n')
        f.close()
    except Exception, msg:
        authors = 'NOT FOUND'

    try:
        f = open(TRANSLATORS_FILE, 'r')
        translators = f.read()
        f.close()
    except Exception, msg:
        translators = 'NOT FOUND'

    try:
        f = open(VERSION_FILE, 'r')
        version = f.read().split('\n')[0].split('=')[1].strip('"')
        f.close()
    except Exception, msg:
        version = 'NOT FOUND'

    about.set_translator_credits(translators)
    about.set_authors(authors)
    about.set_license(license)
    about.set_version(version)

    about.run()
    about.destroy()

def ProgressWindow(text, title, q_window, q_bar, q_msg, term = False,
                    q_terminal = '', fcancel = False, pcancel = ()):

    dialog = gtk.Dialog()
    dialog.set_title(title)
    dialogarea = dialog.get_content_area()
    dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    if term:
        dialog.set_size_request(window_width, window_height)
    else:
        dialog.set_size_request(window_width*3/4, window_height/4)
    dialog.set_resizable(False)

    box = gtk.VBox()
    box.set_border_width(borderwidth)

    label = gtk.Label()
    label.set_markup(text)
    label.set_justify(gtk.JUSTIFY_CENTER)
    progress = gtk.ProgressBar()

    if term:
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        terminal = vte.Terminal()
        terminal.set_cursor_blinks(True)
        terminal.set_emulation('xterm')
        terminal.set_scrollback_lines(1000)
        terminal.set_audible_bell(True)
        terminal.set_visible_bell(False)
        scroll.add(terminal)

    box.pack_start(label, False, False, 5)
    box.pack_start(progress, False, False, 0)

    if term:
        box.pack_start(gtk.HSeparator(), False, False, 0)
        box.pack_start(scroll, True, True, 0)

    button = gtk.Button(stock = gtk.STOCK_CANCEL)
    button.connect_object("clicked", gtk.Window.destroy, dialog)

    if fcancel:
        button.connect("clicked", fcancel, *pcancel)

    box.pack_start(gtk.HSeparator(), False, False, 0)
    box.pack_start(button, False, False, 0)

    dialogarea.add(box)
    dialog.show_all()
    
    q_window.put(dialog)
    q_bar.put(progress)
    q_msg.put(label)
    if term:
        q_terminal.put(terminal)
    return dialog

def LimitEntry(editable, new_text, new_text_length, position, regex):
    limit = re.compile(regex)
    if limit.match(new_text) is None:
        editable.stop_emission('insert-text')

def CleanEntry(editable, textbuffer):
    textbuffer.set_text('')

def ClearEntry(editable, new_text, text):
    content = editable.get_text()
    if content == text:
        editable.set_text('')

def FillEntry(editable, new_text, text):
    content = editable.get_text()
    if content == '':
        editable.set_text(text)
