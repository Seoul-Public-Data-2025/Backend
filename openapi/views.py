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
            'result':{
                'policeOffice': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        
        
from .serializer import CCTVSerializer, SafetyFacilitySerializer, SafetyServiceSerializer
from .models import CCTV, SafetyFacility, SafetyService
import os
import re
from drf_yasg.utils import swagger_auto_schema
from .swagger_docs import cctv_fetch_doc, safety_facility_doc, safety_service_doc

class CCTVFetchView(APIView):
    @swagger_auto_schema(**cctv_fetch_doc)
    def get(self, request, *args, **kwargs):
        district_code = request.query_params.get('district_code')
        if not district_code:
            return Response({
                'success': False,
                'message': 'district_code query param is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        api_key = os.getenv("OPEN_API_KEY")
        base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/safeOpenCCTV_{district_code}"
        initial_url=f"{base_url}/1/1/"
        response = requests.get(initial_url)
        
        if response.status_code != 200:
            return Response({
                'success':False,
                'message':'Failed to fetch data from API'
                }, status=status.HTTP_400_BAD_REQUEST)
        data = response.json()
        data_key = f"safeOpenCCTV_{district_code}"
        total_count = data.get(data_key, {}).get('list_total_count', 0)
        if total_count == 0:
            return Response({
                'success':False,
                'message': 'No CCTV data available for this district'
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
            'result':{
                'message': f'{len(saved_instances)} CCTV records saved successfully',
                'cctv': serializer.data
                }
            }, status=status.HTTP_200_OK)

class SafetyFacilityFetchView(APIView):
    @swagger_auto_schema(**safety_facility_doc)
    def get(self, request, *args, **kwargs):
        api_key = os.getenv("OPEN_API_KEY")
        base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tbSafeReturnItem"
        page_size = 1000

        def extract_coords_from_point(point_str):
            match = re.search(r"POINT\s*\(?([\d.]+)\s+([\d.]+)\)?", point_str, re.IGNORECASE)
            if match:
                lng = float(match.group(1))
                lat = float(match.group(2))
                return lng, lat
            return None, None

        # 전체 건수 확인
        url = f"{base_url}/1/1/"
        res = requests.get(url)
        if res.status_code != 200:
            return Response({
                'success':False,
                'message': 'Failed to fetch data from API'
                }, status=status.HTTP_400_BAD_REQUEST)
        try:
            total = res.json()['tbSafeReturnItem']['list_total_count']
        except Exception as e:
            return Response({
                'success': False,
                'message': f"총 건수 파싱 실패: {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)

        # 반복 수집
        saved = []
        for start in range(1, total + 1, page_size):
            end = min(start + page_size - 1, total)
            url = f"{base_url}/{start}/{end}/"
            res = requests.get(url)
            if res.status_code != 200:
                continue

            try:
                rows = res.json()['tbSafeReturnItem']['row']
            except Exception:
                continue

            for row in rows:
                lng, lat = extract_coords_from_point(row.get("POINT_WKT", ""))
                try:
                    instance = SafetyFacility.objects.create(
                        facility_id=row.get("FACI_ID"),
                        facility_type=row.get("FACI_CODE"),
                        facility_latitude=lat,
                        facility_longitude=lng,
                        facility_location=row.get("DELOC"),
                        sigungu_code=row.get("SGG_CODE"),
                        eupmyeondong_code=row.get("EMD_CODE"),
                        sigungu_name=row.get("SGG_NAME"),
                        eupmyeondong_name=row.get("EMD_NM"),
                    )
                    saved.append(instance)
                except Exception as e:
                    continue

        serializer = SafetyFacilitySerializer(saved, many=True)
        return Response({
            'success':True,
            'result':{
                'message': f"{len(saved)} Facility records saved successfully",
                'data': serializer.data
            }
        }, status=status.HTTP_200_OK)

class SafetyServiceFetchView(APIView):
    @swagger_auto_schema(**safety_service_doc)
    def get(self, request, *args, **kwargs):
        api_key = os.getenv("OPEN_API_KEY")
        base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tbSafeReturnService"
        page_size = 1000

        def extract_coords_from_point(point_str):
            match = re.search(r"POINT\s*\(?([\d.]+)\s+([\d.]+)\)?", point_str, re.IGNORECASE)
            if match:
                lng = float(match.group(1))
                lat = float(match.group(2))
                return lng, lat
            return None, None

        # 전체 건수 확인
        url = f"{base_url}/1/1/"
        res = requests.get(url)
        if res.status_code != 200:
            return Response({
                'success':False,
                'message':'Failed to fetch data from API'
                }, status=status.HTTP_400_BAD_REQUEST)
        try:
            total = res.json()['tbSafeReturnService']['list_total_count']
        except Exception as e:
            return Response({
                'success': False,
                'message': f"총 건수 파싱 실패: {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)

        # 반복 수집
        saved = []
        for start in range(1, total + 1, page_size):
            end = min(start + page_size - 1, total)
            url = f"{base_url}/{start}/{end}/"
            res = requests.get(url)
            if res.status_code != 200:
                continue

            try:
                rows = res.json()['tbSafeReturnService']['row']
            except Exception:
                continue

            for row in rows:
                try:
                    instance = SafetyService.objects.create(
                        service_id=row.get("SERVICE_ID"),
                        service_type=row.get("SISUL_CODE"),
                        service_latitude=row.get("LATITUDE"),
                        service_longitude=row.get("LONGITUDE"),
                        service_location=row.get("DE_LOC"),
                        sigungu_code=row.get("SGG_CODE"),
                        eupmyeondong_code=row.get("EMD_CODE"),
                        sigungu_name=row.get("SGG_NM"),
                        eupmyeondong_name=row.get("EMD_NM"),
                    )
                    saved.append(instance)
                except Exception as e:
                    continue

        serializer = SafetyServiceSerializer(saved, many=True)
        return Response({
            'success':True,
            'result':{
                'message': f"{len(saved)} Service records saved successfully",
                'data': serializer.data
            }
        }, status=status.HTTP_200_OK)