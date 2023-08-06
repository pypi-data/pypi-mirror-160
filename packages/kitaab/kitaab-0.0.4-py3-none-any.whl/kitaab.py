
from github import Github
import os
import sys
from datetime import datetime
from rich.console import Console


import sqlite3
from typing import List



import os
from rich.console import Console
from rich.columns import Columns
from rich import box, print
from rich.panel import Panel
from rich.table import Table


console = Console()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def error():
    console.print("oops! invalid input 😓", style="orchid2")
    console.print("type 1 to Create a new note", style="orchid2")
    console.print("type 2 to Edit note", style="orchid2")
    console.print("type 3 to Edit note content", style="orchid2")
    console.print("type 4 to Delete note", style="orchid2")


def menu():
    print("\n")
    console.print(" 1 --> New note", style="orchid2")
    console.print(" 2 --> Edit name", style="pale_violet_red1")
    console.print(" 3 --> Edit content", style="light_coral")
    console.print(" 4 --> Delete note", style="red3")


def Help():
    console.print(
        " type add-token --> setup github integration ", style="red3")
    console.print(" type board --> view notes as board ", style="light_coral")
    console.print(" type quit or q -->  to exit ", style="pale_violet_red1")


def print_table():
    '''
        Creating table using Rich.
    '''

    table = Table(title="Al-kitaab", title_style="indian_red1",
                  style="indian_red1", box=box.ROUNDED)

    table.add_column("🌵", style="orange3")
    table.add_column("Name", style="orchid1", header_style="orange3")
    table.add_column("Content", style="medium_spring_green",
                     header_style="orange3")
    table.add_column("Last Modified", style="yellow1",
                     justify="center", header_style="orange3")

    # get all notes from database
    notes = get_all_notes()
    for idx, note in enumerate(notes, start=1):
        table.add_row(str(idx), note.name, note.content[:30], note.date_Added)
    console.print(table)


# BOARD VIEW
def get_content(user):
    '''
        getting content for board view.
    '''

    content = user["content"]
    name = user["title"]
    return f"[medium_spring_green]{content}\n[orchid1]{name}"


def print_board():
    '''
        building board view with Rich.
    '''

    console = Console()
    users = get_dict()
    if users == []:
        console.print("notebook is empty", style='yellow3')
    else:
        user_renderables = [Panel(get_content(
            user), expand=True,  border_style="indian_red1")for user in users]
        console.print(Columns(user_renderables))

class Note:
    def __init__(self, idx, name, content, date_Added):
        self.idx = idx
        self.name = name
        self.content = content
        self.date_Added = date_Added

    def __repr__(self) -> str:
        return f"({self.idx},{self.name}, {self.content}, {self.date_Added})"

# connect to database
conn = sqlite3.connect('notes.db')

# create a cursor
c = conn.cursor()


def create_table():
    '''
        create notes table in database.
    '''

    c.execute(""" CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title text,
            content text,
            dateAdded text
        )""")


create_table()


def token_table():
    '''
        create token table in database.
    '''

    c.execute(""" CREATE TABLE IF NOT EXISTS Token(
            token text
        )""")


token_table()


def drop_token():
    '''
        delete token from the table.
    '''

    with conn:
        c.execute(""" DROP TABLE IF EXISTS Token """)
        conn.commit()


def add_token(mytoken: str):
    '''
        adds token to table.
    '''

    drop_token()
    token_table()
    with conn:
        c.execute("INSERT INTO Token(token) VALUES(:token)",
                  {'token': mytoken})
        conn.commit()


def show_token():
    '''
        fetch token from the table.
    '''

    token_table()
    with conn:
        c.execute("SELECT token from Token")
        tokens = None
        tokens = c.fetchone()
        if tokens is not None:
            for token in tokens:
                return token
        else:
            return tokens


def create_note(note: Note):
    '''
        add new note.
    '''

    with conn:
        c.execute("INSERT INTO notes(title, content, dateAdded) VALUES( :title, :content, :dateAdded)",
                  {'title': note.name, 'content': note.content, 'dateAdded': note.date_Added})
        conn.commit()


def get_note(new_name: str):
    '''
        access content from specific note.
    '''

    with conn:
        c.execute('''SELECT content from notes WHERE title LIKE ?''', (new_name,))
        rows = c.fetchone()
        for row in rows:
            return row


def update_note_name(noteName: str, newName: str, newDate: str):
    '''
        edit note name.
    '''

    with conn:
        c.execute('''UPDATE notes SET title = ? WHERE title LIKE ? ''',
                  (newName, noteName,))
        conn.commit()
    with conn:
        c.execute(
            '''UPDATE notes SET dateAdded = ? WHERE title LIKE ? ''', (newDate, newName,))
        conn.commit()


def update_note_content(noteName: str, newContent: str, newDate: str):
    '''
        edit note content.
    '''

    with conn:
        c.execute('''UPDATE notes SET content = ? WHERE title LIKE ? ''',
                  (newContent, noteName,))
        conn.commit()
    with conn:
        c.execute(
            '''UPDATE notes SET dateAdded = ? WHERE title LIKE ? ''', (newDate, noteName,))
        conn.commit()


