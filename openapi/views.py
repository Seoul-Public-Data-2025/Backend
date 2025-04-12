import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CCTVSerializer
from .models import CCTV
import os

class CCTVFetchView(APIView):
    def get(self, request, *args, **kwargs):
        district_code = request.query_params.get('district_code')
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
                instance=CCTV.objects.create(
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