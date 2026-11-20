from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class RealtorLoginTests(TestCase):
    password = "Testing-a-secure-password-74"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.realtor = User.objects.create_user("realtor", password=cls.password, is_staff=True)
        cls.member = User.objects.create_user("member", password=cls.password)
        cls.inactive = User.objects.create_user(
            "inactive", password=cls.password, is_staff=True, is_active=False
        )

    def login(self, username="realtor", password=None, **extra):
        return self.client.post(reverse("admin:login"), {
            "username": username, "password": password or self.password, **extra,
        })

    def test_authorized_realtor_login(self):
        response = self.login()
        self.assertRedirects(response, reverse("admin:index"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.realtor.pk)

    def test_invalid_accounts_have_identical_generic_errors(self):
        for username, password in [
            ("realtor", "wrong"), ("unknown", self.password),
            ("inactive", self.password), ("member", self.password),
        ]:
            with self.subTest(username=username):
                response = self.login(username, password)
                self.assertContains(response, "Unable to sign in with those credentials.")
                self.assertNotIn("_auth_user_id", self.client.session)
                self.assertNotContains(response, f'value="{password}"')

    def test_login_page_accessible_fields(self):
        response = self.client.get(reverse("admin:login"))
        self.assertContains(response, "Realtor Login")
        self.assertContains(response, 'type="password"')
        self.assertContains(response, 'for="id_username"')
        self.assertContains(response, 'for="id_password"')

    def test_safe_next_and_external_next(self):
        for destination, expected in [
            ("/admin/password_change/", "/admin/password_change/"),
            ("https://evil.example/", reverse("admin:index")),
            ("//evil.example/", reverse("admin:index")),
        ]:
            with self.subTest(destination=destination):
                self.client.logout()
                response = self.login(next=destination)
                self.assertRedirects(response, expected)

    def test_all_existing_admin_pages_and_actions_require_authorization(self):
        targets = [
            reverse("admin:index"), reverse("admin:auth_user_changelist"),
            reverse("admin:auth_user_add"),
            reverse("admin:auth_user_change", args=[self.realtor.pk]),
            reverse("admin:auth_user_delete", args=[self.realtor.pk]),
            reverse("admin:auth_group_add"), reverse("admin:password_change"),
            reverse("admin:autocomplete"),
        ]
        for authenticated in (False, True):
            if authenticated:
                self.client.force_login(self.member)
            for target in targets:
                for method in ("get", "post"):
                    with self.subTest(authenticated=authenticated, target=target, method=method):
                        response = getattr(self.client, method)(target, {"username": "intruder"})
                        self.assertEqual(response.status_code, 403 if authenticated else 302)
                        if not authenticated:
                            self.assertTrue(response.url.startswith(reverse("admin:login") + "?next="))
        self.assertEqual(get_user_model().objects.count(), 3)
        self.realtor.refresh_from_db()
        self.assertEqual(self.realtor.username, "realtor")

    def test_staff_still_need_model_permissions(self):
        self.client.force_login(self.realtor)
        for method in ("get", "post"):
            response = getattr(self.client, method)(reverse("admin:auth_user_add"))
            self.assertEqual(response.status_code, 403)

    def test_csrf_and_post_only_logout(self):
        client = Client(enforce_csrf_checks=True)
        login_url = reverse("admin:login")
        response = client.get(login_url)
        token = client.cookies["csrftoken"].value
        credentials = {"username": "realtor", "password": self.password}
        self.assertEqual(client.post(login_url, credentials).status_code, 403)
        response = client.post(login_url, {**credentials, "csrfmiddlewaretoken": token})
        self.assertRedirects(response, reverse("admin:index"))
        logout_url = reverse("admin:logout")
        self.assertEqual(client.get(logout_url).status_code, 405)
        self.assertEqual(client.post(logout_url).status_code, 403)
        self.assertIn("_auth_user_id", client.session)
        response = client.post(logout_url, {
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        })
        self.assertRedirects(response, reverse("home") + "?logged_out=1")
        self.assertNotIn("_auth_user_id", client.session)

    def test_admin_has_post_logout_control(self):
        self.client.force_login(self.realtor)
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, 'id="logout-form"')
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_public_home_remains_available(self):
        self.assertContains(self.client.get(reverse("home")), "CK Realestate")

    def test_logout_control_is_consistent_across_admin_sections(self):
        from django.contrib.auth.models import Permission

        self.realtor.user_permissions.add(Permission.objects.get(codename="view_user"))
        self.client.force_login(self.realtor)
        targets = [
            reverse("admin:index"),
            reverse("admin:auth_user_changelist"),
            reverse("admin:password_change"),
        ]
        for target in targets:
            with self.subTest(target=target):
                response = self.client.get(target)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'id="logout-form"')
                self.assertContains(response, 'method="post"')
                self.assertContains(response, 'action="/admin/logout/"')

    def test_logout_ends_session_and_returns_to_public_logged_out_result(self):
        self.client.force_login(self.realtor)

        response = self.client.post(reverse("admin:logout"))

        self.assertRedirects(response, reverse("home") + "?logged_out=1")
        self.assertNotIn("_auth_user_id", self.client.session)

        home = self.client.get(reverse("home") + "?logged_out=1")
        self.assertContains(home, "You have been logged out.")

    def test_old_session_cannot_access_or_submit_admin_requests_after_logout(self):
        self.client.force_login(self.realtor)
        old_cookie = self.client.cookies["sessionid"].value
        self.client.post(reverse("admin:logout"))

        self.client.cookies["sessionid"] = old_cookie
        targets = [
            reverse("admin:index"),
            reverse("admin:auth_user_changelist"),
            reverse("admin:auth_user_add"),
        ]
        for target in targets:
            with self.subTest(method="get", target=target):
                response = self.client.get(target)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("admin:login") + "?next="))
            with self.subTest(method="post", target=target):
                response = self.client.post(target, {"username": "intruder"})
                self.assertIn(response.status_code, (302, 403))

        self.assertEqual(get_user_model().objects.filter(username="intruder").count(), 0)
