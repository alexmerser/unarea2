

class PostsModel(object):
    def __init__(self, posts_resource):
        self._posts_resource = posts_resource

    def create_post(self, post):
        res = self._posts_resource.insert(post.serialize())
        return res
