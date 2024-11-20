import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt


dataframe = pd.DataFrame()

def total_books():
    total = dataframe["Кількість примірників"].sum()
    print(f"Загальна кількість книг у бібліотеці: {total}")
    return total

def popular_genres():
    genres_count = dataframe["Жанр"].value_counts()
    print("Найпопулярніші жанри (за кількістю книг):")
    print(genres_count)
    return genres_count

def popular_genres_by_copies():
    genres_copies = dataframe.groupby("Жанр")["Кількість примірників"].sum().sort_values(ascending=False)
    print("Найпопулярніші жанри (за кількістю примірників):")
    print(genres_copies)
    return genres_copies

def search_by_author(author):
    books = dataframe[dataframe["Автор"].str.contains(author, case=False, na=False)]
    print(f"Книги автора '{author}':")
    print(books)
    return books

def search_by_year(year):
    books = dataframe[dataframe["Рік видання"] == int(year)]
    print(f"Книги, видані у {year} році:")
    print(books)
    return books

def load_csv():
    global dataframe
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        try:
            dataframe = pd.read_csv(filepath)
            update_table()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити файл: {e}")

def save_csv():
    global dataframe
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filepath:
        try:
            dataframe.to_csv(filepath, index=False)
            messagebox.showinfo("Успіх", "Дані успішно збережено!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

def add_book():
    global dataframe
    new_data = {
        "Назва": entry_title.get(),
        "Автор": entry_author.get(),
        "Рік видання": entry_year.get(),
        "Жанр": entry_genre.get(),
        "Кількість примірників": entry_copies.get(),
    }
    new_row = pd.DataFrame([new_data])
    dataframe = pd.concat([dataframe, new_row], ignore_index=True)
    update_table()


def edit_book():
    global dataframe
    selected_item = table.focus()
    if not selected_item:
        messagebox.showwarning("Увага", "Оберіть книгу для редагування")
        return
    index = table.item(selected_item)["values"][0]
    dataframe.loc[index, "Назва"] = entry_title.get()
    dataframe.loc[index, "Автор"] = entry_author.get()
    dataframe.loc[index, "Рік видання"] = entry_year.get()
    dataframe.loc[index, "Жанр"] = entry_genre.get()
    dataframe.loc[index, "Кількість примірників"] = entry_copies.get()
    update_table()

def delete_book():
    global dataframe
    selected_item = table.focus()
    if not selected_item:
        messagebox.showwarning("Увага", "Оберіть книгу для видалення")
        return
    index = table.item(selected_item)["values"][0]
    dataframe = dataframe.drop(index)
    update_table()

def update_table():
    table.delete(*table.get_children())
    for idx, row in dataframe.iterrows():
        table.insert("", "end", values=[idx] + list(row))


def genre_pie_chart():
    genre_counts = dataframe["Жанр"].value_counts()
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Розподіл книг за жанрами")
    plt.show()

def year_histogram():
    try:

        years = pd.to_numeric(dataframe["Рік видання"], errors="coerce").dropna()
        years = years.astype(int)  # Гарантуємо цілі числа
        if years.empty:
            messagebox.showwarning("Попередження", "Дані про роки видання відсутні або некоректні.")
            return


        plt.hist(years, bins=range(years.min(), years.max() + 1), color="lightblue", edgecolor="black")
        plt.title("Кількість книг за роками видання")
        plt.xlabel("Рік видання")
        plt.ylabel("Кількість книг")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося побудувати гістограму: {e}")


def display_total_books():
    total = total_books()
    messagebox.showinfo("Загальна кількість книг", f"Загальна кількість книг у бібліотеці: {total}")

def display_popular_genres():
    genres = popular_genres()
    messagebox.showinfo("Найпопулярніші жанри", genres.to_string())

def search_author_gui():
    author = entry_author.get()
    result = search_by_author(author)
    text_widget.insert(tk.END, result.to_string(index=False))

def search_year_gui():
    year = entry_year.get()
    result = search_by_year(year)
    text_widget.insert(tk.END, result.to_string(index=False))


root = tk.Tk()
root.title("Управління бібліотекою книг")


control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Button(control_frame, text="Завантажити CSV", command=load_csv).pack(side=tk.LEFT, padx=5)
tk.Button(control_frame, text="Зберегти CSV", command=save_csv).pack(side=tk.LEFT, padx=5)
tk.Button(control_frame, text="Додати книгу", command=add_book).pack(side=tk.LEFT, padx=5)
tk.Button(control_frame, text="Редагувати книгу", command=edit_book).pack(side=tk.LEFT, padx=5)
tk.Button(control_frame, text="Видалити книгу", command=delete_book).pack(side=tk.LEFT, padx=5)


input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(input_frame, text="Назва").grid(row=0, column=0)
entry_title = tk.Entry(input_frame)
entry_title.grid(row=0, column=1)

tk.Label(input_frame, text="Автор").grid(row=0, column=2)
entry_author = tk.Entry(input_frame)
entry_author.grid(row=0, column=3)

tk.Label(input_frame, text="Рік видання").grid(row=1, column=0)
entry_year = tk.Entry(input_frame)
entry_year.grid(row=1, column=1)

tk.Label(input_frame, text="Жанр").grid(row=1, column=2)
entry_genre = tk.Entry(input_frame)
entry_genre.grid(row=1, column=3)

tk.Label(input_frame, text="Кількість примірників").grid(row=2, column=0)
entry_copies = tk.Entry(input_frame)
entry_copies.grid(row=2, column=1)


table_frame = tk.Frame(root)
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ["Index", "Назва", "Автор", "Рік видання", "Жанр", "Кількість примірників"]
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for col in columns:
    table.heading(col, text=col)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget = tk.Text(root, height=20, width=60)
text_widget.pack(pady=10)


frame_search = tk.Frame(root)
frame_search.pack()

tk.Label(frame_search, text="Автор:").grid(row=0, column=0, padx=5, pady=5)
entry_author = tk.Entry(frame_search)
entry_author.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_search, text="Рік:").grid(row=1, column=0, padx=5, pady=5)
entry_year = tk.Entry(frame_search)
entry_year.grid(row=1, column=1, padx=5, pady=5)




btn_total = tk.Button(control_frame, text="Загальна кількість книг", command=display_total_books)
btn_total.pack(pady=5)

btn_genres = tk.Button(control_frame, text="Найпопулярніші жанри", command=display_popular_genres)
btn_genres.pack(pady=5)

btn_search_author = tk.Button(frame_search, text="Пошук за автором", command=search_author_gui)
btn_search_author.grid(row=0, column=2, padx=5, pady=5)

btn_search_year = tk.Button(frame_search, text="Пошук за роком", command=search_year_gui)
btn_search_year.grid(row=1, column=2, padx=5, pady=5)

chart_frame = tk.Frame(root)
chart_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

tk.Button(control_frame, text="Розподіл за жанрами", command=genre_pie_chart).pack(side=tk.LEFT, padx=5)
tk.Button(control_frame, text="Кількість за роками", command=year_histogram).pack(side=tk.LEFT, padx=5)

root.mainloop()



