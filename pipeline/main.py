import click
import structlog
from pipeline.extractors.kafka_consumer import OrderEventConsumer
from pipeline.extractors.s3_reader import S3Reader
from pipeline.transformers.enrichment import enrich_order
from pipeline.loaders.warehouse import WarehouseLoader

logger = structlog.get_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--topic", default="order.created")
@click.option("--group", default="data-pipeline")
def consume(topic: str, group: str):
    consumer = OrderEventConsumer(topic=topic, group_id=group)
    loader = WarehouseLoader()
    logger.info("Starting consumer", topic=topic, group=group)
    for event in consumer.stream():
        enriched = enrich_order(event)
        loader.load_order(enriched)


@cli.command()
@click.option("--bucket", required=True)
@click.option("--prefix", required=True)
def backfill(bucket: str, prefix: str):
    reader = S3Reader(bucket=bucket)
    loader = WarehouseLoader()
    for record in reader.read_jsonl(prefix):
        enriched = enrich_order(record)
        loader.load_order(enriched)


if __name__ == "__main__":
    cli()
