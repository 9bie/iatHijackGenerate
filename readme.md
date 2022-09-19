# what's this

快速生成用于白加黑劫持的DLL，劫持类型为导入表劫持，不需要考虑原始程序代码流程等。支持大部分程序。

# 使用方法

使用的前提，程序必须是导入表导入的，不能是loadlibrary的，loadlibrary的不能用这个脚本，可以用其他方法处理。

直接把EXE从安装文件夹复制出来，然后双击运行，假设会出现如下报错（找不到DLL的），就说明是可以劫持的
![1.jpg][1]
![2.jpg][2]
弹窗越少越好，但是不能没有，1个最好，如果有多个就得多次生成文件，我这边这个程序弹了两个。

记录下这些缺少的DLL，依次执行命令
```
python iat_dll_hijack.py 目标.exe libcef.dll a1.c
python iat_dll_hijack.py 目标.exe encrashrep.dll a2.c
```
然后修改最后一次报错dll输出的代码，修改DLLmain里面的shellcode。(重要，不然会影响程序执行流程)
然后执行gcc命令编译
```
gcc a1.c -lShlwapi -lPsapi -shared -o libcef.dll
gcc a2.c -lShlwapi -lPsapi -shared -o encrashrep.dll
```
![3.jpg][3]

然后把生成的dll和目标exe放在一起，双击执行即可上线
![4.jpg][4]

# 缺点

这种类型的导出DLL暂时没办法自动处理
![5.jpg][5]


  [1]: https://9bie.org/usr/uploads/2022/09/2732797578.jpg
  [2]: https://9bie.org/usr/uploads/2022/09/2201903473.jpg
  [3]: https://9bie.org/usr/uploads/2022/09/3584777043.jpg
  [4]: https://9bie.org/usr/uploads/2022/09/980536341.jpg
  [5]: https://9bie.org/usr/uploads/2022/09/4108777365.jpg