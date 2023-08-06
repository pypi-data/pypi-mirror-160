import re


class Extractor:
    def __init__(self, http_client):
        self._http_client = http_client

    def scan(self, target_urls):
        resources = {
            'images': dict(),
            'videos': set()
        }

        print('Scanning the targets. This can take a while.')

        for target_url in target_urls:
            media_id = self._get_media_id(target_url)
            media_info = self._get_media_info(media_id)

            if 'status' in media_info and media_info['status'] != 'ok':
                raise RuntimeError(media_info['message'])

            for item in media_info['items']:
                if 'carousel_media' in item:
                    carousel_items = item['carousel_media']

                    for carousel_item in carousel_items:
                        image_url = carousel_item['image_versions2']['candidates'][0]['url']
                        image_id = carousel_item['id']

                        resources['images'][image_url] = {
                            'url': image_url,
                            'id': image_id
                        }

                        if 'video_versions' in carousel_item:
                            video_url = carousel_item['video_versions'][0]['url']

                            resources['videos'].add(video_url)
                else:
                    image_url = item['image_versions2']['candidates'][0]['url']
                    image_id = item['id']

                    resources['images'][image_url] = {
                        'url': image_url,
                        'id': image_id
                    }

                    if 'video_versions' in item:
                        video_url = item['video_versions'][0]['url']

                        resources['videos'].add(video_url)

        return resources

    def _get_media_info(self, media_id):
        response = self._http_client.get(
            f'https://i.instagram.com/api/v1/media/{media_id}/info/',
            timeout=10,
            headers={
                'x-ig-app-id': '936619743392459'
            }
        )

        return response.json()

    def _get_media_id(self, url):
        response = self._http_client.get(url, timeout=10)
        media_id = re.search(r'"media_id"\s*:\s*"(.*?)"', response.text)

        if not media_id:
            raise RuntimeError(f'Failed to retrieve media id from {url}')
        
        return media_id.group(1)
