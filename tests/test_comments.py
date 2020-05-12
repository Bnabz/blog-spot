import unittest
from app.models import Comment
from app import db


class CommentsTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Comment Class
    '''
    def setUp(self):

        self.new_comment = Comment(id=1, comment='Test comment',dateposted=2020/5/11 )

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def tearDown(self):
        Comment.query.delete()


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.comment,'Test comment')
        self.assertEquals(self.new_comment.dateposted,2020/5/11)



    def test_get_comment_by_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comment(1)
        self.assertTrue(len(got_comments) == 1)