def delete_note(noteName: str):
    '''
        delete note.
    '''

    with conn:
        c.execute('''DELETE FROM notes WHERE title LIKE ? ''', (noteName,))
        conn.commit()


def get_all_notes() -> List[Note]:
    '''
        fetch all notes from the table.
    '''

    c.execute("SELECT * from notes")
    results = c.fetchall()
    notes = []
    for result in results:
        notes.append(Note(*result))
    return notes


def get_dict():
    '''
    fetch all notes & add to dictionary.
    '''

    with conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM notes")
        rows = curs.fetchall()
        Dict = []
        for row in rows:
            Dict.append(dict(row))
        return Dict


console = Console()

console = Console()


# Token
key = show_token()
token = os.getenv('GITHUB_TOKEN', key)
g = Github(token)
user = g.get_user()


def check_token_validity():
    '''
        checking if token entered by user is valid or not.
    '''

    token_valid = False
    key = show_token()
    token = os.getenv('GITHUB_TOKEN', key)
    g = Github(token)
    user = g.get_user()
    try:
        if key is not None:
            console.print(
                f"your github account is [yellow3]{user.login}[/]", style="red")
            token_valid = True
            return token_valid
    except:
        return token_valid


def check_repo_exist():
    '''
        checking if kitaab repository exists.
    '''

    exist = False
    try:
        user.get_repo("My-Kitaab")
        exist = True
        return exist
    except:
        return exist


REPO_EXIST = check_repo_exist()


def create_github_note(noteName: str, noteContent: str):
    '''
        commit note to repository.
    '''

    if key is not None:
        repo = user.get_repo("My-Kitaab")
        repo.create_file(noteName, "added new note", noteContent)


def create_github_repo():
    '''
        create My-Kitaab repository.
    '''

    if key is not None and REPO_EXIST is False:
        print("please wait...")
        repo = user.create_repo("My-Kitaab")
        repo.create_file("readme.md", "add readme",
                         "## This repository is auto created by a note-taking app named kitaab.<br/>learn more https://github.com/Fareed-Ahmad7/Kitaab")
        notes = get_all_notes()
        for note in notes:
            create_github_note(note.name, note.content)


create_github_repo()


def edit_github_note_name(noteName: str, newName: str):
    '''
        commit new note name.
    '''

    if key is not None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.delete_file(file.path, "deleted note", file.sha)
        note_content = get_note(newName)
        create_github_note(newName, note_content)


def edit_github_note_content(noteName: str, newContent: str):
    '''
        commit new note content.
    '''

    if key is not None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.update_file(file.path, "edited note content",
                         newContent, file.sha)


def delete_github_note(noteName: str):
    '''
        delete note from the repository.
    '''

    if key is not None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.delete_file(file.path, "deleted note", file.sha)


def loop():

    response = input("🦄 ")

    try:
        # Help
        if response == 'help':
            Help()
            loop()

        # Quit
        elif response in ('quit', 'q'):
            console.print("exited successfully!", style="orchid1")
            os._exit(0)

        # Board
        elif response == 'board':
            print_board()
            loop()

        # Add Token
        elif response == 'add-token':
            console.print("Adding token requires restart!", style="yellow3")
            token = input("Enter github personal access token: ")
            add_token(token)
            token_valid = check_token_validity()
            if token_valid is False:
                drop_token()
                console.print(
                    "[red]Invalid token[/] -- please check your token or add a new one", style="light_coral")

        # Create Note
        elif int(response) == 1:
            idx = 0
            note_name = input("Name: ")
            note_content = input("Content: ")
            date = datetime.today().strftime('%d/%b/%H:%M')
            note = Note(idx, note_name, note_content, date)
            create_note(note)
            create_github_note(note_name, note_content)
            clear()
            app()

        # Update Note Name
        elif int(response) == 2:
            note_name = str(input("Note name: "))
            new_name = str(input("New name: "))
            date = datetime.today().strftime('%d/%b/%H:%M')
            update_note_name(note_name, new_name, date)
            edit_github_note_name(note_name, new_name)
            clear()
            app()

        # Update Note Content
        elif int(response) == 3:
            note_name = str(input("Note name: "))
            new_content = str(input("New content: "))
            date = datetime.today().strftime('%d/%b/%H:%M')
            update_note_content(note_name, new_content, date)
            edit_github_note_content(note_name, new_content)
            clear()
            app()

        # Delete Note
        elif int(response) == 4:
            note_name = str(input("Note name: "))
            delete_note(note_name)
            delete_github_note(note_name)
            clear()
            app()

        else:
            error()
            loop()
    except:
        console.print("oops! invalid text input 😓", style="orchid2")
        console.print(
            "use [orchid2]help[/] to list all existing input", style="indian_red1")
        loop()


def app():
    clear()
    print_table()
    menu()
    loop()


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        clear()
        sys.exit(0)
