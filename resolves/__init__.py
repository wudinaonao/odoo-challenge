"""
Author: wudinaonao
Date: 2022-06-25 14:22:10
LastEditors: wudinaonao
LastEditTime: 2022-06-25 19:02:18
Description: 




"""


def __scan_module():
    """扫描包里的模块
    装载到 __modules_class__ 变量, 格式如下

        {
            "name": "class",
            ....
        }
        
    """
    global __modules_class__
    import importlib
    import os
    _module_names = os.listdir(__name__.replace(".", "/"))
    __modules_class__ = {}
    for _module_name in _module_names:
        if not (_module_name.startswith("_")):
            _module_path = f"{__name__}.{_module_name[:_module_name.index('.')]}"
            _module_class = importlib.import_module(_module_path)
            if not hasattr(_module_class, "Resolve"):
                raise NotImplementedError("解析器模块里必须存在一个名为 Resolve 并且实现了 IResolve 接口的类")
            __modules_class__.setdefault(_module_name.replace(".py", ""), _module_class)

__scan_module()
