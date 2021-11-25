# BOOK SCRAPING

## Description

Beta version of the web library scraping.
This program will scrap all book per category of the [books to scrape](http://books.toscrape.com) website storing them in csv file.
<details>
<summary>
The information provided are :
</summary>

- product_page_url
- universal_product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
</details>

The program offers the choice to download the book's cover.
<details>
<summary>
The data structure is as follows :
</summary>

```
Project/
├── __init__.py
├── requirements.txt
├── README.md
├── main.py
├── web_scraping/
│ ├── __init__.py
│ ├── client.py
│ ├── category_page.py
│ └── book_page.py
├── infrastructure/
│ ├── repository.py
│ └── __init__.py
└── Data/
  ├── image
  └── book

```

</details>

## Installation

First clone the project and move in it :
> git clone git@github.com:Riazzor/books_2_scrap.git

### Without virtual environment :
> pip install -r requirements.txt

### With virtual environment :
Multiple choice are available to handle your Virtual environment. My choice goes to [Pipenv](https://github.com/pypa/pipenv) for small project.

I will show you on virtualenv for now :
> pip install virtualenv
>
> virtualenv venv # create a folder named venv containing your virtual environment

You can name it venv or any other name. Just make sure to replace it in the next command if you choose another name.

On linux and mac :
> source venv/bin/activate # to activate your environment
>
> pip install -r requirements.txt

On Windows :
> venv/Scripts/activate
>
> pip install -r requirements.txt


## How to use
From the root of your project (if you have one, activate your environment)
> python3 -m main

Type 'oui' or 'non' when prompted to decide if you want the book's cover.

