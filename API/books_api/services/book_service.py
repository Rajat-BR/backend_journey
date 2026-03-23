from fastapi import HTTPException
from schemas import Book
from database import get_connection

def format_book(row):
    book = {
            "id": row["id"],
            "title": row["title"],
            "author": row["author"],
            "is_read": bool(row["is_read"])
        }
    return book

def create_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books(title, author, is_read)
        VALUES (?, ?, ?)
        """,
        (book.title, book.author, book.is_read))
    
    conn.commit()
    conn.close()


def get_books(author: str | None,
              is_read: bool | None, 
              sort: str | None, 
              order: str | None,
              limit: int | None,
              offset: int | None
              ):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM books"
    conditions = []
    values = []

    #Filtering
    if author is not None:
        conditions.append("author = ?")
        values.append(author)

    if is_read is not None:
        conditions.append("is_read = ?")
        values.append(is_read)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    allowed_sorts = ["id", "title"]
    allowed_orders = ["asc", "desc"]


    #Sorting and directing
    if sort is not None:
        if sort not in allowed_sorts:
            conn.close()
            raise HTTPException(status_code=400, detail="Invalid sort field")
        
        if order is None:
            order = "asc"

        if order not in allowed_orders:
            conn.close()
            raise HTTPException(status_code=400, detail="Invalid order field")
        
        query += f" ORDER BY {sort} {order}"
    
    elif order is not None:
        conn.close()
        raise HTTPException(status_code=400, detail="Order requires sort first")


    #Limit and Offset
    if limit is not None:
        if limit <= 0:
            conn.close()
            raise HTTPException(status_code=400, detail="Invalid limit field")
        
        if offset is not None and offset < 0:
            conn.close()
            raise HTTPException(status_code=400, detail="Invalid offset field")
        
        if offset is None:
            offset = 0
        
        query += " LIMIT ? OFFSET ?"
        values.append(limit)
        values.append(offset)
    
    elif offset is not None:
        conn.close()
        raise HTTPException(status_code=400, detail="Limit must exist before offset")
        
        
    cursor.execute(query, tuple(values))
    rows = cursor.fetchall()

    conn.close()
    books = [format_book(row) for row in rows]
    
    return books

def get_book(book_id: int, ):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = format_book(row)
    conn.close()

    return book

def update_book(updated_book: Book, book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ? , author = ? , is_read = ?
        WHERE id = ?
        """,
        (updated_book.title, updated_book.author, updated_book.is_read, book_id))
    
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    
    conn.close()

def remove_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    
    conn.close()