import unittest
import os.path

from anet.core import checker
from anet.core import fs
from anet.core.registry import registry
from anet.iptc import iptc

class ClassesTestCase(unittest.TestCase):

    def setUp(self):
        # is executes before EVERY test
        self.mystring = ""

    def tearDown(self):
        # is executes after EVERY test
        self.mystring = None

    def checkRegistryUse(self):
        checker.checkregistry()

    def checkToolcatInstallation(self):
        checker.checktoolcat("iptc")

    def checkIPTC01(self):
        IPTC = iptc.getiptc_path("abc.jpg")
        E = {'SpecialInstructions': 'Special instructions', 'CaptionWriter': 'Caption writer', 'Headline': 'Headline', 'Caption': 'Caption', 'Keywords': ['kw1', 'kw2'], 'CopyrightNotice': 'Copyright'}
        assert IPTC == E, "Expected:\n%r\n\nGot:\n%r\n" % (E, IPTC)



classes_testsuite = unittest.makeSuite(ClassesTestCase, "check")
runner = unittest.TextTestRunner()
runner.run(classes_testsuite)
