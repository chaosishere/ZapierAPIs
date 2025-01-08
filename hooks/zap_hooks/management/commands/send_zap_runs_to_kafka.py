import time
from django.core.management.base import BaseCommand
from django.db import transaction
from zap_hooks.models import ZapRunOutbox, ZapRun
from zap_hooks.kafka_producer import create_kafka_producer, delivery_report

class Command(BaseCommand):
    help = 'Push ZapRunOutbox data to Kafka indefinitely'

    def handle(self, *args, **kwargs):
        producer = create_kafka_producer()
        topic = 'zap_run_topic'  # Specify the Kafka topic

        self.stdout.write("Starting Kafka producer...")

        while True:
            try:
                # Fetch unsent data from ZapRunOutbox
                outbox_entries = ZapRunOutbox.objects.all()

                # If no unsent data, wait for a bit and retry
                if not outbox_entries:
                    self.stdout.write("No unsent messages, waiting...")
                    time.sleep(5)  # Adjust this to control how often it checks for new data
                    continue

                # Process each outbox entry
                for entry in outbox_entries:
                    try:
                        zap_run = entry.zap_run
                        message_data = {
                            'zap_run_id': str(zap_run.id),
                            'metadata': zap_run.metadata,
                        }

                        # Send the data to Kafka
                        producer.produce(topic, key=str(zap_run.id), value=str(message_data), callback=delivery_report)

                        # After sending the message to Kafka, mark the entry as processed
                        with transaction.atomic():
                            entry.delete()  # Or update status to indicate it's been processed

                    except Exception as e:
                        self.stderr.write(f"Error sending message to Kafka: {e}")

                # Wait for any outstanding messages to be delivered
                producer.flush()

            except KeyboardInterrupt:
                self.stdout.write("Kafka producer stopped manually.")
                break
            except Exception as e:
                self.stderr.write(f"Error in Kafka producer: {e}")
                time.sleep(5)  # Wait before retrying after an error
