from django.views.decorators.http import (
    require_http_methods,
    require_GET,
    require_POST,
)
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render
import json
from . import models

# Create your views here.
WAITING = "待定"


def index(request):
    return render(request, "index.html")


@require_GET
def get_color_tags(request):
    response = {}
    color_medium = models.ColorMedium.objects.all()
    color_mediums, color_basics = [], []
    for item in color_medium:
        color_basic = item.colorbasic_set.all()
        color_mediums.append(
            [
                item.name,
                item.rgb_front(),
            ]
        )
        color_basics.append(
            [[bas.name, bas.rgb_front()] for bas in color_basic]
        )
    # color_basic = [color_basic.color]
    try:
        response["color_tags"] = [color_mediums, color_basics]
    except:
        pass
    return JsonResponse(response)


@require_GET
def get_complete_color(request):
    response = {}
    color_medium = models.ColorMedium.objects.all()
    color_mediums = []
    for item in color_medium:
        color_basic = item.colorbasic_set.all()
        color_mediums.append(
            [  # medium
                item.name,
                item.rgb_front(),
                [  # basic
                    [
                        bas.name,
                        bas.rgb_front(),
                        [  # color
                            [color.hlc, color.rgb_front()]
                            for color in bas.color_set.all()
                        ],
                    ]
                    for bas in color_basic
                ],
            ]
        )
    try:
        response["color"] = [color_mediums]
    except:
        pass
    return JsonResponse(response)


@require_GET
def get_colors(request):
    response = {}
    color_medium = models.ColorMedium.objects.all()
    # color_basic = models.ColorBasic.objects.all()
    colors = [
        [(col.hlc, col.rgb_front()) for col in bas.color_set.all()]
        for medium in color_medium
        for bas in medium.colorbasic_set.all()
    ]

    try:
        response["colors"] = colors
    except:
        pass
    return JsonResponse(response)


@csrf_exempt
def changeColor(request):

    changeRecords = None
    try:
        # print(request.POST["changeRecords"])
        changeRecords = json.loads(request.POST["changeRecords"])
        print(len(changeRecords))
        # return HttpResponse(f"已保存{len(changeRecords)}条数据")
        for record in changeRecords:
            # print(record)
            if record["opType"] == "color":
                # def opColor(record):
                current, target, bgcs = (
                    record["current"],
                    record["target"],
                    record["bgcs"],
                )

                print("color", current, target, len(bgcs))
                hlcs = []
                for bgc in bgcs:
                    hlcs.append(bgc[0])
                models.Color.objects.filter(hlc__in=hlcs).update(
                    color_basic=models.ColorBasic.objects.get(
                        name=target
                    )
                )

            elif record["opType"] == "basic":
                current, target = record["current"], record["target"]
                print("basic", current, target)
                if current == -1:
                    models.ColorBasic.objects.create(
                        name=target[1][0],
                        color_tag="-".join(
                            target[1][1][1:-1].split(",")
                        ),
                        color_medium=models.ColorMedium.objects.get(
                            name=target[0]
                        ),
                    )

                elif target == -1:
                    models.ColorBasic.objects.get(
                        name=current,
                    ).delete()
                else:
                    target_medium = models.ColorMedium.objects.get(
                        name=target,
                    )
                    models.ColorBasic.objects.filter(
                        name=current,
                    ).update(color_medium=target_medium)

            elif record["opType"] == "medium":
                current, target = record["current"], record["target"]
                print("medium", current[0], target[0])
                if current == -1:
                    target_medium = models.ColorMedium(
                        name=target[0],
                        color_tag="-".join(
                            target[1][1:-1].split(",")
                        ),
                    )
                    target_medium.create()
                    basics = []
                    for bas in target[2]:
                        basics.append(
                            models.ColorBasic(
                                name=target[0],
                                color_tag="-".join(
                                    target[1][1:-1].split(",")
                                ),
                                color_medium=target_medium,
                            )
                        )
                    models.ColorBasic.objects.bulk_create(basics)

                elif target == -1:
                    current_medium = models.ColorMedium.objects.get(
                        name=current[0],
                    )
                    basics = current_medium.colorbasic_set.all()
                    basics.delete()
                    current_medium.delete()

    except Exception as e:
        print(e)

    return HttpResponse(f"已保存{len(changeRecords)}条数据")
