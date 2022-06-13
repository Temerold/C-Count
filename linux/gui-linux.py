import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import colorama as col
import subprocess as sp
import os
import multitasking
from termcolor import cprint


# To avoid the "Security-Alert: try to store file outside of dist-directory. Aborting."
# error `pyinstaller` raises when we try to build with paths in `..`, we have to have
# seperate paths, based on if the code has been built or not.
# First of all: it raises this error when trying to build a Python program that tries to
# access files locaded in `..`, in other words, the parent directory. However, there are
# no parent directories to the .exe (`C-Count.exe`).*
#
# This is the directory structue according to the .py file (`gui.py`):
# |   README.md
# |
# +---linux
# |       build-linux.sh
# |       compile-linux.sh
# |       count-linux.exe
# |       count-linux.c
# |       gui-linux.py
# |
# +---src
# |       logo.ico
# |       logo.png
# |       logo.xbm
# |       off.png
# |       off_small.png
# |       on.png
# |       on_small.png
# |
# \---windows
#        build.bat
#        compile.bat
#        count.c
#        count.exe
#        gui.py
#
# So `..` takes the program to `C-Count-master` (or whatever the parent directory is
# named).
#
# And this is what the directory looks like, according to the .exe (`C-Count.exe`):
# |   count.exe
# |   gui.exe
# |   logo.ico
# |   off_small.png
# |   on_small.png
# |   ... [More -- insignificant]
#
# *There is no `..`, since there is no parent directory inside of it.
# So, we have to access files in `.` if it's been built.
# However, we can't use `.`, because that is the .exe's directory. When the `pyinstaller`
# .exe is ran, it creates a temp folder, in which it places all the files -- so, the .py
# file, icons, images, and such. If it's been built, we have to access all the files from
# the temp folder (`file_path`).
file_path = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(file_path + "\\.exe_identifier"):
    icon_path = file_path + "\\logo.ico"
    off_path = file_path + "\\off_small.png"
    on_path = file_path + "\\on_small.png"
    count_path = file_path + "\\count.exe"

else:
    icon_path = "../src/logo.ico"
    off_path = "../src/off_small.png"
    on_path = "../src/on_small.png"
    count_path = "/count.exe"


root = tk.Tk()
root.title("C-Count")
root.geometry("320x500")
root.resizable(width=False, height=False)
root.minsize(320, 500)

# TODO: Make icon colored
root.iconphoto(True, ImageTk.PhotoImage(file="../src/logo.xbm"))

col.init()  # Initialize Colorama's text color-coding


def shutdown_protocol():
    kill_counting()
    root.destroy()
    os._exit(0)


@multitasking.task
def raise_message(text, title="Error!", type="error"):
    if type == "error":
        messagebox.showerror(title, text)
    elif type == "warning":
        messagebox.showwarning(title, text)
    else:
        raise_message('`raise_message()` only accepts types "error" and "warning"!')


def kill_counting():
    # Shell command that kills `count.exe`
    shutdown_command = "pkill count-linux"

    # `subprocess.run()` takes the command argument as a list, so we have to do this
    command_list = shutdown_command.split(" ")
    sp.run(command_list, stdout=sp.DEVNULL)  # `stdout=sp.DEVNULL` mutes the output


def run_checks(start, end, change_color_on_error=True, show_message_box_on_error=True):
    ## Check if entry boxes are empty. If so, return False.
    if start == "" and change_color_on_error:
        start_entry.config({"background": "red"})
        start_entry.config({"foreground": "white"})

    if end == "" and change_color_on_error:
        end_entry.config({"background": "red"})
        end_entry.config({"foreground": "white"})

    if start == "" or end == "":
        if show_message_box_on_error:
            raise_message("Invalid input! Entry boxes can't be empty.")

        return False

    ## Check if start integer is greater than end integer. If so, return False.
    # Use try except, in case conversion of `start` and `end` to integers fail, due to
    # them not being numbers.
    try:
        if int(start) > int(end) and end != "-1" and end != "":
            if show_message_box_on_error:
                raise_message(
                    "Invalid input! Start integer can't be greater than end integer."
                )

            if change_color_on_error:
                start_entry.config({"background": "red"})
                start_entry.config({"foreground": "white"})

            return False
    except ValueError:
        pass

    ## Check if end "integer" is "-". If so, return False.
    if change_color_on_error and end == "-":
        raise_message("Invalid input! End integer can't be only a minus.")
        end_entry.config({"background": "red"})
        end_entry.config({"foreground": "white"})

        return False

    start_entry.config({"background": "white"})
    start_entry.config({"foreground": "black"})
    end_entry.config({"background": "white"})
    end_entry.config({"foreground": "black"})

    return True


start_entry_old_state = ""
end_entry_old_state = ""
infinity_mode = tk.BooleanVar()


def infinity_mode_switch(event=None):
    global start_entry_old_state
    global end_entry_old_state
    global infinity_mode

    if not infinity_mode.get():  # Enable
        # If the start entry box is empty, fill it in with 1
        if start_entry.get() == "":
            # Save start entry box's current state
            start_entry_old_state = start_entry.get()
            start_entry.delete(0, "end")  # Delete start entry box's contents
            start_entry.insert(0, "1")

        end_entry_old_state = end_entry.get()  # Save end entry box's current state
        end_entry.delete(0, "end")
        end_entry.insert(0, "Infinity")
        end_entry.config(state="disabled")

    else:  # Disable
        end_entry.config(state="normal")
        end_entry.delete(0, "end")

        if start_entry_old_state == "" and start_entry.get() == "1":
            start_entry.delete(0, "end")  # Revert to old state -- ""

        if end_entry_old_state not in ["-1", "-", "1"]:
            # Insert the old value (`end_entry_old_state`)
            end_entry.insert(0, end_entry_old_state)

    # After entry boxs' contents are deleted, their validate keys get removed. Why? I
    # don't know. Anyway, we have to redefine them:
    start_entry.config(validate="key")
    end_entry.config(validate="key")


