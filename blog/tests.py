from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from blog.models import BlogPost

User = get_user_model()


class BlogPostPermissionsTest(TestCase):
    """Тесты прав доступа к блогу"""

    @classmethod
    def setUpTestData(cls):
        # Создаем группу "Content manager"
        cls.group, created = Group.objects.get_or_create(name="Content manager")

        if created:
            content_type = ContentType.objects.get_for_model(BlogPost)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["add_blogpost", "change_blogpost", "delete_blogpost", "view_blogpost"],
            )
            cls.group.permissions.set(permissions)

    def setUp(self):
        # Создаем пользователя с правами
        self.user = User.objects.create_user(email="manager@test.com", password="manager123")
        self.user.groups.add(self.group)

        # Создаем обычного пользователя
        self.regular_user = User.objects.create_user(email="user@test.com", password="user123")

        self.post = BlogPost.objects.create(title="Тестовая статья", content="Содержание", is_published=True)

    def test_create_permission(self):
        """Только контент-менеджер может создавать статьи"""
        self.client.login(email="manager@test.com", password="manager123")
        response = self.client.get(reverse("blog:blogpost_create"))
        self.assertEqual(response.status_code, 200)

        # Обычный пользователь не может создать
        self.client.login(email="user@test.com", password="user123")
        response2 = self.client.get(reverse("blog:blogpost_create"))
        self.assertEqual(response2.status_code, 403)

    def test_update_permission(self):
        """Только контент-менеджер может редактировать статьи"""
        self.client.login(email="manager@test.com", password="manager123")
        response = self.client.get(reverse("blog:blogpost_update", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

        # Обычный пользователь не может редактировать
        self.client.login(email="user@test.com", password="user123")
        response2 = self.client.get(reverse("blog:blogpost_update", args=[self.post.pk]))
        self.assertEqual(response2.status_code, 403)

    def test_delete_permission(self):
        """Только контент-менеджер может удалять статьи"""
        self.client.login(email="manager@test.com", password="manager123")
        response = self.client.post(reverse("blog:blogpost_delete", args=[self.post.pk]))
        self.assertRedirects(response, reverse("blog:blogpost_list"))
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())
