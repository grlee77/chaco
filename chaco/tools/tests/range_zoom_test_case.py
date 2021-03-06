from unittest import TestCase

import mock
import numpy

from chaco.api import create_line_plot
from chaco.tools.api import BetterSelectingZoom
from enable.testing import EnableTestAssistant


class BackgroundColorTestCase(EnableTestAssistant, TestCase):
    """Regression tests for BetterSelectingZoom issue with background alpha.

    The BetterSelectingZoom overlay would override any user-specified value for
    the alpha channel of the selection plot, causing the selected region to
    appear completely opaque. This issue was reported (and fixed) in GH #309.

    """
    def setUp(self):
        values = numpy.arange(10)
        self.plot = create_line_plot((values, values))
        self.plot.bounds = [100, 100]
        self.plot._window = self.create_mock_window()
        self.tool = BetterSelectingZoom(component=self.plot, always_on=True)
        self.plot.active_tool = self.tool
        self.plot.do_layout()

    def tearDown(self):
        del self.tool
        del self.plot

    def test_rgba_background_box(self):
        tool = self.tool
        tool.tool_mode = 'box'
        tool.alpha = 0.3
        tool.color = 'red'
        gc = self.create_mock_gc(100, 100, methods=('set_fill_color',))

        kwargs = {
            'window': self.plot._window, 'control_down': True
        }
        self.mouse_down(self.tool, 0.0, 0.0, **kwargs)
        self.mouse_move(self.tool, 10.0, 10.0, **kwargs)

        tool.overlay(self.plot, gc)

        self.assertEqual(gc.set_fill_color.call_args,
                         mock.call([1.0, 0.0, 0.0, 0.3]))

    def test_rgba_background_range(self):
        tool = self.tool
        tool.tool_mode = 'range'
        tool.alpha = 0.3
        tool.color = 'red'
        gc = self.create_mock_gc(100, 100, methods=('set_fill_color',))

        kwargs = {
            'window': self.plot._window, 'control_down': True
        }
        self.mouse_down(self.tool, 0.0, 0.0, **kwargs)
        self.mouse_move(self.tool, 10.0, 10.0, **kwargs)

        tool.overlay(self.plot, gc)

        self.assertEqual(gc.set_fill_color.call_args,
                         mock.call([1.0, 0.0, 0.0, 0.3]))


if __name__ == '__main__':
    from unittest import main
    main()
