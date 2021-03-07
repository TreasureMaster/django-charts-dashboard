============
Usage
============


Charts as views
---------------

If you want render only one chart, you can inherit ChartViews available. Is required that you define two essential methods: "generate_labels" and "generate_values".

Available BarChartView, PieChartView, DoughnutChartView, RadarChartView, HorizontalBarChartView, PolarAreaChartView, LineChartView, GroupChartView

in views.py import type chart to want use:

.. code-block:: python

    from django.views.generic.base import TemplateView
    from charts.views import BarChartView

    class ExampleChart(BarChartView, TemplateView):
        ...
        title = "Index of ..."

        def generate_labels(self):
            return ["Africa","Brazil","Japan","EUA"]

        def generate_values(self):
            return [1,10,15,8]

**in your template that you want render chart, use this tag:**

.. code-block:: html

    {% load charts %}
    <html>
    <head></head>
    <body>

    {% render_chart chart %}

    </body>
    </html>


Options charts views
~~~~~~~~~~~~~~~~~~~~

below default values

.. code-block:: python

    title = ""
    legend = False
    beginAtZero = False
    aspectRatio = True
    width = 100
    height = 100
    tooltip = None

| **title:** Define a title for chart,
| **legend:** Enable or disable legend in chart,
| **beginAtZero:** Define yAxis init with zero,
| **aspectRatio:** Enable resize chart when option defined as False,
| **stepSize:** Define interval yAxis,
| **width:** Define width chart (When aspectRatio as False),
| **height:** Define height chart (When aspectRatio as False),
| **tooltip:** Define as string tooltip when on mouse hover chart.
| **colors:** Define list of colors (string hex representation) to override random colors

If you want resize the chart, just define width an height properties and set aspectRatio as False:

.. code-block:: python

    from django.views.generic.base import TemplateView
    from charts.views import BarChartView

    class ExampleChart(BarChartView, TemplateView):
        ...
        title = "Index of ..."
        aspectRatio = False
        width = 300
        height = 250

        def generate_labels(self):
            return ["Africa","Brazil","Japan","EUA"]

        def generate_values(self):
            return [1,10,15,8]


RadarChartView
~~~~~~~~~~~~~~

To use `RadarChartView` you need create an special node to add dataset. Using 'create_node' method
you can pass 'label', data (list) and optional parameter 'color', if you don't pass color, will be generate random color to node. Use this in generate_values method.

Example below:


.. code-block:: python

    from django.views.generic.base import TemplateView
    from charts.views import RadarChartView

    class ExampleChart(RadarChartView, TemplateView):
        ...
        title = "Index of ..."

        def generate_labels(self):
            return ["Africa","Brazil","Japan","EUA"]

        def generate_values(self):
            dataset = []
            nodeOne = self.create_node("Example 1", [15,5,2,50]) #you can create many nodes to view in chart
            ....
            dataset.append(nodeOne)

            return dataset


LineChartView
~~~~~~~~~~~~~

If you want use `LineChartView`, is same method that RadarChartView, 
but have unique difference is the parameter 'fill' that by default is False. 
The linechart too have create_node method to generate special node for chart.


For generate a AreaChart define fill as True on create_node method. 
You too can be pass a color as parameter on this method.

The color must be passed as a string "#606060"

**Example:** self.create_node("Test", [1,2,3,4,5], "#606060")


GroupChartView
~~~~~~~~~~~~~~

Too heve a crete_node method and same method generate of charts above.


Charts as objects
-----------------

in your views.py:

.. code-block:: python

    from django.views.generic import TemplateView
    from charts.objects import BarChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            chart = BarChart()
            chart.title = "Example charts title"
            chart.labels = ["test 1","test 2", "test 3", "test 4"]
            chart.data = [2,3,10,6]
            chart.data_label = "Test"

            context["chart"] = chart.build_chart()

            return context

**And in your "example.html" template use this:**

.. code-block:: html

    <canvas id="mychart"></canvas>

**on script section:**

.. code-block:: javascript

    $(function(){
        var dataset = JSON.parse('{{ chart|safe }}');
        new Chart(document.getElementById("mychart"), dataset);
    })

**You can be use chart object in any function in your views.py, for example:**

.. code-block:: python

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            chart = BarChart()
            chart.title = "Example charts title"
            chart.labels = ["test 1","test 2", "test 3", "test 4"]
            chart.data = [2,3,10,6]
            chart.data_label = "Test"

            return chart.build_chart()

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["chart"] = self.my_method() #any key in context

            return context


The charts available in package is: BarChart, PieChart, HorizontalBarChart, DoughnutChart, PolarAreaChart, RadarChart, LineChart, GroupChart

It's possible define options to object chart, for example:

| barchart.title = "..."
| barchart.legend = True


Define fixed colors to chart
----------------------------

For define fixed instead random colors use this:

.. code-block:: python

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            chart = BarChart()
            chart.set_colors(["#fff","#B4edf",...]) # set your color list here



