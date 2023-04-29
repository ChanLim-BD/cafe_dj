import json, bcrypt

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from .models import Account

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        
        # 유효한 회원가입 요청 데이터
        self.valid_data = {
            'phone': '01012345678',
            'password': 'password123',
        }
        
        # 중복된 핸드폰 번호를 가진 유효하지 않은 회원가입 요청 데이터
        self.duplicate_phone_data = {
            'phone': '01012345678',
            'password': 'password123',
        }
        
        # 유효하지 않은 핸드폰 번호를 가진 유효하지 않은 회원가입 요청 데이터
        self.invalid_phone_data = {
            'phone': '1234',
            'password': 'password123',
        }
        
        # 유효하지 않은 비밀번호를 가진 유효하지 않은 회원가입 요청 데이터
        self.invalid_password_data = {
            'phone': '01012345678',
            'password': '1234',
        }
    
    def test_valid_signup(self):
        response = self.client.post(self.signup_url, json.dumps(self.valid_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS'})
    
    def test_duplicate_phone_signup(self):
        # 가입 요청을 두 번 보냅니다.
        response_1 = self.client.post(self.signup_url, json.dumps(self.duplicate_phone_data), content_type='application/json')
        response_2 = self.client.post(self.signup_url, json.dumps(self.duplicate_phone_data), content_type='application/json')
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_1.json(), {'MESSAGE': 'SUCCESS'})
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.json(), {'MESSAGE': 'PHONE_DUPLICATED'})
    
    def test_invalid_phone_signup(self):
        response = self.client.post(self.signup_url, json.dumps(self.invalid_phone_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': 'INVALID_PHONE_NUMBER'})
    
    def test_invalid_password_signup(self):
        response = self.client.post(self.signup_url, json.dumps(self.invalid_password_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE': 'PASSWORD_VALIDATION'})


class SignInViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        
            # 회원가입 후 로그인 요청을 보낼 데이터
        self.signup_data = {
            'phone': '01012345678',
            'password': 'password123',
        }
        
        # 유효한 로그인 요청 데이터
        self.valid_signin_data = {
            'phone': '01012345678',
            'password': 'password123',
        }
        
        # 빈 phone 필드를 갖는 로그인 요청 데이터
        self.empty_phone_signin_data = {
            'phone': '',
            'password': 'password123',
        }
        
        # 빈 password 필드를 갖는 로그인 요청 데이터
        self.empty_password_signin_data = {
            'phone': '01012345678',
            'password': '',
        }
        
        # 존재하지 않는 계정으로 로그인 요청을 보낼 데이터
        self.invalid_phone_signin_data = {
            'phone': '01000000000',
            'password': 'password123',
        }
        
        # 잘못된 비밀번호로 로그인 요청을 보낼 데이터
        self.invalid_password_signin_data = {
            'phone': '01012345678',
            'password': 'wrongpassword',
        }
        
        # JWT 인증 토큰
        self.access_token = ''
        
        # 테스트용 계정 생성
        hashed_pw = bcrypt.hashpw(self.signup_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        Account.objects.create(
            phone=self.signup_data['phone'],
            password=hashed_pw,
            is_active=True,
            is_admin=True,
        )
        
    def test_signin_success(self):
        response = self.client.post(self.signin_url, data=self.valid_signin_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['Authorization']
        
    def test_signin_empty_phone(self):
        response = self.client.post(self.signin_url, data=self.empty_phone_signin_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['MESSAGE'], 'Enter Your User Phone or Password')
        
    def test_signin_empty_password(self):
        response = self.client.post(self.signin_url, data=self.empty_password_signin_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['MESSAGE'], 'Enter Your User Phone or Password')
        
    def test_signin_invalid_phone(self):
        response = self.client.post(self.signin_url, data=self.invalid_phone_signin_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['MESSAGE'], 'INVALID_USER')
        
    def test_signin_invalid_password(self):
        response = self.client.post(self.signin_url, data=self.invalid_password_signin_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['MESSAGE'], 'INVALID_USER')
        
    def test_signout_success(self):
        # 로그인
        response = self.client.post(self.signin_url, data=self.valid_signin_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['Authorization']
        
        # 로그아웃
        response = self.client.get(reverse('signout'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'MESSAGE': 'SUCCESS'})
