from django.db import models

# Create your models here.
class ColorMedium(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color_tag = models.CharField(max_length=20, null=True)

    def rgb_front(self):
        return "(" + self.color_tag.replace("-", ",") + ")"

    def __str__(self):
        return self.name


class ColorBasic(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color_tag = models.CharField(max_length=20, null=True)
    color_medium = models.ForeignKey(
        "ColorMedium", on_delete=models.CASCADE, null=True
    )

    def rgb_front(self):
        return "(" + self.color_tag.replace("-", ",") + ")"

    def __str__(self):
        return self.name


class Color(models.Model):
    hlc = models.CharField(max_length=20)
    rgb = models.CharField(max_length=20)
    color_basic = models.ForeignKey(
        "ColorBasic", on_delete=models.CASCADE
    )

    def rgb_front(self):
        return "(" + self.rgb.replace("-", ",") + ")"

    def hlc_rgb(self):
        return [hlc, self.rgb_front]

    def __str__(self):
        return self.hlc
