import os
import sys
import timeit
from tkinter import *
from tkinter.font import Font
import tkinter.ttk as ttk
import pygame
import requests
from . import Search


class StockTracker:
    def __init__(self, company_symbol=None, show_gui=True):
        if show_gui:
            self.StartTimer = 0
            self.ErrorTimer = None
            self.PreviousSearch = ''
            self.LocalSearchIndex = 0
            self.GlobalSearchIndex = 0
            self.DEFAULTTEXT = 'COMPANY SYMBOL'

            if sys.platform == 'win32':
                self.ErrorAudio = self.ResourcePath('WinErrSound.wav')

            else:
                self.ErrorAudio = self.ResourcePath('LinuxErrSound.wav')

            pygame.mixer.init()
            pygame.mixer.music.load(self.ErrorAudio)

            self.master = Tk()
            self.master.withdraw()
            self.master.title('Nepal Stock Tracker')
            self.master.iconbitmap(self.ResourcePath('icon.ico'))
            self.SEARCH = Search.Search(self.ShowErrorMessage, self.CheckInternet, master=self.master)

            self.OptionValues = self.SEARCH.GetCompaniesNameList()
            self.TitleImage = PhotoImage(file=self.ResourcePath('TitleImage.png'))

            self.TitleLabel = Label(self.master, image=self.TitleImage)
            self.TitleLabel.pack()

            self.CompanyNameVar = StringVar()
            self.CompanyNameVar.set(self.DEFAULTTEXT)
            self.CompanyName = ttk.Combobox(self.master, textvariable=self.CompanyNameVar, values=self.OptionValues, width=41, justify='center', state='readonly')
            self.CompanyName.pack(pady=10, ipady=3)

            self.DataButton = Button(self.master, text="Get Company Details", width=33, fg='white', bg="#5d9130", activebackground="#5d9130", activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.GetMarketDetails)
            self.DataButton.pack(ipady=5)

            self.DetailsFrame = Frame(self.master)
            self.DetailsFrame.pack(pady=10, side=BOTTOM)

            self.InitialPosition()

            self.master.bind('<Control-r>', self.Retry)
            self.master.bind('<Button-1>', self.ChangeFocus)
            self.master.bind_all('<F5>', self.GetMarketDetails)
            self.CompanyName.bind('<Return>', self.GetMarketDetails)
            self.CompanyName.bind('<KeyRelease>', self.AutoComplete)

            self.master.mainloop()

        else:
            self.SEARCH = Search.Search(self.ShowErrorMessage, self.CheckInternet)
            self.details = self.SEARCH.get_data(company_symbol)

    def InitialPosition(self):
        '''Set window position to the center of the screen when program starts first time'''

        self.master.update()
        self.master.resizable(0, 0)
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.deiconify()

        self.OptionValues.sort()
        self.CompanyName['values'] = self.OptionValues

    def Retry(self, event=None):
        '''Retry to get the company names if not retrieved at first'''

        if self.CheckInternet():
            self.OptionValues = self.SEARCH.GetCompaniesNameList()
            self.CompanyNameVar.set(self.DEFAULTTEXT)
            self.CompanyName.config(values=self.OptionValues)
            self.ShowErrorMessage('Retrieved Company Names successfully')

        else:
            self.ShowErrorMessage('Failed to get Company Names. No Internet.\nPress Control + R to retry.', _time=5000, height=230)

    def CheckInternet(self):
        '''Check if the user is connected to internet'''

        try:
            requests.get('https://google.com')
            return True

        except requests.ConnectionError:
            return False

    def ChangeFocus(self, event=None):
        '''Change focus to the respective widget where user has clicked'''

        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)

        if not isinstance(widget, (ttk.Combobox, type(None))):
            widget.focus_set()

    def GetMarketDetails(self, event=None):
        '''Display company details if available'''

        for child in self.DetailsFrame.winfo_children():  # Destroying all widgets inside of self.DetailsFrame
            child.destroy()

        error_message = ''
        value = self.CompanyNameVar.get().strip()

        if '(' in value:
            value = value[:value.index('(')]

        # Fonts for the extracted values
        label_font = Font(size=10, weight='bold')
        font1, font2 = Font(size=15), Font(size=10)

        if value and value != self.DEFAULTTEXT:
            if self.CheckInternet():
                details = self.SEARCH.get_data(value)

                if details:
                    company_name = details['company_name']
                    sector = details['sector']
                    share_value = details['market_price']
                    change = details['change']
                    date = details['last_traded_on']
                    high_low = details['high_low']
                    average_value = details['average']

                    company_name_label = Label(self.DetailsFrame, text=company_name, font=font1, fg='green', wraplength=250)
                    company_name_label.pack()

                    # Displaying sector details
                    sector_frame = Frame(self.DetailsFrame)
                    sector_frame.pack(fill='x')
                    sector_label = Label(sector_frame, text="Sector", fg="#333333", font=label_font)
                    sector_label.pack(side=LEFT)
                    sector_name = Label(sector_frame, text=sector, fg='#1c8b98', font=font2)
                    sector_name.pack(side=RIGHT)

                    # Displaying current stock value of the company
                    market_price_frame = Frame(self.DetailsFrame)
                    market_price_frame.pack(fill='x')
                    market_label = Label(market_price_frame, text='Market Price', fg="#333333", font=label_font)
                    market_label.pack(side=LEFT)
                    market_price = Label(market_price_frame, text=share_value, font=Font(size=10, weight='bold'))
                    market_price.pack(side=RIGHT)

                    # Displaying change percentage
                    change_frame = Frame(self.DetailsFrame)
                    change_frame.pack(fill='x')
                    change_label = Label(change_frame, text='% Change', fg="#333333", font=label_font)
                    change_label.pack(side=LEFT)
                    change_value = Label(change_frame, text=change, font=font2)
                    change_value.pack(side=RIGHT)

                    # Displaying last trade date of the company
                    last_trade_frame = Frame(self.DetailsFrame)
                    last_trade_frame.pack(fill='x')
                    last_trade_date_label = Label(last_trade_frame, text='Last Traded On', fg="#333333", font=label_font)
                    last_trade_date_label.pack(side=LEFT)
                    last_trade_date = Label(last_trade_frame, text=date, width=20, anchor='e', font=font2)
                    last_trade_date.pack(side=RIGHT)

                    # Displaying high and low price of the company
                    high_low_frame = Frame(self.DetailsFrame)
                    high_low_frame.pack(fill='x')
                    high_low_label = Label(high_low_frame, text='High-Low', fg="#333333", font=label_font)
                    high_low_label.pack(side=LEFT)
                    high_low_label_value = Label(high_low_frame, text=high_low, width=20, anchor='e', font=font2)
                    high_low_label_value.pack(side=RIGHT)

                    # Displaying company's average market value of the company
                    average_frame = Frame(self.DetailsFrame)
                    average_frame.pack(fill='x')
                    average_label = Label(average_frame, text='120 Day Average', fg="#333333", font=label_font)
                    average_label.pack(side=LEFT)
                    average_label_value = Label(average_frame, text=average_value, width=20, anchor='e', font=font2)
                    average_label_value.pack(side=RIGHT)

                    changed = self.SEARCH.Profit_Loss_Or_Neutral(value)

                    if change == '0 %':  # When company stock price has not been changed
                        color = '#ed9c28'

                    elif 'decrease' in changed:  # When company stock price has been decreased
                        color = '#ff3333'

                    else:  # When company stock price has been increased
                        color = '#0dbe0d'

                    market_price.config(fg=color)
                    change_value.config(fg=color)

                    self.master.update()
                    self.master.geometry(f'{self.master.winfo_width()}x{self.master.winfo_reqheight()}')

                else:
                    self.ShowErrorMessage(f'Cannot retrieve data.\nMaybe {value} has not\npublished its market value yet.', _time=2500, height=255)

            else:
                # When user is not connected to internet
                error_message = 'No Internet Connection'

        else:
            # When user tries to get company market details without
            # inserting any company in the entry widget
            error_message = 'Invalid Company Symbol'

        if error_message:
            self.ShowErrorMessage(error_message)

    def ShowErrorMessage(self, error_message, _time=1500, height=215):
        '''
        Show error message when there is no internet and when user
        does not provide any company name

        error_message: The actual error message to display
        _time: For long should the error message be displayed (in millisecond)
        height: Height of window to fit error message        (in pixel)
        '''

        if self.ErrorTimer is None:
            for child in self.DetailsFrame.winfo_children():
                child.destroy()

            pygame.mixer.music.play()

            error_message_var = StringVar()
            error_message_var.set(error_message)

            self.master.geometry(f'304x{height}')

            label = Label(self.DetailsFrame, textvariable=error_message_var, fg='red', font=Font(size=10, weight='bold'))
            label.pack()
            self.ErrorTimer = self.master.after(_time, lambda: self.RemoveErrorMessage(label))

        else:
            self.master.after_cancel(self.ErrorTimer)
            self.ErrorTimer = None
            self.master.after(0, lambda: self.ShowErrorMessage(error_message, _time, height))

    def RemoveErrorMessage(self, lbl):
        '''Destroy the error message'''

        lbl.destroy()
        self.ErrorTimer = None
        self.master.geometry('304x196')

    def AutoComplete(self, event=None):
        '''Search value when the focus is in ttk.Combobox'''

        _char = event.char.upper()

        if _char == '':
            return 'break'

        if self.StartTimer:
            end_timer = timeit.default_timer()
            escaped = end_timer - self.StartTimer

            if 0 < escaped < 0.27:
                _char = self.PreviousSearch + _char

        common_names = list(filter(lambda item: item.startswith(_char), self.OptionValues))

        if self.PreviousSearch != _char or self.LocalSearchIndex == len(common_names) - 1:
            self.LocalSearchIndex = 0

        self.PreviousSearch = _char
        self.StartTimer = timeit.default_timer()

        if common_names:
            self.ToSelectValue = common_names[self.LocalSearchIndex]
            self.LocalSearchIndex += 1

            self.CompanyName.set(self.ToSelectValue)
            self.CompanyNameVar.set(self.ToSelectValue)

    def ResourcePath(self, FileName):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', FileName)


if __name__ == '__main__':
    StockTracker()
