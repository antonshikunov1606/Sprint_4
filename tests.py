import pytest

from main import BooksCollector


class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')


        assert len(collector.get_books_genre()) == 2

    # проверяем что книга, содержащая в названии более 40 символов, не добавляется
    def test_add_new_book_with_more_40_characters_does_not_add(self):
        collector = BooksCollector()

        collector.add_new_book('Название книги которое содержит более 40 символов')

        assert len(collector.get_books_genre()) == 0

    # проверяем что дубликат книги не добавляется
    def test_add_new_book_add_dublicate_does_not_add(self):
        collector = BooksCollector()

        collector.add_new_book('Бойцовский клуб')
        collector.add_new_book('Бойцовский клуб')

        assert len(collector.get_books_genre()) == 1

    # проверяем что устанавливается жанр книги, если книга есть в books_genre
    # и её жанр входит в список genre
    def test_set_book_genre_sets_genre_if_book_exists_and_genre_is_valid(self):
        collector = BooksCollector()

        collector.add_new_book('Ущелье')
        collector.set_book_genre('Ущелье', 'Фантастика')
        expected = {'Ущелье': 'Фантастика'}

        assert collector.get_books_genre() == expected

    # проверяем что жанр не устанавливается, если книги нет в books_genre
    def test_set_book_genre_non_existent_book_genre_does_not_set(self):
        collector = BooksCollector()

        collector.set_book_genre('Оборотни', 'Фантастика')

        assert collector.get_book_genre('Оборотни') is None

    # проверяем что жанр не устанавливается если такого жанра нет в genre
    def test_set_book_genre_non_existent_genre_this_genre_does_not_set(self):
        collector = BooksCollector()

        collector.add_new_book('Оборотни')
        collector.set_book_genre('Оборотни', 'Триллеры')
        expected = ''

        assert collector.get_book_genre('Оборотни') == expected

    # проверяем вывод жанра книги по её имени
    def test_get_book_genre_book_exists_returns_correct_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Ущелье')
        collector.set_book_genre('Ущелье', 'Фантастика')
        expected = 'Фантастика'

        assert collector.get_book_genre('Ущелье') == expected

    # проверяем что возвращается пустая строка вместо жанра, если жанр книги не установлен
    def test_get_book_genre_book_without_genre_returns_empty_string(self):
        collector = BooksCollector()

        collector.add_new_book('Ущелье')
        expected = ''

        assert collector.get_book_genre('Ущелье') == expected

    # проверяем вывод списка книг с определённым жанром при условии, что они есть
    def test_get_books_with_specific_genre_book_exists_returns_book(self):
        collector = BooksCollector()

        books_to_add = [
            ('Ущелье', 'Фантастика'),
            ('От заката до рассвета', 'Фантастика')
        ]

        for name, genre in books_to_add:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        expected = ['Ущелье', "От заката до рассвета"]

        assert collector.get_books_with_specific_genre('Фантастика') == expected

    # проверяем что метод возвращает пустой список, если нет книг с указанным жанром
    def test_get_books_with_specific_genre_book_does_not_exist_not_books(self):
        collector = BooksCollector()

        expected = []

        assert collector.get_books_with_specific_genre('Ужасы') == expected

    # проверяем что метод get_books_genre возвращает словарь books_genre
    def test_get_books_genre_returns_book_genre(self):
        collector = BooksCollector()

        books_to_add = [
            ('Ущелье', 'Фантастика'),
            ('Новогодний корпоратив', 'Комедии')
        ]

        for name, genre in books_to_add:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        expected = {'Ущелье': 'Фантастика', 'Новогодний корпоратив': 'Комедии'}

        assert collector.get_books_genre() == expected

    # проверяем что метод get_books_for_children возвращает
    # книги всех жанров без возрастного рейтинга
    @pytest.mark.parametrize(
        'name, genre',
        [
            ['Дюна', 'Фантастика'],
            ['Шрек', 'Мультфильмы'],
            ['Такси', 'Комедии']
        ]
    )
    def test_get_books_for_children_not_age_rating_genres_return(self, name, genre):
        collector = BooksCollector()

        collector.add_new_book(name)
        collector.set_book_genre(name, genre)

        assert len(collector.get_books_for_children()) == 1

    # проверяем что метод get_books_for_children не возвращает
    # книги всех жанров с возрастным рейтингом
    @pytest.mark.parametrize(
        'name, genre',
        [
            ['Инсомния', 'Ужасы'],
            ['Восточный экспресс', 'Детективы']
        ]
    )
    def test_get_books_for_children_age_rating_genres_do_not_return(self, name, genre):
        collector = BooksCollector()

        collector.add_new_book(name)
        collector.set_book_genre(name, genre)

        assert len(collector.get_books_for_children()) == 0

    # проверяем что метод add_book_in_favorites добавляет одну
    # книгу в избранное, если она находится в словаре books_genre
    def test_add_book_in_favorites_add_one_existing_book(self):
        collector = BooksCollector()

        collector.add_new_book('Инсомния')
        collector.add_book_in_favorites('Инсомния')

        assert len(collector.favorites) == 1

    # проверяем что метод add_book_in_favorites добавляет
    # книги в избранное, если они находятся в словаре books_genre
    def test_add_book_in_favorites_add_multiply_existing_books(self):
        collector = BooksCollector()

        collector.add_new_book('Инсомния')
        collector.add_new_book('Задача трех тел')
        collector.add_book_in_favorites('Инсомния')
        collector.add_book_in_favorites('Задача трех тел')

        assert len(collector.favorites) == 2

    # проверяем что метод add_book_in_favorites не добавляет
    # книгу в избранное, если её нет в словаре books_genre
    def test_add_book_in_favorites_add_non_existing_book_does_not_add(self):
        collector = BooksCollector()

        collector.add_new_book('Инсомния')
        collector.add_book_in_favorites('Такси')

        assert len(collector.favorites) == 0

    # проверяем что метод add_book_in_favorites не добавляет
    # повторно одну книгу, если она уже есть в списке favorites
    def test_add_book_in_favorites_add_duplicate_book_does_not_add(self):
        collector = BooksCollector()

        collector.add_new_book('Инсомния')
        collector.add_book_in_favorites('Инсомния')
        collector.add_book_in_favorites('Инсомния')

        assert len(collector.favorites) == 1

    # проверяем что метод delete_book_from_favorites удаляет
    # книгу из списка favorites
    def test_delete_book_from_favorites_existent_book_from_favorites_is_deleted(self):
        collector = BooksCollector()

        collector.add_new_book('Задача трех тел')
        collector.add_book_in_favorites('Задача трех тел')
        collector.delete_book_from_favorites('Задача трех тел')

        assert len(collector.favorites) == 0

    # проверяем что метод не удаляет книги из списка favorites, если указанной
    # книги нет в этом списке
    def test_delete_book_from_favorites_non_existent_book_is_not_deleted(self):
        collector = BooksCollector()

        collector.add_new_book('Задача трех тел')
        collector.add_book_in_favorites('Задача трех тел')
        collector.delete_book_from_favorites('Мои идеи')

        assert len(collector.favorites) == 1

    # проверяем что метод get_list_of_favorites_books возвращает
    # список favorites, содержащая одну книгу
    def test_get_list_of_favorites_books_one_book_in_favorites_returns_this_book(self):
        collector = BooksCollector()

        collector.add_new_book('Куджо')
        collector.add_book_in_favorites('Куджо')
        expected = ['Куджо']

        assert collector.get_list_of_favorites_books() == expected

    # проверяем что метод возвращает полный список favorites
    # при добавлении туда нескольких книг
    def test_get_list_of_favorites_books_multiply_books_in_favorites_returns_full_list(self):
        collector = BooksCollector()

        books_to_add = [
            'Собачье сердце',
            '100 дней'
        ]
        for book in books_to_add:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        expected = ['Собачье сердце', '100 дней']

        assert collector.get_list_of_favorites_books() == expected

    # проверяем что метод возвращает пустой список, если в favorites
    # нет книг
    def test_get_list_of_favorites_no_books_in_favorites_returns_empty_list(self):
        collector = BooksCollector()

        expected = []

        assert collector.get_list_of_favorites_books() == expected
