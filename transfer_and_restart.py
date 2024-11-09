import os
import shutil
import signal
import subprocess
import time
import zipfile
import psutil 

def stop_flask_app():
    current_pid = os.getpid()
    print(current_pid)
    for proc in psutil.process_iter(attrs=["pid","name","cmdline"]):
        if proc.info['pid'] != current_pid:  
            # print(proc)
            # proc.kill()
            if proc.info['name'] == "python.exe":
            # if 'flas' in proc.name() or 'flas' in ' '.join(proc.cmdline()).lower():
            # if proc.info['name'] == "flas":
                # print(proc)
                try:
                    parent_proc = proc.parent()
                    print("python process : ",proc)
                    print("parent process : ",parent_proc)

                    

                    # if parent_proc:
                    #     # if "cmd.exe" in parent_proc.info['name'].lower() or "powershell.exe" in parent_proc.info['name'].lower():
                    #     if parent_proc.name == "cmd.exe" or parent_proc.name == "powershell.exe":
                    #         # parent_proc.kill()
                    #         # parent_proc.terminate()
                    #         # subprocess.run(["taskkill","/f,"/pid",str(parent_proc.pid)],check=True)
                    #         # os.kill(parent_proc.pid,signal.SIGTERM)
                    #         subprocess.run(['taskkill','/PID',str(parent_proc.pid),'/T','/F'],capture_output=True,text=True,check=True)
                    #         print(f"Killed parent process : ",parent_proc.name)
                    # proc.kill()
                    subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True,text=True,check=True)
                    print("killed process: ",proc.pid)
                    parent_parent_proc = parent_proc.parent()
                    if parent_proc:
                        subprocess.run(['taskkill','/PID',str(parent_proc.pid),'/T','/F'],capture_output=True,text=True,check=True)
                        print("killed parent : ",parent_proc.pid)
                        print("parent parent proc : ",parent_parent_proc)
                        if parent_proc.name() == "python.exe":
                            subprocess.run(['taskkill','/PID',str(parent_parent_proc.pid),'/T','/F'],capture_output=True,text=True,check=True)
                            print("killed parent parent : ",parent_parent_proc.pid)
                        # if parent_parent_proc:
                        #     subprocess.run(['taskkill','/PID',str(parent_parent_proc.pid),'/T','/F'],capture_output=True,text=True,check=True)
                        #     print("killed parent : ",parent_parent_proc.pid)
                    # proc.kill()
                    # print("Killed process with PIC : ",proc.pid) 
                    # print("Killed process with PIC : {proc.pid} ")  
                except psutil.NoSuchProcess:
                    pass
    print("processes stopped")

    # current_pid = os.getpid()
    # print ("current pid : ",current_pid)
    # for proc in psutil.process_iter(attrs=["pid","name","cmdline"]):
    #     if proc.info['pid'] != current_pid:
    #         # if "python.exe" in proc.info['name'].lower() or "Flask" in ' '.join(proc.info['cmdline']).lower():
    #         if "python.exe" in proc.info['name'].lower() or "Flask" in ' '.join(str(arg) for arg in proc.info['cmdline']).lower():
    #             print(f"Killing process : {proc.info['cmdline']}")
    #             try:
    #                 parent_proc = proc.parent()
    #                 if parent_proc:
    #                     if "cmd.exe" in parent_proc.info['name'].lower() or "powershell.exe" in parent_proc.info['name'].lower():
    #                         parent_proc.kill()
    #                         print(f"Killed parent process : {parent_proc.info['cmdline']}")
    #                 proc.kill()
    #                 print(f"Killed process with pid : {proc.pid}")
    #             except (psutil.NoSuchProcess,psutil.AccessDenied):
    #                 pass
    # print("processed stopped")

def stop_flask(appName):
    for proc in psutil.process_iter(attrs=["pid","name"]):
        if proc.info['name'] == f"{appName}":
            try:
                proc.kill()
                print("killed flask application : ",proc.pid)
            except psutil.NoSuchProcess:
                pass
        subprocess.run('exit',shell=True)
def delete_dir(dest_folder):
    
    if not os.path.exists(dest_folder):
        print("Error : Dir '"+dest_folder+"' is not exists")
    
    for entry in os.listdir(dest_folder):
        full_path = os.path.join(dest_folder,entry)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)

def copy_folder(src_folder,dest_folder,app_script,checkout_folder):
    #copy content of the source folder to dest folder

    delete_dir(dest_folder)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    with zipfile.ZipFile(checkout_folder,'r') as zip_ref:
        zip_ref.extractall(dest_folder)


    print("data copied to ",dest_folder)
    delete_dir(src_folder)

    #restart he flask application

    print ("running application command path : ",app_script)
    open_new_terminal_window(app_script)

def open_new_terminal_window(command_path):

    command = f"start cmd.exe /K \"cd {command_path} && python flas.py\""
    print(command)
    subprocess.Popen(command,shell=True)
    time.sleep(2)

def main():
    #main function block

    src_folder = "C://Users//projadmin//Downloads//Git_Deploy_POC//localRepo"
    dest_folder = "C://Users//projadmin//Downloads//Git_Deploy_POC//transferDir"
    app_script = dest_folder+"//flas.py"

    copy_folder(src_folder,dest_folder,app_script)

if __name__ == "__main__":
    main()