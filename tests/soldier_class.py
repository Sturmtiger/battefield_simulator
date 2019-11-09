import unittest
from units import Soldier


class TestSoldier(unittest.TestCase):
    def setUp(self):
        self.soldier = Soldier()

    def test_init(self):
        self.assertEqual(self.soldier.exp, 0)
        self.assertEqual(self.soldier.recharge_time, 0)
        self.assertNotEqual(self.soldier.hp, 0)

    def test_inflict_damage(self):
        self.assertEqual(self.soldier.inflict_damage(), 0.05)

        self.soldier.gain_exp()
        self.assertEqual(round(self.soldier.inflict_damage(), 2), 0.06)

    def test_gain_exp(self):
        self.soldier.gain_exp()
        self.assertEqual(self.soldier.exp, 1)

        self.soldier.exp = 50
        self.soldier.gain_exp()
        self.assertNotEqual(self.soldier.exp, 51)

    def test_get_damage(self):
        self.soldier.get_damage(20)
        self.assertEqual(self.soldier.hp, 80)

    def test_recharge(self):
        self.soldier.recharge()
        self.assertGreater(self.soldier.recharge_time, 0)

    def test_is_charged(self):
        self.assertTrue(self.soldier.is_charged)

        self.soldier.recharge()
        self.assertFalse(self.soldier.is_charged)

    def test_is_active(self):
        self.assertTrue(self.soldier.is_active)

        self.soldier.get_damage(100)
        self.assertFalse(self.soldier.is_active)

    def test_attack_success(self):
        probability = self.soldier.attack_success()
        self.assertTrue(0 <= probability <= 1)


if __name__ == '__main__':
    unittest.main()
