import unittest
import random


class testFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.seq = list(range(10))

    def test_choice_ok(self):
        '''测试选择样本是否在序列中'''
        item = random.choice(self.seq)
        result = item in self.seq
        self.assertTrue(result)

    def test_sample_ok(self):
        """测试长度是否一致"""
        item = random.sample(self.seq, 4)
        self.assertEqual(len(item), 4)

    def tearDown(self) -> None:
        del self.seq
