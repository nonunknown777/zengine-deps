



import os
import shutil
import subprocess
import multiprocessing

path_main = os.path.dirname(os.path.abspath(__file__))

path_jolt =     f'{path_main}/JoltPhysics'
path_rho =      f'{path_main}/PlayRho'
path_yaml =     f'{path_main}/yaml-cpp'
path_raylib =   f'{path_main}/raylib'
path_rres =     f'{path_main}/rres'
path_raudio =   f'{path_main}/raudio'


output_folder_name = "place_inside_zengine"

path_output = f"{path_main}/{output_folder_name}"
path_output_libs = f"{path_output}/libs"

num_processors = multiprocessing.cpu_count()

def run_command(command):
    try:
        # Run the command, capture output and errors
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # If the command was successful
        print("Command executed successfully.")
        print("Output:")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        # If the command failed
        print("Error executing the command.")
        print("Error message:")
        print(e.stderr)
        return False

def copy_header_files(source_folder, destination_folder):
    try:
        # Ensure the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Walk through the source folder
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                # Check if the file has a .h or .hpp extension
                if file.endswith(('.h', '.hpp')):
                    source_path = os.path.join(root, file)
                    
                    # Create the corresponding folder structure in the destination folder
                    relative_path = os.path.relpath(source_path, source_folder)
                    destination_path = os.path.join(destination_folder, relative_path)

                    # Ensure the destination folder for the current file exists
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                    # Copy the file to the destination folder
                    shutil.copy2(source_path, destination_path)

                    # Uncomment the next line if you want to print each file copy operation
                    # print(f"Copied: {source_path} to {destination_path}")

        print("Header files copied successfully.")
        return True

    except Exception as e:
        print(f"Error copying header files: {e}")
        return False

def remove_folder(folder_path):
    try:
        # Use shutil.rmtree to remove the folder and its contents recursively
        shutil.rmtree(folder_path)
        
        print(f"Folder '{folder_path}' removed successfully.")
        return True

    except Exception as e:
        if "Errno 2" in str(e): 
            print( "OK")
            return True
        print(f"Error removing folder '{folder_path}': {e}")
        return False

def create_folder(folder_path):
    try:
        # Use os.makedirs with exist_ok=True to create the folder (and its parents) if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully.")
        return True

    except Exception as e:
        # Handle other exceptions, if any
        print(f"Error creating folder '{folder_path}': {e}")
        return False

def run_make(directory="."):
    try:
        # Get the number of available processors
        num_processors = multiprocessing.cpu_count()

        # Run the make command with the -jN option, where N is the number of processors
        make_command = f"make -j{num_processors}"
        
        # Change to the specified directory before running the make command
        os.chdir(directory)

        subprocess.run(make_command, shell=True, check=True)
        print(f"Make command '{make_command}' executed successfully in directory '{directory}'.")
        return True

    except subprocess.CalledProcessError as e:
        # If the make command failed
        print(f"Error executing make command in directory '{directory}': {e.stderr}")
        return False

def move_file(file_path, destination_folder, new_file_name=None):
    try:
        # Create the destination folder and any necessary intermediate folders if they don't exist
        os.makedirs(destination_folder, exist_ok=True)

        # If a new file name is provided, use it; otherwise, keep the original file name
        if new_file_name:
            destination_path = os.path.join(destination_folder, new_file_name)
        else:
            destination_path = os.path.join(destination_folder, os.path.basename(file_path))

        # Use shutil.move to move the file to the destination folder
        shutil.move(file_path, destination_path)

        print(f"File moved successfully to '{destination_path}'.")
        return True

    except Exception as e:
        print(f"Error moving file: {e}")
        return False

#specific for playRho
def run_cmake_build(path,type):
    try:
        print("running cmake at: ", path)


        # Construct the cmake build command
        cmake_build_command = f"cd {path_main} && cmake --build PlayRhoBuild --config {type} -j{num_processors} --clean-first"

        # Run the cmake build command
        subprocess.run(cmake_build_command, shell=True, check=True)
        
        print("CMake build completed successfully.")
        return True

    except subprocess.CalledProcessError as e:
        # If the cmake build command failed
        print(f"Error running CMake build command: {e.stderr}")
        return False


## BEGIN
# print("removing output folder!")
# if (remove_folder(path_output)):
#     print("Done...")


if not create_folder(path_output): exit(-1)
if not create_folder(path_output_libs): exit(-1)


print("Starting jolt physics build:")

folder_debug = f"{path_jolt}/build_debug"
folder_release = f"{path_jolt}/build_release"

print("Debug build...")

if not create_folder(folder_debug): exit(-1)
if not run_command(f"cd {folder_debug} && cmake -DCMAKE_BUILD_TYPE=Debug ../Build"): exit(-1)
if not run_make(folder_debug): exit(-1)
if not move_file(f"{folder_debug}/libJolt.a",f"{path_output_libs}", "libJoltDebug.a"): exit(-1)

print("Release Build...")

if not create_folder(folder_release): exit(-1)
if not run_command(f"cd {folder_release} && cmake -DCMAKE_BUILD_TYPE=Release ../Build"): exit(-1)
if not run_make(folder_release): exit(-1)
if not move_file(f"{folder_release}/libJolt.a",f"{path_output_libs}", "libJoltRelease.a"): exit(-1)

