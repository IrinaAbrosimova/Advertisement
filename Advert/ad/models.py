from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to="media/author")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to="media/category")
    subcriber =models.ManyToManyField(User, blank=True, verbose_name='Подписчик')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = RichTextUploadingField(verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    poster = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to="media/ad")
    draft = models.BooleanField('Черновик', default=False)
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def get_absolute_url(self):
        return f'/{self.id}'

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


class MediaFile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to="media/ad_shots/")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class StarRating(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(StarRating, on_delete=models.CASCADE, verbose_name="звезда")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.ad}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    draft = models.BooleanField('Не опубликован', default=True)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    ad = models.ForeignKey(Ad, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.ad}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
