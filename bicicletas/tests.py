from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bicicleta, Categoria, Marca, Modelo


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Montaña",
            descripcion="Bicicletas para senderos",
            activa=True,
        )

    def test_creacion_categoria(self):
        self.assertEqual(self.categoria.nombre, "Montaña")
        self.assertTrue(self.categoria.activa)

    def test_str_categoria(self):
        self.assertEqual(str(self.categoria), "Montaña")


class MarcaModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nombre="Trek", segmento="ALTA_GAMA")

    def test_creacion_marca(self):
        self.assertEqual(self.marca.nombre, "Trek")
        self.assertEqual(self.marca.segmento, "ALTA_GAMA")

    def test_str_marca(self):
        self.assertEqual(str(self.marca), "Trek")


class ModeloModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nombre="Trek")
        self.categoria = Categoria.objects.create(nombre="Montaña")
        self.modelo = Modelo.objects.create(
            marca=self.marca,
            categoria=self.categoria,
            nombre="Marlin 5 (Aro 29)",
        )

    def test_creacion_modelo(self):
        self.assertEqual(self.modelo.marca, self.marca)
        self.assertEqual(self.modelo.categoria, self.categoria)

    def test_str_modelo(self):
        self.assertEqual(str(self.modelo), "Trek - Marlin 5 (Aro 29)")


class BicicletaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Montaña")
        self.marca = Marca.objects.create(nombre="Trek")
        self.modelo = Modelo.objects.create(
            marca=self.marca,
            categoria=self.categoria,
            nombre="Marlin 5 (Aro 29)",
        )
        self.bicicleta = Bicicleta.objects.create(
            modelo_rel=self.modelo,
            tipo="MONTANA",
            aro=29,
            precio=500000,
            stock=5,
            color="Negro",
            categoria_rel=self.categoria,
        )

    def test_creacion_bicicleta(self):
        self.assertEqual(self.bicicleta.precio, 500000)
        self.assertEqual(self.bicicleta.stock, 5)
        self.assertEqual(self.bicicleta.color, "Negro")

    def test_str_bicicleta(self):
        self.assertEqual(str(self.bicicleta), "Trek Marlin 5 (Aro 29)")

    def test_propiedades_bicicleta(self):
        self.assertEqual(self.bicicleta.marca, "Trek")
        self.assertEqual(self.bicicleta.modelo, "Marlin 5 (Aro 29)")
        self.assertEqual(self.bicicleta.categoria, "Montaña")


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.categoria = Categoria.objects.create(nombre="Montaña")
        self.marca = Marca.objects.create(nombre="Trek")
        self.modelo = Modelo.objects.create(
            marca=self.marca,
            categoria=self.categoria,
            nombre="Marlin 5 (Aro 29)",
        )
        self.bicicleta = Bicicleta.objects.create(
            modelo_rel=self.modelo,
            tipo="MONTANA",
            aro=29,
            precio=500000,
            stock=5,
            color="Negro",
            categoria_rel=self.categoria,
        )

    def test_inicio_redirect_autenticado(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.status_code, 302)

    def test_inicio_no_autenticado(self):
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.status_code, 200)

    def test_lista_redireccion_si_no_autenticado(self):
        response = self.client.get(reverse("lista_bicicletas"))
        self.assertEqual(response.status_code, 302)

    def test_lista_autenticado(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("lista_bicicletas"))
        self.assertEqual(response.status_code, 200)

    def test_detalle_bicicleta(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("detalle_bicicleta", args=[self.bicicleta.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_crear_bicicleta_requiere_login(self):
        response = self.client.get(reverse("crear_bicicleta"))
        self.assertEqual(response.status_code, 302)