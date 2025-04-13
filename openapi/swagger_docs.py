from drf_yasg import openapi

# CCTV 수집 API
cctv_fetch_doc = {
    "operation_summary": "CCTV 데이터 수집",
    "operation_description": "서울시 OpenAPI를 통해 자치구별 CCTV 위치 정보를 수집하고 저장합니다.",
    "manual_parameters": [
        openapi.Parameter(
            name="district_code",
            in_=openapi.IN_QUERY,
            description="자치구 코드 (예: sm, sd, gb 등)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    "responses": {
        200: openapi.Response(
            description="성공",
            examples={
                "application/json": {
                    "success": True,
                    "data": {
                        "message": "120 CCTV records saved successfully",
                        "cctv": [
                            {
                                "id": 3224,
                                "district": "서대문구",
                                "lat": "37.5770",
                                "lot": "126.9457",
                                "addr": "(광역감시01) 서05-703 안산철탑_회전_서북"
                            }
                        ]
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Failed to fetch data from API",
            examples={
                "application/json": {
                    'success':False,
                    'data':{
                        'error': 'Failed to fetch data from API'
                    }
                }
            }
        ),
        404: openapi.Response(
            description="No CCTV data available for this district",
            examples={
                "application/json": {
                    'success':False,
                    'data':{
                        'message': 'No CCTV data available for this district'
                    }
                }
            }
        )
    }
}

# 안심 시설물 수집 API
safety_facility_doc = {
    "operation_summary": "안심 시설물 수집",
    "operation_description": "서울시 안심귀가 시설물 데이터를 OpenAPI를 통해 수집하고 저장합니다.",
    "responses": {
        200: openapi.Response(
            description="성공",
            examples={
                "application/json": {
                    "success": True,
                    "data": {
                        "message": "300 Facility records saved successfully",
                        "data": [
                            {
                                "id": 1,
                                "facility_id": "1111011000_04_P01",
                                "facility_type": "301",
                                "facility_latitude": 37.1234,
                                "facility_longitude": 126.9876,
                                "facility_location": "서울시 강남구 논현로 123",
                                "sigungu_code": "11680",
                                "eupmyeondong_code": "11680510",
                                "sigungu_name": "강남구",
                                "eupmyeondong_name": "논현동",
                                "created_at": "2025-04-13T08:12:34.338969Z"
                            }
                        ]
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Failed to fetch data from API",
            examples={
                "application/json": {
                    'success':False,
                    'data':{
                        'error': 'Failed to fetch data from API'
                    }
                }
            }
        ),
        404: openapi.Response(
            description="No Facility data available for this district",
            examples={
                "application/json": {
                    'success':False,
                    'data':{
                        'error': "총 건수 파싱 실패: error"
                    }
                }
            }
        )
    }
}

# 귀가 서비스 지점 수집 API
safety_service_doc = {
    "operation_summary": "귀가 서비스 지점 수집",
    "operation_description": "서울시 귀가서비스 지점 데이터를 OpenAPI를 통해 수집하고 저장합니다.",
    "responses": {
        200: openapi.Response(
            description="성공",
            examples={
                "application/json": {
                    "success": True,
                    "data": {
                        "message": "150 Service records saved successfully",
                        "data": [
                            {
                                "id": 1,
                                "service_id": "1111011000_04_P01",
                                "service_type": "401",
                                "service_latitude": 37.5678,
                                "service_longitude": 127.1234,
                                "service_location": "서울시 중구 세종대로 1길 5",
                                "sigungu_code": "11140",
                                "eupmyeondong_code": "11140550",
                                "sigungu_name": "중구",
                                "eupmyeondong_name": "명동",
                                "created_at": "2025-04-13T08:12:34.338969Z"
                            }
                        ]
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Failed to fetch data from API",
            examples={
                "application/json": {
                    'success': False,
                    'data': {
                        'error': 'Failed to fetch data from API'
                    }
                }
            }
        ),
        404: openapi.Response(
            description="No Service data available for this district",
            examples={
                "application/json": {
                    'success': False,
                    'data': {
                        'error': "총 건수 파싱 실패: error"
                    }
                }
            }
        )
    }
}