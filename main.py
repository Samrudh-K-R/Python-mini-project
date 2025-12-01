import wx
import wx.adv
import wx.dataview
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import database

class AddExpenseDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Add Expense")
        
        self.date_picker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        
        categories = ["Food", "Transport", "Utilities", "Shopping", "Entertainment", "Health", "Other"]
        self.category_text = wx.ComboBox(self, choices=categories, style=wx.CB_DROPDOWN)
        
        self.amount_text = wx.TextCtrl(self)
        self.desc_text = wx.TextCtrl(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        form_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        form_sizer.Add(wx.StaticText(self, label="Date:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.date_picker, 0, wx.EXPAND)
        form_sizer.Add(wx.StaticText(self, label="Category:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.category_text, 0, wx.EXPAND)
        form_sizer.Add(wx.StaticText(self, label="Amount:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.amount_text, 0, wx.EXPAND)
        form_sizer.Add(wx.StaticText(self, label="Description:"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.desc_text, 0, wx.EXPAND)
        
        sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        btn_sizer = wx.StdDialogButtonSizer()
        save_btn = wx.Button(self, wx.ID_OK, label="Save")
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(save_btn)
        btn_sizer.AddButton(cancel_btn)
        btn_sizer.Realize()
        
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Fit()

    def get_data(self):
        date = self.date_picker.GetValue().FormatISODate()
        category = self.category_text.GetValue()
        try:
            amount = float(self.amount_text.GetValue())
        except ValueError:
            amount = 0.0
        description = self.desc_text.GetValue()
        return date, category, amount, description

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Expense Tracker", size=(900, 600))
        
        database.init_db()
        
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left side: List and Controls
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.expense_list = wx.dataview.DataViewListCtrl(panel)
        self.expense_list.AppendTextColumn("Date", width=100)
        self.expense_list.AppendTextColumn("Category", width=100)
        self.expense_list.AppendTextColumn("Amount", width=80)
        self.expense_list.AppendTextColumn("Description", width=150)
        
        left_sizer.Add(self.expense_list, 1, wx.EXPAND | wx.ALL, 5)
        
        add_btn = wx.Button(panel, label="Add Expense")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_expense)
        left_sizer.Add(add_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        main_sizer.Add(left_sizer, 1, wx.EXPAND | wx.ALL, 5)
        
        # Right side: Chart
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(panel, -1, self.figure)
        
        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(main_sizer)
        
        self.refresh_data()
        
    def on_add_expense(self, event):
        dlg = AddExpenseDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            date, category, amount, description = dlg.get_data()
            if category and amount > 0:
                database.add_expense(date, category, amount, description)
                self.refresh_data()
        dlg.Destroy()
        
    def refresh_data(self):
        self.expense_list.DeleteAllItems()
        expenses = database.get_expenses()
        for row in expenses:
            # row: id, date, category, amount, description
            self.expense_list.AppendItem([row[1], row[2], f"₹{row[3]:.2f}", row[4]])
            
        self.update_chart()
        
    def update_chart(self):
        self.axes.clear()
        data = database.get_expenses_by_category()
        if data:
            categories = [row[0] for row in data]
            amounts = [row[1] for row in data]
            self.axes.pie(amounts, labels=categories, autopct='%1.1f%%')
            self.axes.set_title("Expenses by Category (₹)")
        else:
            self.axes.text(0.5, 0.5, "No Data", ha='center')
            
        self.canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
