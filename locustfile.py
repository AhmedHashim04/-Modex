from locust import HttpUser, task, between
import random

# locust -f locustfile.py

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"

    @task
    def view_home(self):
        self.client.get("/")

    @task
    def view_product_list(self):
        self.client.get("/en/products/")

    @task
    def search_with_filters(self):
        url = "/en/products/?search=قميص&category=&tag=خصم&min_price=50&max_price=100&sort_by=name_desc&view_mode=grid&items_per_page=24"
        self.client.get(url)

    @task
    def view_product_detail(self):
        # منتجات عشوائية بافتراض slugs مثلًا
        slugs = ["t-shirt", "jacket", "jeans", "hat"]
        slug = random.choice(slugs)
        self.client.get(f"/products/{slug}/")

    @task
    def add_to_cart(self):
        slugs = ["t-shirt", "jacket", "jeans", "hat"]
        slug = random.choice(slugs)
        self.client.get(f"/cart/add/{slug}/")

    @task
    def update_cart(self):
        slug = "t-shirt"
        self.client.get(f"/cart/update/{slug}/")

    @task
    def remove_from_cart(self):
        slug = "t-shirt"
        self.client.get(f"/cart/remove/{slug}/")

    @task
    def clear_cart(self):
        self.client.get("/cart/clear/")

    @task
    def view_orders(self):
        self.client.get("/order/")

    @task
    def view_profile(self):
        self.client.get("/my-account/profile/")

    @task
    def view_privacy(self):
        self.client.get("/privacy/")

    @task
    def view_terms(self):
        self.client.get("/terms/")

    @task
    def view_contact(self):
        self.client.get("/contact/")

from locust import HttpUser, task, between

class AuthenticatedUser(HttpUser):
    wait_time = between(1, 3)

    """


        افتح DevTools (F12)

        من التبويب Application > Cookies

        دور على اسم الكوكي: sessionid

        انسخ القيمة
    """
    def on_start(self):
        # ✳️ حط هنا sessionid بتاعك
        self.client.headers.update({
            "Cookie": "sessionid=abc123xyz456",  # ← غيرها للقيمة بتاعتك
        })

    @task
    def view_profile(self):
        self.client.get("/account/profile/")

    @task
    def add_address(self):
        self.client.post("/account/address/add/", {
            "full_name": "Locust Bot",
            "phone": "01000000000",
            "address_line1": "123 Test Street",
            "city": "Cairo",
            "postal_code": "12345",
            "country": "EG",
        })

    @task
    def delete_address(self):
        # ✳️ غيّر الـ ID حسب الموجود فعليًا
        self.client.post("/account/address/1/delete/")

    @task
    def place_order(self):
        # لازم يكون فيه عنوان وcart جاهزين قبل كده
        self.client.post("/order/place/", {
            "address_id": 1,  # ✳️ غيّر حسب عنوان فعلي
            "payment_method": "cash",  # أو حسب الخيارات عندك
        })

    @task
    def contact_us(self):
        self.client.post("/contact/", {
            "name": "Locust Bot",
            "email": "locust@example.com",
            "message": "Testing contact form under load.",
        })

"""
locust -f locustfile.py --host=http://127.0.0.1:8000

ثم افتح:
🌐 http://127.0.0.1:8089
وحط عدد المستخدمين ووقت الزيادة (spawn rate) وابدأ.

"""