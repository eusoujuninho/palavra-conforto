import unittest
from models.lead_model import Lead

class TestLeadCreation(unittest.TestCase):

    def test_lead_creation(self):
        print("Iniciando teste de criação do Lead...")

        # Criação de um novo Lead
        new_lead = Lead(
            name="John Doe",
            email="johndoe@example.com",
            mobile_phone="123456789",
            city="New York",
            country="USA",
            document="123-456-789",
            utm_source="Google",
            utm_medium="CPC",
            utm_campaign="Summer_Sale",
            utm_term="buy+summer+shirts",
            utm_content="logolink",
            src="website"
        )

        # Verifica se o lead ainda não possui um ID (não foi salvo)
        self.assertTrue(new_lead.id is None or new_lead.id == '', "O lead já possui um ID antes de ser salvo.")

        self.assertFalse(new_lead.exists(), "O lead já existe antes de ser salvo.")
        print("Lead criado, mas ainda não salvo.")

        # Salva o lead no Airtable e verifica se agora existe
        self.assertTrue(new_lead.save(), "Falha ao salvar o lead no Airtable.")
        self.assertTrue(new_lead.exists(), "O lead não existe após ser salvo.")
        print("Lead salvo no Airtable.")

        # Modificação de atributos e verificação após salvar
        new_lead.city = "Los Angeles"
        new_lead.save()
        new_lead.fetch()  # Recarrega do Airtable
        self.assertEqual(new_lead.city, "Los Angeles", "A cidade do lead não foi atualizada corretamente.")
        print("Atributo do lead atualizado e verificado.")

        # Limpeza: deleta o lead criado
        # new_lead.delete()
        # self.assertFalse(new_lead.exists(), "O lead ainda existe após ser deletado.")
        # print("Lead deletado com sucesso.")

# Teste para operações em lote
# Note que este teste depende da implementação de métodos de classe para operações em lote que seu modelo pode ou não suportar.
# Este é apenas um exemplo simplificado.
@unittest.skip("Pulando teste de operações em lote. Implementar conforme necessário.")
def test_batch_operations(self):
    print("Testando operações em lote...")

if __name__ == '__main__':
    unittest.main()