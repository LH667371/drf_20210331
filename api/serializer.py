from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer

from api.models import Press, Book


class PressModeSerializer(ModelSerializer):
    """出版社序列化器"""

    class Meta:
        model = Press
        fields = ('press_name', 'address')


class BookModelSerializer(ModelSerializer):
    """图书的序列化器"""
    publish = PressModeSerializer()

    class Meta:
        model = Book
        fields = ('book_name', 'price', 'pic', 'publish', 'authors_list')


class BookDeModelSerializer(ModelSerializer):
    """
    反序列化器  数据入库时使用
    """

    class Meta:
        model = Book

        fields = ("book_name", "price", "publish", "authors")

        # 添加DRF官方所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填项
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度太短了"
                }
            },
            "price": {
                "max_digits": 10,
            }
        }

    def validate_book_name(self, value):
        book = Book.objects.filter(book_name=value)
        if book:
            raise exceptions.ValidationError("图书名已存在")
        return value

    def validate(self, attrs):
        return attrs


class BookModelSerializerV2(ModelSerializer):
    """序列化器与反序列化器整合"""

    class Meta:
        model = Book
        # 字段应该写哪些  应该写参与序列化与反序列化的并集
        fields = ("book_name", "price", "publish", "authors", "pic")

        # 添加DRF官方所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填项
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度太短了"
                }
            },
            # 指定该字段只参与反序列化  保存时提交
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            # 指定该字段只参与序列化  查询时使用
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        book = Book.objects.filter(book_name=value)
        if book:
            raise exceptions.ValidationError("图书名已存在")
        return value

    def validate(self, attrs):
        # 可以自定义校验规则
        price = attrs.get("price")
        if price > 1000:
            raise exceptions.ValidationError("超过最高价格了~~")
        return attrs
