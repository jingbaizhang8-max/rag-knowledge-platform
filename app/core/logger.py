import logging

logger = logging.getLogger("rag_knowledge_platform")

logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.propagate = False

