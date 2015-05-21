
"""
Sizun - Software Quality Inspection
MIT License
(C) 2015 David Rieger
"""
import unittest
import os
import logging
from flask import Flask
from sizun.controllers.linegrabber import LineGrabber
from test.mocks.settingsmock import InspectionSettingsMock


class TestLineGrabber(unittest.TestCase):

    JAVA_SAMPLE_1 = "test/__testdata__/java_1.sample"

    def setUp(self):
        self.settings = InspectionSettingsMock()
        self.linegrabber = LineGrabber(self.settings)
        self.testfiles = [self.JAVA_SAMPLE_1]
        self.app = Flask(__name__)
        self.logger = logging.getLogger()

    def test_line_grabber_single_line_success(self):
        with self.app.app_context():
            _res_line = self.linegrabber.get_lines(self.testfiles[0], start_line=28)
            self.assertEqual("public class User extends BlogEntity {", _res_line.strip())

    def test_line_grabber_multi_line_success(self):
        with self.app.app_context():
            _res_line = self.linegrabber.get_lines(self.testfiles[0], start_line=80, end_line=82)
            # self.logger.warning("result from linegrabber is :: {}".format(_res_line))
            _expected = ["public static String hashPassword(String clear) {",
                         "logger.debug(\"Hash password!\");",
                         "return DigestUtils.sha1Hex(clear);"]
            self.assertEqual(_expected, _res_line)

    def test_line_grabber_single_line_fail(self):
        with self.app.app_context():
            _res_line = self.linegrabber.get_lines(self.testfiles[0], start_line=28)
            self.assertNotEqual("public class User extends logEntity {", _res_line.strip())

    def test_line_grabber_multi_line_fail(self):
        with self.app.app_context():
            _res_line = self.linegrabber.get_lines(self.testfiles[0], start_line=80, end_line=82)
            # self.logger.warning("result from linegrabber is :: {}".format(_res_line))
            _expected = ["public static String hashPassword(String clear)  {",
                         "logger.debug(\"Hash password!\");",
                         "return DigestUils.sha1Hex(clear);"]
            self.assertNotEqual(_expected, _res_line)
