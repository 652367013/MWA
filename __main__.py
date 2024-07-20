#路径可能有问题


from typing import Tuple

# python -m pip install maafw
from maa.define import RectType
from maa.resource import Resource           # 加载资源路径，也就是MWA的resource/base，
                                            # 主要资源有image，model，pipeline
from maa.controller import AdbController    # 连接adb需要使用的包
from maa.instance import Instance           # 运行maafw里的操作需要用到的库
from maa.toolkit import Toolkit             # 工具包,主要用于一些前期的准备，比如启用当前目录下的工具包选项配置
from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import asyncio                              # 协程,产生异步任务
import os                                   #调用同一目录下其他的py文件


async def main():
    user_path = "./"
    Toolkit.init_option(user_path)
    print(Toolkit.init_option)
    #注册用户路径

    resource = Resource()
    #实例化
    await resource.load("./resource/base")
    # 等待资源加载完毕
    device_list = await Toolkit.adb_devices()
    #如果找不到adb就退出，toolkit.adb_devices()可以返回一个adb列表，要记得异步加载，否则会出错
    #print(device_list,type(device_list))
    #[AdbDevice(name='MuMuPlayer12',
    # adb_path=WindowsPath('D:/game/MuMuPlayer-12.0/shell/adb.exe'),
    # address='127.0.0.1:16384',
    # controller_type=16645886,
    # config='{"extras":{"mumu":{"enable":true,"index":0,"path":"D:/game/MuMuPlayer-12.0"}}}')]
    # <class 'list'>

    if not device_list:
        print("No ADB device found.")
        exit()

    # for demo, we just use the first device
    device = device_list[0]
    print(device,type(device))
    # AdbDevice(name='MuMuPlayer12', adb_path=WindowsPath('D:/game/MuMuPlayer-12.0/shell/adb.exe'),
    #           address='127.0.0.1:16384', controller_type=16645886,
    #           config='{"extras":{"mumu":{"enable":true,"index":0,"path":"D:/game/MuMuPlayer-12.0"}}}')
    #<class 'maa.toolkit.AdbDevice'>

    # 目前默认使用device_list第1个adb，如需要指定adb路径可将device.adb_path和device.address修改为指定字符串，
    # 需要注意的是adb路径不允许有中文
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
    )
    await controller.connect()
    # 最后等待加载connect连接完成
    maa_inst = Instance()
    # 实例化Instance类
    maa_inst.bind(resource, controller)
    # 该方法需要两个参数，一个是resource路径，
    # 一个是controller也就是刚才连接的adb
    print('AdbController:',AdbController,type(AdbController))

    #print('resource路径:',resource,type(resource))
    #resource: < maa.resource.Resourceobjectat0x000002D1323CE990 >
    # type(resource):<class 'maa.resource.Resource'>
    #print('controller:', controller,type(controller))
    #<maa.controller.AdbController object at 0x000002D1323CF3D0>
    #<class 'maa.controller.AdbController'>

    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()
    # 如果资源路径加载不成功添加报错信息

    maa_inst.register_recognizer("MyRec", my_rec)
    maa_inst.register_action("MyAct", my_act)

    #await maa_inst.run_task("StartUp")
    #await maa_inst.run_task("Collect_operators")
    await maa_inst.run_task("kaituozhe",{
    "kaituozhe": {
        "expected": "任务",
        "post_delay": 30000,
    }
})
    #这里是pipeline里面json的任务名

class MyRecognizer(CustomRecognizer):
    def analyze(
        self, context, image, task_name, custom_param
    ) -> Tuple[bool, RectType, str]:
        # maafw定义的方法
        return True, (0, 0, 100, 100), "Hello World!"


class MyAction(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        context.click(200, 200)  # 运行点击坐标200,200
        return True

    def stop(self) -> None:
        pass


my_rec = MyRecognizer()
my_act = MyAction()


if __name__ == "__main__":
    #os.system('python startmumu.py')
    asyncio.run(main())