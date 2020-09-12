import imdb
import datetime
import tkinter as tk
from tkinter.ttk import Progressbar
import tkinter.font as font
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
import numpy as np
import random


query_movies = []


def movies_list_2_text(width):
    global query_movies
    if not query_movies:
        print("WFT man ...")

    txt = ""
    for movie in query_movies:
        txt += f"""
        {"-" * width}
        {movie['title']}
        ({movie['year']})
        Score: {movie['score']}
        Cast: {', '.join([actor.get('name') for actor in movie['cast'][:3]])}
        Director: {', '.join([director.get('name') for director in movie['director']])}
        URL: {movie['url']}
        """

    return txt


def sort_list_by(par, key):
    global query_movies
    query_movies = sorted(query_movies, key=lambda x: x[key], reverse=False if key == 'title' else True)
    par.destroy()
    movieList()


def movieList():
    new_window = tk.Toplevel(root)
    new_window.title("DIEGO'S MOVIE LIST")

    menubar = tk.Menu(new_window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Box-Office", command=lambda: sort_list_by(new_window, 'box_office'))
    filemenu.add_command(label="Score", command=lambda: sort_list_by(new_window, 'score'))
    filemenu.add_command(label="Alphabetical", command=lambda: sort_list_by(new_window, 'title'))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=new_window.quit)
    menubar.add_cascade(label="Sort results", menu=filemenu)
    new_window.config(menu=menubar)

    title_font = font.Font(family='Times', size=25)
    label = tk.Label(new_window, text="MOVIES FOUND:", font=title_font)
    label.grid(column=0, row=0)

    text_area = scrolledtext.ScrolledText(new_window,
                                          wrap=tk.WORD,
                                          width=60,
                                          height=10,
                                          font=("Times New Roman",
                                                15))
    text_area.grid(column=0, row=1)
    text_area.focus()

    text_area.insert(tk.INSERT, movies_list_2_text(width=60))
    text_area.configure(state='disabled')


