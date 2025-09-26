from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
import datetime

from books.forms import BookForm
from books.models import Book, Category

class TestBook(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.category1 = Category.objects.create(title="Fiction")
        cls.category2 = Category.objects.create(title="Science")
        cls.category3 = Category.objects.create(title="History")        

        cls.user1 = User.objects.create_user(
            username = 'user1',
            email = 'user1@gmail.com',
            phone_number = "09121234567",
            password = "password1"
        )

        cls.user2 = User.objects.create_user(
            username = 'user2',
            email = "user2@gmail.com",
            phone_number = "09112345678",
            password = "password2"
        )

        cls.admin = User.objects.create_superuser(
            username = "admin",
            email = "admin@gmail.com",
            phone_number = "09134567891"
        )

        cls.book1 = Book.objects.create(
            user = cls.user1,
            title = "Title1",
            description = "Text1",
            author = "Author1",
            status = "R",
            category = cls.category1,
            shabak_number = "9781234567891",
            modified_datetime = timezone.now() - datetime.timedelta(days=1)
        )

        cls.book2 = Book.objects.create(
            user = cls.user2,
            title = "Title2",
            description = "Text2",
            author = "Author2",
            category = cls.category2,
            shabak_number = "9781234567892",
            status = "NR",
            modified_datetime = timezone.now() - datetime.timedelta(days=2)
        )

        cls.book3 = Book.objects.create(
            user = cls.admin,
            title = "Title3",
            description = "Text3",
            author = "Author3",
            category = cls.category3,
            shabak_number = "9781234567893",
            status = "B",
            modified_datetime = timezone.now() - datetime.timedelta(days=3)
        )

    def test_user_information(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.email, 'user1@gmail.com')
        self.assertEqual(self.user1.phone_number, "09121234567")

        self.assertEqual(self.user2.username, 'user2')
        self.assertEqual(self.user2.email, 'user2@gmail.com')
        self.assertEqual(self.user2.phone_number, "09112345678")


class TestBookList(TestBook):

    def test_book_list_view(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)

    def test_book_list_name_view(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertEqual(response.status_code, 200)

    def test_book_list_template(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertTemplateUsed("books/books_list_page.html")

    def test_book_list_view_content(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book2.title)
        self.assertIn(self.book1, response.context["books"])
        self.assertIn(self.book2, response.context["books"])

    def test_book_list_empty(self):
        Book.objects.all().delete()
        response = self.client.get(reverse("books:book-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["books"]), 0)

    def test_book_list_ordering(self):
        response = self.client.get(reverse("books:book-list"))
        books = response.context['books']
        self.assertEqual(books[0], self.book3)  # Most recent
        self.assertEqual(books[1], self.book2)
        self.assertEqual(books[2], self.book1)  # Oldest


class TestBookDetail(TestBook):

    def test_book_detail_url(self):
        response = self.client.get(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, 200) 
    
    def test_book_detail_name(self):
        response = self.client.get(reverse("books:book-detail", kwargs={"pk": self.book1.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_view_content(self):
        url = reverse('books:book-detail', kwargs={"pk": self.book1.id})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book1.description)
        self.assertEqual(response.context['book'], self.book1)
    
    def test_blog_detail_invalid_pk(self):
        response = self.client.get(reverse('books:book-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class TestBookCreate(TestBook):

    def test_book_create_view_url(self):
        response = self.client.get("/books/create/")
        self.assertEqual(response.status_code, 200)

    def test_book_create_view_name(self):
        response = self.client.get(reverse("books:book-create"))
        self.assertEqual(response.status_code, 200)

    def test_book_template_used(self):
       response = self.client.get(reverse("books:book-create"))
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, "books/book_create_page.html")

    def test_book_view_form(self):
        url = reverse('books:book-create')  
        response = self.client.post(  
            path=url,
            data={
            "user":self.user1.id,
            "title":"Title4",
            "author":"Author4",
            "description":"Text4",
            "category":self.category2.id, 
            "shabak_number":"9783161484100",
            "status": "R",
            "modified_datetime":timezone.now(),
            },
        )
        
        # Debug: Print form errors if status is not 302
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        book = Book.objects.first()
        self.assertIsNotNone(book)  
        self.assertEqual(Book.objects.first().user, self.user1)
        self.assertEqual(Book.objects.first().title, 'Title4')
        self.assertEqual(Book.objects.first().description, 'Text4')
        self.assertEqual(Book.objects.first().status, 'R')
        self.assertEqual(response.url, book.get_absolute_url())  # Check redirect URL


class TestBookUpdate(TestBook):
    
    def test_book_update_url(self):
        response = self.client.get(f"/books/{self.book1.id}/update/")
        self.assertEqual(response.status_code, 200)
    
    def test_book_update_name(self):
        response = self.client.get(reverse("books:book-update", kwargs={"pk": self.book1.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_update_template_used(self):
        response = self.client.get(reverse("books:book-update", kwargs={"pk": self.book1.id}))
        self.assertTemplateUsed(response, "books/book_update_page.html")

    def test_book_update_context(self):
        response = self.client.get(reverse("books:book-update", kwargs={"pk": self.book1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["book"], self.book1)
        self.assertIsInstance(response.context["form"], BookForm)
    
    def test_book_update_form_submission(self):
        update_date = {
            "user":self.user1.id,
            "title":"Updated Title",
            "author":"Updated Author",
            "description":"Updated Description",
            "category":self.category3.id, 
            "shabak_number":"9783161484101",
            "status": "NR",
        }

        url = reverse("books:book-update", kwargs={"pk": self.book1.id})
        response = self.client.post((url), data=update_date)

        if response.status_code != 302:
            print(f"Form submission failed: {response.context["form"]}")
        
        self.assertEqual(response.status_code, 302, f"Expected redirect, got status {response.status_code}")

        # Verify the book was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")
        self.assertEqual(self.book1.author, "Updated Author")
        self.assertEqual(self.book1.description, "Updated Description")
        self.assertEqual(self.book1.shabak_number, "9783161484101")
        self.assertEqual(self.book1.category, self.category3)
        self.assertEqual(self.book1.status, "NR")


class BookDeleteTest(TestBook):
    
    def test_book_delete_url(self):
        response = self.client.get(f"/books/{self.book1.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_book_delete_name(self):
        response = self.client.get(reverse("books:book-delete", kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_delete_template_used(self):
        response = self.client.get(reverse("books:book-delete", kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_delete_page.html")


    def test_blog_delete_form_submission(self):
        response = self.client.post(reverse("books:book-delete", kwargs={"pk": self.book1.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())  
        self.assertRedirects(response, reverse('books:book-list'))

        
    def test_book_delete_invalid_pk(self):
        response = self.client.post(reverse("books:book-delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)  # Non-existent blog  