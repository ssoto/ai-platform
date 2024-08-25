#!/bin/bash

celery -A ai_platform.task_queue.main worker --queues default --pool solo
