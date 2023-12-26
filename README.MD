# ZEngine - Dependency Builder

Welcome to the ZEngine Builder repository! ZEngine is a custom game engine built on top of the fantastic Raylib framework. This readme will guide you through setting up the project with its submodule dependencies.

For ZEngine repository [CLICK HERE](https://github.com/nonunknown777/ZEngine)

## Submodules Dependencies

1.  **Raylib - Base Game Framework**
    [Website](https://www.raylib.com/)
2.  **YAML-CPP - YAML Parser**
    [GitHub Repository](https://github.com/jbeder/yaml-cpp)
3.  **PlayRho - 2D Physics**
    [GitHub Repository](https://github.com/louis-langholtz/PlayRho)
4.  **Jolt - 3D Physics**
    [GitHub Repository](https://github.com/jrouwe/JoltPhysics)
5.  **RRes - Pack Files into Binary Form**
    [GitHub Repository](https://github.com/raysan5/rres)
6.  **RAudio - Raysan's Audio for Raylib**
    [GitHub Repository](https://github.com/raysan5/raudio)

## Requirements

- python 3.x
- cmake 3.x
- (you can try to build after installing above, but some libraries may require any extra stuff, if any error check the Repository of the target library building in your os)

## Getting Started

You just need to do if either **Your OS isnt listed in the releases of the ZEngine repo** or **You want to contribute to the engine development**

Follow these steps to clone the builder repository with its submodules:


```
 git clone --recursive git@github.com:nonunknown777/zengine-deps.git

 cd zengine-deps/

 git submodule update --init --recursive

 #execute the python script

 python ./build.py
```


## After build

- a folder called `place_inside_zengine` will be generated
- copy all the content of this folder inside zengine folder
- if you have any problems during the execution of the script make sure you meet the requirements of the library that has thrown the error



Now you have the ZEngine repository with all its dependencies ready to go!
Feel free to explore, modify, and have fun building awesome games with ZEngine. If you encounter any issues or have suggestions, don't hesitate to reach out.

Happy coding! 🚀

## Disclaimer

The `build.py` was done in one day only, so its not very code organized is just to make the process easier to update / get code running