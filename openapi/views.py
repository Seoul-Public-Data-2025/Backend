import requests
from geopy.geocoders import Nominatim
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CCTVSerializer,PoliceOfficeSerializer
from .models import CCTV,PoliceOffice
import os
import time
class PoliceOfficeFetchView(APIView):
    def get(self,request,*args,**kwargs):
        service_key = os.getenv("SERVICE_KEY")
        police_api_url=f'https://api.odcloud.kr/api/15077036/v1/uddi:dc5ea479-c327-4ae7-916c-e52e3784b6ef?serviceKey={service_key}'
        police_params = {
            "page": 1,
            "perPage": 30,
            "returnType": "json",
        }
        try:
            response = requests.get(police_api_url, params=police_params)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        
        police_data = response.json().get("data", [])
        geolocator = Nominatim(user_agent="SeoulMaum",timeout=None)
        created = []
        for item in police_data:
            address = item.get("도로명주소")
            if not address or "서울" not in address:
                continue
            office_name = item.get("전체기관명")
            start = time.time()
            location = geolocator.geocode(address)
            print(f"Geocode took: {time.time() - start:.2f} seconds")
            if not location:
                continue
            
            lat = location.latitude
            lot = location.longitude
            
            try:
                # get_or_create로 중복 여부 체크
                office, created_flag = PoliceOffice.objects.get_or_create(
                    lat=lat,
                    lot=lot,
                    defaults={
                        "officeName": office_name,
                        "addr": address,
                    }
                )
                if created_flag:
                    created.append(office)
            except Exception as e:
                continue
        serializer = PoliceOfficeSerializer(created, many=True)
        return Response({
            'success':True,
            'data':{
                'policeOffice': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        
        
class CCTVFetchView(APIView):
    def get(self, request, *args, **kwargs):
        district_code = request.query_params.get('district_code')
        if not district_code:
            return Response({
                'success': False,
                'data':{
                    'error': 'district_code query param is required'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        api_key = os.getenv("OPEN_API_KEY")
        base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/safeOpenCCTV_{district_code}"
        initial_url=f"{base_url}/1/1/"
        response = requests.get(initial_url)
        
        if response.status_code != 200:
            return Response({
                'success':False,
                'data':{
                        'error': 'Failed to fetch data from API'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        data = response.json()
        data_key = f"safeOpenCCTV_{district_code}"
        total_count = data.get(data_key, {}).get('list_total_count', 0)
        if total_count == 0:
            return Response({
                'success':False,
                'data':{
                        'message': 'No CCTV data available for this district'
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        
        per_page = 1000
        cctvs = []
        for start in range(1, total_count + 1, per_page):
            end = min(start + per_page - 1, total_count)
            paginated_url = f"{base_url}/{start}/{end}/"
            response = requests.get(paginated_url)
            
            if response.status_code == 200:
                batch = response.json().get(data_key, {}).get('row', [])
                cctvs.extend(batch)
                
        saved_instances = []
        for cctv in cctvs:
            try:
                instance = CCTV.objects.create(
                    district=cctv.get('SVCAREAID'),
                    lat=cctv.get('WGSXPT'),
                    lot=cctv.get('WGSYPT'),
                    addr=cctv.get('ADDR'),
                )
                saved_instances.append(instance)

            except Exception as e:
                continue
            
        serializer = CCTVSerializer(saved_instances, many=True)
        return Response({
            'success':True,
            'data':{
                'message': f'{len(saved_instances)} CCTV records saved successfully',
                'cctv': serializer.data
                }
            }, status=status.HTTP_200_OK)