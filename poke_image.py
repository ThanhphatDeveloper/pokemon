# import requests
# from bs4 import BeautifulSoup
# import os
# import urllib.parse

# def download_image(img_url, img_name, folder):
#     try:
#         os.makedirs(folder, exist_ok=True)
#     except OSError as e:
#         print(f"Lỗi: {folder}: {e}")

#     img_path = os.path.join(folder, img_name)

#     try:
#         img_response = requests.get(img_url)
#         with open(img_path, 'wb') as img_file:
#             img_file.write(img_response.content)
#         print(f"Tải xuống ảnh: {img_name}")
#     except Exception as e:
#         print(f"Lỗi khi tải xuống ảnh {img_name}: {e}")

# def download_pokemon_images(base_url, start_id, end_id, folder):
#     for pokemon_id in range(start_id, end_id + 1):
#         url = f"{base_url}/{pokemon_id:04d}"
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         img_tags = soup.find_all('img')

#         for img_tag in img_tags:
#             img_src = img_tag.get('src')
#             if img_src and img_src.endswith('.png'):
#                 img_name = img_src.split('/')[-1]
#                 img_url = urllib.parse.urljoin(url, img_src)
#                 download_image(img_url, img_name, folder)

# # Đường dẫn cơ sở của trang web và thư mục lưu trữ ảnh
# base_url = 'https://vn.portal-pokemon.com/play/pokedex'
# folder = 'pokemon_images'

# # Phạm vi id của Pokémon bạn muốn tải xuống
# start_id = 1
# end_id = 10

# # Gọi hàm để tải xuống ảnh
# download_pokemon_images(base_url, start_id, end_id, folder)

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

def download_pokemon_images(base_url, start_id, end_id, folder):
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as e:
        print(f"Lỗi: {folder}: {e}")

    with requests.Session() as session:
        for pokemon_id in range(start_id, end_id + 1):
            url = f"{base_url}/{pokemon_id:04d}"
            response = session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Lấy tên nhân vật từ class 'pokemon-slider__main-name'
            pokemon_name_tag = soup.find('p', class_='pokemon-slider__main-name')
            if pokemon_name_tag:
                pokemon_name = pokemon_name_tag.text.strip()

                # Lấy danh sách các ảnh
                img_tags = soup.find_all('img', class_='lazyload')
                if img_tags:
                    for idx, img_tag in enumerate(img_tags):
                        img_src = img_tag.get('data-src')
                        if img_src and img_src.endswith('.png'):
                            # Tạo tên file dựa trên tên và số thứ tự của ảnh
                            img_name = f"{pokemon_id:04d}"
                            if idx > 0:
                                img_name += f"_{idx}"
                            img_name += ".png"
                            
                            img_url = urllib.parse.urljoin(url, img_src)
                            img_path = os.path.join(folder, img_name)

                            try:
                                img_response = session.get(img_url)
                                with open(img_path, 'wb') as img_file:
                                    img_file.write(img_response.content)
                                print(f"Tải xuống: {img_name}")
                            except Exception as e:
                                print(f"Lỗi khi tải xuống {img_name}: {e}")
            else:
                print("Không tìm thấy tên nhân vật.")

# Đường dẫn cơ sở của trang web và thư mục lưu trữ ảnh
base_url = 'https://vn.portal-pokemon.com/play/pokedex'
folder = 'pokemon_images'

# Phạm vi id của Pokémon bạn muốn tải xuống
start_id = 1
end_id = 905

# Gọi hàm để tải xuống ảnh của mỗi nhân vật và đặt tên file dựa trên số thứ tự của ảnh (nếu có)
download_pokemon_images(base_url, start_id, end_id, folder)
