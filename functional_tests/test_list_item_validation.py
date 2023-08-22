from unittest import skip

from .base import FunctionalTest


class TestItemValidation(FunctionalTest):
    """
    Набор тестов эмулирующий некорректные вводы пользователя и реакцию на них
    """
    @skip
    def test_cannot_add_empty_list_items(self):
        """Тест: Проверяет что пользователь не может создать пустой элемент списка"""
        self.fail("Напиши меня")
