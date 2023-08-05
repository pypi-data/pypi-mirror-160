# -*- coding: utf-8 -*-
import logging
import time

from Products.PluginIndexes.interfaces import ILimitedResultIndex
from Products.ZCatalog.plan import Benchmark, CatalogPlan, PriorityMap

logger = logging.getLogger(__name__)


def CatalogPlan_stop(self):
    self.end_time = time.time()
    self.duration = self.end_time - self.start_time
    # Make absolutely sure we never omit query keys from the plan
    current = PriorityMap.get_entry(self.cid, self.key)
    for key in self.query.keys():
        key = self.querykey_to_index.get(key, key)
        if key not in self.benchmark.keys():
            if current and key in current:
                self.benchmark[key] = Benchmark(*current[key])
            else:
                if key in self.catalog.indexes:
                    index = self.catalog.indexes[key]
                    self.benchmark[key] = Benchmark(
                        0, 0, ILimitedResultIndex.providedBy(index)
                    )
                else:
                    self.benchmark[key] = Benchmark(0, 0, False)
    PriorityMap.set_entry(self.cid, self.key, self.benchmark)
    self.log()


logger.info("*** CatalogPlan.stop monkey patch ***")
CatalogPlan.stop = CatalogPlan_stop
