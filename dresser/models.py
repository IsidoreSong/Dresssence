from django.db import models

Feelings = ["happy", "sad"]
Characters = ["opening", "outgoing"]


class ColorFeeling(models.Model):
    color = models.OneToOneField(
        "ColorThird", on_delete=models.CASCADE
    )
    for feel in Feelings:
        exec(feel + "=models.FloatField()")


class ColorCharacter(models.Model):
    color = models.OneToOneField(
        "ColorThird", on_delete=models.CASCADE
    )
    for character in Characters:
        exec(character + "=models.FloatField()")


class ColorFirst(models.Model):
    name = models.CharField(max_length=20)


class ColorSecond(models.Model):
    name = models.CharField(max_length=20)
    color_first = models.ForeignKey(
        "ColorFirst", on_delete=models.CASCADE
    )


class ColorThird(models.Model):
    name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    color_second = models.ForeignKey(
        "ColorSecond", on_delete=models.CASCADE
    )


class ColorParing(models.Model):
    color = models.OneToOneField(
        "ColorThird", on_delete=models.CASCADE
    )
    red = models.FloatField()
    yellow = models.FloatField()


class Style(models.Model):
    name = models.CharField(max_length=20)


class StyleFeeling(models.Model):
    style = models.OneToOneField("Style", on_delete=models.CASCADE)
    for feel in Feelings:
        exec(feel + "=models.FloatField()")


class StyleCharacter(models.Model):
    style = models.OneToOneField("Style", on_delete=models.CASCADE)
    for character in Characters:
        exec(character + "=models.FloatField()")