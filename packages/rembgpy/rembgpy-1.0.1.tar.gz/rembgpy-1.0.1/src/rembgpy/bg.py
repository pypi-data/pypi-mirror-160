import requests
import logging

base_url = "https://api.remove.bg/v1.0/removebg"

class RemBg(object):

    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def _fetch_check_arguments(self, size, type, type_level, format, channels):
        if size not in ["auto", "preview", "small", "regular", "medium", "hd", "full", "4k"]:
            raise ValueError("[*] (size) argument wrong")

        if type not in ["auto", "person", "product", "animal", "car", "car_interior", "car_part", "transportation", "graphics", "other"]:
            raise ValueError("[*] (type) argument wrong")

        if type_level not in ["none", "latest", "1", "2"]:
            raise ValueError("[*] (type_level) argument wrong")

        if format not in ["jpg", "zip", "png", "auto"]:
            raise ValueError("[*] (format) argument wrong") 
 
        if channels not in ["rgba", "alpha"]:
            raise ValueError("[*] (channels) argument wrong") 
        
    def _out_file(self, respr, nfn):
        if respr.status_code == requests.codes.ok:
            with open(nfn, 'wb') as removed_bg_file:
                removed_bg_file.write(respr.content)
        else:
            error_reason = respr.json()["errors"][0]["title"].lower()
            logging.error("[*] Unable to save the file %s due to %s", nfn, error_reason)
            return "[*] Unable to save the file %s due to %s", nfn, error_reason
        
    def remove_img(self, img_file_path, size="regular", 
                                       type="auto", type_level="none", 
                                       format="auto", roi="0 0 100% 100%", 
                                       crop=None, scale="original", 
                                       position="original", channels="rgba", 
                                       shadow=False, semitransparency=True,
                                       bg=None, bg_type=None, nfn="removed-bg.png"):
        self._fetch_check_arguments(size, type, type_level, format, channels)

        img_file = open(img_file_path, 'rb')
        files = {'image_file': img_file}
        
        data = {
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        respr = requests.post(
            base_url,
            files=files,
            data=data,
            headers={'X-Api-Key': self.__api_key})
        respr.raise_for_status()
        self._out_file(respr, nfn)

        img_file.close()
        return "[*] Process finished."

    def remove_img(self, img_url, size="regular", 
                                       type="auto", type_level="none", 
                                       format="auto", roi="0 0 100% 100%", 
                                       crop=None, scale="original", 
                                       position="original", channels="rgba", 
                                       shadow=False, semitransparency=True,
                                       bg=None, bg_type=None, nfn="removed-bg.png"):
        self._fetch_check_arguments(size, type, type_level, format, channels)

        files = {}
        
        data = {
            'image_url': img_url,
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        respr = requests.post(
            base_url,
            data=data,
            headers={'X-Api-Key': self.__api_key}
        )
        respr.raise_for_status()
        self._out_file(respr, nfn)
        return "[*] Process finished."

    def remove_b64(self, base64_img, size="regular", 
                                          type="auto", type_level="none", 
                                          format="auto", roi="0 0 100% 100%", 
                                          crop=None, scale="original", 
                                          position="original", channels="rgba", 
                                          shadow=False, semitransparency=True,
                                          bg=None, bg_type=None, nfn="removed-bg.png"):
        self._fetch_check_arguments(size, type, type_level, format, channels)

        files = {}
        
        data = {
            'image_file_b64': base64_img,
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        respr = requests.post(
            base_url,
            data=data,
            headers={'X-Api-Key': self.__api_key}
        )
        respr.raise_for_status()
        self._out_file(respr, nfn)
        return "[*] Process finished."