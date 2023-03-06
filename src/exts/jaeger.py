from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from config import Config


def configure_tracer() -> None:
    """Адаптировал пример из теории, добавил указание Resource:

    https://opentelemetry-python.readthedocs.io/en/latest/sdk/resources.html?highlight=Resource#opentelemetry.sdk.resources.Resource.create

    """
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: 'Auth_Service'})
    )
    trace.set_tracer_provider(provider)

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=Config.JAEGER_HOST,
                agent_port=Config.JAEGER_AGENT_PORT,
            )
        )
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


def get_jaeger(app: Flask):
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)