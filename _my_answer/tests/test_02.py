# python3 -m unittest test_01.py 

import sys
from unittest import TestCase, main

sys.path.append("..")

NUM = 1

### Reference
#
# Python の 単体テストで 大量の入力パターンを効率よくテストする方法 : https://qiita.com/Asayu123/items/61ef72bb829dd8baba9f
### 
class Test01(TestCase):
    """ This test case tests rock_paper_scissors method """

    # I want to automate (from <div class="language-bash highlighter-rouge">)

    def test_with_valid_params(self):
        """
        With SubTest, All patterns will be tested even if there are some failures.
        Consequently, we can test all patterns every time.
        """
        from p_02 import my01, my02

        ans01 = """Du = 
[[ 5.  3.  1.]
 [ 6.  2.  1.]
 [ 4.  1.  1.]
 [ 8.  5. -1.]
 [ 2.  4. -1.]
 [ 3.  6. -1.]
 [ 7.  6. -1.]
 [ 4.  2. nan]
 [ 5.  1. nan]
 [ 8.  6. nan]
 [ 3.  4. nan]
 [ 4.  7. nan]
 [ 4.  4. nan]]"""

        ans02 = "Duの形状 = (13, 3)"

        test_patterns = []

        for i in range(1,3):
            test_patterns.append((locals()[f"my0{i}"],locals()[f"ans0{i}"]))

        for my_ans, expected_result in test_patterns:
            with self.subTest(my_ans=my_ans):
                self.assertEqual(my_ans, expected_result)


    """ This test case tests rock_paper_scissors method """

    # I want to automate (from <div class="language-bash highlighter-rouge">)

    def test_with_valid_params(self):
        """
        With SubTest, All patterns will be tested even if there are some failures.
        Consequently, we can test all patterns every time.
        """
        from p_01 import my01, my02

        ans01 = """Du = 
[[ 5.  3.  1.]
 [ 6.  2.  1.]
 [ 4.  1.  1.]
 [ 8.  5. -1.]
 [ 2.  4. -1.]
 [ 3.  6. -1.]
 [ 7.  6. -1.]
 [ 4.  2. nan]
 [ 5.  1. nan]
 [ 8.  6. nan]
 [ 3.  4. nan]
 [ 4.  7. nan]
 [ 4.  4. nan]]"""

        ans02 = "Duの形状 = (13, 3)"

        test_patterns = []

        for i in range(1,3):
            test_patterns.append((locals()[f"my0{i}"],locals()[f"ans0{i}"]))

        for my_ans, expected_result in test_patterns:
            with self.subTest(my_ans=my_ans):
                self.assertEqual(my_ans, expected_result)