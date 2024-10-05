import sys

from pymongo import MongoClient


class Library:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client['LibraryDB']
        self.collectionBooks = self.database.books

    def add_book(self, title):

        # .find() - Wypisuje wszystkie dokumenty w danej kolekcji według parametrów.
        # .find_one() - Wypisuje konkretny dokument zgodny z podanymi parametrami.
        # .insert_one() - Wstawianie nowego dokumentu do danej kolekcji.
        # .update_one() - Edytowanie konkretnego wyszukanego dokumentu według parametrów.

        new_id = self.collectionBooks.find_one(sort=[("_id", -1)])
        new_id = new_id["_id"] + 1
        print(new_id)

        self.collectionBooks.insert_one({"_id": new_id, "TITLE": title, "STATE": 'free'})
        return self.menu()

    def borrow_book(self, book_id):
        self.collectionBooks.update_one(book_id, {'$set': {'STATE': 'borrowed'}})
        return self.menu()

    def return_book(self, book_id):
        self.collectionBooks.update_one(book_id, {'$set': {'STATE': 'free'}})
        return self.menu()

    def view_available_books(self):
        for current_book in self.collectionBooks.find({"STATE": 'free'}):
            print(current_book, "\n")
        return self.menu()

    def view_all_books(self):
        for current_book in self.collectionBooks.find():
            print(current_book, "\n")
        return self.menu()

    def view_borrowed_books(self):
        for current_book in self.collectionBooks.find({"STATE": 'borrowed'}):
            print(current_book, "\n")
        return self.menu()

    def menu(self):
        choose = input(
            "1. Dodaj książkę\n2. Wypożycz książkę\n3. Zwrot książki\n4. Wyświetl wszystkie książki\n"    
            "5. Wyświetl dostępne książki\n6. Wyświetl wypożyczone książki\n7. Wyjdź\n\nWybierz opcję: ")
        if choose == '1':
            self.add_book(input("Podaj tytuł książki: "))
        elif choose == '2':
            self.borrow_book(int(input("Podaj ID książki: ")))
        elif choose == '3':
            self.return_book(int(input("Podaj ID książki: ")))
        elif choose == '4':
            self.view_all_books()
        elif choose == '5':
            self.view_available_books()
        elif choose == '6':
            self.borrow_book()
        elif choose == '7':
            sys.exit()


library = Library()
library.menu()