# 📌 API 명세서 – 서울시 안심귀가 시스템

---

## ✅ 1. CCTV 수집 API

- **Method**: `GET`
- **Endpoint**: `/api/fetch-cctv/`
- **Query Parameters**:
  - `district_code` (string, **필수**)  
    자치구 코드 (예: `sm`, `sd`, `gb` 등)

### 🔹 요청 예시

```
GET /api/fetch-cctv/?district_code=sm
```

### 🔹 응답 예시 (성공)

```json
{
  "success": true,
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
```

### 🔹 오류 응답

- **400 (API 호출 실패)**

```json
{
  "success": false,
  "data": {
    "error": "Failed to fetch data from API"
  }
}
```

- **404 (CCTV 없음)**

```json
{
  "success": false,
  "data": {
    "message": "No CCTV data available for this district"
  }
}
```

---

## ✅ 2. 안심 시설물 수집 API

- **Method**: `GET`
- **Endpoint**: `/api/fetch-facility/`

### 🔹 응답 예시 (성공)

```json
{
  "success": true,
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
```

### 🔹 오류 응답

- **400**

```json
{
  "success": false,
  "data": {
    "error": "Failed to fetch data from API"
  }
}
```

- **404**

```json
{
  "success": false,
  "data": {
    "error": "총 건수 파싱 실패: error"
  }
}
```

---

## ✅ 3. 귀가 서비스 지점 수집 API

- **Method**: `GET`
- **Endpoint**: `/api/fetch-service/`

### 🔹 응답 예시 (성공)

```json
{
  "success": true,
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
```

### 🔹 오류 응답

- **400**

```json
{
  "success": false,
  "data": {
    "error": "Failed to fetch data from API"
  }
}
```

- **404**

```json
{
  "success": false,
  "data": {
    "error": "총 건수 파싱 실패: error"
  }
}
```
