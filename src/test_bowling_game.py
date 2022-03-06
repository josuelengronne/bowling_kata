from src.bowling_game import BowlingGame
import pytest


class TestBowlingGame:
    game = None

    @pytest.fixture(autouse=True)
    def game(self):
        self.game = BowlingGame()

    def test_score_has_exception_when_no_roll(self):
        self.attest_not_finished()

    def test_after_20_1_roll_has_score(self):
        self.roll_multiple(20, 1)
        assert self.game.score() is not None

    def test_after_1_1_roll_has_exception(self):
        self.game.roll(1)
        self.attest_not_finished()

    def test_after_has_score_roll_has_exception(self):
        self.roll_multiple(20, 1)
        with pytest.raises(BowlingGame.AlreadyFinishedException):
            self.game.roll(1)

    def test_if_1_10_need_19_for_score(self):
        self.game.roll(10)
        self.roll_multiple(18, 1)
        assert self.game.score() is not None

    def test_11_exception(self):
        with pytest.raises(BowlingGame.TooManyPinsKnockedException):
            self.game.roll(11)

    def test_5_then_6_exception(self):
        self.game.roll(5)
        with pytest.raises(BowlingGame.TooManyPinsKnockedException):
            self.game.roll(6)

    def test_20_1_then_20_points(self):
        self.roll_multiple(20, 1)
        assert self.game.score() == 20

    def test_spare_multiplies_next(self):
        self.game.roll(9)
        self.roll_multiple(19, 1)
        assert self.game.score() == 29

    def test_strike_multiplies_2_next(self):
        self.game.roll(10)
        self.roll_multiple(18, 1)
        assert self.game.score() == 30

    def test_spare_has_extra_throw(self):
        self.roll_multiple(19, 1)
        self.game.roll(9)
        self.game.roll(4)
        assert self.game.score() == 32

    def test_strike_has_2_extra_throw(self):
        self.roll_multiple(18, 1)
        self.game.roll(10)
        self.roll_multiple(2, 1)
        assert self.game.score() == 30

    def test_12_10_then_score(self):
        self.roll_multiple(12, 10)
        assert self.game.score() == 300

    def test_extra_roll_sum_10(self):
        self.roll_multiple(10, 10)
        self.game.roll(9)
        with pytest.raises(BowlingGame.TooManyPinsKnockedException):
            self.game.roll(2)

    def test_print(self):
        self.roll_multiple(20, 1)
        assert self.game.__str__() == '[(1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (None,None)]'

    def attest_not_finished(self):
        with pytest.raises(BowlingGame.NotFinishedException):
            self.game.score()

    def roll_multiple(self, roll_amount, value):
        for i in range(roll_amount):
            self.game.roll(value)


