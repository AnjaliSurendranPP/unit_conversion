from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
conversion={
        "km":{
            "m":1000,
            "cm":100000
        },
        "m":{
            "km":0.001,
            "cm":100
        },
        "cm":{
            "m":0.01,
            "km":0.00001
        }
    }
@method_decorator(csrf_exempt,name='dispatch')
class UnitConverterView(View):
    def get(self,request):
        value=5
        result=value*1000
        return JsonResponse({
            "original":value,
            "from":"km",
            "to":"m",
            "converted_value":result
        })
    
    def post(self,request):
        try:
            data=json.loads(request.body)
            value=data.get("value")
            from_unit=data.get("from_unit")
            to_unit=data.get("to_unit")
            # print(value,from_unit,to_unit)
            if from_unit not in conversion:
                return JsonResponse({"error":"invalid from unit"},status=400)
            if to_unit not in  conversion:
                return JsonResponse({"error":"invalid to unit"},status=400)

            result=value*conversion[from_unit][to_unit]
            # print(result)
            return JsonResponse({
                "value":value,
                "from_unit":from_unit,
                "to_unit":to_unit,
                "result":round(result,4)
            })
        except (ValueError,TypeError,json.JSONDecodeError):
            return JsonResponse({"error":"invalid"},status=400)