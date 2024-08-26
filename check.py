import os


def check_fail_name(name):
    os.chdir("static/img")
    fl = True
    if name in os.listdir():
        fl = False
    os.chdir("..")
    os.chdir("..")
    return fl


def create_name(object_="icon"):
    os.chdir("static/img")
    list_dir = os.listdir()
    name = None
    fl = True
    le = len(list_dir)
    if object_ == "icon":
        while fl:
            if not (f"{object_}{le + 1}" in list_dir):
                name = f"{object_}{le + 1}"
                fl = False
            else:
                le -= 1
    elif object_ == "product":
        while fl:
            if not (f"{object_}{le + 1}" in list_dir):
                name = f"{object_}{le + 1}"
                fl = False
            else:
                le -= 1
    elif object_ == "rest":
        while fl:
            if not (f"{object_}{le + 1}" in list_dir):
                name = f"{object_}{le + 1}"
                fl = False
            else:
                le -= 1
    os.chdir("..")
    os.chdir("..")
    return name

