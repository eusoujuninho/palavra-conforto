from models.lead_model import Lead
from models.customer_model import Customer
from pyairtable.orm import ApiError

class CustomerService:

    @staticmethod
    def get_customer_by_id(customer_id):
        """
        Busca um customer pelo ID.

        :param customer_id: ID do customer a ser buscado.
        :return: Instância de Customer ou None se não encontrado.
        """
        try:
            return Customer.get(customer_id)
        except ApiError as e:
            print(f"Erro ao buscar customer: {e}")
            return None

    @staticmethod
    def create_customer(document, utm_source, utm_medium, utm_campaign, utm_term, utm_content, src, lead_link):
        """
        Cria um novo customer.

        :param document: Documento do customer.
        :param utm_source: Fonte UTM.
        :param utm_medium: Meio UTM.
        :param utm_campaign: Campanha UTM.
        :param utm_term: Termo UTM.
        :param utm_content: Conteúdo UTM.
        :param src: Fonte do customer.
        :param lead_link: Lista contendo o ID do Lead relacionado.
        :return: Instância de Customer criada ou None em caso de falha.
        """
        try:
            new_customer = Customer(
                document=document,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
                utm_term=utm_term,
                utm_content=utm_content,
                src=src,
                lead_link=lead_link
            )
            new_customer.save()
            return new_customer
        except ApiError as e:
            print(f"Erro ao criar customer: {e}")
            return None

    @staticmethod
    def transform_lead_to_customer(lead_id, **kwargs):
        """
        Transforma um lead em um customer, criando um registro de customer associado ao lead.

        :param lead_id: ID do Lead a ser transformado em Customer.
        :param kwargs: Argumentos adicionais para criar o Customer.
        :return: Instância de Customer criada ou None em caso de falha.
        """
        lead = Lead.get(lead_id)
        if not lead:
            print("Lead não encontrado.")
            return None

        try:
            # Aqui, assumimos que o Lead possui todos os dados necessários para criar o Customer
            # e que esses dados estão sendo passados diretamente via kwargs.
            new_customer = Customer(
                document=lead.document,  # Exemplo, ajuste conforme a estrutura do seu modelo Lead
                lead_link=[lead_id],
                **kwargs
            )
            new_customer.save()
            return new_customer
        except ApiError as e:
            print(f"Erro ao transformar lead em customer: {e}")
            return None
