from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from rentapp.models import Conversacion, Mensaje

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class MensajeriaViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user(username='alice', email='alice@example.com', password='pass')
        self.u2 = User.objects.create_user(username='bob', email='bob@example.com', password='pass')
        self.conv = Conversacion.objects.create(participante1=self.u1, participante2=self.u2)
        # login as u1 by default
        self.client.login(username='alice', password='pass')

    def test_obtener_mensajes_nuevos_empty(self):
        url = reverse('rentapp:obtener_mensajes_nuevos', args=[self.conv.id])
        resp = self.client.get(url, {'ultimo_id': 0}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('mensajes', data)
        self.assertEqual(len(data['mensajes']), 0)

    def test_obtener_mensajes_nuevos_returns_new_messages_and_marks_read(self):
        # crear mensajes por u2 (el otro participante)
        m1 = Mensaje.objects.create(conversacion=self.conv, remitente=self.u2, contenido='hola1')
        m2 = Mensaje.objects.create(conversacion=self.conv, remitente=self.u2, contenido='hola2')
        url = reverse('rentapp:obtener_mensajes_nuevos', args=[self.conv.id])
        resp = self.client.get(url, {'ultimo_id': m1.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # solo mensajes con id > m1.id deben devolverse (m2)
        self.assertEqual(len(data['mensajes']), 1)
        self.assertEqual(data['mensajes'][0]['id'], m2.id)
        # los mensajes del otro usuario que se devolvieron deben marcarse como leídos
        m2.refresh_from_db()
        self.assertTrue(m2.leido)

    def test_post_message_ajax_creates_message_and_returns_json(self):
        url = reverse('rentapp:chat', args=[self.conv.id])
        resp = self.client.post(url, {'contenido': 'mensaje desde test'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # la vista debería devolver JSON indicando éxito
        self.assertIn(resp.status_code, (200, 201))
        data = resp.json()
        self.assertTrue(data.get('success', False))
        self.assertIn('mensaje', data)
        # mensaje creado en BD
        msg_id = data['mensaje']['id']
        m = Mensaje.objects.get(id=msg_id)
        self.assertEqual(m.contenido, 'mensaje desde test')
        self.assertEqual(m.remitente, self.u1)