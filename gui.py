from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
import tkinter as tk
from shutil import copy
"""
待改进：
1.加载图片不能加载bmp格式，(已经可以加载了)
2.图片不能缩放
3.使用txt进行传值(已经可以正常传值了，封装成类就行了)
"""

"""
增加功能：
1.读取文件路径 （已经解决）
    a.深度学习处理图
    b.最终输出结果图
    c.原图路径
    d.保存路径
2.同步刷新两个看图Frame（已经解决）

3.鼠标点击左侧目录栏，可定位该图片

4.最主要的功能：
    图片分类：
        少点图文件夹中：1.少正极点 2.少负极点
        错点文件夹中：1.正极错判成负极 2.负极错判成正极
        飞点文件夹中：

5.传值的时候如何更新值（已经解决）

6.增加图片总数及当前图片序号，显示图片的信息（平板号，夹具角度，）

7.按照列表加载图片还是有可能会出现错误 改进一下这种方法

"""

class myDialog(tk.Toplevel):
    def __init__(self):
        super(myDialog, self).__init__()
        # Toplevel.title('设置图片信息')
        self.inputPicPath()
        pass

    def inputPicPath(self):
        print("输入图片路径")
        # global top_level
        # top_level = Toplevel()
        frame=Frame(self, width=300, height=150)
        frame.pack()

        Label(frame,text="请输入图片路径:").grid(row=0)
        Label(frame, text="请输入存储路径:").grid(row=1)

        global entry_text1,entry_text2
        entry_text1 = StringVar()
        entry_text2=StringVar()
        entry1=Entry(frame,textvariable=entry_text1)
        entry2 = Entry(frame, textvariable=entry_text2)

        entry1.grid(row=0, column=1, padx=10, pady=5)
        entry2.grid(row=1, column=1, padx=10, pady=5)

        #command里面的方法不要加上（），否则会报奇奇怪怪的错误
        button1=Button(frame,text="路径选择", width=10, height=1,command=self.openFile)
        button2 = Button(frame, text="路径选择", width=10, height=1,command=self.saveFile)
        button3 = Button(frame, text="确定", width=10, height=1,command=self.ok)
        button4=Button(frame, text="取消", width=10, height=1,command=self.cancel)

        button1.grid(row=0, column=2, padx=5, pady=5)
        button2.grid(row=1, column=2, padx=5, pady=5)
        button3.grid(row=2,column=1,padx=5,pady=5)
        button4.grid(row=2,column=2,padx=5,pady=5)

    def openFile(self):
        directory1 = askdirectory(initialdir="/")
        print(directory1)
        entry_text1.set(directory1)
        return directory1

    def saveFile(self):
        directory2 = askdirectory(initialdir="/")
        print(directory2)
        entry_text2.set(directory2)
        return directory2

    def ok(self):
        self.userinfo = [entry_text1.get(),entry_text2.get()]
        self.destroy()
        # myGUI=GUI()
        # myGUI.filename_list=os.listdir(self.userinfo[0])
        return self.userinfo

    def cancel(self):
        self.userinfo=None
        self.destroy()

