#!/bin/bash

celery -A ai_platform.task_queue.main worker --queues default --pool solo --concurrency 1 --loglevel DEBUG --without-gossip