print("moving necessary files")

path_output_header_jolt = f"{path_output}/includes/jolt"
if not create_folder(path_output_header_jolt): exit(-1)
if not copy_header_files(f"{path_jolt}/Jolt",path_output_header_jolt): exit(-1)


# PlayRho

print("Starting PlayRho Build...")

path_headers_rho = f"{path_rho}/Library/include/"
path_headers_output_rho = f"{path_output}/includes/"
path_lib_rho = f"{path_main}/PlayRhoBuild/Library/libPlayRho.a"


print("Building PlayRho debug...")

if not run_command(f"cd {path_main} && cmake -S PlayRho -B PlayRhoBuild"): exit(-1)
if not run_cmake_build(path_main, "Debug"): exit(-1)
if not move_file(path_lib_rho,f"{path_output_libs}", "libPlayRhoDebug.a"): exit(-1)

print("Building PlayRho debug...")
if not remove_folder(f"{path_main}/PlayRhoBuild"): exit(-1)
if not run_command(f"cd {path_main} && cmake -S PlayRho -B PlayRhoBuild"): exit(-1)
if not run_cmake_build(path_main, "Release"): exit(-1)
if not move_file(path_lib_rho,f"{path_output_libs}", "libPlayRhoRelease.a"): exit(-1)

print("moving necessary files")
if not create_folder(path_headers_output_rho): exit(-1)
if not copy_header_files(path_headers_rho,path_headers_output_rho): exit(-1)



# Raylib

print("Starting Raylib build...")

path_header_raylib = f"{path_raylib}/src/"
path_output_headers_raylib = f"{path_output}/includes/raylib"
path_build_debug_raylib = f"{path_raylib}/build_debug"
path_build_release_raylib = f"{path_raylib}/build_release"
path_lib_raylib_debug = f"{path_build_debug_raylib}/raylib/libraylib.a"
path_lib_raylib_release = f"{path_build_release_raylib}/raylib/libraylib.a"

print("Raylib Debug: ")
if not create_folder(path_build_debug_raylib): exit(-1)
if not run_command(f"cd {path_raylib} && make clean && cmake -DCMAKE_BUILD_TYPE=Debug -B {path_build_debug_raylib}"): exit(-1)
if not run_command(f"cd {path_build_debug_raylib} && make clean && make -j{num_processors}"): exit(-1)
if not move_file(path_lib_raylib_debug,path_output_libs,"libraylibDebug.a"): exit(-1)


print("Raylib Release: ")
if not create_folder(path_build_release_raylib): exit(-1)
if not run_command(f"cd {path_raylib} && make clean && cmake -DCMAKE_BUILD_TYPE=Release -B {path_build_release_raylib}"): exit(-1)
if not run_command(f"cd {path_build_release_raylib} && make clean && make -j{num_processors}"): exit(-1)
if not move_file(path_lib_raylib_release,path_output_libs,"libraylibRelease.a"): exit(-1)

print("moving necessary files")
if not create_folder(path_output_headers_raylib): exit(-1)
if not copy_header_files(path_header_raylib,path_output_headers_raylib): exit(-1)

# YAML cpp

print("starting YAML Cpp build...")


path_header_yaml = f"{path_yaml}/include/"
path_output_headers_yaml = f"{path_output}/includes/"
path_build_debug_yaml = f"{path_yaml}/build_debug"
path_build_release_yaml = f"{path_yaml}/build_release"
path_lib_yaml_debug = f"{path_build_debug_yaml}/libyaml-cppd.a"
path_lib_yaml_release = f"{path_build_release_yaml}/libyaml-cpp.a"

print("yaml Debug: ")
if not create_folder(path_build_debug_yaml): exit(-1)
if not run_command(f"cd {path_yaml} && make clean && cmake -DCMAKE_BUILD_TYPE=Debug -B {path_build_debug_yaml}"): exit(-1)
if not run_command(f"cd {path_build_debug_yaml} && make clean && make -j{num_processors}"): exit(-1)
if not move_file(path_lib_yaml_debug,path_output_libs,"libyamlDebug.a"): exit(-1)

print("yaml release: ")
if not create_folder(path_build_release_yaml): exit(-1)
if not run_command(f"cd {path_yaml} && make clean && cmake -DCMAKE_BUILD_TYPE=Release -B {path_build_release_yaml}"): exit(-1)
if not run_command(f"cd {path_build_release_yaml} && make clean && make -j{num_processors}"): exit(-1)
if not move_file(path_lib_yaml_release,path_output_libs,"libyamlRelease.a"): exit(-1)

print("moving necessary files")
if not create_folder(path_output_headers_yaml): exit(-1)
if not copy_header_files(path_header_yaml,path_output_headers_yaml): exit(-1)


print("Starting RRes header moving")
path_res_headers = f"{path_rres}/src/"
path_res_output = f"{path_output}/includes/rres"
if not create_folder(path_res_output): exit(-1)
if not copy_header_files(path_res_headers,path_res_output): exit(-1)

print("Starting RAudio header moving")
path_audio_headers = f"{path_raudio}/src/"
path_audio_output = f"{path_output}/includes/raudio"
if not create_folder(path_audio_output): exit(-1)
if not copy_header_files(path_audio_headers,path_audio_output): exit(-1)