class GUI():
    current=0
    # file_path=[]

    def __init__(self):
        #初始化图片路径
        self.file_path=r"E:\choose_image-master\initPic"
        self.save_path=r"E:\choose_image-master\initPic"
        self.filename_list = os.listdir(self.file_path)
        self.resultPic=os.listdir(self.file_path)
        self.setUI()

    def choose(self,path):
        picList=[]

        originalPic=[]
        resultPic=[]
        for filename in os.listdir(path):
            if filename.endswith((".jpg",".png",".bmp")):
                picList.append(filename)
        #区分深度学习结果图 以及 原图
        for name in picList:
            if name.split(".")[-1]=="bmp" and name.split("_")[3]!="DL":
                originalPic.append(name)
            elif name.split(".")[-1]=="bmp" and name.split("_")[3]=="DL":
                resultPic.append(name)
        #返回结果图和原图不一致情况
        if len(originalPic)!=len(resultPic):
            print("结果图和原图没有对应上")
        # print(originalPic)
        # print("******")
        # print(resultPic)
        return originalPic,resultPic

    def setup_config(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        print(res)
        if res is None:
            return
        # 更改参数

        self.file_path, self.save_path = res[:2]
        #筛选出jpg,png,bmp图片格式的图片
        self.filename_list,self.resultPic=self.choose(self.file_path)
        #更新左边目录列表
        content.set(self.filename_list)

        #更新左右两张图片 分别是深度学习结果图 还有原图
        self.current=0
        global photo_update_L,photo_update_R
        image_update_L=Image.open(os.path.join(self.file_path, self.filename_list[self.current])).resize((500,500))
        photo_update_L = ImageTk.PhotoImage(image_update_L)
        rightLabel1.config(image=photo_update_L)

        image_update_R = Image.open(os.path.join(self.file_path, self.resultPic[self.current])).resize((500, 500))
        photo_update_R = ImageTk.PhotoImage(image_update_R)
        rightLabel2.config(image=photo_update_R)


    def ask_userinfo(self):
        inputDialog = myDialog()
        Toplevel.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog.userinfo

    def setUI(self):
        root = Tk()
        #设置顶级菜单
        menubar = Menu(root, tearoff=False)
        #文件顶级菜单
        filemenu =Menu(menubar, tearoff=False)
        filemenu.add_command(label="打开", command=self.setup_config)
        #分界线
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)

        #帮助顶级菜单
        helpmenu = Menu(menubar, tearoff=False)
        helpmenu.add_command(label="快捷键", command=self.callback)
        helpmenu.add_command(label="使用说明", command=self.callback)
        menubar.add_cascade(label="帮助", menu=helpmenu)

        root.config(menu=menubar)

        # filename_list = os.listdir(self.file_path)
        # print("打印当前目录的文件"+str(filename_list))
        # 设置分割线样式为sunken
        panedWindow = PanedWindow(orient=HORIZONTAL,sashrelief='sunken')
        panedWindow.pack(fill=BOTH, expand=True)

        #左显示界面 上界面是显示目录列表 下界面是按钮功能界面
        leftFrame = Frame(panedWindow, width=100, height=250)

        #左上界面：文件目录名列表
        leftFrame1=Frame(leftFrame, width=100, height=150,relief='sunken',borderwidth=1)
        leftFrame1.pack()
        #给左上界面增加滚动条
        scrollbar = Scrollbar(leftFrame1)
        scrollbar.pack(side=RIGHT, fill=Y)
        #给左上边框架添加一个Listbox控件
        global content
        content=tk.StringVar()
        left_list = Listbox(leftFrame1, width=30, height=30,listvariable=content,yscrollcommand=scrollbar.set)

        # print("打印filename_list:"+str(self.filename_list))
        for filename in self.filename_list:
            left_list.insert(END, filename)
        left_list.pack()
        #设置滑动条可随着列表数据移动
        scrollbar.config(command=left_list.yview)

        # 左下界面：按钮功能界面
        leftFrame2 = Frame(leftFrame, width=230, height=100, relief='sunken', borderwidth=1)
        leftFrame2.pack()

        # 增加按钮
        def lastPic():
            print("点击了上一张")
            # 防止数组越界
            if self.current == 0:
                self.current = len(self.filename_list)
            self.current -= 1
            print("当前所在列表位置："+str(self.current))
            image_last_L = Image.open(os.path.join(self.file_path, self.filename_list[self.current])).resize((500, 500))
            image_last_R = Image.open(os.path.join(self.file_path, self.resultPic[self.current])).resize((500, 500))
            # 定义为global全局变量 防止垃圾回收机制会把变量photo_next给回收了
            global photo_last_L,photo_last_R
            photo_last_L = ImageTk.PhotoImage(image_last_L)
            photo_last_R = ImageTk.PhotoImage(image_last_R)
            rightLabel1.configure(image=photo_last_L)
            rightLabel2.configure(image=photo_last_R)


        button1 = Button(leftFrame2, text="上一张", width=10, height=1, command=lastPic)
        button1.grid(row=0,column=0)

        def nextPic():
            print("点击了下一张")
            self.current += 1
            #防止数组越界
            if self.current == len(self.filename_list):
                self.current = 0
            print("当前所在列表位置："+str(self.current))
            image_next_L = Image.open(os.path.join(self.file_path, self.filename_list[self.current])).resize((500, 500))
            image_next_R = Image.open(os.path.join(self.file_path, self.resultPic[self.current])).resize((500, 500))
            #定义为global全局变量 防止垃圾回收机制会把变量photo_next给回收了
            global photo_next_L,photo_next_R
            photo_next_L = ImageTk.PhotoImage(image_next_L)
            photo_next_R= ImageTk.PhotoImage(image_next_R)
            rightLabel1.configure(image=photo_next_L)
            rightLabel2.configure(image=photo_next_R)

        button2 = Button(leftFrame2, text="下一张", width=10, height=1, command=nextPic)
        button2.grid(row=0,column=1)

        def savePic():
            copy(os.path.join(self.file_path, self.filename_list[self.current]),self.save_path)
            copy(os.path.join(self.file_path, self.resultPic[self.current]), self.save_path)
            print("保存图片")



        button3 = Button(leftFrame2, text="保存图片", width=10, height=1,command=savePic)
        button3.grid(row=0,column=2)


        #创建新的分类
        def makeNewCls():
            print("创建新的分类")

            pass
        label_Cls1=Label(leftFrame2, text="类名:")
        label_Cls1.grid(row=1,column=0)
        global entry_Cls1
        entry_Cls1 = StringVar()
        entry1 = Entry(leftFrame2,width=10,textvariable=entry_Cls1)
        entry1.grid(row=1,column=1)

        button4 = Button(leftFrame2, text="创建分类", width=10, height=1, command=makeNewCls)
        button4.grid(row=1,column=2)

        panedWindow.add(leftFrame)

        #右显示界面 设置两个图片显示画面 一个是深度学习处理图，一个是最终结果图
        rightFrame = Frame(panedWindow,width=900, height=650)

        #filename_list：['7_3_4_-31.55_3_00CA83088213_1.jpg', '7_3_5_DL_3_00CA83088213_1.jpg', '图标.png', '示例图片.png']

        #定义初始化图像界面
        image = Image.open(os.path.join(self.file_path,self.filename_list[self.current])).resize((500, 500))

        photo = ImageTk.PhotoImage(image)

        global rightLabel1,rightLabel2

        rightLabel1 = Label(rightFrame,image=photo,width=450,height=650,relief='sunken',borderwidth=1)
        rightLabel1.pack(side='left')

        rightLabel2 = Label(rightFrame,image=photo,width=450,height=650,relief='sunken',borderwidth=1)
        rightLabel2.pack(side='left')

        panedWindow.add(rightFrame)

        panedWindow.mainloop()
    """
    输入图片路径后，比如错点路径，然后将该路径下的文件分为四类，分别对应四个平板
    """



    def callback(self):
        print("调用了")

    # 设置参数
    # def setup_config(self):
    #     # 接收弹窗的数据
    #     res = self.ask_userinfo()
    #     # print(res)
    #     if res is None:
    #         return
    #     # 更改参数
    #     self.name, self.age = res
    #     # 更新界面
    #     self.l1.config(text=self.name)
    #     self.l2.config(text=self.age)
    #
    #     # 弹窗
    #
    # def ask_userinfo(self):
    #     inputDialog = MyDialog()
    #     self.wait_window(inputDialog)  # 这一句很重要！！！
    #     return inputDialog.userinfo


if __name__ == '__main__':
    import os
    # file_path=r"E:\choose_image-master\pics"
    GUI()