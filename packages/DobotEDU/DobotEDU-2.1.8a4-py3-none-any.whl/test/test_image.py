import base64
import uuid
import oss2
# auth = oss2.Auth('LTAI5tFU8HsxU531eP34p5qA', 'xIAzsYLc5gb7g9TFLCymQ8orWqKB3O')
# bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'dobot-image')

# def upload_oss(img_base64):
#     datas = base64.b64decode(img_base64)
#     new_pic = f"expire/{str(uuid.uuid4())}.txt"
#     # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
#     bucket.put_object(new_pic, datas)


def ToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        file = open("333.png", "wb")
        file.write(image_data)


def convert(image_name):
    endpoint = 'oss-cn-shenzhen.aliyuncs.com'
    access_key_id = 'LTAI5tFU8HsxU531eP34p5qA'
    access_key_secret = 'xIAzsYLc5gb7g9TFLCymQ8orWqKB3O'
    # yourBucketName目标Bucket名称。
    bucket_name = image_name.split(":")[0]
    key = image_name.split(":")[1]
    new_pic = f"/{str(uuid.uuid4())}.txt"
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint,
                         bucket_name)
    bucket.get_object_to_file(key, new_pic)
    base64_data = ""
    with open(new_pic, 'rb') as f:
        base64_data = f.read()
    return base64_data


# res = ToBase64('C:/Users/Administrator/Downloads/333.txt')
# res2 = convert("dobotlab-dev:expire/8da132a0-0406-11ed-bebc-9f1dfdb4d6d9.txt")
res2 = convert("dobot-image:expire/235573f7-36b7-4cc1-859e-11b33aace580.txt")
print(res2)