from django.db import models

# Create your models here.

class BaseModel(models.Model):
    status = models.BooleanField(default=True, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True

class Book(BaseModel):
    book_name = models.CharField(max_length=60, verbose_name='书名')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='价格')
    pic = models.ImageField(upload_to='pic', default='pic/1.jpg', verbose_name='头像')
    publish = models.ForeignKey(to='Press', on_delete=models.CASCADE,
                                db_constraint=False,
                                related_name='books')
    authors = models.ManyToManyField(to='Author', db_constraint=False, related_name='books')

    @property
    def authors_list(self):
        return self.authors.values('author_name', 'age', 'detail__phone')

    class Meta:
        db_table = "book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

class Press(BaseModel):
    press_name = models.CharField(max_length=60, verbose_name='名称')
    pic = models.ImageField(upload_to='pic', default='pic/1.jpg', name='头像')
    address = models.CharField(max_length=255, verbose_name='地址')

    class Meta:
        db_table = 'press'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name

class Author(BaseModel):
    author_name = models.CharField(max_length=128, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')

    class Meta:
        db_table = "author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    author = models.OneToOneField(to="Author", on_delete=models.CASCADE, related_name="detail")

    class Meta:
        db_table = "author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s的详情' % self.author.author_name