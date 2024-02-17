def process_hotmart_webhook(webhook_data):
    buyer_info = webhook_data.get('data', {}).get('buyer', {})
    subscription_info = webhook_data.get('data', {}).get('subscription', {})
    
    # Extrai informações do comprador
    name = buyer_info.get('name', 'None')
    email = buyer_info.get('email', 'None')
    mobile_phone = buyer_info.get('checkout_phone', 'None')
    
    # Extrai informações da subscrição, se disponíveis
    sub_plan_id = subscription_info.get('plan', {}).get('id', 'None')
    sub_plan_name = subscription_info.get('plan', {}).get('name', 'None')
    
    # Extrai o status geral do evento
    event_status = webhook_data.get('event', 'None')
    
    # Organiza e retorna os dados extraídos no formato especificado
    return {
        'name': name,
        'email': email,
        'mobile_phone': mobile_phone,
        'status': subscription_info.get('status', 'None'),  # Status da subscrição
        'sub': {
            'plan': {
                'id': sub_plan_id,
                'name': sub_plan_name,
            }
        },
        'event_status': event_status,  # Status geral do evento
    }
