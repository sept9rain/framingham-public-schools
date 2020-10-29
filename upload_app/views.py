import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from djangoProject.settings import BASE_DIR


@csrf_exempt
def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")

        destination = open(os.path.join(BASE_DIR, os.path.join("data", myFile.name)), 'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("<br>Upload Finished!<br> The administrator will get a Email notifications once the Algorithm complete assignment.")



def upload_index(request):
    return render(request,"index.html")
