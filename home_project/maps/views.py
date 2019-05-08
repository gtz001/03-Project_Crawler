from django.shortcuts import render
import json
from maps.models import address_info




def first_page(request):
    address_point = address_info.objects.all()
    address_longitude = []
    address_latitude = []
    address_data = []
    for i in range(len(address_point)):
        address_longitude.append(address_point[i].longitude)
        address_latitude.append(address_point[i].latitude)
        address_data.append(address_point[i].data)


    # # 调试代码测试用数据
    # address_longitude = [117.159879]
    # address_latitude = [39.107937]
    # address_data = ['测试４']



    return render(request, 'address.html',
                  {'address_longitude': json.dumps(address_longitude),
                   'address_latitude': json.dumps(address_latitude),
                   'address_data': json.dumps(address_data)})
