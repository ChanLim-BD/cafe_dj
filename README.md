![](https://velog.velcdn.com/images/chan9708/post/62e761c1-3054-49c2-b737-bcbd607bace0/image.jpg)

---

## Development Environment

> **Django/DRF, mySQL:5.7**

![](https://velog.velcdn.com/images/chan9708/post/2c8a1985-45e0-4299-b503-47002396e536/image.png)

![](https://velog.velcdn.com/images/chan9708/post/ecc496d5-4fb8-46df-9814-f447687a6935/image.png)

![](https://velog.velcdn.com/images/chan9708/post/c0d3cbd0-45bf-4601-a651-87c6d55263ec/image.png)

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

* 상품 이름 기반으로 `like 검색`과 `초성 검색`이 가능합니다.
  * jamo 패키지

* Custom Response Json 형식
  * 'meta' 와 'data' 형식으로 반환합니다.

---

### 개선해야할 점
* Django User를 Customize하는 방식.
* Django의 내장된 User를 사용하면 인증 및 회원가입 로그인/로그아웃이 간편해진다.
  * 다만, JWT 이용이 애매해진다. 
* 기본 DRF를 활용하는 방법에 대해 덜 익숙하다.
  * Django REST API가 제공하는 클래스들을 활용하면 REST API일지라도 데이터 입력하는 FORM을 제공하므로 DB에 데이터 추가하기 편하다.
  * 안그러면 일일이 JSON 형식으로 작성해서 보내야한다.