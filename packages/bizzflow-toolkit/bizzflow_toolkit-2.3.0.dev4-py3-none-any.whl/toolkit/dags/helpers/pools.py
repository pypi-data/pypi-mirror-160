import logging

from airflow.models import Pool
from airflow.settings import Session

logger = logging.getLogger(__name__)


class PoolCreator:
    def __init__(self):
        self.session = None
        self.available_pools = None

    def create_pool_if_not_exists(self, pool_name: str):
        if self.session is None:
            self.open_session()
        if pool_name not in self.available_pools:
            logger.info(f"Creating worker pool {pool_name}")
            worker_pool = Pool(
                pool=pool_name,
                slots=1,
                description="Making sure only one task with same id will run just once at the same time",
            )
            self.session.add(worker_pool)
            self.session.commit()

    def open_session(self):
        self.close_session()
        self.session = Session()
        self.available_pools = [p.pool for p in self.session.query(Pool).all()]

    def close_session(self):
        if self.session:
            self.session.close()
        self.session = None

    def __del__(self):
        self.close_session()
