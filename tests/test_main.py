import pytest
from meal_planner.main import MealPlanner
from kivy.base import EventLoop

class TestMealPlannerApp:
    def setup_method(self):
        # Initialize Kivy event loop
        EventLoop.ensure_window()

    def teardown_method(self):
        # Stop Kivy event loop
        EventLoop.close()

    def test_meal_planner_app(self):
        app = MealPlanner()
        assert app is not None
        # Additional tests for the Kivy interface can be added here
