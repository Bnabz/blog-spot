
import unittest
from app.models import Post
from app import db


class PostTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Post Class
    '''
    def setUp(self):

        self.new_post = Post(id=1, title='Test', date_posted=2020/5/10, content='Test comment')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))

    def tearDown(self):
        Post.query.delete()


    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.id,1)
        self.assertEquals(self.new_post.title,'Test')
        self.assertEquals(self.new_post.date_posted,2020/5/10)
        self.assertEquals(self.new_post.content,'Test comment')



    def test_get_post_by_id(self):
        self.new_post.save_post()
        got_posts = Post.get_post(1)
        self.assertTrue(len(got_posts) == 1)