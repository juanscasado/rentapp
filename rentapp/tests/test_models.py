from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from rentapp.models import Conversacion, Mensaje

User = get_user_model()

class ConversacionMensajeModelTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.u2 = User.objects.create_user(username='u2', email='u2@example.com', password='pass')
        # Conversacion without Local (local can be None)
        self.conv = Conversacion.objects.create(participante1=self.u1, participante2=self.u2)

    def test_get_otro_participante(self):
        self.assertEqual(self.conv.get_otro_participante(self.u1), self.u2)
        self.assertEqual(self.conv.get_otro_participante(self.u2), self.u1)

    def test_contar_no_leidos_and_leido_flag(self):
        # crear mensajes: uno de u2 (no leído) y uno de u1 (no leído pero remitente es u1)
        m1 = Mensaje.objects.create(conversacion=self.conv, remitente=self.u2, contenido='hola')
        m2 = Mensaje.objects.create(conversacion=self.conv, remitente=self.u1, contenido='respuesta')
        # para u1 debe haber 1 no leído (m1)
        self.assertEqual(self.conv.contar_no_leidos(self.u1), 1)
        # marcar m1 como leído y comprobar
        m1.leido = True
        m1.save()
        self.assertEqual(self.conv.contar_no_leidos(self.u1), 0)

    def test_ordering_by_created_at(self):
        m_old = Mensaje.objects.create(conversacion=self.conv, remitente=self.u2, contenido='older', created_at=timezone.now())
        m_new = Mensaje.objects.create(conversacion=self.conv, remitente=self.u2, contenido='newer', created_at=timezone.now())
        # mensajes.last() debería devolver el más reciente según ordering de modelo
        self.assertEqual(self.conv.mensajes.last().contenido, m_new.contenido)