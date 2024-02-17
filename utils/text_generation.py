def generate_text_chunks(text, max_chunk_size=500):
    # Divide o texto em partes de acordo com o tamanho máximo do chunk
    chunks = []
    start_index = 0
    
    while start_index < len(text):
        # Encontra o próximo ponto final antes do limite de caracteres
        end_index = start_index + max_chunk_size
        if end_index >= len(text):
            chunks.append(text[start_index:])
            break
        next_period_index = text.rfind('.', start_index, end_index)
        if next_period_index != -1:
            end_index = next_period_index + 1
        chunks.append(text[start_index:end_index])
        start_index = end_index
    
    return chunks