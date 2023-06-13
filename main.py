import datasource
import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image,ImageTk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        main_frame = tk.Frame(self)
        main_frame.pack()

        # 放置LOGO
        logoImage = Image.open('image/output.png')
        resizeImage = logoImage.resize((500, 100), Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(main_frame, image=self.logoTkimage)
        logoLabel.pack()

        # 站點選單
        top_frame = tk.Frame(main_frame)
        top_frame.pack()
        comboBoxFrame = ttk.LabelFrame(top_frame, text='出發站點')
        comboBoxFrame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.startStationComboBoxValues = ('請選擇站點',
                            '南港', '台北', '板橋', '桃園', '新竹', '苗栗', '台中', '彰化', '雲林', '嘉義', '台南', '左營')
        self.startStationComboBox = ttk.Combobox(
            comboBoxFrame, state='readonly', width=9)
        self.startStationComboBox.pack()
        self.startStationComboBox['values'] = self.startStationComboBoxValues
        self.startStationComboBox.current(0)

        comboBoxFrame2 = ttk.LabelFrame(top_frame, text='到達站點')
        comboBoxFrame2.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.endStationComboBoxValues = ('請選擇站點',
                            '南港', '台北', '板橋', '桃園', '新竹', '苗栗', '台中', '彰化', '雲林', '嘉義', '台南', '左營')
        self.endStationComboBox = ttk.Combobox(
            comboBoxFrame2, state='readonly', width=9)
        self.endStationComboBox.pack()
        self.endStationComboBox['values'] = self.endStationComboBoxValues
        self.endStationComboBox.current(0)

        # 日期輸入框
        dateBoxFrame = ttk.LabelFrame(top_frame,text='日期(YYYY-MM-DD)')
        dateBoxFrame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=10)
        self.entry = ttk.Entry(dateBoxFrame,width=15)
        self.entry.pack()

        # 新增查詢按鈕
        queryButton = ttk.Button(
            top_frame, text='查詢', command=self.queryButtonClicked)
        queryButton.pack(pady=25)

        # 創建 ttk.Treeview 的 LabelFrame
        self.treeViewFrame = ttk.LabelFrame(main_frame, text='高鐵時刻表')
        self.treeViewFrame.pack(fill=tk.BOTH,
                        padx=10, pady=5, expand=True)

        # 創建 ttk.Treeview
        columns = ('#1','#2','#3','#4','#5','#6')
        self.treeView = ttk.Treeview(
            self.treeViewFrame, columns=columns, show='headings')
        self.treeView.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.treeView.column('#1', width=100, anchor='center')
        self.treeView.column('#2', width=100, anchor='center')
        self.treeView.column('#3', width=100, anchor='center')
        self.treeView.column('#4', width=100, anchor='center')
        self.treeView.column('#5', width=130, anchor='center')
        self.treeView.column('#6', width=100, anchor='center')

        # 設置 ttk.Treeview 的欄位
        self.treeView.heading('#1', text='出發站點')
        self.treeView.heading('#2', text='出發時間')
        self.treeView.heading('#3', text='到達站點')
        self.treeView.heading('#4', text='到達時間')
        self.treeView.heading('#5', text='行駛時間(時:分)')
        self.treeView.heading('#6', text='車次')

        # treeview的scrollbar
        scrollbar = ttk.Scrollbar(self.treeViewFrame,command=self.treeView.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeView.config(yscrollcommand=scrollbar.set)

        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(padx=15,pady=10,fill='x')

        # 票價欄位
        label1 = ttk.Label(bottom_frame,text='車廂票價參考',font=("微軟正黑體",20))
        label1.pack()
        label2 = ttk.Label(bottom_frame,text='\n\n標準車廂\n\n商務車廂\n\n自由座車廂',font=("微軟正黑體",15))
        label2.pack(side='left',padx=30)
        self.label3 = ttk.Label(bottom_frame,font=("微軟正黑體",15),justify='center')
        self.label3.pack(side='left')
        self.label4 = ttk.Label(bottom_frame,font=("微軟正黑體",15),justify='center')
        self.label4.pack(side='left',padx=30)
        self.label5 = ttk.Label(bottom_frame,font=("微軟正黑體",15),justify='center')
        self.label5.pack(side='left',anchor='n')

    # 查詢按鈕點擊事件
    def queryButtonClicked(self):
        # 先取得使用者選擇的出發站點和到達站點
        start = self.startStationComboBox.get()
        end = self.endStationComboBox.get()
        date = self.entry.get()

        if start != '請選擇站點' and end != '請選擇站點' and date != '':
            for item in self.treeView.get_children():
                self.treeView.delete(item)
            for item in datasource.getInfo(start,end,date):
                travel_time = datetime.datetime.strptime(item['DestinationStopTime']['ArrivalTime'],'%H:%M') - datetime.datetime.strptime(item['OriginStopTime']['DepartureTime'],'%H:%M')
                self.treeView.insert('',tk.END,values=[item['OriginStopTime']['StationName']['Zh_tw'],item['OriginStopTime']['DepartureTime'],item['DestinationStopTime']['StationName']['Zh_tw'],item['DestinationStopTime']['ArrivalTime'],str(travel_time)[:-3],item['DailyTrainInfo']['TrainNo']])

            words1 = f'全票\n\n${datasource.priceInfo(start,end)[0]}\n\n${datasource.priceInfo(start,end)[1]}\n\n${datasource.priceInfo(start,end)[2]}'
            self.label3.configure(text=words1)
            words2 = f'孩童票/敬老票/愛心票\n\n${datasource.priceInfo(start,end)[3]}\n\n${datasource.priceInfo(start,end)[4]}\n\n${datasource.priceInfo(start,end)[5]}'
            self.label4.configure(text=words2)
            words3 = f'團體票\n\n${datasource.priceInfo(start,end)[6]}\n\n${datasource.priceInfo(start,end)[7]}'
            self.label5.configure(text=words3)

def main():
    window = Window()
    window.title('高鐵時刻表')
    window.mainloop()

if __name__ == '__main__':
    main()