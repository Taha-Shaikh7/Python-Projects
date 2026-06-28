books={
    "harry poter":["author","publication","genra"],
    "red rose":["author1","publication1","genra1"],
    "mobile phone":["author2","publication2","genra2"]
}
print("Welcome To Library Managment System")
print("1.Add a book")
print("2.Delete a book")
print("3.Search a book")
print("4.Update a book")
print("5.View all books")
print("6.Exit")

user=int(input("Enter choice: "))
if user==1:
    bookname=input("Enter the book name: ")
    author=input("Enter the author name: ")
    publication=int(input("Enter the publiction year: "))
    genra=input("Enter the genra: ")
    books.update({bookname:[author,publication,genra]})
    print("Added successfully")

elif user==2:
    bookname=input("Enter the book name: ")
    if bookname in books:
        del books[bookname]
        print("Deleted Successfully")
    else:
        print("This book is not in library")

elif user==3:
    bookname=input("Enter the book name: ")
    if bookname in books:
        print(books[bookname])
    else:
        print("Book not found")

elif user==4:
    bookname=input("Enter the book name: ")
    if bookname in books:
            author=input("Enter the author name: ")
            publication=int(input("Enter the publiction year: "))
            genra=input("Enter the genra: ")
            books.update({bookname:[author,publication,genra]})
            print("Updated successfully")
    else:
        print("Book not found")
        
elif user==5:
    items=list(books.items())
    print(items)

elif user==6:
    print("Exiting...")
    exit()

else:
    print("Invalid")
