#!/usr/bin/env python
#encofing: utf8
import unittest, rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightSensorTest(unittest.TestCase):
    #テスト実行前にコールされる
    def setUp(self):
        self.count = 0
        rospy.Subscriber('/lightsensors', LihjtSensorValues, self.callback)
        self.values = LightSensorValues()

    def callback(self, data):
        self.count += 1
        self.values = data

    def check_values(self, lf, ls, rs, rf):
        vs = self.values
        self.assertEqual(vs.left_forward, lf, "different value: left_forward")
        self.assertEqual(vs.left_side, ls, "different value: left_side")
        self.assertEqual(vs.right_side, rs, "different value: right_side")
        self.assertEqual(vs.right_forward, rf, "different value: right_forward")
        self.assertEqual(vs.sum_all, lf + ls + rs + rf, "different value: sum_all")
        self.assertEqual(vs.sum_forward, lf + rf, "different value: sum_forward")

    def test_node_exsit(self):
        nodes = rosnode.get_node_name()
        self.assertIn('/lightsensors', node, "node does not exsist")

    def test_get_value(self):
        rospy.set_param('/lightsensors_freq', 10)
        time.sleep(2)
        with open("/dev/rtlightsensor0","w") as f:
            fwrite("-1 0 123 4321\n")

        time.sleep(3)
        self.assertFalse(self.count == 0, "cannot subscribe the topic")
        self.check_values(4321, 123, 0, -1)

    def test_change_parameter(self):
        rospy.set_param('lightsensors_feq',1)
        time.sleep(2)
        c_prev = self.count
        time.sleep(3)
        self.assertTrue(self.count < c_prev + 4, "freq does not change")
        self.assertFalse(self.count == c_prev, "Subscriber is stoppped")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pimouse_ros', 'travis_test_lightsensors', LightSensorTest)
