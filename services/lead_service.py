from models.lead_model import Lead
from pyairtable.orm import ApiError

class LeadService:
    @staticmethod
    def create_lead(name, email, mobile_phone, city, country, document, utm_source, utm_medium, utm_campaign, utm_term, utm_content, src):
        """
        Cria um novo lead.

        :param name: Nome do lead.
        :param email: Email do lead.
        :param mobile_phone: Telefone móvel do lead.
        :param city: Cidade do lead.
        :param country: País do lead.
        :param document: Documento do lead.
        :param utm_source: Fonte UTM.
        :param utm_medium: Meio UTM.
        :param utm_campaign: Campanha UTM.
        :param utm_term: Termo UTM.
        :param utm_content: Conteúdo UTM.
        :param src: Fonte do lead.
        :return: Instância de Lead criada ou None em caso de falha.
        """
        try:
            new_lead = Lead(
                name=name,
                email=email,
                mobile_phone=mobile_phone,
                city=city,
                country=country,
                document=document,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
                utm_term=utm_term,
                utm_content=utm_content,
                src=src
            )
            new_lead.save()
            return new_lead
        except ApiError as e:
            print(f"Erro ao criar lead: {e}")
            return None

    @staticmethod
    def check_and_create_lead(email, **kwargs):
        """
        Verifica se um lead existe com base no email. Se não existir, cria um novo lead.

        :param email: Email do lead para verificação.
        :return: Instância de Lead criada ou existente, None em caso de falha.
        """
        existing_leads = Lead.filter_by_formula(f"{{Email}} = '{email}'", max_records=1)
        if existing_leads:
            print("Lead já existe.")
            return existing_leads[0]  # Retorna o primeiro lead encontrado

        # Se o lead não existe, cria um novo
        return LeadService.create_lead(email=email, **kwargs)
