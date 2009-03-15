##!/usr/bin/env python
## coding:utf-8 ##
#### 使用Struct,Ctypes库 ####

import struct
import ctypes

nInt = int("0xe3", 16)
str = "good"

# 十六进制数，字符串转换
buffer = struct.pack("!H4sbB", nInt, str, 180,180)
print repr(buffer)
print struct.unpack("!H4sbB", buffer)
print

# 计算转换的结构字节数
print struct.calcsize("!B16B4sHIBH4sBBBHBIBB") #转换网络字节序
print struct.calcsize("=B16B4sHIBH4sBBBHBIBB") #保持原来字节序
print struct.calcsize("B16B4sHIBH4sBBBHBIBB")  #自动对齐数据
print

# ！表示网络字节序
# 使用apply是封装该函数的调用，返回值是struct.pack的返回值
data = [4123456789, 'cd', 3]
fmt = "!I%dsb" % len(data[1])
#buffer = apply(struct.pack, ("!Icb", ) + tuple(data))  //apply使tuple展开为参数
#                                                       //表达式可以用字符串代替
buffer = apply(struct.pack, (fmt, ) + tuple(data)) 
print repr(buffer)
#print struct.unpack("!I2sb", buffer)
print struct.unpack("!I", buffer[:4])
print

# 二进制数据的组合
buf = ctypes.create_string_buffer("hello",10)   #建立char[10]
struct.pack_into("!B2sB", buf, 5, 17, "PY", 19) #从char[5]处写入数据
print ctypes.sizeof(buf), repr(buf.raw)         #显示写入后打包的二进制表示
print struct.unpack_from("!B2sB", buf, 5)       #从char[5]处解包后返回tuple



