import csv
import os


def save_book_to_csv_file(book_info: dict, category: str = 'uncategorized') -> None:
    """One csv file per category with each book in it."""

    # on first use, create Data/image
    if not os.path.exists("./Data"):
        os.makedirs("./Data/image")

    
    csv_columns = book_info.keys()
    csv_file = f"Data/{category}.csv"

    # If file doesn't exist, we need to write the header first :
    if os.path.exists(csv_file) and os.path.getsize(csv_file) != 0:
        with open(csv_file, 'a') as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=csv_columns
            )
            writer.writerow(book_info)
    else:
        with open(csv_file, 'w') as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=csv_columns
            )
            writer.writeheader()
            writer.writerow(book_info)


if __name__ == "__main__":
    from book_page import get_book_info
    book_info = get_book_info(
        'http://books.toscrape.com/catalogue/the-requiem-red_995/index.html'
    )
    # print(book_info)
    save_book_to_csv_file(book_info)
