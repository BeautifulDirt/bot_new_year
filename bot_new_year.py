#!/usr/bin/env python
# --coding:utf-8--

import vk_api
import time
import random
import urllib2
import string
from PIL import Image, ImageDraw, ImageFont

vk = vk_api.VkApi(token='11aa22bb33cc...') # ваш токен
vk._auth_token()
upload = vk_api.VkUpload(vk)

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower().encode('utf-8').translate(None, string.punctuation) == "арт":
                vk.method("messages.send", {"peer_id": id, "random_id": 0, "message": "Ок, ждите&#128527;"})
                profiles = vk.method('users.get', {'user_ids' : id, 'fields': 'photo_400'})
                print(profiles[0]['first_name']+ ' ' +profiles[0]['last_name'])
                try:
                    url = profiles[0]['photo_400']
                    xx, yy = (800, 550)
                except Exception as E:
                    print(E)
                    profile = vk.method('users.get', {'user_ids' : id, 'fields': 'photo_max_orig'})
                    url = profile[0]['photo_max_orig']
                    xx, yy = (800, 572) 
                finally:    
                    print(url)
                    url = url.replace("?ava=1", "")
                    response = urllib2.urlopen(url)
                    content = response.read()
                    file = open('image.jpg', 'w')
                    file.write(content)
                    file.close()
                    numart = random.randint(0, 9)
                    if numart in [1,2]:
                        x, y = (590, 185)
                    else:
                        x, y = (60, 440)
                    
                    img = Image.open('/img/img' + str(numart) + '.jpg')
                    watermark = Image.open('image.jpg')
                    water = Image.open('/template/i' + str(numart) + '.png')

                    img = img.convert('RGBA')
                    watermark = watermark.convert('RGBA')
                    water = water.convert('RGBA')

                    img.paste(watermark, (xx, yy),  watermark)
                    img.paste(water, (781, 412),  water)

                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype("font.otf", 48)

                    text = profiles[0]['first_name']+'!'
                    draw.text((x-1, y-1), text, font=font, fill=(79,79,79))
                    draw.text((x+1, y-1), text, font=font, fill=(79,79,79))
                    draw.text((x-1, y+1), text, font=font, fill=(79,79,79))
                    draw.text((x+1, y+1), text, font=font, fill=(79,79,79))
                    draw.text((x, y), text, font=font, fill=(255,255,255))

                    img.save("img_result.png")

                    photo = upload.photo_messages('img_result.png')
                    owner_id = photo[0]['owner_id']
                    photo_id = photo[0]['id']
                    access_key = photo[0]['access_key']
                    attachment = 'photo{owner_id}_{photo_id}_{access_key}'.format(owner_id=owner_id, photo_id=photo_id, access_key=access_key)
                    print(attachment)
                    vk.method("messages.send", {"peer_id": id, "random_id": 0, "attachment": attachment})
            else:
                pass
    except Exception as E:
    	print(E)
        time.sleep(1)