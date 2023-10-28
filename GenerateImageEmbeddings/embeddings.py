import logging
import requests
'''
### Generate Embeddings
This function will call the Cognitive Services Computer Vision Vectorize Image API to generate embeddings for the image provided.
'''
def generate_embeddings(stream, aiVisionEndpoint, aiVisionApiKey):
    logging.info("Generating embeddings...")
    url = f"{aiVisionEndpoint}/computervision/retrieval:vectorizeImage"
    params = {
        "api-version": "2023-02-01-preview",
        "modelVersion": "latest"
    }
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": aiVisionApiKey
    }
    response = requests.post(url, params=params, headers=headers, data=stream)
  
    if response.status_code == 200:
        logging.info("Embeddings generated successfully")
        embeddings = response.json()["vector"]
        return embeddings
    else:
        logging.error(f'generate_embeddings Error {response.status_code}: {response.text}')
        return None