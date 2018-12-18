from metrics.views.metrics import metric, metrics_collection


# def includeme(config):
#     config.add_static_view('static', 'static', cache_max_age=3600)
#     config.add_route('home', '/')
def includeme(config):
    # Define the routes for metrics
    config.add_route('metrics', '/metrics/')
    config.add_route('metric', '/metrics/{id:\d+}/')
    # Match the metrics views with the appropriate routes
    config.add_view(metrics_collection, 
        route_name='metrics', 
        renderer='json')
    config.add_view(metric, 
        route_name='metric', 
        renderer='json')
