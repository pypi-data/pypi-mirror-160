import base64
from typing import List, Any
from .pause.pauselab import PauseLab, pause
import oss2
import uuid

auth = oss2.Auth('LTAI5tFU8HsxU531eP34p5qA', 'xIAzsYLc5gb7g9TFLCymQ8orWqKB3O')
bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'dobot-image')


class InvalidDataError(Exception):
    def __init__(self, error: str):
        super().__init__(error)


class ImageGroupError(Exception):
    def __init__(self, error: str):
        super().__init__(error)


class Pyimageom(PauseLab):
    def __init__(self, rpc_adapter):
        self._r_client = rpc_adapter

    def upload_oss(self, img_base64):
        new_pic = f"expire/{str(uuid.uuid4())}.txt"
        # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
        bucket.put_object(new_pic, img_base64)
        new_pic = "dobot-image:" + new_pic
        return new_pic

    @pause
    def image_cut(self, img_base64: str):
        if len(img_base64) != 0:
            image_name = self.upload_oss(img_base64)
            return self._r_client.image_cut(image_name=image_name)
        else:
            raise InvalidDataError("img_base64 cannot be empty.")

    @pause
    def feature_image_classify(self, img_base64s: List[Any], lables: List[int],
                               class_num: int, flag: int):
        img_names = []
        for i in img_base64s:
            img = self.upload_oss(i)
            img_names.append(img)
        return self._r_client.feature_image_classify(img_names=img_names,
                                                     lables=lables,
                                                     class_num=class_num,
                                                     flag=flag)

    @pause
    def feature_image_group(self, img_base64: str):
        if len(img_base64) != 0:
            try:
                image_name = self.upload_oss(img_base64)
                res = self._r_client.feature_image_group(image_name=image_name)
            except Exception as e:
                raise ImageGroupError(
                    f"Please add at least two sets of data with no less than 3 photos in each group. ERROR: {e}"
                )
            return res
        else:
            raise InvalidDataError("img_base64 cannot be empty.")

    @pause
    def find_chessboard_corners(self, img_base64: str):
        if len(img_base64) != 0:
            image_name = self.upload_oss(img_base64)
            return self._r_client.find_chessboard_corners(
                image_name=image_name)
        else:
            raise InvalidDataError("img_base64 cannot be empty.")

    @pause
    def color_image_cut(self, img_base64: str):
        if len(img_base64) != 0:
            image_name = self.upload_oss(img_base64)
            return self._r_client.color_image_cut(image_name=image_name)
        else:
            raise InvalidDataError("img_base64 cannot be empty.")

    @pause
    def color_image_classify(self, img_base64s: List[Any], lables: List[int],
                             class_num: int, flag: int):
        img_names = []
        for i in img_base64s:
            img = self.upload_oss(i)
            img_names.append(img)
        return self._r_client.color_image_classify(img_names=img_names,
                                                   lables=lables,
                                                   class_num=class_num,
                                                   flag=flag)

    @pause
    def color_image_group(self, img_base64: str):
        if len(img_base64) != 0:
            try:
                image_name = self.upload_oss(img_base64)
                res = self._r_client.color_image_group(image_name=image_name)
            except Exception as e:
                raise ImageGroupError(
                    f"Please add at least two sets of data with no less than 3 photos in each group. ERROR: {e}"
                )
            return res
        else:
            raise InvalidDataError("img_base64 cannot be empty.")

    @pause
    def set_background(self, img_base64: str):
        if len(img_base64) != 0:
            image_name = self.upload_oss(img_base64)
            return self._r_client.set_background(image_name=image_name)
        else:
            raise InvalidDataError("img_base64 cannot be empty.")