class App:
    def __init__(self, master):
        self.master = master

        self.master.title("DIEGO'S MOVIE PICKER")

        title_font = font.Font(family='Times', size=25)
        label_font = font.Font(family='Arial', size=10)

        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Guide", command=lambda: messagebox.showinfo("How to use", "Select your year and score range. Then, you can select or a key-word or up to two genres. The query can take A LOT of time (~10min). Same movie query should get different random results every time."))
        filemenu.add_command(label="Genres", command=lambda: messagebox.showinfo("Genres Information", "Can select up to two genres from: action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film-noir, horror, musical, mystery, romance, sci-fi, thriller, war and western. SHOULD BE THE SAME NAME."))
        filemenu.add_command(label="Key-Words", command=lambda: messagebox.showinfo("Key-Words Information", "Selec a theme (ie. aliens, superheroes, weddings, ... ). The results should be VERY different for the same key-word query."))
        filemenu.add_command(label="Troubleshoot", command=lambda: messagebox.showinfo("Troubleshoot", "Should take a lot of time, up to 10 minutes. If no results were found or the movies are not satifing, search again without changing anything and should change the output. YOU CAN'T SELECT KEYWORDS AND GENRES, JUST ONE OF BOTH."))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="Help", menu=filemenu)
        master.config(menu=menubar)

        self.label = tk.Label(text="DIEGO'S MOVIE PICKER", font=title_font)
        self.label.grid(column=1, row=0)

        self.label = tk.Label(text='Min Score:', font=label_font)
        self.label.grid(column=0, row=1)
        self.min_score_var = tk.IntVar()
        self.min_score = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, variable=self.min_score_var)
        self.min_score.grid(column=0, row=2)
        self.min_score.set(60)

        self.label = tk.Label(text='Max Score:', font=label_font)
        self.label.grid(column=0, row=3)
        self.max_score_var = tk.IntVar()
        self.max_score = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, variable=self.max_score_var)
        self.max_score.grid(column=0, row=4)
        self.max_score.set(100)

        self.label = tk.Label(text='Min Year:', font=label_font)
        self.label.grid(column=2, row=1)
        self.min_year_var = tk.IntVar()
        self.min_score = tk.Scale(orient=tk.HORIZONTAL, from_=1900, to=datetime.datetime.now().year,
                                  variable=self.min_year_var)
        self.min_score.grid(column=2, row=2)
        self.min_score.set(1960)

        self.label = tk.Label(text='Max Year:', font=label_font)
        self.label.grid(column=2, row=3)
        self.max_year_var = tk.IntVar()
        self.max_score = tk.Scale(orient=tk.HORIZONTAL, from_=1900, to=datetime.datetime.now().year,
                                  variable=self.max_year_var)
        self.max_score.grid(column=2, row=4)
        self.max_score.set(datetime.datetime.now().year)

        self.label_query = tk.Label(text='Query Progress:', font=label_font)
        self.progressbar = Progressbar(orient=tk.HORIZONTAL, length=100, mode='determinate')

        self.label = tk.Label(text='Max number of movies to display:', font=label_font)
        self.label.grid(column=1, row=3)
        self.MOVIE_LIMIT = tk.IntVar()
        self.max_score = tk.Scale(orient=tk.HORIZONTAL, from_=1, to=20,
                                  variable=self.MOVIE_LIMIT)
        self.max_score.grid(column=1, row=4)
        self.max_score.set(7)

        self.label = tk.Label(text='Key-Word:', font=label_font)
        self.label.grid(column=0, row=5)
        self.key_word = tk.Entry()
        self.key_word.grid(column=0, row=6)

        self.label = tk.Label(text='Genre 1:', font=label_font)
        self.label.grid(column=1, row=5)
        self.genre_1 = tk.Entry()
        self.genre_1.grid(column=1, row=6)

        self.label = tk.Label(text='Genre 2:', font=label_font)
        self.label.grid(column=2, row=5)
        self.genre_2 = tk.Entry()
        self.genre_2.grid(column=2, row=6)

        self.button1 = tk.Button(text='Enlighten me!', command=self.start_search)
        self.button1.grid(column=1, row=7)

        self.ia = imdb.IMDb()
        self.data = pd.read_csv('movies.csv')
        self.genres_list = ["action", "adventure", "animation", "children", "comedy", "crime", "documentary", "drama",
                            "fantasy", "film-noir", "horror", "musical", "mystery", "romance", "sci-fi", "thriller",
                            "war", "western"]
        self.known_movies_title_list = []
        self.known_movies_years_list = []
        self.known_movies_genres_list = []
        for idx, (title, genre) in enumerate(zip(self.data['title'], self.data['genres'])):
            self.known_movies_title_list.append(' '.join(title.split(' ')[:-1]))
            year = int(title.split(' ')[-1][1:-1])
            self.known_movies_years_list.append(year)
            self.known_movies_genres_list.append([g.lower() for g in genre.split('|')])

    def create_movie_dict(self, title, info=False):
        movies = self.ia.search_movie(title)

        if info:
            print("\nProcessing", title)

        score = (self.min_score_var.get(), self.max_score_var.get())
        year = (self.min_year_var.get(), self.max_year_var.get())

        movie = None
        for m in movies:
            y = m.get('year')
            if not y:
                if info:
                    print("No year info ...")
                return None
            if year[0] <= y <= year[1]:
                movie = m
                break

        if not movie:
            if info:
                print("Movie not found or not in year period ...")
            return None

        movieID = movie.movieID
        movie = self.ia.get_movie(movieID)

        score_met = self.ia.get_movie_critic_reviews(movieID)['data']
        if score_met:
            score_met = score_met.get('metascore')
            if score_met is None:
                if info:
                    print("No score found ...")
                return None
            if not score[0] <= int(score_met) <= score[1]:
                if info:
                    print("Score not in range ...")
                return None
        else:
            if info:
                print("No score found ...")
            return None

        if info:
            print("PROCESSED!")

        box_office = movie.get('box office')
        if box_office:
            box_office = box_office.get('Cumulative Worldwide Gross')
        title = movie.get('title')
        year = movie.get('year')
        genres = movie.get('genre')
        plot = movie.get('plot')
        if plot:
            plot = plot[0]
        cast = movie.get('cast')
        cover = movie.get('cover url')
        director = movie.get('director')
        url = self.ia.get_imdbURL(movie)

        return {'title': title, 'year': year, 'director': director, 'score': score_met, 'genres': genres,
                'box_office': int(''.join([b for b in box_office if b.isdigit()])) if box_office is not None else 0,
                'cast': cast, 'cover': cover, 'plot': plot, 'url': url}

    def start_search(self):
        self.progressbar.grid(column=1, row=2)
        self.label_query.grid(column=1, row=1)
        self.data = self.data.reindex(np.random.permutation(self.data.index))
        if self.key_word.get():
            possible_keywords = self.ia.search_keyword(self.key_word.get())
            possible_movies = []
            keyword = random.choice(possible_keywords)
            self.key_word.delete(0, "end")
            self.key_word.insert(0, keyword)
            movies = self.ia.get_keyword(keyword)
            random.shuffle(movies)
            for movie in movies:
                self.progressbar['value'] = int(len(possible_movies) / self.MOVIE_LIMIT.get() * 100)
                root.update_idletasks()
                if len(possible_movies) >= self.MOVIE_LIMIT.get():
                    break
                movie_dic = self.create_movie_dict(movie['title'])
                if movie_dic:
                    possible_movies.append(movie_dic)
        else:
            if not self.genre_1.get() and not self.genre_2.get():
                messagebox.showinfo("Are you OK?", "No genres or key-words were set ...")
                return
            possible_movies = []
            for title, year, genres in zip(self.known_movies_title_list, self.known_movies_years_list,
                                           self.known_movies_genres_list):
                self.progressbar['value'] = int(len(possible_movies) / self.MOVIE_LIMIT.get() * 100)
                root.update_idletasks()
                if len(possible_movies) == self.MOVIE_LIMIT.get():
                    break
                if self.min_year_var.get() < int(year) < self.max_year_var.get():
                    if self.genre_1.get():
                        if self.genre_2.get():
                            if self.genre_1.get() in genres and self.genre_2.get() in genres:
                                movie_dic = self.create_movie_dict(title)
                                if movie_dic:
                                    possible_movies.append(movie_dic)
                        elif self.genre_1.get() in genres:
                            movie_dic = self.create_movie_dict(title)
                            if movie_dic:
                                possible_movies.append(movie_dic)
                    elif self.genre_2.get():
                        if self.genre_2.get() in genres:
                            movie_dic = self.create_movie_dict(title)
                            if movie_dic:
                                possible_movies.append(movie_dic)

        if not possible_movies:
            messagebox.showinfo("Ouff", "ANY movie could fit your description ...")
            self.label_query.grid_forget()
            self.progressbar.grid_forget()
            return
        messagebox.showinfo("Success", f"{len(possible_movies)} movies matching your description were found!")
        global query_movies
        query_movies = []
        query_movies = possible_movies
        self.label_query.grid_forget()
        self.progressbar.grid_forget()
        movieList()


root = tk.Tk()
app = App(root)
root.mainloop()
