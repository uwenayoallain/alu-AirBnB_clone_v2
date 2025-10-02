#!/usr/bin/python3
"""Tests for the console create command with parameters"""

import os
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage


class TestConsoleCreate(unittest.TestCase):
    """Validate parameter handling for the create command"""

    def setUp(self):
        """Prepare isolated storage for each test"""
        self.console = HBNBCommand()
        self.created_keys = []
        self.original_file_path = FileStorage._FileStorage__file_path
        self.original_objects = FileStorage._FileStorage__objects
        FileStorage._FileStorage__file_path = 'test_file.json'
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up created objects and restore storage state"""
        temp_objects = storage.all()
        for key in self.created_keys:
            temp_objects.pop(key, None)
        FileStorage._FileStorage__file_path = self.original_file_path
        FileStorage._FileStorage__objects = self.original_objects
        try:
            os.remove('test_file.json')
        except FileNotFoundError:
            pass

    def _create_with_output(self, command):
        """Execute a console command and capture its stdout"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd(command)
            return output.getvalue().strip()

    def test_create_state_with_name_parameter(self):
        """Ensure string parameters are parsed and stored"""
        obj_id = self._create_with_output('create State name="California"')
        self.assertTrue(obj_id)
        key = 'State.{}'.format(obj_id)
        self.created_keys.append(key)
        objects = storage.all()
        self.assertIn(key, objects)
        state = objects[key]
        self.assertEqual(state.name, 'California')

    def test_create_place_with_typed_parameters(self):
        """Ensure numeric parameters are converted to proper types"""
        command = (
            'create Place city_id="0001" user_id="0001" '
            'name="My_little_house" number_rooms=4 '
            'number_bathrooms=2 max_guest=10 price_by_night=300 '
            'latitude=37.773972 longitude=-122.431297'
        )
        obj_id = self._create_with_output(command)
        self.assertTrue(obj_id)
        key = 'Place.{}'.format(obj_id)
        self.created_keys.append(key)
        objects = storage.all()
        self.assertIn(key, objects)
        place = objects[key]
        self.assertEqual(place.name, 'My little house')
        self.assertEqual(place.city_id, '0001')
        self.assertEqual(place.user_id, '0001')
        self.assertIsInstance(place.number_rooms, int)
        self.assertEqual(place.number_rooms, 4)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertIsInstance(place.max_guest, int)
        self.assertEqual(place.max_guest, 10)
        self.assertIsInstance(place.price_by_night, int)
        self.assertEqual(place.price_by_night, 300)
        self.assertIsInstance(place.latitude, float)
        self.assertAlmostEqual(place.latitude, 37.773972)
        self.assertIsInstance(place.longitude, float)
        self.assertAlmostEqual(place.longitude, -122.431297)


if __name__ == '__main__':
    unittest.main()
