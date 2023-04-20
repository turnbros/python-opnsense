import json
import os.path
import unittest
from unittest.mock import Mock, MagicMock

from pydantic import ValidationError

from opnsense_api import Opnsense
from opnsense_api.firewall.category_controller import Category, CategoryController
from opnsense_api.util.exceptions import FailedToDeleteException, ItemNotFoundException, FailedToAddItemException, \
    InvalidItemException, FailedToSetItemException

parent_dir = os.path.dirname(os.path.abspath(__file__))


class TestCategory(unittest.TestCase):
    def test_init(self):
        # minimal configuration
        category_item = Category(name="Name")
        self.assertEqual(category_item.uuid, None)
        self.assertEqual(category_item.name, "Name")
        self.assertEqual(category_item.auto, True)
        self.assertEqual(category_item.color, "")
        # maximal configuration
        category_item = Category(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Name",
            auto=False,
            color="aaaaaa"
        )
        self.assertEqual(category_item.uuid, "11111111-1111-1111-1111-11111111111")
        self.assertEqual(category_item.name, "Name")
        self.assertEqual(category_item.auto, False)
        self.assertEqual(category_item.color, "aaaaaa")
        # tests constraints
        # lowercase color
        category_item.color = "AAAAAA"
        self.assertEqual(category_item.color, "aaaaaa")
        # color is "" or len(color) == 6
        with self.assertRaises(ValidationError):
            category_item.color = None
        with self.assertRaises(ValidationError):
            category_item.color = "aa"
        # non-hex characters
        with self.assertRaises(ValidationError):
            category_item.color = "aaaaax"


class TestCategoryController(unittest.TestCase):
    category_controller: CategoryController

    @classmethod
    def setUpClass(cls) -> None:
        cls.category_controller = CategoryController(device=Mock(spec=Opnsense))

    def test_init(self):
        self.assertEqual(TestCategoryController.category_controller._module, 'firewall')
        self.assertEqual(TestCategoryController.category_controller._controller, 'category')

    def test_opnsense_item_class(self):
        self.assertEqual(TestCategoryController.category_controller._opnsense_item_class, Category)

    def test_list(self):
        with open(os.path.join(parent_dir, 'json_src', 'category_list_response.json')) as f:
            list_response = json.loads(f.read())

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            return_value=list_response)
        categories = TestCategoryController.category_controller.list()

        TestCategoryController.category_controller._device._authenticated_request.assert_called_once_with(
            'POST', 'firewall/category/searchItem',
            body=None)

        self.assertListEqual(categories, [
            Category(uuid="6ce2534f-8037-46ff-852a-aca295550aec",
                     name="Category1",
                     auto=True,
                     color="aaaaaa"),
            Category(uuid="3290ae86-e6ee-4e0c-a95d-99e53d34c9ec",
                     name="Category2",
                     auto=False),
            Category(uuid="521b4779-a493-4790-b1a2-92738f4c85c0",
                     name="Category3",
                     auto=False,
                     color="121212")
        ])

    def test_get(self):
        with open(os.path.join(parent_dir, 'json_src', 'category_get_response.json')) as f:
            get_response = json.loads(f.read())

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(return_value=get_response)
        category = TestCategoryController.category_controller.get("11111111-1111-1111-1111-11111111111")

        TestCategoryController.category_controller._device._authenticated_request.assert_called_once_with(
            'GET',
            "firewall/category/getItem/11111111-1111-1111-1111-11111111111",
            body=None)

        self.assertEqual(category, Category(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Category1",
            auto=False,
            color="afaf16"
        ))

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(return_value={})
        with self.assertRaises(ItemNotFoundException):
            TestCategoryController.category_controller.get("11111111-1111-1111-1111-11111111111")

    def test_delete(self):
        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'deleted'})

        category = Category(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Name",
            auto=False,
            color="aaaaaa"
        )

        TestCategoryController.category_controller.delete(category)

        TestCategoryController.category_controller._device._authenticated_request.assert_called_once_with(
            'POST',
            'firewall/category/delItem/11111111-1111-1111-1111-11111111111',
            body=None
        )

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'not found'}
        )
        with self.assertRaises(FailedToDeleteException):
            TestCategoryController.category_controller.delete(category)

    def test_add(self):
        with open(os.path.join(parent_dir, 'json_src', 'category_add_request.json')) as f:
            add_request = json.loads(f.read())

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'saved', 'uuid': '11111111-1111-1111-1111-11111111111'}
        )

        category = Category(name="New Category", color="aaaaaa")
        TestCategoryController.category_controller.add(category)

        TestCategoryController.category_controller._device._authenticated_request.assert_called_once_with(
            'POST',
            'firewall/category/addItem',
            body=add_request
        )
        self.assertEqual('11111111-1111-1111-1111-11111111111', category.uuid)

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            return_value={'result': 'failed', 'validations': {'category.auto': 'value should be a boolean (0,1)'}}
        )

        with self.assertRaises(FailedToAddItemException):
            TestCategoryController.category_controller.add(category)

    def test_set(self):
        with open(os.path.join(parent_dir, 'json_src', 'category_get_response.json')) as f:
            get_response = json.loads(f.read())

        with open(os.path.join(parent_dir, 'json_src', 'category_set_request.json')) as f:
            set_request = json.loads(f.read())

        category = Category(
            uuid="11111111-1111-1111-1111-11111111111",
            name="Category1",
            auto=False,
            color="afaf16"
        )

        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            side_effect=[get_response, {'result': 'saved'}])

        TestCategoryController.category_controller.set(category)
        TestCategoryController.category_controller._device._authenticated_request.assert_called_with(
            'POST',
            'firewall/category/setItem/11111111-1111-1111-1111-11111111111',
            body=set_request
        )

        # missing uuid
        category.uuid = ""
        with self.assertRaises(InvalidItemException):
            TestCategoryController.category_controller.set(category)

        # failed response
        category.uuid = "11111111-1111-1111-1111-11111111111"
        TestCategoryController.category_controller._device._authenticated_request = MagicMock(
            side_effect=[get_response, {'result': 'failed',
                                        'validations': {'category.name': 'A category with this name already exists.'}}])

        with self.assertRaises(FailedToSetItemException):
            TestCategoryController.category_controller.set(category)


if __name__ == '__main__':
    unittest.main()
