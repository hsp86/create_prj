#-*- coding: utf-8 -*-
import wx
import os,sys

class myapp(wx.App):
    def __init__(self):
        wx.App.__init__(self)#必须调用父类的构造函数__init__
    def OnInit(self):#在程序开始的时候就会被自动调用
        self.frame = myframe()
        self.frame.Show()#显示
        self.SetTopWindow(self.frame)
        return True#必须要返回True才会继续执行，返回False则退出程序
    
    
class myframe(wx.Frame):#自建窗口类
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"创建总线模板文件---胡祀鹏设计制作",size = (550,450))

        self.bus_list = []
        # 整个界面大sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 输入框，显示浏览的目录
        self.dir_text = wx.TextCtrl(self,-1,u'请选择目录')
        # 浏览按钮
        self.dir_button = wx.Button(self,-1,u'浏览')
        self.dir_button.Bind(wx.EVT_BUTTON,self.dir_button_click)
        # 工程名和显示信息
        self.prj_text = wx.TextCtrl(self,-1,u'请输入工程名')
        self.prj_text.Bind(wx.EVT_TEXT,self.prj_text_change) # 工程名改变时
        self.text_label = wx.StaticText(self,-1,u'显示信息')

        # 数据操作按钮
        # 下拉选项
        bus_list = ['AXI-lite','AXI-stream','AXI full master','AXI full slave','wishbone slave','wishbone master','wb slave burst','wb master burst']
        self.mychoice = wx.Choice(self,-1,choices = bus_list)
        self.mychoice.Bind(wx.EVT_CHOICE,self.onchoice)
        self.add_button = wx.Button(self,-1,u'添加')
        self.add_button.Bind(wx.EVT_BUTTON,self.add_button_click)
        self.create_button = wx.Button(self,-1,u'生成')
        self.create_button.Bind(wx.EVT_BUTTON,self.create_button_click)

        # 浏览部分sizer
        sizer1 = wx.FlexGridSizer(rows = 1,cols = 2,hgap = 1,vgap = 0)
        sizer1.AddGrowableCol(0,5)
        sizer1.AddGrowableCol(1,1)
        sizer1.Add(self.dir_text,0,wx.EXPAND)
        sizer1.Add(self.dir_button,0,wx.EXPAND)

        # 工程名和显示信息部分sizer
        sizer2 = wx.FlexGridSizer(rows = 1,cols = 2,hgap = 0,vgap = 0)
        sizer2.AddGrowableCol(0,1)
        sizer2.AddGrowableCol(1,2)
        sizer2.Add(self.prj_text,0,wx.EXPAND)
        sizer2.Add(self.text_label,0,wx.EXPAND)

        # 数据操作部分sizer
        sizer3 = wx.FlexGridSizer(rows = 1,cols = 3,hgap = 0,vgap = 0)
        sizer3.AddGrowableCol(0,1)
        sizer3.AddGrowableCol(1,1)
        sizer3.AddGrowableCol(2,1)
        sizer3.Add(self.mychoice,0,wx.EXPAND)
        sizer3.Add(self.add_button,0,wx.EXPAND)
        sizer3.Add(self.create_button,0,wx.EXPAND)

        # 显示添加目录的sizer
        self.add_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加以上sizer
        self.sizer.Add(sizer1,0,wx.EXPAND | wx.ALL,5)
        self.sizer.Add(sizer2,0,wx.EXPAND | wx.ALL,5)
        self.sizer.Add(sizer3,0,wx.EXPAND | wx.ALL,5)
        self.sizer.Add(self.add_sizer,1,wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,5)

        self.SetSizer(self.sizer)

    # 浏览打开一个目录
    def dir_button_click(self,e):
        dir_dlg = wx.DirDialog(None,u'请选择一个目录',style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
            self.dir_text.SetValue(dir_dlg.GetPath())
            self.text_label.SetLabel(u'你选择的目录为'+self.dir_text.GetValue())
        dir_dlg.Destroy()

    def prj_text_change(self,e):
        self.text_label.SetLabel(u'工程会放入目录'+self.dir_text.GetValue()+'/'+self.prj_text.GetValue())

    def onchoice(self,e):
        print u'被选中：',self.mychoice.GetStringSelection()

    def add_button_click(self,e):
        print u'添加',self.mychoice.GetStringSelection()
        sizer1 = wx.FlexGridSizer(rows = 1,cols = 3,hgap = 3,vgap = 3)
        temp_obj = {}
        temp_obj['check'] = wx.CheckBox(self,-1,self.mychoice.GetStringSelection(),name = self.mychoice.GetStringSelection())#通过name保存
        # temp_obj['check'].Bind(wx.EVT_CHECKBOX,self.checkbox_click)
        temp_obj['check'].SetValue(True)
        self.bus_list.append(temp_obj)
        sizer1.Add(temp_obj['check'],0,wx.EXPAND)
        self.add_sizer.Add(sizer1, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Fit(self)

    def create_button_click(self,e):
        fid = open('test.txt')
        all_the_text = fid.read()
        fid.close()
        fid2 = open('test2.txt','w')
        var1 = 10
        var3 = 8
        w_text = all_the_text.decode('utf-8') %(var1,var3)
        print w_text
        # all_the_text = fid2.write(w_text)#这样不行，需要如下编码
        all_the_text = fid2.write(w_text.encode('utf-8'))
        fid2.close()
        print u'生成的总线有：'
        for item in self.bus_list:
            if(item['check'].IsChecked()):
                print item['check'].GetName()+';'+item['check'].GetLabelText()


def wx_run(msg):
    print msg
    wx_app = myapp()
    wx_app.MainLoop()
    print 'wx bay!'

if __name__ == '__main__':
    wx_run('start!')
