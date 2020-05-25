from django.shortcuts import render
from .models import Jiancheng
# Create your views here.
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import JianchengSerializers
from rest_framework.decorators import list_route, detail_route
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.classification import accuracy_score
import logging
import datetime
logger = logging.getLogger(__name__)
def index(request):
    jiancheng_data=Jiancheng.objects.all()
    return render(request,"index.html",locals())

class JianchengViewsSet(viewsets.ModelViewSet):
    queryset =Jiancheng.objects.all()
    serializer_class = JianchengSerializers

    @list_route(methods=['post'])
    def y_search(self,request):
        y_data=request.POST.get("y_data")
        y_data=int(y_data)
        if request.POST.get("y_range") == "=":
            data_y=Jiancheng.objects.filter(data_y=y_data).values("data_y","data_x","id")
        elif request.POST.get("y_range") == ">":
            data_y = Jiancheng.objects.filter(data_y__gt=y_data).values("data_y","data_x","id")
        elif request.POST.get("y_range") == ">=":
            data_y = Jiancheng.objects.filter(data_y__gte=y_data).values("data_y","data_x","id")
        elif request.POST.get("y_range") == "<":
            data_y = Jiancheng.objects.filter(data_y__lt=y_data).values("data_y","data_x","id")
        else:
            data_y = Jiancheng.objects.filter(data_y__lte=y_data).values("data_y","data_x","id")
        return JsonResponse(list(data_y),safe=False)

    @list_route(methods=['post'])
    def x_search(self,request):
        x_data = request.POST.get("x_data")
        x_data = int(x_data)
        if request.POST.get("x_range") == "=":
            data_x = Jiancheng.objects.filter(data_x=x_data).values("data_y", "data_x", "id")
        elif request.POST.get("x_range") == ">":
            data_x = Jiancheng.objects.filter(data_x__gt=x_data).values("data_y", "data_x", "id")
        elif request.POST.get("x_range") == ">=":
            data_x = Jiancheng.objects.filter(data_x__gte=x_data).values("data_y", "data_x", "id")
        elif request.POST.get("x_range") == "<":
            data_x = Jiancheng.objects.filter(data_x__lt=x_data).values("data_y", "data_x", "id")
        else:
            data_x = Jiancheng.objects.filter(data_x__lte=x_data).values("data_y", "data_x", "id")
        return JsonResponse(list(data_x), safe=False)
    def joinstring(self,string, symbol):
        string = "".join(string.split(symbol))
        return string


    def undate(self):
        date = str(datetime.datetime.now())
        new_date = self.joinstring(self.joinstring(self.joinstring(date, " "), "-"), ":").split(".")[0]
        return new_date

    def plotdata(self,x,y,filename):
        import plotly.graph_objects as go
        from plotly.offline import plot
        import plotly.io
        fig = go.Figure([go.Bar(x=x, y=y)])

        plotly.io.write_image(fig=fig, file=r"C:\Users\user\PycharmProjects\ScrapyNews\Jiancheng\app\static\images\{}.jpg".format(filename))


    @list_route(methods=['post'])
    def drawing(self,request):
        data_list=request.POST.get("data_list")
        data_list=eval(data_list)
        print(data_list)
        filename = self.undate()
        self.plotdata(data_list[0],data_list[1],filename)
        word={"imgpath":"/images/{}.jpg".format(filename)}
        return JsonResponse(word)
