
asset_list = {}


class asset_enroller(object):
    def __init__(self, cls, *args, **kwargs):
        asset_list.update({
            cls.__name__: cls
        })

        self.cls = cls

    def __call__(self, *args, **kwargs):
        pass
