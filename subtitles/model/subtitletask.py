from django.db import models
from ckeditor.fields import RichTextField

class SubTitleTask(models.Model):
    primary_language = models.CharField(max_length=10, verbose_name='زبان اصلی')
    primary_subtitle = RichTextField(verbose_name='زیر نویس اولیه')
    cleaned_subtitle = RichTextField(null=True, blank=True, verbose_name='زیرنویس پاکسازی شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"subtitle #{self.id} - {self.primary_language}"

    class Meta:
        verbose_name = 'پردازش زیر نویس'
        verbose_name_plural = 'پردازش زیر نویس'
        ordering = ['-created_at']  # جدیدترین تسک های اولیه پردازش
