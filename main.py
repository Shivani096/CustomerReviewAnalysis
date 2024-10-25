from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
from extract import Extract
from analyze import Analyze
from threading import Thread

BACKGROUND = "#131417"


class Window:

    e = Extract()
    a = Analyze()

    def __init__(self):
        root = Tk()
        root.title("MyApp")
        root.state("zoomed")

        self.main_frame = Frame(root)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.title_label = Label(self.main_frame, text="Amazon Review Analysis")
        self.title_label.configure(font="-family Cambria -size 28")
        self.title_label.pack(fill=X)

        self.entry_frame = Frame(self.main_frame)
        self.entry_frame.pack(fill=X, padx=100, pady=60)

        self.entry_title = Label(self.entry_frame, text="Enter product URL : ")
        self.entry_title.configure(font="-family Cambria -size 20")
        self.entry_title.pack(fill=X, side=LEFT, expand=False)

        self.url_entry = ttk.Entry(self.entry_frame)
        self.url_entry.configure(font="-family Cambria -size 18")
        self.url_entry.pack(fill=X, side=LEFT, expand=True)

        style = ttk.Style()
        style.configure('my.TButton', font=('Cambria', 14))

        self.url_button = ttk.Button(self.entry_frame, text="Search", style='my.TButton')
        self.url_button.configure(width=15, cursor="hand2", command=self.run_thread)
        self.url_button.pack(fill=X, side=LEFT, expand=False, ipady=3, padx=20)

        self.operation_frame = Frame(self.main_frame)
        self.operation_frame.pack(fill=BOTH, expand=True, side=LEFT)

        self.operation_title = Label(self.operation_frame, text="OPERATION")
        self.operation_title.configure(font="-family Cambria -size 20")
        self.operation_title.pack(fill=X, side=TOP)

        self.operation_area = ScrolledText(self.operation_frame)
        self.operation_area.configure(font="-family Cambri")
        self.operation_area.see(END)
        self.operation_area.pack(fill=BOTH, side=LEFT, padx=60, pady=60)

        self.bar_frame = Frame(self.main_frame)
        self.bar_frame.pack(fill=BOTH, expand=True, side=LEFT)

        self.bar_title = Label(self.bar_frame, text="PIE CHART")
        self.bar_title.configure(font="-family Cambria -size 20")
        self.bar_title.pack(fill=X, side=TOP)

        img = ImageTk.PhotoImage(Image.open("mypng.png"))
        self.image = Label(self.bar_frame, image=img)
        self.image.pack_forget()

        root.mainloop()

    reviewList = []

    def run_thread(self):
        self.t1 = Thread(target=self.getReviewUrl)
        self.t1.start()
        

    def getReviewUrl(self):
        self.operation_area.delete('1.0', END)
        self.image.pack_forget()
        url = self.url_entry.get()
        reviewUrl = self.e.ReviewUrl(url)
        total_review = self.e.total_reviews(reviewUrl)
        count = 0
        for item in total_review:
            count += 1
            text = f"Extracting review {count}\n"
            self.operation_area.insert("insert", text)
            review = self.e.extractReview(item)
            print(review)
            self.reviewList.append(review)

        text = "\nExtraction done Succesfully!!\n\n"
        self.operation_area.insert("insert", text)
        self.operation_area.see(END)
        self.e.exportToExcel(self.reviewList)
        self.analyzeData()
        return

    def analyzeData(self):
        data = self.a.total_data()
        for i in range(len(data)):
            run = f"Analyzing review {i+1}\n"
            self.operation_area.insert("insert", run)
            str1 = self.a.analysis(data.iloc[i][2])
            self.operation_area.insert("insert", str1)
            self.operation_area.see(END)

        pos, neg = self.a.get_pos_neg()
        text = f"""Analysis done!!\nPositivity is {pos}%\nNegativity is {neg}%\n"""
        self.operation_area.insert("insert", text)
        if pos > neg:
            text = "Overall statement is Positive\nHence, Review is good for the product."
        else:
            text = "Overall statement is Negative\nHence, Review is bad for the product."
        self.operation_area.insert("insert", text)
        self.operation_area.see(END)
        self.a.positive.clear()
        self.a.negative.clear()
        self.reviewList.clear()
        self.a.create_chart(pos, neg)
        self.image.pack(side=RIGHT, padx=20)
        

w = Window()