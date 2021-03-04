import os
import sys
import subprocess

BASE_DIR = "./"
FRONTEND_DIR = "autonomus-app"
FRONTEND_GIT = "https://git.lais.huol.ufrn.br/ela/autonomus-app.git"
KEYBOARD_DIR = "back-end-teclado-interativo"
KEYBOARD_GIT = "https://git.lais.huol.ufrn.br/ela/back-end-teclado-interativo.git"


os.system("color")

def cprint(msg):
    YELLOW = "\033[33m"
    WHITE = "\033[0m"
    print(YELLOW + msg + WHITE)

def repo_exists(repo_dir, repo_git, branch="dev" ):
    exists = os.path.exists(repo_dir + "/.git")
    if exists:
        cprint("\n ## Atualizando repositorio " + repo_dir + ".\n")
        subprocess.call('', shell=True)
        os.chdir(repo_dir)
        os.system("git checkout " + branch)
        os.system("git pull")
        os.chdir("..")
    else:
        cprint("\n ## Repositorio " + repo_dir + " nao existe.\n ## Clonando o repositorio.\n")
        os.system("git clone " + repo_git)

def build_front():
    os.chdir(FRONTEND_DIR)
    cprint("\n ## Baixando dependencias de " + FRONTEND_DIR + "\n")
    os.system("npm install")
    cprint("\n ## Compilando " + FRONTEND_DIR + "\n")
    os.system("npm run build")
    os.system("npm run electron-build")
    #  os.system("npm run electron-pack")
    os.chdir("..")

def build_keyboard():
    os.chdir(KEYBOARD_DIR)
    if (not os.path.exists("venv")):
        os.system("virtualenv venv")
    VENV_DIR = "venv\\Scripts\\"
    CV2_DIR = "venv\\Lib\\site-packages\\cv2\\"
    OPENCV_FILE = ""
    cprint("\n ## Baixando dependencias de " + KEYBOARD_DIR + "\n")
    os.system("pip install pyinstaller")
    os.system(VENV_DIR + "pip install -r requirements.txt")
    cprint("\n ## Verificando versao do OpenCV e adicionando DLL ao instalador \n")
    for file in os.listdir(CV2_DIR):
        if file.endswith(".dll"):
            OPENCV_FILE = file
            os.system("copy /y " + CV2_DIR + OPENCV_FILE + ".")
    cprint("\n ## Compilando backend e modelo da piscada \n")
    os.system('pyinstaller --hidden-import=pyttsx3 -p venv\\lib\\site-packages --add-data src\\words_filtered.txt;. --add-data src\\big_text.txt;. --add-data src\\autocomplete\\models_compressed.pkl;autocomplete\\ --add-data "' + OPENCV_FILE + ';." --hidden-import=pyttsx3.drivers.sapi5 --hidden-import=pywin32 --hidden-import=pywin32-ctypes --hidden-import=pkg_resources.py2_warn src\\build.py --noconfirm')
    os.chdir("..")

def build_installer():
    cprint("\n ## Construindo o instalador.\n")
    bat = os.open("tmp.bat", os.O_WRONLY | os.O_CREAT)
    command = str.encode('"%programfiles(x86)%\\NSIS\makensis.exe" /V4 make_installer.nsi')
    os.write(bat, command)
    os.close(bat)
    cprint("\n ### Executando script nsi.\n")
    os.system("tmp.bat")
    os.remove("tmp.bat")

def finished():
    cprint("\n ## Instalador criado com sucesso: autonomus-installer.exe")

if len(sys.argv) == 2:
    BASE_DIR = sys.argv[1]

os.chdir(BASE_DIR)
repo_exists(FRONTEND_DIR, FRONTEND_GIT, "master")
repo_exists(KEYBOARD_DIR, KEYBOARD_GIT, "master")
build_front()
build_keyboard()
build_installer()
finished()
