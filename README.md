![](https://velog.velcdn.com/images/chan9708/post/62e761c1-3054-49c2-b737-bcbd607bace0/image.jpg)

---

## Development Environment

> **Django/DRF, mySQL:5.7**

![](https://velog.velcdn.com/images/chan9708/post/51ce05c0-e255-49a9-93db-86135a91f53d/image.png)

![](https://velog.velcdn.com/images/chan9708/post/5d64864d-b36f-456b-9d2d-ee72ac372aea/image.png)

![](https://velog.velcdn.com/images/chan9708/post/ccc594fa-c9fa-4135-93bc-1951fe2ff113/image.png)

---

## Requirement

> **1. Login | Logout**

- JSON 형식의 데이터를 받아들이고, 응답으로 JSON 형식의 데이터를 반환합니다.
  <br>
- APIView 클래스를 상속받아 HTTP 메소드인 GET, POST를 사용하여 HTTP 요청을 처리합니다.
  <br>
- RESTful API를 구현하기 위해 HTTP 상태 코드(status code)를 사용하여 적절한 응답을 반환합니다.
  <br>
- JWT 패키지를 사용하여 사용자 인증을 처리합니다.

> **2. Products**
>
> - > 속성 :
>   > Name
>   > Description
>   > Categories
>   > Barcode
>   > Price
>   > Cost
>   > Expiration_date
>   > Size
