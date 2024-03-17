import sys
sys.path.append('..')
import helper
import subprocess
import os
import platform
import importlib
try:
    from PIL import Image
except ImportError:
    print("PIL is not installed. Installing...")
    import pip
    pip.main(['install', 'Pillow'])  # Pillow is the modern version of PIL
    importlib.reload(Image)

Logger = helper.setup_logging()

def install_prereqs():

    os_name = platform.system()
    print(f"OS: {os_name}")
    if "Windows" in os_name:
        print("Installing ImageMagick via chocolatey...")
        subprocess("choco install ImageMagick", shell=True)

def get_files():
    Logger.info("running get_files()")
    files = helper.select_files()
    return files

def compress_files(files):
   Logger.info("running compress_files()")
   compress_mag = 50
   compress_mag = input("\nWhat percent of the original do you want to keep? ")

   for image in files:
      cmd = f"magick convert {image} -quality {compress_mag} {image}"
      print(cmd)
      subprocess.run(cmd, shell=True)

def add_border(files):

   Logger.info("running add_border()")
   color = input("Enter the color name(common colors, hex code rgb(0,0,0), rgba(0,0,0,0)) :")
   for image in files:
      img = Image.open(image)
      bw, bl = img.size
      bw = bw//10
      bl = bl//10

      cmd = f"magick convert {image} -border {bw}x{bl} -bordercolor {color} {image}"
      print(cmd)
      subprocess.run(cmd, shell=True)

def add_watermark(files):
   Logger.info("running add_watermark()")
   watermark = helper.select_files()[0]
   for image in files:
      cmd = f"magick composite -gravity center {watermark} {image} {image}"
      print(cmd)
      subprocess.run(cmd, shell=True)

def create_CNAME():
    Logger.info("running create_CNAME()")
    folders = helper.select_folders()
    for folder in folders:
        name = input(f"Enter the cname for {folder}")
        name = f"{name}.surge.sh"
        cmd = f"echo {name} >> CNAME"
        subprocess.run(cmd, cwd=folder, shell=True)

def deploy_to_cdn(generate_filelist = False):
    folders = helper.select_folders()
    for folder in folders:
        cmd = f"surge"
        subprocess.run(cmd, cwd=folder, shell=True)
    
    if generate_filelist == True:
        for folder in folders:
            with open(f"{folder}/urls.txt", 'a') as output:
                with open(f"{folder}/CNAME", 'r') as CNAME_FILE:
                    cname = CNAME_FILE.readline().strip()
                # Iterate over all files in the folder
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    # Check if the current item is a file
                    if os.path.isfile(file_path):
                        # Open the file and read its contents
                        with open(file_path, 'r') as f:
                            # Read the contents of the file and append it to the output file
                            output.write(f"{cname}/{f.read()}")
                            output.write('\n') 

def generate_filelist():
    folders = helper.select_folders()
    for folder in folders:
        with open(f"{folder}/urls.txt", 'a', encoding="utf-8") as output:
            with open(f"{folder}/CNAME", 'r') as CNAME_FILE:
                cname = CNAME_FILE.readline().strip()
                CNAME_FILE.close()
            # Iterate over all files in the folder
            for filename in os.listdir(folder):
                # Read the contents of the file and append it to the output file
                output.write(f"{cname}/{filename}")
                output.write('\n') 

            output.close()




def run_cmds():
    #print("get_files()")
    #files = get_files()
    #print("compress_files()")
    #compress_files(files)
    #print("add_border()")
    #add_border(files)
    #deploy_to_cdn()
    generate_filelist()

run_cmds()

   

