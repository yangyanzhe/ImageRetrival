程序可在ubuntu 12.04 LTS 上运行，编译

程序运行需要：
**注意：由于数据过大，我们没有附带image数据文件夹，需要手动添加至imageRetrieval文件夹中（和源代码同级）
python2.7（其他版本应当也可以）
安装至少一个浏览器
可能：必要的opencv运行库，openCL 运行库
openCL运行库可通过synaptic包管理器安装nvidia-opencl-dev及其依赖包

/////////////////////////////
程序运行方式：
在imageRetrieval下提供了可执行文件imageRetrieval，可以通过./imageRetrieval运行，运行后输入待查图片路径，程序会自动打开浏览器显示查询结果，也可以手动打开test.html显示查询结果。

程序运行需要以下数据：
ann.net，存放训练完成的神经网络。
image文件夹，存放数据图片。
dataForSorting，存放数据图片的(H,S,V)=(8,8,0)特征信息。
以上数据我们都已事先提供。

////////////////////////////////
编译程序需要：
python, python-dev
opencv, opencv-dev
fann2.2
fann2.2在ubuntu12.04的软件库中没有，可能需要从源代码编译
我们的程序中使用了opencv的non-free模块，这在ubuntu的包管理器中没有，可能需要从源代码编译安装opencv库。如果遇到cannot open shared object file 错误，可按照http://stackoverflow.com/questions/12335848/opencv-program-compile-error-libopencv-core-so-2-4-cannot-open-shared-object-f中的步骤处理。
fann的安装可参照http://leenissen.dk/fann/wp/help/installing-fann，需要使用cmake。
其余库在ubuntu下可通过ubuntu包管理器下载，也可手动编译（如果包管理器没有对应版本或模块）。编译时需要将Python.h，libpythonxy.so加入程序编译，链接的附加文件。opencv可参照http://docs.opencv.org/doc/tutorials/introduction/linux_install/linux_install.html进行配置。fann需要设置include path，并链接libfann.so。

//////////////////////////////////
我们还提供了以下文件：
imageRetrieval/testData，存储我们使用不同特征训练神经网络的测试结果。
imageRetrieval/python，存放用于数据处理，数据分析及进行人工神经网络初步测试的python代码。
imageRetrieval/sortedimagelist, 由数据集的imagelist排序而成，testData中的以NewOrder为文件名后缀的数据是基于这个顺序