def validate_input(name, action, new, old):
    """
    @ name: The name of the widget.
    @ action: Action code; "0" for an attempted deletion, "1" for an attempted insertion,
            @ or "-1" if the callback was called for focus in, focus out, or a change to
            @ the textvariable.
    @ new: The value that the text will have if the change is allowed.
    @ old: The text in the entry before the change.
    """

    allowed_chars = "0123456789-"

    ## Check if attempted action is deletion. If so, allow it.
    if action == "0":
        return True

    ## Check if input is "Infinity". If so, allow it.
    if name == "end" and new == "Infinity":
        return True

    ## Check if the input is longer than 1 character. If so, break it up into several
    ## `validate_input()` calls.
    # Go through `new`, and check for illegal characters. If any are found, none of the
    # characters gets through.
    if len(new) - len(old) > 1:
        for char in new:
            if not validate_input(name, "1", char, ""):
                return False

    if action != "1":
        return False

    # `_input` is what character has been typed
    if len(new) == 1:
        _input = new
    else:
        # Go through the `old` and `new` character pairs, and check where they differ.
        # These are the rules for each recursion:
        # We can always assume that `new` is longer than `old`, because we're adding 1
        # character to `old` in `new`. So, if they differ on index `index`, we know
        # that the differing (the input) character is `new[index]`.
        # If `old`'s length is `index`, and `old[index]` and `new[index]` are the
        # same, we know that the differing (the input) character is
        # `new[index + 1]`.
        index = 0
        for old_char, new_char in zip(old, new):
            if len(old) == index + 1 and old_char == new_char:
                _input = new[index + 1]
            elif old_char != new_char:
                _input = new[index]
                break

            index += 1

    # If `_input` doesn't exist, it means that `validate_input()` has recieved a
    # longer-than-1-character input. If it continued to here, it means that each
    # individual character is legal anyways, so we can define (lie) `_input` as "0" (which
    # is in `allowed_chars`), so that it passes below.
    # ! IMPORTANT: If the `_input` variable's name changes, this if statement won't work,
    # ! because it's looking for a variable named "_input"!
    if "_input" not in locals():
        _input = "0"

    if _input not in allowed_chars:
        return False

    ## Check if value is going to be (or be able to become) "-1". If so, allow it.
    if name == "end" and new == "-1":
        infinity_mode_switch()
        inifnity_mode_check_button.select()

        return True

    if _input == "-":
        if name == "start":
            return False

        if old == "":
            return True

        if old == "-" and new != "-1":
            return False

        return False

    if old == "-" and new != "-1":
        return False

    return True


def entry_vcmd_while_typing(name, action, new, old):
    result = validate_input(name, action, new, old)

    if result:  # Run checks if the the characters are legal
        if name == "start":
            run_checks(
                new,
                end_entry.get(),
                change_color_on_error=False,
                show_message_box_on_error=False,
            )
        else:
            run_checks(
                start_entry.get(),
                new,
                change_color_on_error=False,
                show_message_box_on_error=False,
            )

    return result


class Image_button(tk.Button):
    def __init__(self, master, unclicked, clicked):
        self.unclicked_image = tk.PhotoImage(file=unclicked)
        self.clicked_image = tk.PhotoImage(file=clicked)
        super().__init__(
            master, image=self.unclicked_image, height=250, width=250, bd=0
        )
        self.toggle_state = -1  # -1 is off; 1 is on
        self.bind("<Button-1>", self.click_function)

    @multitasking.task
    def click_function(self, event=None):
        self.toggle_state *= -1
        if self.toggle_state == 1:  # On

            start = start_entry.get()
            end = end_entry.get()
            if end == "Infinity":
                end = "-1"

            if run_checks(start, end):
                c_program = sp.Popen(["./count-linux.exe", start, end])
                self.config(image=self.clicked_image)
                c_program.communicate()[0]
                return_code = c_program.returncode
                if return_code == 0:
                    cprint("\nSuccess!", "green")

                self.config(image=self.unclicked_image)

        else:  # Off
            self.config(image=self.unclicked_image)

            kill_counting()
            cprint("\nTerminated.", "red")

        self.toggle_state = -1


button = Image_button(root, "../src/off_small.png", "../src/on_small.png")
button.pack()

# Start entry box validation command
start_vcmd = (root.register(entry_vcmd_while_typing), "start", "%d", "%P", "%s")

# End entry box validation command
end_vcmd = (root.register(entry_vcmd_while_typing), "end", "%d", "%P", "%s")

frame = tk.Frame()
frame.pack()

start_label = tk.Label(frame, text="Start at")
start_label.grid(row=0, column=0, sticky="e")

start_entry = tk.Entry(frame)
start_entry.grid(row=0, column=1, sticky="w")
start_entry.config(validate="key", validatecommand=start_vcmd)

end_label = tk.Label(frame, text="End at")
end_label.grid(row=1, column=0, sticky="e")

end_entry = tk.Entry(frame)
end_entry.grid(row=1, column=1, sticky="w")
end_entry.config(validate="key", validatecommand=end_vcmd)

inifnity_mode_check_button = tk.Checkbutton(
    frame,
    text="Infinity mode",
    variable=infinity_mode,
    onvalue=True,
    offvalue=False,
)
inifnity_mode_check_button.grid(row=2, column=1, sticky="w")
inifnity_mode_check_button.bind("<Button-1>", infinity_mode_switch)

root.protocol("WM_DELETE_WINDOW", shutdown_protocol)
root.mainloop()