Many charts by views
~~~~~~~~~~~~~~~~~~~~

Here you can be render more than one charts in your template html, just call
instances of charts and define key in context

.. code-block:: python

    from django.views.generic import TemplateView
    from charts.objects import BarChart, PieChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_barchart(self):
            chart = BarChart()
            chart.title = "Example charts title"
            chart.labels = ["test 1","test 2", "test 3", "test 4"]
            chart.data = [2,3,10,6]
            chart.data_label = "Test"

            return chart.build_chart()

        def my_piechart(self):
            chart = PieChart()
            chart.title = "Example charts title"
            chart.labels = ["test 1","test 2", "test 3", "test 4"]
            chart.data = [2,3,10,6]
            chart.data_label = "Test"

            return chart.build_chart()


        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["barchart"] = self.my_barchart()
            context["piechart"] = self.my_piechart()

            return context

**In your template body:**

Example using bootstrap:

.. code-block:: html

    <div class="row">
        <div class="col-6">
            <canvas id="mybarchart"></canvas>
        </div>
        <div class="col-6">
            <canvas id="mypiechart"></canvas>
        </div>
    </div>

and section scripts:

.. code-block:: javascript

    $(function(){
        var bardata = JSON.parse('{{ barchart|safe }}');
        new Chart(document.getElementById("mybarchart"), bardata);

        var piedata = JSON.parse('{{ piechart|safe }}');
        new Chart(document.getElementById("mypiechart"), piedata);
    });


RadarChart
~~~~~~~~~~

For use radar charts as a object in your view, do this:

.. code-block:: python

    from django.views.generic import TemplateView
    from charts.objects import RadarChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            chart = RadarChart()
            chart.title = "Example charts title"

            labels = ["test 1","test 2", "test 3", "test 4"]
            data = []
            data.append(chart.create_node("Example 1", [5,8,9,64,3]))
            data.append(chart.create_node("Example 2", [10,1,19,6,13]))
            ....

            return radarchart.generate_dataset(labels, data)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["chart"] = self.my_method()

            return context


LineChart
~~~~~~~~~

.. code-block:: python

    from django.views.generic import TemplateView
    from charts.charts import LineChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            chart = LineChart()
            chart.title = "Example charts title"

            labels = ["test 1","test 2", "test 3", "test 4"]
            data = []
            data.append(chart.create_node("Example 1", [5,8,9,64,3]))
            ....

            return chart.generate_dataset(labels, data)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["chart"] = self.my_method()

            return context


AreaChart
~~~~~~~~~

Just use LineChart and define fill parameter as a True, you can define color to node if you want.

.. code-block:: python

    from django.views.generic import TemplateView
    from charts.charts import LineChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            chart = LineChart()
            chart.title = "Example charts title"

            labels = ["test 1","test 2", "test 3", "test 4"]
            data = []
            data.append(chart.create_node("Example 1", [5,8,9,64,3], True))
            ....

            return chart.generate_dataset(labels, data)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["chart"] = self.my_method()

            return context


GroupChart
~~~~~~~~~~

The same method that charts above, only difference is the create_node method have a color parameter.


Override Tooltips
-----------------

You can override tooltips in charts, just only define `chart.tooltips` with list tooltips itens.

chart as object

**views.py**

.. code-block:: python

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            barchart = BarChart()
            barchart.title = "Example charts title"
            barchart.tooltips = ["tooltip 1","tooltip 2","tooltip 3"]

            ...

or chart as a view:

**views.py**

.. code-block:: python

    from django.views.generic.base import TemplateView
    from charts.views import BarChartView

    class ExampleChart(BarChartView, TemplateView):
        ...
        title = "Index of ..."

        def generate_labels(self):
            return ["Africa","Brazil","Japan","EUA"]

        def generate_values(self):
            return [1,10,15,8]
        
        def get_tooltips(self):
            return ["tooltip 1","tooltip 2","tooltip 3"]


**And your template use this:**

.. code-block:: javascript
    
    $(function(){

        var dataset = JSON.parse('{{ chart|safe }}');
        var tooltips = {{ tooltips|safe }};

        callback = {
            callbacks: {
                label: function(tooltipItem,data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    return tooltips[tooltipItem.index] + dataset.data[tooltipItem.index];
                }
            }
        }

        dataset.options.tooltips = Object.assign(callback);

        $(function(){
            new Chart(document.getElementById("chart_view"), dataset);
        });
    });

Override yAxes in BarCharts
---------------------------

You can override yAxes to show values in percentage, just only add extra scales options:

PS: you need convert value to percentage value in django views or in callback function into javascript.

.. code-block:: javascript

    $(function(){

        var dataset = JSON.parse('{{ chart|safe }}');

        scales = {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    min: 0,
                    max: this.max,
                    callback: function (value) {
                        return value + '%';
                    },
                }
            }]
        }

        dataset.options.scales = Object.assign(scales); //append extra option into context option

        new Chart(document.getElementById("mychart"), dataset);
    });