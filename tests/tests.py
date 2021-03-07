import json
from django.test import TestCase
from charts.objects import BarChart


class TestCaseChart(TestCase):

    def test_should_return_barchart_data(self):
        barchart = BarChart()
        barchart.title = "Example charts title"

        barchart.labels = ["test 1", "test 2", "test 3", "test 4"]
        barchart.data = [2, 3, 10, 6]
        barchart.data_label = "Test"

        data = barchart.build_chart()
        options = barchart.generate_options()

        assert data == expected_data(barchart, options)


def expected_data(chart, options):
    return json.dumps({
        "type": chart.type_chart,
        "data": {
            "labels": [label for label in chart.labels],
            "datasets": [
                {
                    "label": chart.data_label,
                    "backgroundColor": [color for color in chart.get_colors],
                    "data": [value for value in chart.data]
                }
            ]
        },
        "options": {
            "responsive": options["responsive"],
            "maintainAspectRatio": options["maintainAspectRatio"],
            "legend": {
                "display": chart.legend,
            },
            "title": {
                "fontSize": 14,
                "display": True if chart.title else False,
                "text": chart.title if chart.title else ""
            },
            "scales": {
                "yAxes": [
                    {
                        "display": True,
                        "ticks": {
                            "beginAtZero": chart.begin_at_zero,
                            "stepSize": chart.step_size
                        }
                    }
                ]
            }
        }
    }, ensure_ascii=False)
