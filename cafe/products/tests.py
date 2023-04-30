from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import RequestFactory
from accounts.models import Account
from products.models import Product


class ProductListTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create(phone='01012345678')
        self.user.set_password('testpassword')
        self.user.save()
        self.product = Product.objects.create(name='Test Product', description='This is a test product', account=self.user)

    def test_product_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_list_pagination(self):
        self.client.force_authenticate(user=self.user)
        for i in range(15):
            Product.objects.create(name=f'Test Product {i}', description='This is a test product', account=self.user)

        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 16)
        self.assertEqual(response.data['next_cursor'], '2')
        self.assertIsNone(response.data['prev_cursor'])
        self.assertEqual(len(response.data['results']), 10)

        url = f"{reverse('product-list')}?cursor=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 16)
        self.assertIsNone(response.data['next_cursor'])
        self.assertEqual(response.data['prev_cursor'], '1')
        self.assertEqual(len(response.data['results']), 6)
        


class ProductDetailTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create(phone='01012345678')
        self.user.set_password('testpassword')
        self.user.save()
        self.product = Product.objects.create(name='Test Product', description='This is a test product', account=self.user)

    def test_product_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_product_detail_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class ProductCreateTest(APITestCase):
    def setUp(self):
        self.user = Account.objects.create(phone='01012345678')
        self.user.set_password('testpassword')
        self.user.save()

    def test_product_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 0)


class ProductUpdateTest(APITestCase):
    def setUp(self):
        self.user = Account.objects.create(phone='01012345678')
        self.user.set_password('testpassword')
        self.user.save()

        self.product = Product.objects.create(
            name='Product 1',
            description='This is product 1',
            category='category_name',
            barcode='1234567890',
            price=10000,
            cost=5000,
            expiration_date='2024-04-30',
            size='small',
            account=self.user
        )

    def test_update_own_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-update', args=[self.product.pk])
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.description, 'This is an updated product')

    def test_update_other_user_product(self):
        other_user = Account.objects.create(phone='01099999999')
        other_user.set_password('testpassword')
        other_user.save()

        self.client.force_authenticate(user=other_user)
        url = reverse('product-update', args=[self.product.pk])
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, 'Updated Product')
        self.assertNotEqual(self.product.description, 'This is an updated product')

    def test_update_unauthenticated(self):
        url = reverse('product-update', args=[self.product.pk])
        data = {
            'name': 'Updated Product',
            'description': 'This is an updated product',
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, 'Updated Product')
        self.assertNotEqual(self.product.description, 'This is an updated product')



class ProductDeleteTest(APITestCase):
    def setUp(self):
        self.user = Account.objects.create(phone='01012345678')
        self.user.set_password('testpassword')
        self.user.save()
        self.product = Product.objects.create(name='Test Product', description='This is a test product', account=self.user)

    def test_delete_product(self):
        other_user = Account.objects.create(phone='01087654321')
        other_user.set_password('testpassword')
        other_user.save()
        
        self.client.login(phone='01087654321', password='testpassword')
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(phone='01012345678', password='testpassword')
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)