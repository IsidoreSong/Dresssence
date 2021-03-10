import os, sys
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dresssence.settings")
import django

django.setup()

from colorClassifier.models import ColorMedium, ColorBasic, Color


def createColorMedium(color_class, Create=False):

    color_medium = list(
        set(color_class["color_medium"].dropna().to_list())
    )
    color_medium.sort(reverse=True)
    color_medium = [
        ColorMedium(name=med, color_tag="(222,222,22)")
        for (i, med) in enumerate(color_medium)
    ]
    color_medium.sort(key=lambda x: x.name, reverse=True)
    if Create:
        ColorMedium.objects.all().delete()
        ColorMedium.objects.bulk_create(color_medium)


def createColorBasic(color_class, Create=False):

    basic_medium = {
        basic: medium
        for (basic, medium) in zip(
            color_class["color_basic"].dropna(),
            color_class["color_medium"].dropna(),
        )
    }

    color_basic = [
        ColorBasic(
            name=item[0],
            color_tag="(222,222,22)",
            color_medium=ColorMedium.objects.get(name=item[1]),
        )
        for (i, item) in enumerate(basic_medium.items())
    ]

    color_basic.sort(key=lambda x: x.color_medium.name, reverse=True)

    if Create:
        ColorBasic.objects.all().delete()
        ColorBasic.objects.bulk_create(color_basic)


def createColor(color_class, colors, Create=False):
    Color.objects.all().delete()
    hlc_rgb = {hlc: rgb for (hlc, rgb) in zip(colors.hlc, colors.rgb)}
    colors = []
    color_basic = {
        item.name: item for item in ColorBasic.objects.all()
    }
    for (i, column) in enumerate(
        list(
            filter(
                lambda x: not x.startswith("c"),
                color_class.columns.to_list(),
            )
        )
    ):
        for (j, col) in enumerate(color_class[column].dropna()):
            colors.append(
                Color(
                    hlc=col,
                    rgb=hlc_rgb[col],
                    color_basic=color_basic[column],
                )
            )
    colors.sort(key=lambda x: x.hlc)
    if Create:
        Color.objects.all().delete()
        Color.objects.bulk_create(colors)


def tidingColor():
    for bas in ColorBasic.objects.all():
        colors = bas.color_set.all()
        if len(colors):
            r, g, b = [], [], []
            for color in colors:
                rgb = color.rgb.split("-")
                r.append(int(rgb[0]))
                g.append(int(rgb[1]))
                b.append(int(rgb[2]))
            r, g, b = (
                sum(r) // len(r),
                sum(g) // len(g),
                sum(b) // len(b),
            )
            # print("-".join([str(r), str(g), str(b)]))
            bas.color_tag = "-".join([str(r), str(g), str(b)])
            bas.save()
    for med in ColorMedium.objects.all():
        basics = med.colorbasic_set.all()
        r, g, b = [], [], []
        for basic in basics:
            rgb = basic.color_tag.split("-")
            r.append(int(rgb[0]))
            g.append(int(rgb[1]))
            b.append(int(rgb[2]))
        r, g, b = sum(r) // len(r), sum(g) // len(g), sum(b) // len(b)
        # print("-".join([str(r), str(g), str(b)]))
        med.color_tag = "-".join([str(r), str(g), str(b)])
        med.save()


def clearColor():
    Color.objects.all().delete()
    ColorBasic.objects.all().delete()
    ColorMedium.objects.all().delete()


def main():
    # clearColor(),return

    if len(sys.argv) > 1:
        clearColor()
    create = True
    color_class = pd.read_excel(
        "../ZYX/Docs/color-classification.xlsx", sheet_name="Sheet2"
    )
    colors = pd.read_csv("../ZYX/Docs/colors.csv")
    createColorMedium(color_class, create)
    createColorBasic(color_class, create)
    createColor(color_class, colors, create)
    tidingColor()


if __name__ == "__main__":
    main()