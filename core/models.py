from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models

User = get_user_model()


class UserModelMixin(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='%(class)ss',
        null=True
    )

    class Meta:
        abstract = True


class MaterialModelMixin(models.Model):
    material = models.ForeignKey(
        'core.Material',
        verbose_name=_('Material'),
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True


class DateInfoModelMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Material(UserModelMixin, DateInfoModelMixin):
    NEWS = 1
    ARTICLE = 2

    MATERIAL_TYPE_CHOICES = (
        (NEWS, 'news'),
        (ARTICLE, 'article'),
    )

    material_type = models.IntegerField(verbose_name=_('Type'), choices=MATERIAL_TYPE_CHOICES)
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    text = models.TextField(verbose_name=_('Text'))
    published = models.DateTimeField(verbose_name=_('Date published'), blank=True, null=True)

    def __str__(self):
        return f'{self.author.username}, {self.title}'

    @property
    def pluses(self):
        return self.marks.filter(mark=Mark.PLUS).count()

    @property
    def minuses(self):
        return self.marks.filter(mark=Mark.MINUS).count()

    class Meta:
        ordering = ('-published', '-added', '-updated')


class Comment(UserModelMixin, MaterialModelMixin, DateInfoModelMixin):
    text = models.TextField(verbose_name=_('Text'))

    def __str__(self):
        return f'{self.author.username}, {self.material.title}'

    class Meta:
        ordering = ('-added', '-updated')


class Mark(UserModelMixin, MaterialModelMixin, DateInfoModelMixin):
    PLUS = 1
    MINUS = 0
    MARK_CHOICES = (
        (PLUS, '+'),
        (MINUS, '-'),
    )

    mark = models.IntegerField(verbose_name=_('Mark'), choices=MARK_CHOICES)

    def __str__(self):
        return f'{self.author.username}, {self.material.title}, {self.mark}'

    class Meta:
        ordering = ('-added', '-updated')
